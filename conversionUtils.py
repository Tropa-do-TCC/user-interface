
import os

import dicom2nifti


def get_nifti_from_dicom_series(path_to_dicom_series):
    dicom2nifti.dicom_series_to_nifti(
        path_to_dicom_series,
        os.path.join(os.getcwd(), 'patient.nii.gz')
    )
