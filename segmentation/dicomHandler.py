# %%
import matplotlib.pyplot as plt
from pydicom import dcmread
import os
import numpy as np
from pydicom.pixel_data_handlers.util import apply_modality_lut

# %%


def transform_to_hu(medical_image, image):
    intercept = medical_image.RescaleIntercept
    slope = medical_image.RescaleSlope
    hu_image = image * slope + intercept

    return hu_image

# %%


def transform_to_pixel_array(medical_image, hu_image):
    intercept = medical_image.RescaleIntercept
    slope = medical_image.RescaleSlope
    image = (hu_image - intercept)/slope

    return image.astype(np.int16)

# %%


def show_dicom_image(med_img, title=""):
    plt.figure(figsize=(15, 7))
    plt.imshow(med_img, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()

# %%


def read_dicom_image(file_path):
    medical_image = dcmread(file_path)
    pixel_array = medical_image.pixel_array
    return medical_image, pixel_array

# %%


def save_dicom(dicom, new_image, file_path):
    dicom.PixelData = new_image.tobytes()
    dicom.save_as(file_path)
