# 该类用来自动取本地json文件，调用evaluator.py类中的ScoreEvaluator
import json
import sys
from evaluator import ScoreEvaluator

if __name__ == '__main__':
    out = open('res.txt', 'w')
    sys.stdout = out
    f = open('test_data.json', encoding='utf-8')
    res = f.read()
    data = json.loads(res)
    for user in data:
        print('student', user)
        cases = data[user]['cases']
        for case in cases:
            uploads = case['upload_records']
            for upload in uploads:
                url = upload['code_url']
                print('code_url:', url)
                result = ScoreEvaluator.getScore(url)
                if result:
                    print('评估结果————', result)
    f.close()
    out.close()
