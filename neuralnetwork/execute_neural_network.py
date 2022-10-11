from utils import read_landmarks_from_database
from neuralnetwork.util_scripts_data_augmentation import generate_train_file, generate_test_file
from neuralnetwork import infer, train


def read_predict_landmarks(file_path):
    with open(file_path) as file:
        new_points = []
        read = file.read().splitlines()
        for line in read:
            points = line.split()
            converted_points = []

            for one_point in points:
                converted_points.append(float(one_point))
            new_points.append(converted_points)
    return new_points


def read_dataset():
    # STEP 1: read informations from dataset and generate the files
    read_landmarks_from_database.create_output_folder()
    try:
        ct_folders_list = read_landmarks_from_database.generate_files_landmarks_and_nifit("./dataset/")
        size = len(ct_folders_list)
        train_set = ct_folders_list[0: int(size*0.8)]
        test_set = ct_folders_list[int(size*0.8): size]

        generate_train_file.generate_list_train_with_list(train_set)
        generate_test_file.generate_list_test_with_list(test_set)
        print("Dataset foi lido corretamente!")
        print("Os arquivos de teste e treino também foram gerados!")
    except Exception as ex:
        print(ex)


def train_neural_network_with_dataset():
    # STEP 1: read informations from dataset and generate the files
    read_landmarks_from_database.create_output_folder()
    ct_folders_list = read_landmarks_from_database.generate_files_landmarks_and_nifit("../dataset/")

    # STEP 2: Create train/test files and made neural network train with read ct's
    # size = len(ct_folders_list)
    # train_set = ct_folders_list[0: int(size*0.7)]
    # test_set = ct_folders_list[int(size*0.7): size]

    # generate_train_file.generate_list_train_with_list(train_set)
    # generate_test_file.generate_list_test_with_list(test_set)
    # train.main()


def made_a_test_infer_landmarks_and_reconstruct_with_list():
    infer.main()


def made_a_test_infer_landmarks_and_reconstruct():
    # STEP 3: Use test file with 30% and made the test
    infer.main()

    # STEP 4: Reconstruction with predict landmarks
    test_list = generate_test_file.read_test_file()
    for test_input in test_list:
        original_landmarks = read_predict_landmarks("./data/landmarks_from_ct/" + test_input + "_ps.txt")
        predict_landmarks = read_predict_landmarks("./results/landmarks/test/" + test_input + "_ps.txt")
        # TODO: checar modulo de reconstrucao para confirmar se a pasta é essa msm
        dcm_folder = "./data/" + test_input + "/"
        print(original_landmarks)
        print(predict_landmarks)

        return original_landmarks, predict_landmarks


def made_a_test_infer_landmarks_and_reconstruct_with_one_skull(skull_name):
    generate_test_file.generate_list_test_with_list([skull_name])

    # STEP 3: Crate test file with selected skull and made the test
    infer.main()

    # STEP 4: Reconstruction with predict landmarks
    original_landmarks = read_predict_landmarks("./neuralnetwork/data/landmarks_from_ct/" + skull_name + "_ps.txt")
    predict_landmarks = read_predict_landmarks("./neuralnetwork/results/landmarks/test/" + skull_name + "_ps.txt")
    print(original_landmarks)
    print(predict_landmarks)

    return original_landmarks, predict_landmarks
