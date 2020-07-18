import numpy as np
from scipy.cluster.vq import *
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

'''生成示例数据'''
set1 = np.random.normal(1, 0.8, (100, 10))
set2 = np.random.normal(2, 0.8, (100, 10))
set3 = np.random.normal(3, 0.8, (100, 10))
set4 = np.random.normal(4, 0.8, (100, 10))
set5 = np.random.normal(5, 0.8, (100, 10))

'''将两个列数相同的矩阵上下拼接，类似R中的rbind()'''
data = np.concatenate((set1, set2, set3, set4, set5))

'''按行将所有样本打乱顺序'''
np.random.shuffle(data)

'''进行kmeans聚类'''
res, idx = kmeans2(data, 5)

'''为不同类的样本点分配不同的颜色'''
colors = ([([0.4, 1, 0.4], [1, 0.4, 0.4], [0.4, 0.4, 0.4], [0.4, 0.4, 1.0], [1.0, 1.0, 1.0])[i] for i in idx])

'''对样本数据进行降维以进行可视化'''
data_TSNE = TSNE(learning_rate=100).fit_transform(data)

'''绘制所有样本点（已通过聚类结果修改对应颜色）'''
plt.scatter(data_TSNE[:, 0], data_TSNE[:, 1], c=colors, s=12)
plt.title('K-means Cluster')
plt.show()
