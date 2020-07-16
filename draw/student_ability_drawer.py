# 绘制各组所有学生的成绩分布
import matplotlib.pyplot as plt
import numpy as np

import calculate.Calculator as Calculator


def draw_group_ability():
    ax = plt.subplot(121, projection='polar')
    bx = plt.subplot(122)
    for i in range(5):
        ability = Calculator.get_student_ability(i)
        ability = sorted(ability.values())
        print('第', i, '组')
        print('平均能力值为', np.average(ability))
        print(ability)
        theta = [i * 2 * np.pi / len(ability) for i in range(len(ability))]
        ax.plot(theta, ability, linewidth=2)  # 第一个参数为角度，第二个参数为极径
        bx.plot(theta, ability)
        ax.grid(True)  # 是否有网格
        bx.grid(True)
    bx.set_ylabel('ability')
    plt.legend(["group{}".format(i) for i in range(5)])
    plt.show()


draw_group_ability()
