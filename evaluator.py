import json
import os
import shutil
import signal
import subprocess
import time
import zipfile
from urllib import request

from defender import Defender


def deleteDir(dir):
    windowsDeleteDir(dir)


def windowsDeleteDir(dir):
    shutil.rmtree(dir)
    # os.system('rd /r/f/q {}'.format(dir))


def macDeleteDir(dir):
    os.system('rm -rf {}'.format(dir))


def deleteFile(file):
    windowsDeleteFile(file)


def windowsDeleteFile(file):
    os.remove(file)
    # os.system('del /s/f/q {}'.format(dir))


def macDeleteFile(file):
    os.system('rm {}'.format(dir))


def after_timeout():
    print('代码超时!')
    work_dir = os.path.abspath('.')
    deleteFile(work_dir + '/test.txt')
    deleteDir(work_dir + '/resource')
    deleteDir(work_dir + '/tmp')
    deleteFile(work_dir + '/code.zip')


def time_limit(set_time, callback):
    def wraps(func):
        def handler(signum, frame):
            raise RuntimeError()

        def deco(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(set_time)  # set_time单位为s
                res = func(*args, **kwargs)
                signal.alarm(0)
                return res
            except RuntimeError as e:
                callback()

        return deco

    return wraps


class ScoreEvaluator:
    def __init__(self):
        pass

    work_dir = os.path.abspath('.')
    cases = {}
    lines = 0
    all_the_code = []

    @classmethod
    # src_url 代码包url
    def read_from_url(cls, src_url):
        request.urlretrieve(src_url, 'code.zip')
        src = zipfile.ZipFile('code.zip')
        src.extractall('tmp')
        tmp_dir = 'tmp/' + src.namelist()[0]
        files = zipfile.ZipFile(tmp_dir)  # 解压完成
        files.extractall(cls.work_dir + '/resource')
        # 这边的代码是用来处理后事的
        # 这里我会报错，移到后面计算完一起删除 --- by cyz
        # os.system('rm -rf {}'.format(cls.work_dir + '/tmp'))  # 删除非空空目录，这个命令很危险路径不能错
        # deleteDir(cls.work_dir + '/tmp')
        # os.system('rm {}'.format(cls.work_dir + '/code.zip'))  # 删除zip文件
        # deleteFile(cls.work_dir + '/code.zip')
        # 这里是用的macOS终端命令 不一定适用于Windows cmd，如果报错改成相应的cmd命令即可

        return cls.work_dir + '/resource/main.py'  # resource文件夹存放爬取来的、已解压的文件资源

    @classmethod
    # 提取文件中的信息
    def load(cls, file):
        test_cases = cls.work_dir + '/resource/.mooctest/testCases.json'
        cls.all_the_code = open(file, encoding='UTF-8').read().split('\n')
        cls.lines = len(cls.all_the_code)
        with open(test_cases, 'r') as f:
            cls.cases = json.load(f)

    @classmethod
    def afterTheEvaluate(cls):
        # deleteFile(cls.work_dir + '/test.txt')
        deleteDir(cls.work_dir + '/resource')
        deleteDir(cls.work_dir + '/tmp')
        deleteFile(cls.work_dir + '/code.zip')

    # 返回值是一个元组
    @classmethod
    # 循环次数recycle，这是为了减少os.system运行python导致的时间误差，默认为5
    # 测试用例输出的分割符，默认为空格
    def getScore(cls, code_url, recycle=5, separator=' '):
        file = cls.read_from_url(code_url)
        ScoreEvaluator.load(file)  # 导入文件，提取信息

        if Defender.cpp_defend(cls.all_the_code):
            # os.system('rm -rf {}'.format(cls.work_dir + '/resource'))
            deleteDir(cls.work_dir + '/resource')
            return False, 1, 0, cls.lines  # cpp提交

        # 作弊代码
        cheats = Defender.cheat_defend(separator, cls.all_the_code, cls.cases)
        if cheats > 0:
            # os.system('rm -rf {}'.format(cls.work_dir + '/resource'))
            deleteDir(cls.work_dir + '/resource')
            temp = 1 - cheats  # 防止返回负数
            if temp < 0:
                temp = 0
            return True, temp, 0, cls.lines  # 面向用例返回面向用例占比，0到1之间

        runtime = 0  # 运行时间

        for i in range(recycle):
            for case in cls.cases:
                inputs = case["input"] + '\n'

                # test = open(cls.work_dir + '/test.txt', 'w')
                # test.write(inputs + '\n')
                # test.close()
                timestamp_start = time.time() * 1000
                # mac用python3
                process = subprocess.Popen(['python', file], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                           close_fds=True)
                try:
                    process.communicate(inputs.encode(encoding='UTF-8'), 10)
                except subprocess.TimeoutExpired:
                    print('用例运行超时！')
                    process.kill()
                    cls.afterTheEvaluate()
                    return True, 1, 'TIMEOUT', cls.lines
                if process.returncode != 0:
                    print('代码运行错误')
                    process.kill()
                    cls.afterTheEvaluate()
                    return True, 1, 'ERROR', cls.lines
                timestamp_end = time.time() * 1000
                runtime += timestamp_end - timestamp_start
        runtime /= recycle  # 通过取平均值尽量减少子进程运行带来的时间波动误差，如果对次数不满意可以自己传入recycle参数
        print('运行时间为{}ms'.format(runtime))
        # 确保配置了python的环境变量
        # windows环境下将上面的"python3"修改成"python"
        cls.afterTheEvaluate()
        return True, 1, runtime, cls.lines


# 程序入口
if __name__ == '__main__':
    print('开始分析···')
    # print('请输入提交代码url：', end='')
    # url = input()
    # url = 'http://mooctest-dev.oss-cn-shanghai.aliyuncs.com/data/answers/4238/48117/%E6%A2%A6%E4%B8%AD%E7%9A%84%E7%BB%9F%E8%AE%A1_1582535119790.zip'
    url = 'http://mooctest-dev.oss-cn-shanghai.aliyuncs.com/data/answers/4238/3544/%E5%8D%95%E8%AF%8D%E5%88%86%E7%B1' \
         '%BB_1582023289869.zip '
    print(ScoreEvaluator.getScore(url, 1))
