# 分析每个学生对不同类别题目的完成情况
# 尝试使用defender.py修正分数
import json
from evaluator import ScoreEvaluator
from calculate import Calculator
from calculate.StudentGroup import getQuestionGroup

f = open('../test_data.json', encoding='UTF-8')
d = f.read()
data = json.loads(d)
f.close()
f = open('question_info.json')
info = json.loads(f.read())
f.close()

types = ['字符串', '线性表', '数组', '查找算法', '树结构', '图结构', '数字操作', '排序算法']  # 题目种类


# 提取指定用户指定类型的题目
def extract_the_case(src, t):
    res = {}
    for s in src:
        type = info[s]['type']
        if type == t: res[s] = src[s]
    return res


# 获取由题目集得出的该类型题目的水平得分
def get_ability_of_type(src):
    sum_total_score = 0
    sum_total_num = 0
    for s in src:
        sum_total_num += 1
        sum_total_score += s['final_score']
    return sum_total_score / sum_total_num if sum_total_num != 0 else 0


def get_ability_with_defender(src):
    # 调用的是ScoreEvaluator，实际是是为了使用Defender
    sum_total_score = 0
    sum_total_num = 0
    for s in src:
        sum_total_num += 1
        temp = s['final_score']
        if len(s['upload_records']) == 0: continue
        r = ScoreEvaluator.getScore(s['upload_records'][-1]['code_url'], require_time=False)
        temp = r[1] * temp
        sum_total_score += temp
    return sum_total_score / sum_total_num if sum_total_num != 0 else 0


def get_abilities(with_defender=False):
    """
    This method works without defender.py by default, which means it is unable to justify those who cheat.
    While in case with_defender is set True, it works with defender.py.
    :return: a json object carrying the information of students' abilities
    """
    user_ability = {}  # 用户
    for group in range(5):
        for user in data:
            cases = data[user]['cases']
            user_ability[user] = {}
            for t in types:
                user_ability[user][t] = get_ability_with_defender(
                    [c for c in cases if c['case_type'] == t]) if with_defender \
                    else get_ability_of_type([c for c in cases if c['case_type'] == t])
    return user_ability


def get_ability_with_weight(src, curr_type, case_difficulty):
    sum_total_score = 0
    sum_total_num = 0
    for s in src:
        sum_total_num += case_difficulty[s]
        if src[s]: sum_total_score += src[s].score * case_difficulty[src[s].case_id]
    return sum_total_score / sum_total_num


def get_abilities_with_weight():
    user_ability = {}
    for group in range(5):
        student_case_map, case_difficulty = Calculator.init_group(group)
        for student in student_case_map:
            cases = student_case_map[student]
            user_ability[student] = {}
            for t in types:
                user_ability[student][t] = get_ability_with_weight(extract_the_case(cases, t),
                                                                   t, case_difficulty)
    return user_ability


def modify_with_variation():
    """
    用全距（极差）来修正abilities_with_modify.json中的能力值，确保能力值在0～100范围内
    结果保存在final_abilities.json中
    :return: a json object
    """
    file = open('../abilities/abilities_with_modify.json', encoding='utf-8')
    abilities = json.loads(file.read())
    file.close()
    mins = {}
    maxs = {}
    for t in types:
        mins[t] = 10000
        maxs[t] = -1
    res = {}
    for student in abilities:
        for t in types:
            mins[t] = min(abilities[student][t], mins[t])
            maxs[t] = max(abilities[student][t], maxs[t])
    for student in abilities:
        res[student] = {}
        for t in types:
            res[student][t] = 100 * (abilities[student][t] - mins[t]) / (maxs[t] - mins[t])
    return res


if __name__ == '__main__':

    res = modify_with_variation()
    print(res)

    f = open('../abilities/final_abilities.json', 'w')
    f.write(json.dumps(res, ensure_ascii=False))
    f.close()
