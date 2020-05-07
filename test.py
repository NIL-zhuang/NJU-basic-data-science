import json
from evaluator import ScoreEvaluator

f = open('C:\\Users\\admin\\Desktop\\数据科学基础\大作业\\test_data.json', encoding='utf-8')
res = f.read()
data = json.loads(res)
arr = []
for student in data:
    # print(student)
    # print('user_id', data[student]['user_id'])
    cases = data[student]['cases']
    count = 0
    for case in cases:
        if case['final_score'] != 0:
            count += 1
    # print('通过题数', count)
    arr.append((data[student]['user_id'], count))
arr = sorted(arr, key=lambda i: i[1])
for i in arr:
    print(i)
ScoreEvaluator.getscore()
