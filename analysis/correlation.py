from scipy import stats
import calculate.Calculator as Calculator
import json


def get_submits(case_map):
    res = 0
    for key in case_map.keys():
        if case_map[key] is not None:
            res += 1
    return res


def get_ability_submits_corr():
    array_ability = []
    array_submits = []
    for group in range(5):
        ability = Calculator.get_student_ability(group)
        student_case_map = Calculator.get_student_case_map(group)
        ability_sort = sorted(ability.items(), key=lambda x: x[1])
        for item in ability_sort:
            array_ability.append(item[1])
            array_submits.append(get_submits(student_case_map[item[0]]))
    correlation, p_value = stats.pearsonr(array_ability, array_submits)
    print(correlation, p_value)
    return correlation, p_value


def get_difficulty_acp_corr():
    difficulty, ac_portion = [], []
    f = open('../calculate/question_info.json')
    question_info = json.loads(f.read())
    f.close()
    f = open('../calculate/case_difficulty.json')
    temp = json.loads(f.read())
    f.close()
    difficulty_items = sorted(temp.items(), key=lambda x: x[1])
    for item in difficulty_items:
        difficulty.append(item[1])
        info = question_info[item[0]]
        ac_portion.append(info['accepts']/info['submits'])
    correlation, p_value = stats.pearsonr(difficulty, ac_portion)
    print(correlation, p_value)
    return correlation, p_value


if __name__ == '__main__':
    get_ability_submits_corr()
    get_difficulty_acp_corr()
