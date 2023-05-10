PATH_DATA_FILE_TRAIN = "../data/list_train.txt"
PATH_DATA_FILE_TRAIN_NETWORK = "./neuralnetwork/data/list_train.txt"
PATH_DATA_FILE_TEST_NETWORK = "./neuralnetwork/data/list_test.txt"


def generate_list_train():
    with open(PATH_DATA_FILE_TRAIN, 'w') as f:
        for i in range(0, 50):
            f.write("CT-" + str(i) + "\n")
        f.close()


def generate_list_train_with_list(list_read, custom_name=PATH_DATA_FILE_TRAIN_NETWORK):
    with open(custom_name, 'w') as f:
        for folder_read in list_read:
            f.write(folder_read + "\n")
        f.close()
