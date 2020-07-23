import matplotlib.pyplot as plt
import numpy as np
import random
import json

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def euclidean(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))


def k_means(dataset, k, iteration):
    """
    :param dataset: 读入的数据集
    :param k: 分成多少簇
    :param iteration: 迭代次数
    :return:
    """
    # 随机取样,初始化簇心向量、标签
    index = random.sample(list(range(len(dataset))), k)
    vectors = [dataset[i] for i in index]
    labels = [-1] * len(dataset)
    # 根据迭代次数重复k-means聚类过程
    clusters = []
    for _ in range(iteration):
        # 初始化簇
        clusters = [[] for __ in range(k)]
        for labelIndex, item in enumerate(dataset):
            classIndex = -1
            minDist = 1e6
            for i, point in enumerate(vectors):
                dist = euclidean(item, point)
                if dist < minDist:
                    classIndex = i
                    minDist = dist
            clusters[classIndex].append(item)
            labels[labelIndex] = classIndex
        for i, cluster in enumerate(clusters):
            clusterHeart = [0 for _ in range(len(dataset[0]))]
            for item in cluster:
                for j, coordinate in enumerate(item):
                    clusterHeart[j] += coordinate / len(cluster)
            vectors[i] = clusterHeart
    return clusters, labels


f = open('../calculate/question_info.json', encoding='utf-8')
data = json.loads(f.read())
dataset = [(data[question]['submits'], data[question]['accepts']) for question in data]
types = [data[question]['type'] for question in data]
C, labels = k_means(dataset, 5, 200)
colValue = ['r', 'y', 'g', 'b', 'c', 'k', 'm', 'grey']
mark = {"字符串": 'd', "数组": 'o', "排序算法": 'v', "线性表": 'x', "查找算法": 's', "数字操作": '*', "图结构": '+', "树结构": '^'}
keys = [key for key in data]
f, ax = plt.subplots(figsize=(15, 10))
for i in range(len(types)):
    if data[keys[i]]['submits'] > 300: continue
    plt.scatter(data[keys[i]]['submits'], data[keys[i]]['accepts'], marker=mark[types[i]],
             color=colValue[labels[i]], label=types[i])
plt.xlabel('submits')
plt.ylabel('accepts')
# ax.legend(loc='upper left')
plt.show()
