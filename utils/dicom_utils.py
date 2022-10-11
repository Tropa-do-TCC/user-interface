import os

import pydicom


def get_patient_name(dicom_dir_path):
    first_slice = pydicom.dcmread(os.path.join(
        dicom_dir_path, os.listdir(dicom_dir_path)[0]))
    return first_slice.PatientName
