import matplotlib.pyplot as plt
import numpy as np
import json


def draw_submits():
    f = open('../test_data.json', encoding='utf-8')
    data = json.loads(f.read())
    res = []
    for student in data:
        sum_of_submits = 0
        for case in data[student]['cases']:
            sum_of_submits += len(case['upload_records'])
        res.append(sum_of_submits)
    ax = plt.subplot(projection='polar')
    theta = [i * 2 * np.pi / len(data) for i in range(len(data))]
    ax.plot(theta, res, linewidth=1)  # 第一个参数为角度，第二个参数为极径
    ax.grid(True)  # 是否有网格
    plt.show()


if __name__ == '__main__':
    draw_submits()
