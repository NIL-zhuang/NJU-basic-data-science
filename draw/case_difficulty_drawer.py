import matplotlib.pyplot as plt
import calculate.Calculator as Calculator
import numpy as np
import json

labels = ['string', 'list', 'array', 'search-algorithm', 'tree', 'graph', 'numeric-operation', 'sort-algorithm']
types = ['字符串', '线性表', '数组', '查找算法', '树结构', '图结构', '数字操作', '排序算法']
theta = np.linspace(0, 2 * np.pi, 8, endpoint=False)
theta = np.append(theta, theta[0])
f = open('../calculate/question_info.json')
data = json.loads(f.read())
f.close()

difficulties = []
# 分别画五组的难度分布图
for g in range(5):
    case_difficulty = Calculator.get_case_difficulty(g)
    difficulties.append(sum(case_difficulty.values()))
    res = {}
    for t in types:
        res[t] = [0, 0.0]
    for case in case_difficulty:
        for t in types:
            if data[case]['type'] == t:
                res[t][0] += 1
                res[t][1] += case_difficulty[case]
                break
    tmp = []
    for t in types:
        tmp.append(res[t][1]/res[t][0])
    res = np.array(tmp)
    res = np.append(res, res[0])
    ax = plt.subplot(projection='polar')
    ax.plot(theta, res, 'r')
    ax.fill(theta, res, 'r', alpha=0.5)
    ax.set_xticklabels(labels, y=0.01)
    ax.set_title('group{} difficulty'.format(g), size=10)
    plt.savefig('group{}_difficulty'.format(g))
    plt.show()

difficulties = np.array(difficulties)
plt.bar(np.arange(0, 5), difficulties, label='The sum of difficulties')
plt.legend(loc='upper left')
plt.xlabel('group')
plt.ylabel('sum')
plt.savefig('diff_sum_of_groups.png')
plt.show()
