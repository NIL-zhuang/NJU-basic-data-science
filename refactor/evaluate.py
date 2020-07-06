from refactor import download
from defender import Defender
import time
import subprocess
import signal


def finish_eval(*args):
    download.finish()
    return args


class ScoreEvaluator:
    def __init__(self, url: str):
        self.codes, self.cases = download.download(url)
        self.lines = len(self.codes)

    def get_score(self, recycle=5, separator=' '):
        if Defender.cpp_defend(self.codes):
            # 防御C/C++代码
            finish_eval(False, 1, 0, self.lines)
        cheats = Defender.cheat_defend(separator, self.codes, self.cases)
        if cheats > 0:
            # 遇到面向用例的，就返回面向用例的比例 0~1之间
            finish_eval(True, 0 if cheats > 1 else 1 - cheats, self.lines)
        runtime = 0
        for _ in range(recycle):
            for case in self.cases:
                inputs = case['input'] + '\n'
                runtime += self.run_code(inputs)
        runtime /= recycle
        return finish_eval(True, 1, runtime, self.lines)

    def run_code(self, test_case):
        """
        :param test_case: 测试用例
        :return: 代码运行测试用例需要的时间
        """
        file = './resource/main.py'
        start_time = time.time()
        process = subprocess.Popen(['python', file], stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, close_fds=True)
        try:
            process.communicate(test_case.encode(), timeout=10)
        except subprocess.TimeoutExpired:
            print('用例运行超时！')
            process.kill()
            finish_eval(True, 1, 'TIMEOUT', self.lines)
        if process.returncode != 0:
            print('代码运行错误')
            process.kill()
            finish_eval(True, 1, 'ERROR', self.lines)
        end_time = time.time()
        return (end_time - start_time) * 1000
