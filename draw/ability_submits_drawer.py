# 绘制一下学生能力值和有效提交数的图，探索一下有没有什么关系
import matplotlib.pyplot as plt

import calculate.Calculator as Calculator


def draw(group):
    subindex = 320 + group + 1
    subplot = plt.subplot(subindex)
    ability = Calculator.get_student_ability(group)
    student_case_map = Calculator.get_student_case_map(group)
    ability_sort = sorted(ability.items(), key=lambda x: x[1])
    array_ability = []
    array_submits = []
    for item in ability_sort:
        array_ability.append(item[1])
        array_submits.append(get_submits(student_case_map[item[0]]))
    print(array_ability)
    print(array_submits)
    index = [i for i in range(len(array_submits))]
    subplot.plot(index, array_submits)
    subplot1 = subplot.twinx()
    subplot1.plot(index, array_ability,color='r')
    subplot.set_title('group{}'.format(group))
    subplot.legend(['num of submit'])
    subplot1.legend(['ability'])


def get_submits(case_map):
    res = 0
    for key in case_map.keys():
        if case_map[key] != None:
            res += 1
    return res


if __name__ == '__main__':
    for i in range(5):
        draw(i)
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    plt.show()
