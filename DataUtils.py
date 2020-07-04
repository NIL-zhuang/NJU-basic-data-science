import numpy as np


def getAVG(arr):
    return np.average(arr)


def getVAR(arr):
    return np.var(arr)


def omega(x, avg, var):
    if var == 0:
        return 1
    temp = (x - avg) / var
    if temp > 1.29:
        return 0.871
    elif temp < -1.29:
        return 1.129
    else:
        return 1 - temp / 10


if __name__ == '__main__':
    array = [1, 2, 3, 4, 5, 6]
    pj = getAVG(array)
    fc = getVAR(array)
    for i in array:
        omega(i, pj, fc)
