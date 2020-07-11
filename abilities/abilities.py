# 分析每个学生对不同类别题目的完成情况
# 尝试使用defender.py修正分数
import json

from evaluator import ScoreEvaluator

f = open('../test_data.json', encoding='UTF-8')
d = f.read()
data = json.loads(d)

types = ['字符串', '线性表', '数组', '查找算法', '树结构', '图结构', '数字操作', '排序算法']  # 题目种类


# 提取指定用户指定类型的题目
def extract_the_case(src, t):
    result = []
    for s in src:
        if s['case_type'] == t: result.append(s)
    return result


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


def getAbilities(with_defender=False):
    """
    This method works without defender.py by default, which means it is unable to justify those who cheat.
    While in case with_defender is set True, it works with defender.py.
    :return: a json object carrying the information of students' abilities
    """
    user_ability = {}  # 用户
    for user in data:
        cases = data[user]['cases']
        user_ability[user] = {}
        for t in types:
            user_ability[user][t] = get_ability_with_defender(extract_the_case(cases, t)) if with_defender \
                else get_ability_of_type(extract_the_case(cases, t))
    return user_ability


if __name__ == '__main__':
    with_defend = True
    abilities = getAbilities(with_defend)
    res_without_defend = open('abilities.json', 'w', encoding='UTF-8')  # 输出文件
    res_with_defend = open('abilities_with_defend.json', 'w', encoding='UTF-8')
    res_with_defend.write(json.dumps(abilities, ensure_ascii=False)) if with_defend \
        else res_without_defend.write(json.dumps(abilities, ensure_ascii=False))
    res_without_defend.close()
    res_with_defend.close()
