
import matplotlib.pyplot as plt
from pydicom import dcmread
import os
import numpy as np
from pydicom.pixel_data_handlers.util import apply_modality_lut




def image_transformation(pixel_array, b):
    lower_bound = int(pixel_array.min())
    upper_bound = int(pixel_array.max())
    c = 1
    #b = 1.5
    
    transformed = np.sign(pixel_array) * (np.abs(pixel_array)) ** (b)
    normalized = np.interp(transformed, (transformed.min(), transformed.max()), (lower_bound, upper_bound))
    
    return normalized.astype(np.int16)



def transform_to_hu(medical_image, image):
    intercept = medical_image.RescaleIntercept
    slope = medical_image.RescaleSlope
    hu_image = image * slope + intercept

    return hu_image


# https://www.documents.philips.com/doclib/enc/fetch/2000/4504/577242/577256/588723/5144873/5144488/5145048/DICOM_Conformance_Statement_Philips_CT_Scanners_and_Workstations_V2_V3_.pdf
def transform_npy_to_hu(image):
    intercept = -1024
    slope = 1
    hu_image = image * slope + intercept

    return hu_image


def transform_to_pixel_array(medical_image, hu_image):
    intercept = medical_image.RescaleIntercept
    slope = medical_image.RescaleSlope
    image = (hu_image - intercept)/slope

    return image.astype(np.int16)

def transform_to_npy_pixel_array(hu_image):
    intercept = -1024
    slope = 1
    image = (hu_image - intercept)/slope

    return image.astype(np.int16)


def show_dicom_image(med_img, title=""):
    plt.figure(figsize=(15, 7))
    plt.imshow(med_img, cmap='gray')
    plt.title(title)
    plt.axis('off')




def read_dicom_image(file_path):
    medical_image = dcmread(file_path)
    pixel_array = medical_image.pixel_array
    return medical_image, pixel_array

def read_npy_image(file_path):
    pixel_array = np.load(file_path)
    return pixel_array


def save_dicom(dicom, new_image, file_path):
    dicom.PixelData = new_image.tobytes()
    dicom.save_as(file_path)

def save_npy(new_image, file_path):
    with open(file_path, 'wb') as f:
        np.save(f,new_image)