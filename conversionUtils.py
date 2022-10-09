
import os

import dicom2nifti
import SimpleITK as sitk


def get_nifti_from_dicomdir_old(path_to_dicom_series):
    nifti_file_name = 'skull.nii.gz'
    nifti_file_path = os.path.join(os.getcwd(), nifti_file_name)

    dicom2nifti.settings.disable_validate_orthogonal()
    dicom2nifti.dicom_series_to_nifti(path_to_dicom_series, nifti_file_path)

    return nifti_file_name

def get_nifti_from_dicomdir(path_to_dicom_series):
    nifti_file_name = 'skull.nii.gz'
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(path_to_dicom_series)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()

    # Added a call to PermuteAxes to change the axes of the data
    image = sitk.PermuteAxes(image, [2, 1, 0])

    sitk.WriteImage(image, nifti_file_name)
    return nifti_file_name
