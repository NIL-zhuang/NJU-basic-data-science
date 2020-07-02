import json

import DataUtils
from evaluator import ScoreEvaluator

raw_case_map = {}  # 未处理的数据，map，键为case_id，内容为CaseData
deal_case_map = {}  # 修正后的数据


class CaseData:
    def __init__(self, case_id, user_id, url, score, time, line):
        self.user_id = user_id
        self.case_id = case_id
        self.url = url
        self.score = score
        self.time = time
        self.line = line
        # [self.time, self.line] = ScoreEvaluator.getscore(url)

    def __str__(self):
        return 'user:' + str(self.user_id) + ' case:' + str(self.case_id) +' score:' + str(self.score) + ' time:' + str(self.time) + ' line:' + str(
            self.line)

    def __copy__(self):
        copy = CaseData(self.case_id, self.user_id, self.url, self.score, self.time, self.line)
        return copy


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
        deal_case_map[case_id] = []
        for raw_case in raw_case_map[case_id]:
            temp = raw_case.copy()
            # TODO:缺省值处理加载这里，temp是新的对象
            temp.time = DataUtils.omega(raw_case.time, timeAVG, timeVAR)
            temp.line = DataUtils.omega(raw_case.line, lineAVG, lineVAR)
            deal_case_map[case_id].append(temp)
            print(temp)


# 数据读取
def read_data():
    # f = open('C:\\Users\\admin\\Desktop\\数据科学基础\大作业\\test_data.json', encoding='utf-8')
    f = open('C:\\Users\\admin\\Desktop\\数据科学基础\大作业\\sample.json', encoding='utf-8')
    res = f.read()
    data = json.loads(res)
    for student in data:
        cases = data[student]['cases']
        for case in cases:
            raw_score = case['upload_records'][-1]['score']
            url = case['upload_records'][-1]['code_url']
            res = ScoreEvaluator.getScore(url)
            if res[0]:  # 如果不是异常提交，才加入
                if case['case_id'] not in raw_case_map.keys():
                    raw_case_map[case['case_id']] = []
                temp = CaseData(case['case_id'], student, url, raw_score*res[1], res[2], res[3])
                print(temp)
                # raw_case_map[case['case_id']].append(temp)
    # print(raw_case_map)


if __name__ == '__main__':
    read_data()
    # pre_deal_data()
