import numpy as np
import torch
# from lungmask import utils
import utilties as utils
import SimpleITK as sitk
from resunet import UNet
import warnings
import sys
from tqdm import tqdm
import skimage
import logging
import nibabel as nib

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
warnings.filterwarnings("ignore", category=UserWarning)


def apply(image, model=None, force_cpu=False, batch_size=20, volume_postprocessing=True, noHU=False):
    if model is None:
        model = get_model('model.pth')
    
    numpy_mode = isinstance(image, np.ndarray)
    if numpy_mode:
        inimg_raw = image.copy()
    else:
        inimg_raw = sitk.GetArrayFromImage(image)
        directions = np.asarray(image.GetDirection())
        if len(directions) == 9:
            inimg_raw = np.flip(inimg_raw, np.where(directions[[0,4,8]][::-1]<0)[0])
    del image

    if force_cpu:
        device = torch.device('cpu')
    else:
        if torch.cuda.is_available():
            device = torch.device('cuda')
        else:
            logging.info("No GPU support available, will use CPU. Note, that this is significantly slower!")
            batch_size = 1
            device = torch.device('cpu')
    model.to(device)

    
    if not noHU:
        tvolslices, xnew_box = utils.preprocess(inimg_raw, resolution=[256, 256])
        tvolslices[tvolslices > 600] = 600
        tvolslices = np.divide((tvolslices + 1024), 1624)
    else:
        # support for non HU images. This is just a hack. The models were not trained with this in mind
        tvolslices = skimage.color.rgb2gray(inimg_raw)
        tvolslices = skimage.transform.resize(tvolslices, [256, 256])
        tvolslices = np.asarray([tvolslices*x for x in np.linspace(0.3,2,20)])
        tvolslices[tvolslices>1] = 1
        sanity = [(tvolslices[x]>0.6).sum()>25000 for x in range(len(tvolslices))]
        tvolslices = tvolslices[sanity]
    torch_ds_val = utils.LungLabelsDS_inf(tvolslices)
    dataloader_val = torch.utils.data.DataLoader(torch_ds_val, batch_size=batch_size, shuffle=False, pin_memory=False)

    timage_res = np.empty((np.append(0, tvolslices[0].shape)), dtype=np.uint8)

    with torch.no_grad():
        for X in tqdm(dataloader_val):
            X = X.float().to(device)
            prediction = model(X)
            pls = torch.max(prediction, 1)[1].detach().cpu().numpy().astype(np.uint8)
            timage_res = np.vstack((timage_res, pls))

    # postprocessing includes removal of small connected components, hole filling and mapping of small components to
    # neighbors
    if volume_postprocessing:
        outmask = utils.postrocessing(timage_res)
    else:
        outmask = timage_res

    if noHU:
        outmask = skimage.transform.resize(outmask[np.argmax((outmask==1).sum(axis=(1,2)))], inimg_raw.shape[:2], order=0, anti_aliasing=False, preserve_range=True)[None,:,:]
    else:
         outmask = np.asarray(
            [utils.reshape_mask(outmask[i], xnew_box[i], inimg_raw.shape[1:]) for i in range(outmask.shape[0])],
            dtype=np.uint8)
    
    if not numpy_mode:
        if len(directions) == 9:
            outmask = np.flip(outmask, np.where(directions[[0,4,8]][::-1]<0)[0])    
    
    return outmask.astype(np.uint8)


def get_model(modelpath, n_classes=3):
    
    state_dict = torch.load(modelpath, map_location=torch.device('cpu'))

    model = UNet(n_classes=n_classes, padding=True, depth=5, up_mode='upsample', batch_norm=True, residual=False)
    
    model.load_state_dict(state_dict)
    model.eval()
    return model


from glob import glob
import os
# data=glob(os.path.join('D:/Projects/AI Diagnostics/3D Lung Segmentation/imagesTs',"*"))

# for d in data:
#     # print(d.split("\\")[-1])
#     input_image = sitk.ReadImage(d)
#     se= apply(input_image)  

#     ni_img = nib.Nifti1Image(se, affine=np.eye(4))
#     nib.save(ni_img, ("outputs/"+d.split("\\")[-1]))

input_image = sitk.ReadImage("outputs/3000566.nii.gz")
se= apply(input_image)  
# print(se.shape)
np.save("mask_lung_002.npy",se)


ni_img = nib.Nifti1Image(se, affine=np.eye(4))
nib.save(ni_img, "mas_lung_002.nii")
