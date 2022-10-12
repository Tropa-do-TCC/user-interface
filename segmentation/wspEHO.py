# %%
import random
import math
import cv2
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass, field

# %%
from ipynb.fs.full.wspShannonEvaluation import wspShannonEvaluation
from ipynb.fs.full.wspTsallisEvaluation import wspTsallisEvaluation

# %%


@dataclass
class Elephant:
    chrom: field(default_factory=lambda: [])
    cost: float = 0

# %%


def sort_elephants(elephants, fitness, n, hist, lb, ub, objFunc, q):
    for i in range(n):  # Evaluation
        fitness[i] = -objFunc(hist, elephants[i], lb, ub, q)

    indice = np.argsort(fitness)
    fitness.sort()

    ele = np.array(elephants)
    sorted_elephants = ele[indice]

    return sorted_elephants, fitness

# %%


def CalculateClanCenter(Clan, cindex, dim, numElephantInEachClan):
    ClanCenter = np.zeros(dim)

    for Elephantindex in range(numElephantInEachClan):
        ClanCenter = ClanCenter + Clan[cindex][Elephantindex].chrom

    ClanCenter = (1/numElephantInEachClan)*ClanCenter

    return ClanCenter

# %%


def ClearDups(NewClan, lb, ub):
    """Clear Duplicates"""
    for i in range(len(NewClan)):
        Chrom1 = np.sort(NewClan[i].chrom)
        for j in range(i+1, len(NewClan)):
            Chrom2 = np.sort(NewClan[j].chrom)
            if np.array_equal(Chrom1, Chrom2):
                parnum = round(len(NewClan[j].chrom) * np.random.uniform(0, 1))
                NewClan[j].chrom[parnum] = math.floor(
                    lb + (ub - lb + 1) * np.random.uniform(0, 1))

    return NewClan

# %%


def FeasibleFunction(NewClan, n, dim, lb, ub):
    for i in range(n):
        NewClan[i].chrom = np.clip(NewClan[i].chrom, lb, ub)
        NewClan[i].chrom.sort()

    return NewClan

# %%


def CostFunction(NewClan, hist, n, dim, lb, ub, objFunc, q):
    for i in range(len(NewClan)):
        threshs = NewClan[i].chrom
        NewClan[i].cost = -objFunc(hist, threshs.astype(int), lb, ub, q)

    return NewClan

# %%


def PopSort(NewClan):
    NewClan = sorted(NewClan, key=lambda x: x.cost)
    return NewClan

# %%


def CombineClan(NewClan, n, nClan, dim):
    j = 0
    popindex = 0
    Population = [Elephant(np.zeros(dim)) for w in range(n)]

    while popindex < n:
        for clanindex in range(nClan):
            Population[popindex] = NewClan[clanindex][j]
            popindex += 1

        j += 1

    return Population

# %%


def wspElephantHerding(n, dim, nkE, nClan, alpha, beta, maxGeneration, hist, lb, ub, objFunc, q):
    """"
    Elephant Herding Algorithm

    :param n: number of elephants
    :param d: dimension
    :param nkE: (elitism parameter) how many of the best elephants to keep from one generation to the next
    :param nClan: Number of clans
    :param alpha: Impact facotr of matriarch
    :param beta: attractivity factor
    :param maxGeneration: number of max generation
    :param hist: histogram

    :return: thresholding set fi = {l1, l2, ..., ld }
    """
    t = 0
    keep = nkE
    lb = lb + 1
    ub = ub - 1
    numElephantInEachClan = round(n/nClan)
    nEvaluations = n
    # random.seed(0) # Reset the random generator
    # np.random.seed(0)

    elephants = []

    for _ in range(n):  # generate elephants with d-dimensional solution
        elephant = random.sample(range(lb, ub), dim)
        elephant.sort()
        elephants.append(elephant)

    fitness = np.zeros(n)  # Initial fitness of each elephant

    chromKeep = np.zeros((keep, dim), dtype=int)
    costKeep = np.zeros(keep)
    Clan = [[Elephant(np.zeros(dim)) for x in range(
        numElephantInEachClan)] for y in range(nClan)]

    # Sort all the elephants according to their fitness.
    elephants, fitness = sort_elephants(
        elephants, fitness, n, hist, lb, ub, objFunc, q)

    while t < maxGeneration:

        """           Elitism Strategy           """
        # Save the best elephants in a temporary array.
        for i in range(keep):
            chromKeep[i] = elephants[i]
            costKeep[i] = fitness[i]

        """Divide the whole elephant population into some clans according to their fitness."""
        j = 0
        popIndex = 0

        while popIndex < n:
            for cindex in range(nClan):
                Clan[cindex][j] = Elephant(
                    elephants[popIndex], fitness[popIndex])
                popIndex += 1

            j += 1

        """              Clan Updating Operator              """
        j = 0
        popIndex = 0
        NewClan = [[Elephant(np.zeros(dim)) for x in range(
            numElephantInEachClan)] for y in range(nClan)]

        while popIndex < n:
            for cindex in range(nClan):
                ClanCenter = CalculateClanCenter(
                    Clan, cindex, dim, numElephantInEachClan)
                NewClan[cindex][j].chrom = Clan[cindex][j].chrom + alpha * (np.array(
                    Clan[cindex][0].chrom) - np.array(Clan[cindex][j].chrom)) * np.random.uniform(0, 1, dim)

                if np.sum(NewClan[cindex][j].chrom - Clan[cindex][j].chrom) == 0:
                    NewClan[cindex][j].chrom = beta * ClanCenter

                popIndex += 1

            j += 1

        """           Separating Operator          """
        for cindex in range(nClan):
            NewClan[cindex][len(NewClan[cindex])-1].chrom = lb + \
                (ub - lb + 1)*np.random.uniform(0, 1, dim)

        """           Evaluate NewClan          """
        SavePopSize = n
        for i in range(nClan):
            n = numElephantInEachClan
            # Make sure the population does not have duplicates.
            NewClan[i] = ClearDups(NewClan[i], lb, ub)
            # Make sure each individual is legal.
            NewClan[i] = FeasibleFunction(NewClan[i], n, dim, lb, ub)
            # Calculate cost
            NewClan[i] = CostFunction(
                NewClan[i], hist, n, dim, lb, ub, objFunc, q)
            # the number of fitness evaluations
            nEvaluations = nEvaluations + n
            # Sort from best to worst
            NewClan[i] = PopSort(NewClan[i])
        n = SavePopSize

        """Combine two subpopulations into one and rank monarch butterflis"""
        Population = CombineClan(NewClan, n, nClan, dim)
        Population = PopSort(Population)

        """           Elitism Strategy          """
        # Replace the worst with the previous generation's elites.
        p_size = len(Population)-1
        for k in range(keep):
            Population[p_size-k].chrom = chromKeep[k]
            Population[p_size-k].cost = costKeep[k]

        # Sort from best to worst
        Population = PopSort(Population)

        t += 1
    return (Population[0].chrom).astype(int)
