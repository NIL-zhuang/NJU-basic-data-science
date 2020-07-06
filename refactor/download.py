import json
import os
import shutil
from urllib import request
from zipfile import ZipFile

"""
使用download(url)方法，获取该url对应的main.py的代码，测试用例列表
"""

work_dir = os.path.abspath('')


def read_from_url(src_url: str) -> str:
    """
            爬取url对应的代码文件，并删除中间文件
            将解压后的文件资源存在resource文件夹
            :param src_url: 源代码url
            :return: main.py文件的目录
            """

    def download():
        request.urlretrieve(src_url, 'code.zip')
        src = ZipFile('code.zip')
        src.extractall('tmp')
        tmp_dir = 'tmp/' + src.namelist()[0]
        files = ZipFile(tmp_dir)  # 解压完成
        files.extractall(work_dir + '/resource')

    download()
    shutil.rmtree(work_dir + '/tmp')
    os.remove(work_dir + '/code.zip')
    return work_dir + '/resource/main.py'


def read_code(file: str) -> list:
    """
    从文件目录中读取代码并分段，返回每行的代码
    :param file: 文件url
    :return: 分段好的代码
    """
    return open(file, encoding='UTF-8').read().split('\n')


def load(file: str):
    """
    :param file: 传入的代码路径
    :return: 代码内容，用例json
    """
    test_cases = work_dir + '/resource/.mooctest/testCases.json'
    all_the_code = read_code(file)
    with open(test_cases, 'r') as f:
        cases = json.load(f)
    # finish()
    return all_the_code, cases


def finish():
    """
    删除下载后的resource文件夹及内容
    """
    shutil.rmtree(work_dir + '/resource')


def download(url: str):
    """
    :param url: 代码url
    :return: 分段后的代码， 用例列表
    """
    tmp = read_from_url(url)
    return load(tmp)
