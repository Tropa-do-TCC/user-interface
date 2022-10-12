# %%
import random
import math
import cv2
import matplotlib.pyplot as plt
import numpy as np

# %%
from ipynb.fs.full.wspShannonEvaluation import wspShannonEvaluation
from ipynb.fs.full.wspTsallisEvaluation import wspTsallisEvaluation

# %%


def empty_nests(nest, pa, n, dim, lb, ub):
    """Replace some nests by constructing new solutions/nests"""

    # Discovered or not
    tempnest = np.zeros((n, dim))

    K = np.random.uniform(0, 1, (n, dim)) > pa

    stepsize = random.random() * (
        nest[np.random.permutation(n), :] - nest[np.random.permutation(n), :]
    )

    tempnest = nest + stepsize * K

    tempnest = np.int_(tempnest)
    for j in range(len(tempnest)):
        tempnest[j] = np.clip(tempnest[j], lb, ub)
        tempnest[j].sort()

    return tempnest

# %%


def get_cuckoos(nest, best, lb, ub, n, dim):
    tempnest = np.zeros((n, dim))
    tempnest = np.array(nest)
    beta = 3 / 2

    sigma = (
        math.gamma(1 + beta) * math.sin(math.pi * beta / 2)
        /
        (math.gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))
    ) ** (1 / beta)

    s = np.zeros(dim)

    for j in range(0, n):
        s = nest[j, :]
        u = np.random.randn(len(s)) * sigma
        v = np.random.randn(len(s))
        step = u / abs(v) ** (1 / beta)

        stepsize = 0.01 * (step * (s - best))

        s = s + stepsize * np.random.randn(len(s))

        tempnest[j] = np.clip(s, lb, ub)
        tempnest[j].sort()

    return tempnest


# %%
def get_best_nest(nest, new_nest, fitness, n, dim, hist, lb, ub, objectivefunc, q):
    tempnest = np.zeros((n, dim))
    tempnest = np.copy(nest)

    for j in range(0, n):
        fnew = -objectivefunc(hist, new_nest[j], lb, ub, q)
        if fnew <= fitness[j]:
            fitness[j] = fnew
            tempnest[j, :] = new_nest[j, :]

    fmax = min(fitness)
    K = np.argmin(fitness)
    bestlocal = tempnest[K]

    return fmax, bestlocal, tempnest, fitness


# %%
def wspCuckooSearch(n, dim, pa, maxGeneration, hist, lb, ub, objFunc, q):
    """"
    Cuckoo Search algorithm

    :param n: number of nests (or different solutions)
    :param dim: dimension
    :param pa: probability of egg found
    :param maxGeneration: number of max generation
    :param hist: histogram

    :return: thresholding set fi = {l1, l2, ..., ld }
    """
    t = 0
    best_nest = [0]*dim
    lb = lb + 1
    ub = ub - 1

    # random.seed(0) # Reset the random generator

    nests = []  # random inital population

    for _ in range(n):  # generate cuckoos with d-dimensional solution
        cuckoos = random.sample(range(lb, ub), dim)
        cuckoos.sort()
        nests.append(cuckoos)

    new_nest = np.zeros((n, dim))
    new_nest = np.copy(nests)

    fitness = np.zeros(n)  # Initial fitness of each solution

    fmax, best_nest, nests, fitness = get_best_nest(
        nests, new_nest, fitness, n, dim, hist, lb, ub, objFunc, q)

    while t < maxGeneration:
        # Generate new solutions (but keep the current best)
        new_nest = get_cuckoos(nests, best_nest, lb, ub, n, dim)
        # Evaluate new solutions and find best
        fnew, best, nests, fitness = get_best_nest(
            nests, new_nest, fitness, n, dim, hist, lb, ub, objFunc, q)

        new_nest = empty_nests(new_nest, pa, n, dim, lb, ub)

        # Evaluate new solutions and find best
        fnew, best, nests, fitness = get_best_nest(
            nests, new_nest, fitness, n, dim, hist, lb, ub, objFunc, q)

        if fnew > fmax:
            fmax = fnew
            best_nest = best

        t += 1

    return best_nest
