# 分析每个学生对不同类别题目的完成情况
# 尝试使用defender.py修正分数
import json
from defender import Defender

f = open('test_data.json', encoding='utf-8')
d = f.read()
data = json.loads(d)

res = open('abilities.json', 'w')  # 输出文件
types = ['字符串', '线性表', '数组', '查找算法', '树结构', '图结构', '数字操作', '排序算法']  # 题目种类


# 提取指定用户指定类型的题目
def extract_the_case(src, t):
    result = []
    for s in src:
        if s['case_type'] == t: result.append(s)
    return result


# 获取由题目集得出的该类型题目的水平得分
def get_ability_of_type(src):
    return 0


def getAbilities():
    """
    This method works without defender.py, which means, it is unable to justify those who cheat.
    :return: a json object carry the information of students' abilities
    """
    user_ability = {}  # 用户
    for user in data:
        cases = data['cases']
        user_ability[user] = {}
        for t in types:
            user_ability[user][t] = get_ability_of_type(extract_the_case(cases, t))
    return user_ability


# 尝试使用修正的defender来获取得分
def getAbilitiesWithDefender():
    """
    This one work with defender.py.
    :return: also a json object
    """
    return
