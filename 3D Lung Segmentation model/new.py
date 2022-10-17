import numpy as np
import SimpleITK as sitk
image = sitk.ReadImage("D:/Projects/AI Diagnostics/3D Lung Segmentation V2/imagesTs/lung_002.nii.gz")
directions = np.asarray(image.GetDirection())

print(image)