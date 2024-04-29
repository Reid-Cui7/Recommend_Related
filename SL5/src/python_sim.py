import numpy as np


def cosine(n_x, yr, min_support):
    prods = np.zeros((n_x, n_x), dtype=np.double)
    freq = np.zeros((n_x, n_x), dtype=np.int32)
    sqi = np.zeros((n_x, n_x), dtype=np.double)
    sqj = np.zeros((n_x, n_x), dtype=np.double)
    sim = np.zeros((n_x, n_x), dtype=np.double)

    for y, y_ratings in yr.items():
        for xi, ri in y_ratings:
            for xj, rj in y_ratings:
                freq[xi, xj] += 1
                prods[xi, xj] += ri * rj
                sqi[xi, xj] += ri**2
                sqj[xi, xj] += rj**2
    
    for xi in range(n_x):
        sim[xi, xi] = 1
        for xj in range(xi + 1, n_x):
            if freq[xi, xj] < min_support:
                sim[xi, xj] = 0
            else:
                denum = sqrt(sqi[xi, xj] * sqj[xi, xj])
                sim[xi, xj] = prods[xi, xj] / denum
            sim[xj, xi] = sim[xi, xj]
    
    return np.asarray(sim)