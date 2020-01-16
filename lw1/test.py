#! /usr/bin/python3

import numpy as np

def graph_permutation(GM):
    GP = np.array(range(1, GM.shape[0] + 1))
    res = False
    if (GM.shape[0] == GM.shape[1]):
        for n in range(0, GM.shape[0]):
            for m in range(0, GM.shape[1]):
                if (GM[n][m] == 1):
                    GP[n] = m+1
        res = GP
    return(res)

def graph_cycl_formula(GP):
    CF = []
    tmp = []
    for i in range(0, GP.shape[0]):
        if (GP[i] != i + 1):
            tmp.append(GP[i])
        else:
            CF.append([GP[i]])
    CF.append(tmp)
    CF.reverse()
    return(CF)

gm = np.array([[0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0]])
gp = graph_permutation(gm)
print(gp)
cf = graph_cycl_formula(gp)
print(cf)
