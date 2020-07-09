import pycode_similar
import matplotlib.pyplot as plt

plt.fill("time", "signal", data={"time": [0, 1, 2, 3, 4], "signal": [-1, -3, 2, -3, -1]})
plt.title('students')
plt.xlabel('time')
plt.ylabel('signal')
plt.show()
# learn to use matplotlib


class SimilarDetector:
    def __init__(self, codes):
        self.code_list = codes

    def detect(self):
        pycode_similar.detect(self.code_list, diff_method=pycode_similar.UnifiedDiff)


res = pycode_similar.detect(['''
def p():
    print(123)''', '''
def f():
    print(123)'''], diff_method=pycode_similar.TreeDiff)
funcInfos = res[0][1]
sum_plagiarism_count = 0
sum_total_count = 0
for func_info in funcInfos:
    sum_plagiarism_count += func_info.plagiarism_count
    sum_total_count += func_info.total_count
print(sum_plagiarism_count/sum_total_count)
