import numpy as np
import matplotlib.pyplot as plt
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


def pca(matrix, k):
    average = np.mean(matrix, axis=0)
    m, n = np.shape(matrix)
    if k > n:
        print('k必须小于特征数')
        return
    data_adjust = matrix - average
    cov = np.cov(data_adjust.T)
    feature, vector = np.linalg.eig(cov)
    index = np.argsort(-feature)

    for i in index[:k]:
        print(types[i])

    selectVec = vector.T[index[:k]]
    finalData = data_adjust * selectVec.T
    reconData = (finalData * selectVec) + average
    return finalData, reconData


def plotBestFit(data1, data2):
    dataArr1 = np.array(data1)
    dataArr2 = np.array(data2)
    m = np.shape(dataArr1)[0]
    axis_x1 = []
    axis_y1 = []
    axis_x2 = []
    axis_y2 = []
    for i in range(m):
        axis_x1.append(dataArr1[i, 0])
        axis_y1.append(dataArr1[i, 1])
        axis_x2.append(dataArr2[i, 0])
        axis_y2.append(dataArr2[i, 1])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(axis_x1, axis_y1, s=50, c='red')
    ax.scatter(axis_x2, axis_y2, s=50, c='blue')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig('abilities_pca.png')
    plt.show()


finalData, reconData = pca(get_matrix(), 2)
plotBestFit(finalData, reconData)

