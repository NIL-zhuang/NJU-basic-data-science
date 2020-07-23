# 本程序用于数据处理和学生能力值、题目难度计算
import json
import os
import zipfile
from itertools import chain
from math import sqrt
from urllib import error as url_error

import matplotlib.pyplot as plt
import numpy as np

import DataUtils
from StudentGroup import getQuestionGroup, getStudentGroup
from calculate.CaseData import CaseData
from evaluator import ScoreEvaluator

raw_case_map = {}  # 未处理的数据，map，键为case_id，内容为CaseData
case_student_map = {}  # 题目-学生列表
student_case_map = {}  # 学生-题目列表
student_ability = {}  # 学生能力值
case_difficulty = {}  # 题目难度


def root_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


# 算一次，然后存到json里，要不太浪费时间了
def score_evaluator_get_score_save(group):
    """
    :param group: 分组
    :return: 将组内数据写入res.json中
    """
    init_map(group)
    # out = open('group4.json', 'w')
    out = open('test.json', 'w')
    res_map = {}
    f = open('../test_data.json', encoding='utf-8')
    res = f.read()
    f.close()
    data = json.loads(res)
    try:
        for student in student_case_map.keys():
            print('----------------student:', student, '处理开始------------------------')
            res_map[student] = {}
            cases = data[student]['cases']
            for case in cases:
                case_id = case['case_id']
                if len(case['upload_records']) == 0:
                    continue
                    # 不知道为什么会有空的提交记录...直接跳过叭 不然下面IndexError了
                url = case['upload_records'][-1]['code_url']
                try:
                    res = ScoreEvaluator.getScore(url)
                except zipfile.BadZipFile:
                    print(url)
                print('正在处理 student=', student, ',case_id=', case_id)
                print(res)
                if res[2] == 'TIMEOUT':
                    print('timeout', student, case_id)
                res_map[student][case_id] = res

            print('----------------student:', student, '处理结束------------------------')
        out.write(json.dumps(res_map))
        f.close()
        out.close()
    except url_error.URLError:
        print('出现异常')
        f.close()
        out.close()


# 初始化四个map
def init_map(index):
    question_list = getQuestionGroup(index)
    student_list = getStudentGroup(index)
    for question in question_list:
        case_difficulty[question] = 1  # 初始默认难度为1
        case_student_map[question] = {}
        for student in student_list:
            case_student_map[question][student] = None
    for student in student_list:
        student_ability[student] = None
        student_case_map[student] = {}
        for question in question_list:
            student_case_map[student][question] = None


# 数据预处理
def pre_deal_data(alpha=1, beta=1):
    """
    :param alpha: 运行时间权重
    :param beta: 代码行数权重
    """
    for case_id in raw_case_map.keys():
        timeList = []
        lineList = []
        for raw_case in raw_case_map[case_id]:
            # print(raw_case)
            timeList.append(raw_case.time)
            lineList.append(raw_case.line)
        # print(timeList)
        timeAVG = np.average(timeList)
        timeVAR = np.var(timeList)
        lineAVG = np.average(lineList)
        lineVAR = np.var(lineList)
        for raw_case in raw_case_map[case_id]:
            temp = raw_case.copy()
            # TODO:缺省值处理加在这里，temp是新的对象
            time = DataUtils.omega(raw_case.time, timeAVG, timeVAR)
            line = DataUtils.omega(raw_case.line, lineAVG, lineVAR)
            temp.score = temp.score * time ** alpha * line ** beta
            student_case_map[temp.user_id][temp.case_id] = temp
            case_student_map[temp.case_id][temp.user_id] = temp
            # print(temp)


# 数据读取
def read_data(group):
    f2 = open(root_path() + '/calculate/group{}.json'.format(group), encoding='utf-8')
    f = open(root_path() + '/test_data.json', encoding='utf-8')

    res = f.read()
    data = json.loads(res)
    evaluator = json.loads(f2.read())
    # for student in data:
    for student in student_case_map.keys():
        cases = data[student]['cases']
        for case in cases:
            case_id = case['case_id']
            case_type = case['case_type']
            if len(case['upload_records']) == 0:
                continue
                # 不知道为什么会有空的提交记录...直接跳过叭 不然下面IndexError了
            raw_score = case['upload_records'][-1]['score']
            url = case['upload_records'][-1]['code_url']
            res = evaluator[student][case_id]
            # try:
            #     res = evaluator[student][case_id]
            # except KeyError:
            #     print(group)
            #     print(student_case_map[student])
            #     print(student, case_id)
            #     print(evaluator[student])
            #     print(res)
            if res[0] and res[2] != 'ERROR' and res[2] != 'TIMEOUT':  # 如果不是异常提交，才加入
                if case_id not in raw_case_map.keys():
                    raw_case_map[case_id] = []
                temp = CaseData(case_id, student, url, raw_score * res[1], res[2], res[3], case_type)
                # print(calculate)
                raw_case_map[case_id].append(temp)
                student_case_map[student][case_id] = temp
                case_student_map[case_id][student] = temp
    # print(raw_case_map)
    f.close()


