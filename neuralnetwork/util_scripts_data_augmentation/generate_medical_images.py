import shutil

PATH_DATA_FOLDER = "../data/nifit_files_from_ct/CT-"


def generate_images_niigz(file_path="../data/nifit_files_from_ct/CT-144.nii.gz"):
    for i in range(1, 50):
        new_file = PATH_DATA_FOLDER + str(i) + ".nii.gz"
        shutil.copyfile(file_path, new_file)

