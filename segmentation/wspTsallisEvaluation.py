# %%
import numpy as np

# %% [markdown]
# ### Tsallis' Entropy
#
# $$S_q(H) = \frac{1 - \sum_{i=1}^{L}(h_i)^q}{q-1}$$
#

# %%


def TsallisEntropy(hist, q):
    sum_region = np.sum(hist)
    if sum_region > 0:
        hist = hist/sum_region

    S_q = 0

    sums = 0

    for h_i in hist:
        if h_i > 0:
            sums = sums + h_i**q

    S_q = (1 - sums)/(q-1)

    return S_q

# %%


def wspTsallisEvaluation(hist, thresholds, q):
    thresholds = np.concatenate([[0], thresholds, [255]])

    n = len(thresholds)

    a = thresholds[0]+1
    b = thresholds[1]

    light = TsallisEntropy(hist[a:b+1], q)

    if np.isnan(light):
        light = 0

    Plight = light

    for i in range(1, n-1):
        a = thresholds[i]+1
        b = thresholds[i+1]

        ES = TsallisEntropy(hist[a:b+1], q)
        if not np.isnan(ES):
            light += ES
            Plight = Plight * ES

    light = light + (1-q) * Plight

    return light
