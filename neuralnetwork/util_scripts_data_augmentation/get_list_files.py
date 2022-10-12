with open("./neuralnetwork/data/already_trained") as file:
    new_points = []
    read = file.read().splitlines()
    for ct in read:
        ct_number = (ct.replace("CT-", ""))
        new_points.append(int(ct_number))
        new_points.sort()
    print(new_points)