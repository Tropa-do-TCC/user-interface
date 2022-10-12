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


def get_column(matrix, i):
    return [row[i] for row in matrix]

# %%


def findLimits(solution, lb, ub):
    solution = np.clip(solution, lb, ub)
    solution = solution.astype(int)
    solution.sort()

    return solution

# %%


def wspKrillHerd(n, dim, maxGeneration, hist, lb, ub, objFunc, q):
    """"
    Cuckoo Search algorithm

    :param n: number of krills (or different solutions)
    :param dim: dimension
    :param maxGeneration: number of max generation
    :param hist: histogram

    :return: thresholding set fi = {l1, l2, ..., ld }
    """

    t = 0
    lb = lb + 1
    ub = ub - 1
    Dt = np.mean(abs(ub - lb))/2

    # random.seed(0) # Reset the random generator

    F = np.zeros((n, dim))
    D = np.zeros((n, 1))
    N = np.zeros((n, dim))
    Vf = 0.02
    Dmax = 0.005
    Nmax = 0.01
    Sr = 0
    xmin = 0
    xmax = 0.08
    ymin = 0
    ymax = 0.08
    C_flag = 1
    krills = []  # random initial population

    for _ in range(n):  # generate krillls with d-dimensional solution
        fish = random.sample(range(lb, ub), dim)
        fish.sort()
        krills.append(fish)

    fitness = np.zeros(n)  # Initial fitness of each solution

    for i in range(n):  # Calculate fitness of each solution
        fitness[i] = -objFunc(hist, krills[i], lb, ub, q)

    fitnessIb = np.copy(fitness)
    krillsIb = np.copy(krills)

    best_fitness = np.zeros(maxGeneration+1)
    best_krill = np.zeros((maxGeneration+1, dim), dtype=int)

    best_fitness[t] = np.min(fitness)
    index_best_fitness = np.where(fitness == best_fitness[t])[0][0]

    best_krill[t] = krills[index_best_fitness]

    food_fitness = np.zeros(maxGeneration)
    food_krills = np.zeros((maxGeneration, dim), dtype=int)

    while t < maxGeneration:
        temp_fitness = np.array(fitness)

        # Virtual food
        Sf = np.zeros(dim)
        for j in range(0, dim):
            colj = get_column(krills, j)
            Sf[j] = np.sum(np.array(colj)/temp_fitness)

        food_krills[t] = Sf / (sum(1/temp_fitness))  # Food Location
        food_krills[t] = findLimits(food_krills[t], lb, ub)  # Bounds check

        food_fitness[t] = -objFunc(hist, food_krills[t], lb, ub, q)

        if t >= 1:
            if food_fitness[t-1] < food_fitness[t]:
                food_krills[t] = food_krills[t-1]
                food_fitness[t] = food_fitness[t-1]

        Kw_Kgb = np.max(fitness) - best_fitness[t]

        w = (0.1+0.8*(1-t/maxGeneration))

        # For each krill
        for i in range(n):
            # Calculation of distances
            Rf = food_krills[t] - krills[i]

            Rgb = np.array(best_krill[t]) - np.array(krills[i])

            RR = []
            for ii in range(n):
                RR.append(np.array(krills[ii]) - np.array(krills[i]))

            R = np.sqrt(np.sum(np.multiply(RR, RR), axis=1))

            # Movement Induced ##########################33
            # Calculation of BEST KRILL effect

            if best_fitness[t] < fitness[i]:
                alpha_b = -2*(1 + random.uniform(0, 1) * (t/maxGeneration)) * (
                    best_fitness[t] - fitness[i]) / Kw_Kgb / np.sqrt(np.sum(np.multiply(Rgb, Rgb))) * Rgb
            else:
                alpha_b = 0

            # Calculation of NEIGHBORS KRILL effect
            nn = 0
            ds = np.mean(R)/5
            alpha_n = 0

            for j in range(n):
                if R.all() < ds and j != i:
                    nn += 1
                    if nn <= 4 and fitness[i] != fitness[j]:
                        alpha_n = alpha_n - \
                            (fitness[j] - fitness[i]) / Kw_Kgb / R[j] * RR[j]

            # Movement Induced
            N[i] = w*N[i]+Nmax*(alpha_b+alpha_n)

            # Foraging Motion ##########################33
            # Calculation of FOOD atraction
            if food_fitness[t] < fitness[i]:
                Beta_f = -2 * (1-t/maxGeneration)*(
                    food_fitness[t] - fitness[i]) / Kw_Kgb / np.sqrt(np.sum(np.multiply(Rf, Rf))) * Rf
            else:
                Beta_f = 0

            # Calculation of BEST psition attraction
            Rib = krillsIb[i] - krills[i]

            if fitnessIb[i] < fitness[i]:
                Beta_b = -(fitnessIb[i] - fitness[i]) / Kw_Kgb / \
                    np.sqrt(np.sum(np.multiply(Rib, Rib))) * Rib
            else:
                Beta_b = 0

            # Foragin Motion
            F[i] = w*F[i]+Vf*(Beta_b+Beta_f)
            ################# Physical Diffusion ###################
            #print("Menos:", (fitness[i]-best_fitness[t]), "Kw", Kw_Kgb)
            # print((fitness[i]-best_fitness[t])/Kw_Kgb)
            D = Dmax*((1-t)/maxGeneration)*math.floor(random.uniform(0, 1) +
                                                      (fitness[i]-best_fitness[t])/Kw_Kgb)*(2*np.random.uniform(0, 1, dim)-np.ones(dim))

            ################# Motion Process ###################
            DX = Dt*(N[i] + F[i])

            ################# Crossover #######################
            if C_flag == 1:
                C_rate = 0.8 + 0.2*(fitness[i]-best_fitness[t])/Kw_Kgb
                Cr = np.random.uniform(0, 1, dim) < C_rate
                # Random selection of Krill No. for Crossover
                NK4Cr = round((n-1)*random.uniform(0, 1)+0.5)
                # Crossover scheme
                krills[i] = krills[NK4Cr]*(1-Cr)+krills[i]*Cr

            # Update the position
            krills[i] = krills[i] + DX
            krills[i] = findLimits(krills[i], lb, ub)

            fitness[i] = -objFunc(hist, krills[i], lb, ub, q)

            if fitness[i] < fitnessIb[i]:
                fitnessIb[i] = fitness[i]
                krillsIb[i] = krills[i]

        # update the current best
        best_fitness[t+1] = np.min(fitness)
        index_best_fitness = np.where(fitness == best_fitness[t+1])[0][0]

        if best_fitness[t+1] < best_fitness[t]:
            best_krill[t+1] = krills[index_best_fitness]
        else:
            best_fitness[t+1] = best_fitness[t]
            best_krill[t+1] = best_krill[t]

        t += 1

    best_fit = np.max(best_fitness)
    index_best_fit = np.where(best_fitness == best_fit)[0][0]

    threshs = best_krill[index_best_fit]
    return threshs
