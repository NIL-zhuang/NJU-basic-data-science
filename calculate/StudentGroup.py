# 探索学生分组情况
import json

group_list = {}  # 每组学生列表
question_list = []  # 每组题目列表


def contain(list1, list2):
    # 判断list2是否真包含于list1
    for item in list2:
        if item not in list1:
            return False
    return True


# 进行分组
def devideGroup(filter=False):
    """
    进行分组
    :param filter: 是否进行过滤，若为true会放弃对100道题以下同学的分组
    :return:
    """
    f = open('../test_data.json', encoding='utf-8')
    res = f.read()
    data = json.loads(res)
    for student in data:
        cases = data[student]['cases']
        tmp = []
        for case in cases:
            tmp.append(case['case_id'])
        tmp = sorted(tmp)
        if len(tmp) >= 199:
            if len(question_list) == 0 or tmp[0] != question_list[-1][0]:
                question_list.append(tmp)
            # 把下面三行注释打开就知道为什么是五组题目了 不过有点奇怪有个做了206题的
            # print('student', student, end=" ")
            # print(len(tmp), end=" ")
            # print(tmp)

    # print("-----------------------------------")
    # print("----------五组的题目分布如下-----------")
    # for q in question_list:
    #     print(q)
    for index in range(len(question_list)):
        group_list[index] = []  # 有几组，就初始化几个key
    #
    failure_user = {}
    # print('正在分组中...')

    for student in data:
        found = False
        cases = data[student]['cases']
        tmp = []
        if filter:  # 过滤100题以下的同学
            if len(cases) < 100:
                failure_user[student] = tmp.copy()
                continue
        for case in cases:
            tmp.append(case['case_id'])
        # 分组逻辑
        for index in range(len(question_list)):
            if contain(question_list[index], tmp):
                # print(student, '第', index, '组')
                group_list[index].append(student)
                found = True
                break
        if not found:
            print('student', student, '分组失败', end=' ')
            failure_user[student] = tmp.copy()
            print('所做题目为:', failure_user[student])

    # for group in group_list.keys():
    #     print('第', group, '组 人数共', len(group_list[group]))
    # print(group_list[group])

    # print('打印分组失败名单...')
    # for user in failure_user.keys():
    #     print(user, failure_user[user])
    # print(len(failure_user[user]))


# 获取分组名单
def getStudentGroup(index):
    isFilte = False
    if len(group_list.keys()) == 0:
        devideGroup(isFilte)
    return group_list[index]


# 获取对应组的题目列表
def getQuestionGroup(index):
    isFilte = False
    if len(group_list.keys()) == 0:
        devideGroup(isFilte)
    return question_list[index]