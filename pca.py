import numpy as np
import json

types = ['字符串', '线性表', '数组', '查找算法', '树结构', '图结构', '数字操作', '排序算法']


def get_matrix():
    f = open('abilities/final_abilities.json', encoding='utf-8')
    data = json.loads(f.read())
    res = []
    for student in data:
        tmp = []
        for t in data[student]:
            tmp.append(data[student][t])
        res.append(tmp)
    return np.asmatrix(res)


def means(data):
    return np.mean(data, axis=0)


def pca(matrix, k):
    average = means(matrix)
    m, n = np.shape(matrix)
    if k > n:
        print('k必须小于特征数')
        return
    avgs = np.tile(average, (m, 1))
    data_adjust = matrix - avgs
    cov = np.cov(data_adjust.T)
    feature, vector = np.linalg.eig(cov)
    index = np.argsort(-feature)

    for i in index[:k]:
        print(types[i])

    selectVec = vector.T[index[:k]]
    finalData = data_adjust * selectVec.T
    reconData = (finalData * selectVec) + average
    return finalData, reconData


pca(get_matrix(), 2)
