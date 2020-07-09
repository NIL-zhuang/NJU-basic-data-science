import json

import matplotlib.pyplot as plt


# 按照固定区间长度绘制频率分布直方图
# bins_interval 区间的长度
# margin        设定的左边和右边空留的大小
def probability_distribution(data, bins_interval=2, margin=1):
    bins = range(min(data), max(data) + bins_interval, bins_interval)
    print('组数:', len(bins))
    for i in range(0, len(bins)):
        print(bins[i])
    plt.xlim(min(data) - margin, max(data) + margin)
    plt.title("Probability-distribution")
    plt.xlabel('Interval')
    plt.ylabel('Probability')
    # 频率分布normed=True，频次分布normed=False
    # normed is deprecated; use the density keyword argument instead
    plt.hist(x=data, bins=bins, density=True, histtype='bar', color=['r'], alpha=0.8)
    # plt.yticks([])
    plt.grid(True)
    # plt.savefig('Probability-distribution.png')
    plt.show()


if __name__ == '__main__':
    case_map = {}  # 题目集合
    f = open('test_data.json', encoding='utf-8')
    res = f.read()
    data = json.loads(res)
    for student in data:
        cases = data[student]['cases']
        for case in cases:
            if case['case_id'] in case_map.keys():
                case_map[case['case_id']]['student'].append(int(student))
            else:
                case_map[case['case_id']] = {}
                case_map[case['case_id']]['student'] = [int(student)]
    arr = []
    # print(len(case_map.keys()))
    for i in case_map.keys():
        print('题目id', i, end=" ")
        print('作答人数', len(case_map[i]['student']))
        arr.append(len(case_map[i]['student']))
    arr = sorted(arr)
    print(max(arr), min(arr))
    probability_distribution(arr, 4, 5)
