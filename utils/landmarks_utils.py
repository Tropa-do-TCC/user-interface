import json
from neuralnetwork import execute_neural_network


def convert_landmarks_to_ras_coordinates(lps_landmarks):
    for lps_landmark in lps_landmarks:
        yield [-lps_landmark[0], -lps_landmark[1], lps_landmark[2]]


def load_landmarks_from_file(json_file_path):
    extension = json_file_path.split(".")[-1]
    if extension == "json":
        with open(json_file_path, 'r') as json_file:
            landmarks_obj = json.load(json_file)['markups'][0]['controlPoints']
            lps_landmarks = [obj['position'] for obj in landmarks_obj]
    elif extension == "txt":
        with open(json_file_path, 'r') as file:
            lps_landmarks = []
            read = file.read().splitlines()
            for line in read:
                points = line.split()
                converted_points = []

                for one_point in points:
                    converted_points.append(float(one_point))
                lps_landmarks.append(converted_points)
    return lps_landmarks


def get_landmarks_from_network_infer(file_path_cranial):
    real_landmark, detected_landmarks = execute_neural_network.made_a_test_infer_landmarks_and_reconstruct_with_one_skull(
        file_path_cranial.split("/")[-1].split(".")[0])
    return real_landmark, detected_landmarks
