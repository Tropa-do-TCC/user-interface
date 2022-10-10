import SimpleITK as sitk


def get_nifti_from_dicomdir(path_to_dicom_series):
    nifti_file_name = 'skull.nii.gz'

    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(path_to_dicom_series)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()

    image = sitk.PermuteAxes(image, [2, 1, 0])

    sitk.WriteImage(image, nifti_file_name)

    return nifti_file_name
