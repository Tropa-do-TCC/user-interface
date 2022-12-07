class VtkVolume:
    def __init__(self):
        self.reader = None
        self.property = None
        self.patient_name: str = ''
        self.nifti_path: str = ''
        self.dicom_dir: str = ''
