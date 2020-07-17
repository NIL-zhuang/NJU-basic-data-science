import json

f = open('../test_data.json')
data = json.loads(f.read())
f.close()
res = {}
for student in data:
    for c in data[student]['cases']:
        id = c['case_id']
        if id not in res: res[id] = {'type': '', 'submits': 0, 'accepts': 0}
        res[id]['type'] = c['case_type']
        res[id]['submits'] += len(c['upload_records'])
        if c['final_score'] == 100.0:
            accepts = 0
            for upload in c['upload_records']:
                if upload['score'] == 100.0: accepts += 1
            res[id]['accepts'] += accepts
out = open('question_info.json', 'w')
out.write(json.dumps(res, ensure_ascii=False))
out.close()
