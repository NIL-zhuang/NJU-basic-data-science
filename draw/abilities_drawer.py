import matplotlib.pyplot as plt
import numpy as np
import json

labels = ['string', 'list', 'array', 'search-algorithm', 'tree', 'graph', 'numeric-operation', 'sort-algorithm']


theta = np.linspace(0, 2 * np.pi, 8, endpoint=False)
theta = np.append(theta, theta[0])


ax1 = plt.subplot(121, projection='polar')
ax2 = plt.subplot(122, projection='polar')


def draw(ax, data):
    data = np.append(data, data[0])
    ax.plot(theta, data, 'b')
    ax.fill(theta, data, 'b', alpha=0.5)

    ax.set_xticklabels(labels, y=0.01)

    ax.set_yticks([20, 40, 60, 80, 100])


if __name__ == '__main__':
    print('输入目标学生的id: ')
    id = input()
    f = open('../abilities/raw_abilities.json',encoding='utf-8')
    src = json.loads(f.read())
    f.close()
    d = np.array(list(src[id].values()))
    draw(ax1, d)

    f = open('../abilities/final_abilities.json',encoding='utf-8')
    src = json.loads(f.read())
    f.close()
    d = np.array(list(src[id].values()))
    draw(ax2, d)

    plt.show()
