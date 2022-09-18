import random
PATH_DATA_FILE_LANDMARKS = "./data/landmarsk_from_ct/"


def generate_random_landmarks(file_path="../data/landmarks_from_ct/data1_ps.txt"):
    for i in range(100, 200):
        new_file = "CT-" + str(i) + "_ps"

        with open(file_path) as file:
            new_points = []
            read = file.read().splitlines()
            for line in read:
                points = line.split()
                print(points)

                num_1 = float(points[0]) + random.randrange(-2, 3)
                num_2 = float(points[1]) + random.randrange(-2, 3)
                num_3 = float(points[2]) + random.randrange(-2, 3)
                new_points.append([num_1, num_2, num_3])

            with open(PATH_DATA_FILE_LANDMARKS + new_file + '.txt', 'w') as f:
                for points in new_points:
                    f.write(str(points[0]) + " " + str(points[1]) + " " + str(points[2]) + "\n")
                f.close()
