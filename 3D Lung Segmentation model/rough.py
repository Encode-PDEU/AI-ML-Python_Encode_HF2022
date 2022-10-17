import numpy as np
import nibabel as nib

se=np.load("mask_lung_002.npy")
# ni_img = nib.Nifti1Image(se, affine=np.eye(4))
# nib.save(ni_img, "a1_lung_002.nii.gz")

# se=se.reshape((512, 512,269))
ni_img = nib.Nifti1Image(se, affine=np.eye(4))
img = nib.load('timage_res_lung_002.nii.gz')
head=img.header
print(head)
# head.write_to(ni_img)
print(ni_img.header)
# nib.save(ni_img, "a3_lung_002.nii.gz")