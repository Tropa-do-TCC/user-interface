PATH_DATA_FILE_TRAIN = "./neuralnetwork/data/list_train.txt"
PATH_DATA_FILE_TRAIN_NETWORK = "./neuralnetwork/data/list_train.txt"
PATH_DATA_FILE_TEST_NETWORK = "./neuralnetwork/data/list_test.txt"


def generate_list_test_with_list(list_read):
    with open(PATH_DATA_FILE_TEST_NETWORK, 'w') as f:
        for folder_read in list_read:
            f.write(folder_read + "\n")
        f.close()


def generate_empty_test_file():
    with open(PATH_DATA_FILE_TEST_NETWORK, 'w') as f:
        f.close()


def read_test_file():
    with open(PATH_DATA_FILE_TEST_NETWORK, 'r') as f:
        return f.read().splitlines()
