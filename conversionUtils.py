
import os

import dicom2nifti


def get_nifti_from_dicomdir(path_to_dicom_series):
    nifti_file_name = 'skull.nii.gz'
    nifti_file_path = os.path.join(os.getcwd(), nifti_file_name)

    dicom2nifti.settings.disable_validate_orthogonal()
    dicom2nifti.dicom_series_to_nifti(path_to_dicom_series, nifti_file_path)

    return nifti_file_name
