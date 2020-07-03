import json
import random

import DataUtils
from StudentGroup import getQuestionGroup, getStudentGroup
from temp.CaseData import CaseData

raw_case_map = {}  # 未处理的数据，map，键为case_id，内容为CaseData
case_student_map = {}  # 题目*学生列表
student_case_map = {}  # 学生*题目列表


def mock_getScore(url):
    return True, 1, random.random(), random.random()


# 初始化两个map
def init_map(index):
    question_list = getQuestionGroup(index)
    student_list = getStudentGroup(index)
    for question in question_list:
        case_student_map[question] = {}
        for student in student_list:
            case_student_map[question][student] = None
    for student in student_list:
        student_case_map[student] = {}
        for question in question_list:
            student_case_map[student][question] = None


# 数据预处理
def pre_deal_data():
    for case_id in raw_case_map.keys():
        timeList = []
        lineList = []
        for raw_case in raw_case_map[case_id]:
            # print(raw_case)
            timeList.append(raw_case.time)
            lineList.append(raw_case.line)
        # print(timeList)
        timeAVG = DataUtils.getAVG(timeList)
        timeVAR = DataUtils.getVAR(timeList)
        lineAVG = DataUtils.getAVG(lineList)
        lineVAR = DataUtils.getVAR(lineList)
        for raw_case in raw_case_map[case_id]:
            temp = raw_case.copy()
            # TODO:缺省值处理加在这里，temp是新的对象
            temp.time = DataUtils.omega(raw_case.time, timeAVG, timeVAR)
            temp.line = DataUtils.omega(raw_case.line, lineAVG, lineVAR)
            student_case_map[temp.user_id][temp.case_id] = temp
            case_student_map[temp.case_id][temp.user_id] = temp
            print(temp)


# 数据读取
def read_data():
    f = open('C:\\Users\\admin\\Desktop\\数据科学基础\大作业\\test_data.json', encoding='utf-8')
    # f = open('C:\\Users\\admin\\Desktop\\数据科学基础\大作业\\sample.json', encoding='utf-8')
    res = f.read()
    data = json.loads(res)
    # for student in data:
    for student in student_case_map.keys():
        cases = data[student]['cases']
        for case in cases:
            if len(case['upload_records']) == 0:
                continue
                # 不知道为什么会有空的提交记录...直接跳过叭 不然下面IndexError了
            raw_score = case['upload_records'][-1]['score']
            url = case['upload_records'][-1]['code_url']
            # res = ScoreEvaluator.get_score(url)
            res = mock_getScore(url)
            case_id = case['case_id']
            if res[0]:  # 如果不是异常提交，才加入
                if case_id not in raw_case_map.keys():
                    raw_case_map[case_id] = []
                temp = CaseData(case_id, student, url, raw_score * res[1], res[2], res[3])
                # print(temp)
                raw_case_map[case_id].append(temp)
            student_case_map[student][case_id] = temp
            case_student_map[case_id][student] = temp
    # print(raw_case_map)


if __name__ == '__main__':
    init_map(0)
    read_data()
    pre_deal_data()
