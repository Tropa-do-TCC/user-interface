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
class Bee:
    Position: field(default_factory=lambda: [])
    Cost: float = 0

# %%
def FeasibleFunction(newBee, dim, lb, ub):
    newBee = np.clip(newBee, lb, ub)
    newBee.sort()
    
    return newBee

# %%
def CostFunction(thresholds, hist, lb, ub, objFunc, q):
    return -objFunc(hist, thresholds, lb, ub, q)

# %%
def RouletteWheelSelection(P):
    r = np.random.uniform(0, 1)
    C = np.cumsum(P)

    i = (r<=C).nonzero()
    first = i[0][0]
    
    return first

# %%
def wspArtificialBeeColony(n, dim, maxGeneration, hist, lb, ub, objFunc, q):
    """"
    Artificial Bee Colony

    :param n: number of bees
    :param sn: number of food sources (solutions)
    :param dim: dimension
    :param maxGeneration: number of max generation
    :param hist: histogram

    :return: thresholding set fi = {l1, l2, ..., ld }
    """
    
    t = 0
    a = 1  # Acceleration Coefficient Upper Bound
    L = round(0.6*dim*n) # Abandonment Limit Parameter (Trial Limit)

    lb = lb + 1
    ub = ub - 1

    # random.seed(0) # Reset the random generator
    
    # random initial population
    bees = [Bee(np.zeros(dim)) for y in range(n)]

    for i in range(n): # generate firefly with d-dimensional solution
        bee = random.sample(range(lb,ub), dim)
        bee.sort()
        bees[i].Position = bee

    for i in range(n): # Calculate fitness of each solution
        bees[i].Cost = CostFunction(bees[i].Position, hist, lb, ub, objFunc, q)
    
    best_sol = min(bees, key=lambda x: x.Cost)
    

    # Abandonment Counter
    C = np.zeros(n)

    while t < maxGeneration:
        """    Place the EMPLOYED bees on their food sources    """
        # Recruited Bees
        for i in range(n):
            # Choose k randomly, not equal to i
            K = list(range(0,i)) + list(range(i+1,n))
            k = random.choice(K)
            
            # Define Acceleration Coeff.
            phi = a * np.random.uniform(-1, 1, dim)

            # New Bee Position
            new_bee = Bee(np.zeros(dim))
            new_bee.Position = bees[i].Position + phi * (np.array(bees[i].Position) - np.array(bees[k].Position))

            # Make sure each individual is legal.
            new_bee.Position = FeasibleFunction(new_bee.Position, dim, lb, ub)

            # Evaluation
            new_bee.Cost = CostFunction(new_bee.Position.astype(int), hist, lb, ub, objFunc, q)

            # Comparision
            if new_bee.Cost <= bees[i].Cost:
                bees[i] = new_bee
            else:
                C[i] = C[i]+1
        
        # Calculate Fitness Values and Selection Probabilities
        F = np.zeros(n)
        MeanCost = np.mean([b.Cost for b in bees])
        
        for i in range(n):
            F[i] = np.exp(-bees[i].Cost/MeanCost) # Convert Cost to Fitness

        P = F/np.sum(F)

        """    Place the onlooker bees on the food sources depending on their nectar amounts    """
        for m in range(n):
            # Select Source Site
            i = RouletteWheelSelection(P)

            # Choose k randomly, not equal to i
            K = list(range(0,i)) + list(range(i+1,n))
            k = random.choice(K)

            # Define Acceleration Coeff.
            phi = a * np.random.uniform(-1, 1, dim)

            # New Bee Position
            new_bee = Bee(np.zeros(dim))
            new_bee.Position = bees[i].Position + phi * (np.array(bees[i].Position) - np.array(bees[k].Position))

            # Make sure each individual is legal.
            new_bee.Position = FeasibleFunction(new_bee.Position, dim, lb, ub)
            
            # Evaluation
            new_bee.Cost = CostFunction(new_bee.Position.astype(int), hist, lb, ub, objFunc, q)

            # Comparision
            if new_bee.Cost <= bees[i].Cost:
                bees[i] = new_bee
            else:
                C[i] = C[i]+1

        """    Send the scouts to the search area for discovering new food sources    """
        for i in range(n):
            if C[i] >= L:
                bee = np.random.uniform(lb, ub, dim)
                bee.sort()

                bees[i].Position = bee
                bees[i].Cost = CostFunction(bees[i].Position.astype(int), hist, lb, ub, objFunc, q)
                C[i] = 0
                

        """    Memorize the best food source found so far    """
        for i in range(n):
            if bees[i].Cost <= best_sol.Cost:
                best_sol = bees[i]

        t+=1

    return (best_sol.Position).astype(int)


