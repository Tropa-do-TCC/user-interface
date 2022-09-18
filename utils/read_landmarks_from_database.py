import os
from os.path import exists
import shutil

FOLDER_PATH_LANDMARKS = "./neuralnetwork/data/landmarks_from_ct/"
FOLDER_PATH_NIFTI = "./neuralnetwork/data/nifit_files_from_ct/"
FOLDER_PATH_DATA = "./neuralnetwork/data/"


def read_landmarks_points(line):
    new_points = []

    #points = (line.split(":")[1]).replace(",", " ").replace("\"", "").split()
    points = (line.replace(",", "").split(":")[1]).replace("[", "").replace("]", "").split()
    num_1 = float(points[0])
    num_2 = float(points[1])
    num_3 = float(points[2])

    return [num_1, num_2, num_3]


def create_file_with_landmarks(folder, new_points):
    new_file = str(folder) + "_ps"
    with open(FOLDER_PATH_LANDMARKS + new_file + '.txt', 'w') as f:
        for points in new_points:
            f.write(str(points[0]) + " " + str(points[1]) + " " + str(points[2]) + "\n")
        f.close()


def rename_nifi_file(file_path, folder):
    shutil.copyfile(
        file_path + folder + "/cts.nii.gz",
        FOLDER_PATH_NIFTI + folder + ".nii.gz")


def create_output_folder():
    if not exists(FOLDER_PATH_DATA):
        os.mkdir(FOLDER_PATH_DATA)
    if not exists(FOLDER_PATH_LANDMARKS):
        os.mkdir(FOLDER_PATH_LANDMARKS)
    if not exists(FOLDER_PATH_NIFTI):
        os.mkdir(FOLDER_PATH_NIFTI)


def generate_files_landmarks_and_nifit(file_path):
    # Get all folders names
    folders = os.listdir(file_path)
    ct_folders_list = []

    for folder in folders:
        if "CT" in folder:
            ct_folders_list.append(folder)
            if exists(file_path + folder + "/landmarks.json"):
                file_landmarsk_to_read = "/landmarks.json"
            else:
                file_landmarsk_to_read = "/landmarks.mrk.json"

            with open(file_path + folder + file_landmarsk_to_read) as file_landmarsk:
                read_lines = file_landmarsk.read().splitlines()

                read_points_description = []
                for line in read_lines:
                    if "\"position\": " in line:
                        # create txt file with landmarks
                        read_points_description.append(read_landmarks_points(line))

                print("Número de landmarks lidos na pasta " + str(folder) + " : " + str(len(read_points_description)))
                create_file_with_landmarks(folder, read_points_description)

            # create nii.gz file with dataset files
            rename_nifi_file(file_path, folder)

    return ct_folders_list
