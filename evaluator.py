from urllib import request
import zipfile
import os
import time
import json


class ScoreEvaluator:
    workdir = os.path.abspath('.')
    cases = {}

    @classmethod
    def read_from_url(cls, url):
        request.urlretrieve(url, 'code.zip')
        src = zipfile.ZipFile('code.zip')
        src.extractall('tmp')
        dir = 'tmp/'+src.namelist()[0]
        files = zipfile.ZipFile(dir)  # 解压完成

        iscpp = False
        for f in files.namelist():
            if f == 'main.cpp':
                iscpp = True
                break
        if iscpp: return None  # 判断是否为cpp提交

        files.extractall(cls.workdir+'/resource')

        # 这边的代码是用来处理后事的
        os.system('rm -rf {}'.format(cls.workdir + '/tmp'))  # 删除非空空目录，这个命令很危险路径千万别填错！！！
        os.system('rm {}'.format(cls.workdir + '/code.zip'))  # 删除zip文件
        # 这里是用的macOS终端命令 不一定适用于Windows cmd，如果报错改成相应的cmd命令即可

        return cls.workdir+'/resource/main.py'  # resource文件夹存放爬取来的、已解压的文件资源

    @classmethod
    # TODO 逻辑仍需要修改！还需要匹配input！
    def is_cheated(cls, file, separator):
        test_cases = cls.workdir + '/resource/.mooctest/testCases.json'
        all_the_code = open(file).read().split('\n')
        with open (test_cases, 'r') as f:
            cls.cases = json.load(f)
        for case in cls.cases:
            output = case["output"]
            output = output.replace('\n', '').split(separator)
            for code in all_the_code:
                code = code.replace('#.*', '')
                if code != '' and 'return' not in code and '=' not in code:  # 本意是不想把变量声明算进去，但这样似乎又带来了新的问题，仍需要修改
                    times = 0
                    for out in output:
                        if out in code: times += 1
                    if times == len(output): return True  # 匹配成功
            # 这边的代码逻辑有待商榷 到底是只要匹配到一个用例就算作弊 还是匹配到所有才算作弊
        return False

    @classmethod
    def getscore(cls, code_url, recycle=5, separator=' '):
        file = cls.read_from_url(code_url)
        if not file: return -1  # cpp提交
        if cls.is_cheated(file, separator): return 0  # 面向用例

        runtime = 0
        for i in range(recycle):
            for case in cls.cases:
                input = case["input"] + '\n'
                test = open(cls.workdir+'/test.txt', 'w')
                test.write(input)
                test.close()
                timestamp_start = time.time() * 1000
                os.system('python3 {}<{}>>{}'.format(file, cls.workdir+'/test.txt', cls.workdir+'/test.txt'))  # 与真实的运行时间有略微差异，因为是调用os模块从命令行调用的
                timestamp_end = time.time() * 1000
                runtime += timestamp_end - timestamp_start
        runtime /= recycle  # 通过取平均值尽量减少os.system带来的时间波动误差，如果对次数不满意可以自己传入recycle参数
        # 确保配置了python的环境变量
        # window环境下将上面的"python3"修改成"python"

        os.system('rm {}'.format(cls.workdir+'/test.txt'))
        os.system('rm -rf {}'.format(cls.workdir + '/resource'))  # 完成分析后，删除下载下来的资源
        return runtime  # 暂时不知道怎么评分 还是先就返回个运行时间吧


if __name__ == '__main__':
    print('Analyzing···')
    url = input()
    print(ScoreEvaluator.getscore(url))
