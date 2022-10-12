# %%
import numpy as np
import skimage
from skimage import measure
import matplotlib.pyplot as plt

# %%
from ipynb.fs.full.wspFFA import wspFirefly
from ipynb.fs.full.wspCS import wspCuckooSearch
from ipynb.fs.full.wspKH import wspKrillHerd
from ipynb.fs.full.wspEHO import wspElephantHerding
from ipynb.fs.full.wspABC import wspArtificialBeeColony

# %%
from ipynb.fs.full.wspShannonEvaluation import wspShannonEvaluation
from ipynb.fs.full.wspTsallisEvaluation import wspTsallisEvaluation

# %%


def wspGrayHistogram(hu_img):
    lower_bound = int(hu_img.min())
    upper_bound = int(hu_img.max())+1

    #hist, _ = np.histogram(hu_img,256,[0,255])
    hist, bin_edges = np.histogram(hu_img, abs(
        lower_bound)+upper_bound, [lower_bound, upper_bound])
    bin_edges = bin_edges[:-1]

    hist = hist/np.sum(hist)

    return hist, bin_edges, lower_bound, upper_bound

# %%


def apply_threshold(img, thresh, lb, ub):
    row, col = img.shape

    colors = [*range(lb, ub, round(ub/len(thresh)))]
    colors.append(ub)
    #print(colors, thresh)

    img_thres = np.zeros((row, col))

    for i in range(0, row):
        for j in range(0, col):
            pixel = img[i, j]
            color = -1

            for k in range(0, len(thresh)):
                if pixel < thresh[k]:
                    color = colors[k]
                    break

            if color == -1:
                color = colors[len(colors)-1]

            img_thres[i, j] = color

    return img_thres

# %%


def get_high_intensity_pixels(dicom_img):
    max_value = dicom_img.max()
    min_value = dicom_img.min()

    #dicom_img = (dicom_img == max_value) * max_value
    #dicom_img[dicom_img==0] = min_value

    dicom_img = np.where(dicom_img == max_value, max_value, min_value)

    return dicom_img

# %%


def get_largest_region(pixel_array):
    max_value = pixel_array.max()
    min_value = pixel_array.min()

    labels_mask = measure.label(pixel_array)

    regions = measure.regionprops(labels_mask)
    regions.sort(key=lambda x: x.area, reverse=True)

    if len(regions) > 1:
        for rg in regions[1:]:
            labels_mask[rg.coords[:, 0], rg.coords[:, 1]] = min_value

    labels_mask[labels_mask != min_value] = max_value
    mask = labels_mask

    return mask.astype(np.int16)

# %%


def run_firefly(hist, lb, ub, dimension, entropy, q):
    n = 50
    d = dimension
    gama = 1
    alpha = .97
    beta = 1
    maxGeneration = 100

    best_thresholds = wspFirefly(
        n, d, gama, alpha, beta, maxGeneration, hist, lb, ub, entropy, q)

    return best_thresholds

# %%


def run_cuckoo_search(hist, lb, ub, dimension, entropy, q):
    n = 40
    d = dimension
    pa = 0.5
    maxGeneration = 100

    best_thresholds = wspCuckooSearch(
        n, d, pa, maxGeneration, hist, lb, ub, entropy, q)

    return best_thresholds

# %%


def run_krill_herd(hist, lb, ub, dimension, entropy, q):
    n = 40
    d = dimension
    maxGeneration = 100

    best_thresholds = wspKrillHerd(
        n, d, maxGeneration, hist, lb, ub, entropy, q)

    return best_thresholds

# %%


def run_elephant_herding(hist, lb, ub, dimension, entropy, q):
    n = 200
    nkE = 2
    nClan = 5
    alpha = 0.5
    beta = 0.1
    d = dimension
    maxGeneration = 100

    best_thresholds = wspElephantHerding(
        n, d, nkE, nClan, alpha, beta, maxGeneration, hist, lb, ub, entropy, q)

    return best_thresholds

# %%


def run_artificial_bee_colony(hist, lb, ub, dimension, entropy, q):
    n = 20
    d = dimension
    maxGeneration = 100

    best_thresholds = wspArtificialBeeColony(
        n, d, maxGeneration, hist, lb, ub, entropy, q)

    return best_thresholds

# %%


def switch(alg):
    if alg == 'FFA':
        return run_firefly
    elif alg == 'CS':
        return run_cuckoo_search
    elif alg == 'KH':
        return run_krill_herd
    elif alg == 'EHO':
        return run_elephant_herding
    elif alg == 'ABC':
        return run_artificial_bee_colony

# %%


def wspMultithreshold(hu_img, algorithm, dimension, q):
    hist, bin_edges, lb, ub = wspGrayHistogram(hu_img)

    if q == 1:
        entropy = wspShannonEvaluation
    else:
        entropy = wspTsallisEvaluation

    chosen_algorithm = switch(algorithm)
    best_thresholds = chosen_algorithm(hist, lb, ub, dimension, entropy, q)

    img_thres = apply_threshold(hu_img, best_thresholds, lb, ub)

    return hist, bin_edges, best_thresholds, img_thres
