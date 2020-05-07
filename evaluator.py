import json
import os
import time
import zipfile
from urllib import request


class ScoreEvaluator:
    workdir = ''
    cases = {}

    @classmethod
    def read_from_url(cls, url):
        cls.workdir = os.path.abspath('.')
        request.urlretrieve(url, 'code.zip')
        src = zipfile.ZipFile('code.zip')
        src.extractall('tmp')
        dir = 'tmp/' + src.namelist()[0]
        files = zipfile.ZipFile(dir)  # 解压完成

        iscpp = False
        for f in files.namelist():
            if f == 'main.cpp':
                iscpp = True
                break
        if iscpp: return None  # 判断是否为cpp提交

        files.extractall(cls.workdir + '/resource')

        # 这边的代码是用来处理后事的
        # os.system('rm -rf {}'.format(cls.workdir + '/tmp'))  # 删除非空空目录，这个命令很危险路径千万别填错！！！
        # os.system('rm {}'.format(cls.workdir + '/code.zip'))  # 删除zip文件
        # 这里是用的macOS终端命令 不一定适用于Windows cmd，如果报错改成相应的cmd命令即可

        return cls.workdir + '/resource/main.py'  # resource文件夹存放爬取来的、已解压的文件资源

    @classmethod
    # TODO 用来判断是否面向用例
    def ischeated(cls, file):
        test_cases = cls.workdir + '/resource/.mooctest/testCases.json'
        all_the_code = open(file).read()
        # print(all_the_code)
        with open(test_cases, 'r') as f:
            cls.cases = json.load(f)
        for case in cls.cases:
            output = case["output"]
            output = output.replace('\n', '')
            if output in all_the_code: return True  # 这边的代码逻辑有待商榷 到底是只要匹配到一个就算作弊 还是匹配到所有才算作弊
        return False

    @classmethod
    def getscore(cls, url):
        file = cls.read_from_url(url)
        if not file: return -1  # cpp提交
        if cls.ischeated(file): return 0  # 面向用例

        runtime = 0
        for case in cls.cases:
            input = case["input"] + '\n'
            test = open(cls.workdir + '/test.txt', 'w')
            test.write(input)
            test.close()
            timestamp_start = time.time() * 1000
            os.system('python3 {}<{}>>{}'.format(file, cls.workdir + '/test.txt',
                                                 cls.workdir + '/test.txt'))  # 与真实的运行时间有略微差异，因为是调用os模块从命令行调用的
            timestamp_end = time.time() * 1000
            runtime += timestamp_end - timestamp_start

        # 确保配置了python的环境变量
        # window环境下将上面的"python3"修改成"python"

        os.system('rm {}'.format(cls.workdir + '/test.txt'))
        os.system('rm -rf {}'.format(cls.workdir + '/resource'))  # 完成分析后，删除下载下来的资源
        return runtime  # 暂时不知道怎么评分 还是先就返回个运行时间吧


if __name__ == '__main__':
    print('Analyzing···')
    url = "http://mooctest-dev.oss-cn-shanghai.aliyuncs.com/data/answers/4250/59018/%E7%9F%B3%E5%AD%90%E6%B8%B8%E6%88%8F_1583812015501.zip"
    print(ScoreEvaluator.getscore(url))
