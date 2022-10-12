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
def dist(a, b):
    S = 0
    for k in range(len(a)):
        S += (a[k] - b[k]) ** 2
    S = math.sqrt(S)
    return S

# %%
def wspFirefly(n, d, gamma, alpha, beta, maxGeneration, H, lb, ub, objFunc, q):
    """"
    Firefly algorithm

    :param n: number of agents
    :param d: dimension
    :param gamma: absorption coefficient
    :param alpha: step of motion
    :param beta: attractivity factor
    :param maxGeneration: number of max generation
    :param H: histogram

    :return: thresholding set fi = {l1, l2, ..., ld }
    """
    t = 0
    alphat = 1.0
    bests = [0]*d
    
    lb = lb + 1
    ub = ub - 1

    # random.seed(0) # Reset the random generator
    
    fireflies = [] # random initial population

    for _ in range(n): # generate firefly with d-dimensional solution
        firefly = random.sample(range(lb,ub), d)
        firefly.sort()
        fireflies.append(firefly)

    # Iterations or pseudo time marching
    r = []
    for i in range(n):
        lin = [0.0]*n
        r.append(lin)

    Z = [0]*n # Initial light intensity of each firefly

    while t < maxGeneration:
        for i in range(n):
            Z[i] = -objFunc(H, fireflies[i], lb, ub, q)
        
        indice = np.argsort(Z)

        Z.sort()

        Z = [-x for x in Z]
        # Ranking the fireflies by their light intensity
        rank = [0]*n
        for i in range(n):
            rank[i] = fireflies[indice[i]]

        fireflies = rank

        for i in range(n):
            for j in range(n):
                r[i][j] = dist(fireflies[i], fireflies[j])

        alphat = alpha * alphat  # Reduce randomness as iterations proceed
        
        # Move all fireflies to the better locations
        for i in range(n):
            for j in range(n):
                if Z[i] < Z[j]:
                    threshold = random.sample(range(lb, ub), d)
                    threshold.sort()
                    
                    betat = beta * math.exp(-gamma*((r[i][j])**2))

                    if i != n-1:
                        for k in range(d):
                            fireflies[i][k] = int(((1 - betat)*fireflies[i][k] + betat*fireflies[j][k] + alphat*threshold[k])/(1+alphat))
        
        bests = fireflies[0]
        
        t+=1

    bests.sort()
    
    return bests



