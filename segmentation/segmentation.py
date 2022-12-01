import os
import time

import segmentation.dicomHandler as dicomHandler
import segmentation.wspMultithreshold as wspMultithreshold
from morph_operations.morph_operations import apply_closing
from morph_operations.filtters_operation import gaussian_filter
import concurrent.futures
from itertools import repeat

def segment_slice(dcm_file_path, input_dir, current_bio, current_dim, current_q, current_gamma, output_dir):
    dicom_img = input_dir + '/' + dcm_file_path
    
    dicom_image, pixel_array = dicomHandler.read_dicom_image(dicom_img)

    transformed_pixel_array = dicomHandler.image_transformation(pixel_array, current_gamma)

    original_image = pixel_array.copy()

    hu_image = dicomHandler.transform_to_hu(dicom_image, transformed_pixel_array)

    hist, bin_edges, best_thresholds, img_thres = wspMultithreshold.wspMultithreshold(hu_image, current_bio, current_dim, current_q)

    high_intensity = wspMultithreshold.get_high_intensity_pixels(img_thres)

    pixel_array = dicomHandler.transform_to_pixel_array(dicom_image, high_intensity)

    hard_tissue = wspMultithreshold.get_largests_regions(pixel_array, original_image)

    dicomHandler.save_dicom(dicom_image, pixel_array, f'{output_dir}/{dcm_file_path}')

def segmentate(image_folder, bio_algorithm, dimension, q, gama):
    input_dir = image_folder
    all_slices = os.listdir(input_dir)
    current_date = time.strftime("%Y-%m-%d-%H-%M-%S")
    output_dir = input_dir + f"-{current_date}-{bio_algorithm}-d{dimension}-q{q}"
    os.mkdir(output_dir)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(segment_slice, all_slices, repeat(input_dir), repeat(bio_algorithm), repeat(dimension), repeat(q), repeat(gama), repeat(output_dir))

    return output_dir
