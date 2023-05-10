import random
import glob
from generate_test_file import generate_list_test_with_list
from generate_train_file import generate_list_train_with_list

def get_all_ct_files():
    list_files = (glob.glob("../data/landmarks_from_ct/*.txt"))
    output = []
    for file_read in list_files:
        name_file = file_read.replace("../data/landmarks_from_ct/", "").replace("_ps.txt", "")
        output.append(name_file)
    return output


def kfoldcv(indices, k=10, seed=42):
    size = len(indices)
    subset_size = round(size / k)
    random.Random(seed).shuffle(indices)
    subsets = [indices[x:x + subset_size] for x in range(0, len(indices), subset_size)]
    kfolds = []
    for i in range(k):
        test = subsets[i]
        train = []
        for subset in subsets:
            if subset != test:
                train.append(subset)
        print("Teste: " + str(len(test)) + str(test))
        print("Treino: " + str(len(train)) + str(train))
        print("===============================")

        kfolds.append((train, test))

    return kfolds


def generate_files_with_kfold():
    kfolds = kfoldcv(get_all_ct_files(), k=4)

    kfold_index = 1
    for kfold in kfolds:
        test = kfold[1]
        train_list = kfold[0]
        train_list_merged = train_list[0] + train_list[1] + train_list[2]

        generate_list_test_with_list(test, "kfold-" + str(kfold_index))
        generate_list_train_with_list(train_list_merged, "kfold-" + str(kfold_index))
        kfold_index+=1


generate_files_with_kfold()