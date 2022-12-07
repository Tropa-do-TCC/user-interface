class VtkVolume:
    def __init__(self):
        self.reader = None
        self.property = None
        self.patient_name = ''
        self.nifti_path = ''
        self.dicom_dir = ''
