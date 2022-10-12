# %%
import math
import numpy as np

# %% [markdown]
# ### Shannon's Entropy
#
# $P(H) = \{h_1, h_2, ..., h_L\}$
#
# $$S(H) = - \sum_{i=1}^{L}h_i \log_{e}(h_i)$$
#

# %%


def ShannonEntropy(hist):
    sum_region = np.sum(hist)
    if sum_region > 0:
        hist = hist/sum_region

    S = 0

    for h_i in hist:
        if h_i != 0:
            S = S + h_i * math.log(h_i, 2)

    return -S

# %%


def wspShannonEvaluation(hist, thresholds, lb, ub, q=1):
    thresholds = np.concatenate([[lb], thresholds, [ub]])

    n = len(thresholds)

    a = thresholds[0]+1
    b = thresholds[1]

    light = ShannonEntropy(hist[a:b+1])

    for i in range(1, n-1):
        a = thresholds[i]+1
        b = thresholds[i+1]

        ES = ShannonEntropy(hist[a:b+1])
        light += ES

    return light
