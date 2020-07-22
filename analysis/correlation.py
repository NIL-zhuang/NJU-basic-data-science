from scipy import stats
import calculate.Calculator as Calculator


def get_submits(case_map):
    res = 0
    for key in case_map.keys():
        if case_map[key] is not None:
            res += 1
    return res


res = []

for group in range(5):
    ability = Calculator.get_student_ability(group)
    student_case_map = Calculator.get_student_case_map(group)
    ability_sort = sorted(ability.items(), key=lambda x: x[1])
    array_ability = []
    array_submits = []
    for item in ability_sort:
        array_ability.append(item[1])
        array_submits.append(get_submits(student_case_map[item[0]]))
    correlation, p_value = stats.pearsonr(array_ability, array_submits)
    print(correlation, p_value)
    res.append((correlation, p_value))


print(res)
