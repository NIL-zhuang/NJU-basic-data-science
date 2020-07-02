# 该类用来自动取本地json文件，调用evaluator.py类中的ScoreEvaluator
import json
from evaluator import ScoreEvaluator

if __name__ == '__main__':
    # f = open('C:\\Users\\admin\\Desktop\\数据科学基础\大作业\\test_data.json', encoding='utf-8')
    f = open('/Users/chengrongxin/Downloads/数据科学大作业/sample.json', encoding='utf-8')
    # f = open('/Users/chengrongxin/Downloads/数据科学大作业/test_data.json', encoding='utf-8')
    res = f.read()
    data = json.loads(res)
    for user in data:
        print(user)
        cases = data[user]['cases']
        for case in cases:
            uploads = case['upload_records']
            for upload in uploads:
                url = upload['code_url']
                print(url)
                print(ScoreEvaluator.getScore(url))
