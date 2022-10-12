import shutil

PATH_DATA_FOLDER = "./data/Images/CT-"


def generate_images_niigz(file_path="../data/Images/data0.nii.gz"):
    for i in range(1, 200):
        new_file = PATH_DATA_FOLDER + str(i) + ".nii.gz"
        shutil.copyfile(file_path, new_file)
