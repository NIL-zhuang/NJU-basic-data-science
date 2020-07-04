import re


class Defender:
    def __init__(self):
        pass

    @classmethod
    # 检查是否为C/C++提交
    # 原理很简单，用运行cpp程序必不可少的int main或者void main判断即可
    def cpp_defend(cls, code):
        for line in code:
            if 'int main' in line or 'void main' in line:
                return True
        return False

    @classmethod
    def cheat_defend(cls, separator, codes, cases):
        """
        :param separator: 输出结果的分隔符号
        :param codes: 源代码
        :param cases: 用力集，每个元素包含输入和输出
        :return: 作弊次数 / 测试用例数
        """
        cheats = 0
        for case in cases:
            case_input = case['input']
            output = case['output']
            # 逐行代码解释
            for line in codes:
                code = re.sub(r'#.*$', "", line)  # 忽略代码中的注释
                if code == '': continue
                if '+' in code or '-' in code or '*' in code or '/' in code or '=' in code:
                    continue
                if 'for' in code: continue
                # 代码为空，或者四则运算、赋值等情况
                times = 0  # 分段匹配命中次数
                # 暂时需要排除true or false，这个凭借输出不好判断，详见else逻辑块
                if output.lower() != 'true' and output.lower() != 'false':
                    standard = output.replace('\n', '').split(separator)  # 输出不一定是一个值，有可能是一组
                    for out in standard:
                        times += 1 if out != '' and out in code else 0
                else:
                    standard = case_input.replace('\n', '').split(separator)
                    for info in standard:
                        times += 1 if info != '' and info in code else 0

                if times == len(standard):
                    print('发现面向用例代码——' + code, end=' ')
                    cheats += 1  # 匹配成功
                    print('当前发现作弊次数' + str(cheats))
        return min(cheats / len(cases), 1)