# 迭代计算
# times: 迭代轮次
def calculate(times=20):
    """
    :param times: 运行次数
    :return: 拟合后的函数值
    """
    diff_loss_arr, ability_loss_arr = [], []
    for i in range(times):
        # 计算Bi
        diff_loss = ability_loss = 0
        for s in student_ability.keys():  # 对每个学生
            temp_ability = 0
            count = 0  # 有效数据的个数
            for q in case_difficulty.keys():  # 遍历每个题目
                if student_case_map[s][q] is not None:
                    temp_ability += case_difficulty[q] * student_case_map[s][q].score / 20
                    count += 1
            # 这里有两种处理方法，一种是没做的题目也算在n里（即看为0分），一种是不算在n里，不知道取用哪一种
            temp_ability /= len(case_difficulty.keys())
            # temp_ability /= count
            ability_loss += (temp_ability - student_ability[s]) ** 2 if student_ability[s] is not None else 0
            student_ability[s] = temp_ability
        # 计算Qi
        b = 1  # 反正是个常数，当1处理，有需要再修改这里
        array = []
        for value in student_ability.values():
            array.append(value)
        B_AVG = np.average(array)
        B_VAR = np.var(array)
        for q in case_difficulty.keys():
            temp = 0
            count = 0
            for s in student_ability.keys():
                divisor = 1 + abs(student_ability[s] - B_AVG) / sqrt(B_VAR)
                Mij = 0
                if student_case_map[s][q] is not None:
                    Mij = student_case_map[s][q].score
                    count += 1
                temp += b / divisor * ((100 - Mij) if Mij < 100 else 0) / 10
            # 这里同样有两种处理方法，不知道取用哪一种
            temp /= len(student_ability.keys())
            # temp /= count
            diff_loss += (temp - case_difficulty[q]) ** 2 if case_difficulty[q] is not None else 0
            case_difficulty[q] = temp
        print('迭代', i)
        print('题目难度', case_difficulty)
        print('学生能力值', student_ability)
        diff_loss_arr.append(diff_loss)
        ability_loss_arr.append(ability_loss)
    # plt.xlabel('iter time')
    # plt.ylabel('loss')
    # plt.title('difficulty loss')
    # plt.plot(diff_loss_arr[1::], color='r', linewidth=5, linestyle='-', label='难度损失')
    # plt.show()
    # plt.xlabel('iter time')
    # plt.ylabel('loss')
    # plt.title('ability loss')
    # plt.plot(ability_loss_arr[1::], color='g', linewidth=5, linestyle='-', label='能力损失')
    # plt.show()
    # students = list(student_case_map.keys())
    # stu_ability = [student_ability[stu_id] for stu_id in students]
    student_score = []
    # for stu in students:
    #     scores = [student_case_map[stu][q].score * case_difficulty[q] / 2.5 for q in case_difficulty.keys() if
    #               student_case_map[stu][q] is not None]
    #     student_score.append(np.average(scores))
    # return linregress(stu_ability, student_score)
    # for stu_index in range(len(students)):
    #     color = ['red', 'blue', 'green'][np.random.randint(0, 3)]
    #     x, y = stu_ability[stu_index], student_score[stu_index]
    #     plt.scatter(x, y, c=color, alpha=0.6, edgecolors='white')
    # plt.xlabel('student ability')
    # plt.ylabel('average score')
    # plt.grid(True)
    # plt.show()


def run(group, time=5):
    raw_case_map.clear()
    case_student_map.clear()
    student_case_map.clear()  # 清空是为了组组之间互不影响
    case_difficulty.clear()
    student_ability.clear()

    init_map(group)
    read_data(group)
    pre_deal_data()
    calculate(time)
    print("run group {} finish".format(group))


def run_param(times=5):
    """
    执行迭代找好的alpha和beta
    :param times: 迭代次数
    :return:
    """

    x, y = np.arange(-0.15, 0.15, 0.01), np.arange(-0.15, 0.15, 0.01)
    xx, yy = np.meshgrid(x, y)
    ax3 = plt.axes(projection='3d')
    lin_res = []

    def run_rvalue(m):
        alp, be = m
        temp_r_val = 0
        for group_num in range(2, 5):
            raw_case_map.clear()
            case_student_map.clear()
            student_case_map.clear()  # 清空是为了组组之间互不影响
            case_difficulty.clear()
            student_ability.clear()
            init_map(group_num)
            read_data(group_num)
            pre_deal_data(alp, be)
            res = calculate(times)
            temp_r_val += res.rvalue
        temp_r_val /= 3
        print(alp, be, temp_r_val)
        lin_res.append((alp, be, temp_r_val))
        return temp_r_val

    zz = list(map(run_rvalue, zip(chain(*xx), chain(*yy))))
    zz = np.asarray(zz).reshape(*xx.shape)
    ax3.plot_surface(xx, yy, zz, cmap='rainbow', rstride=1, cstride=1)
    plt.xlabel('alpha')
    plt.ylabel('beta')
    plt.title('alpha,beta-rvalue optimize')
    plt.show()
    print("best suit is: ", max(lin_res, key=lambda k: k[2]))


def get_student_ability(group):
    run(group)
    return student_ability


def get_case_difficulty(group):
    run(group)
    return case_difficulty


def get_case_student_map(group):
    run(group)
    return case_student_map


def get_student_case_map(group):
    run(group)
    return student_case_map


def init_group(group):
    run(group)
    return student_case_map, case_difficulty, case_student_map


if __name__ == '__main__':
    # score_evaluator_get_score_save(4)
    # run_param()
    f = open('student_ability.json', encoding='utf-8')
    res = f.read()
    f.close()
    data = json.loads(res)
    # data = get_student_ability(0)
    print('请输入userid:', end=" ")
    userid = input()
    print('ability is ', data[userid])
    data_sort = sorted(data.items(), key=lambda x: x[1])
    for index in range(len(data_sort)):
        if data_sort[index][0] == userid:
            print('超过了', index / len(data_sort) * 100, '%的学生')
