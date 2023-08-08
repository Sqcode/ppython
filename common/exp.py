# 异常类 继承Exception

# 跳过异常
class SkipException(Exception):
    def __init__(self,msg):
        print(f'不可控异常，为不影响原程序运行，抛出此异常提示...{msg}')
        self.msg = msg

# 自定义异常
class MyException(Exception):
    def __init__(self, msg, code='500'):
        self.code = code
        self.msg = msg