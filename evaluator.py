import json
import os
import shutil
import time
import zipfile
from urllib import request

from defender import Defender


def deleteDir(dir):
    windowsDeleteDir(dir)


def windowsDeleteDir(dir):
    shutil.rmtree(dir)


def macDeleteDir(dir):
    os.system('rm -rf {}'.format(dir))


def deleteFile(file):
    windowsDeleteFile(file)


def windowsDeleteFile(file):
    os.remove(file)


def macDeleteFile(file):
    os.system('rm {}'.format(dir))


class ScoreEvaluator:
    def __init__(self):
        pass

    work_dir = os.path.abspath('.')
    cases = {}
    lines = 0
    all_the_code = []

    @classmethod
    def read_from_url(cls, src_url):
        """
        :param src_url: 代码包的src url
        :return: 解压后 main.py 文件的路径
        """
        def retrieve():
            request.urlretrieve(src_url, 'code.zip')  # 下载文件
            src = zipfile.ZipFile('code.zip')
            src.extractall('tmp')
            tmp_dir = 'tmp/' + src.namelist()[0]
            files = zipfile.ZipFile(tmp_dir)  # 解压完成
            files.extractall(cls.work_dir + '/resource')
        retrieve()  # 函数调用结束后释放系统空间，就不用管文件占用什么的了
        shutil.rmtree(cls.work_dir + '\\tmp')
        os.remove(cls.work_dir + '\\code.zip')
        # os.system('rm -rf {}'.format(cls.work_dir + '/tmp'))  # 删除非空空目录，这个命令很危险路径不能错
        # os.system('rm {}'.format(cls.work_dir + '/code.zip'))  # 删除zip文件
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

    # 返回值是一个元组
    @classmethod
    # 循环次数recycle，这是为了减少os.system运行python导致的时间误差，默认为5
    # 测试用例输出的分割符，默认为空格
    def get_score(cls, code_url, recycle=5, separator=' '):
        file = cls.read_from_url(code_url)
        ScoreEvaluator.load(file)  # 导入文件，提取信息

        # cpp提交，需要修改
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
                test = open(cls.work_dir + '/test.txt', 'w')
                test.write(inputs)
                test.close()
                timestamp_start = time.time() * 1000
                # os.system('python {}<{}>>{}'.format(file, cls.work_dir + '/test.txt',
                #                                     cls.work_dir + '/test.txt'))
                # res = os.system('python3 {}<{}>>{}'.format(file, cls.work_dir + '/test.txt', cls.work_dir + '/test.txt'))
                res = os.system('python {}<{}>>{}'.format(file, cls.work_dir + '/test.txt', cls.work_dir + '/test.txt'))
                # 返回值为0说明执行成功，否则说明提交的代码有问题
                # 与真实的运行时间有略微差异，因为是调用os模块从命令行调用的
                if res:
                    print('提交代码有错误，无法正常运行')
                    return True, 0, 0, cls.lines
                timestamp_end = time.time() * 1000
                runtime += timestamp_end - timestamp_start
        runtime /= recycle  # 通过取平均值尽量减少os.system带来的时间波动误差，如果对次数不满意可以自己传入recycle参数
        # 确保配置了python的环境变量
        # windows环境下将上面的"python3"修改成"python"

        # os.system('rm {}'.format(cls.work_dir + '/test.txt'))
        deleteFile(cls.work_dir + '/test.txt')
        # os.system('rm -rf {}'.format(cls.work_dir + '/resource'))  # 完成分析后，删除下载下来的资源
        deleteDir(cls.work_dir + '/resource')

        deleteDir(cls.work_dir + '/tmp')
        deleteFile(cls.work_dir + '/code.zip')
        return True, 1, runtime, cls.lines  # 暂时不知道怎么评分 还是先就返回个运行时间吧


# 程序入口
if __name__ == '__main__':
    print('开始分析···')
    # print('请输入提交代码url：', end='')
    # url = input()
    url = 'http://mooctest-dev.oss-cn-shanghai.aliyuncs.com/data/answers/4239/48117/%E5%BA%8F%E5%88%97%E5%85%83%E7%B4%A0_1584415591348.zip'
    print(ScoreEvaluator.get_score(url))
