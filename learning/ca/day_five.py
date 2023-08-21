
import redis
import timeit
from collections import namedtuple
# import time
from functools import reduce

from datetime import date, datetime 
import time
import calendar
import hashlib
import random
import re
import os, sys

class My_Class(object):

    # 在类定义中定义变量
    cls_var = "类变量"

    def __init__(self):
        print("构造函数")
        self.var = "实例变量"
        # self.x = "构造函数中的属于实例变量"

    # 类方法，第一个参数必须默认传类，一般习惯用 cls。
    @classmethod
    def class_method(cls):
        print("class_method 是类方法，类名直接调用")
        # 类方法不可以调用类内部的对象变量（实例变量）
        # print(cls.x)
    # 普通的对象实例函数
    def instance_method(self):
        # 可以访问类变量
        print(self.cls_var)
        # 可以访问实例变量
        print(self.var)
        print("实例化方法")

    @staticmethod
    def static_method(): #self
        print(My_Class.cls_var)
        # 无法访问到实例变量
        # print(My_Class.var)
        # print(self.var)
        print("静态方法")

# 类方法可以通过类名直接调用，也可以通过对象来调用
# 即使通过实例调用类方法，Python 自动传递的也是类，而不是实例
# My_Class.class_method()
# my_class_dom = My_Class()
# # 通过类的对象调用
# my_class_dom.class_method()

# my_class = My_Class()
#my_class.instance_method()
# 通过对象访问
# my_class.static_method()
# 类名直接访问
#My_Class.static_method()


def os_sys():
    print(sys.platform)
    print(os.name)
    #print(os.environ)

    # os.chdir(path) #修改当前程序操作的路径；
    # print(os.getcwd())#返回程序运行的路径；
    # print(os.getlogin())#获取当前登录用户名称；
    # print(os.cpu_count())#获得当前系统的 CPU 数量；
    # os.urandom(n)##返回一个有 n 个 byte 长的一个随机字符串，用于加密运算。

def rre():
    my_str = '梦想1good1good'
    pattern = r'梦' # 匹配到数据
    pattern = r'good' # 匹配不到数据

    # 正则对象
    regex = re.compile(pattern = r'good')
    ret = regex.sub("nice", my_str)
    print(ret)

    ret = re.match(pattern, my_str)
    if ret:
        print(ret.group())

    pattern = r'good'
    ret = re.findall(pattern, my_str)
    print(ret)

    pattern = r'1'
    ret = re.split(pattern, my_str, 1)
    print(ret)

    pattern = r'(1)'
    ret = re.split(pattern, my_str, 1)
    print(ret)

    pattern = r'good'
    # ret = re.split(pattern, my_str,maxsplit=1)
    ret =re.finditer(pattern, my_str)
    print(ret)

    pattern = r'good'
    ret = re.sub(pattern, "nice", my_str)
    print(ret)

def rrandom():
    my_list = [1,2,3,4,5,6,7,8,9]
    random.shuffle(my_list)
    print(my_list)
    ls = random.sample(my_list, 4)
    print(ls)

    for i in range(3):
        print("*"*20)
        print(random.randrange(10))
        print(random.randrange(5,10))
        print(random.randrange(5,100,5))


    random.seed(11)
    x = random.random()
    print(x)

    random.seed(10)
    y = random.random()
    print(y)

def hhash():
    # MD5算法
    print(hash('123'))
    # print(dir(hashlib)) 
    # ['__all__', '__block_openssl_constructor', '__builtin_constructor_cache', '__builtins__', '__cached__', '__doc__', '__file__', '__get_builtin_constructor', '__loader__', '__name__', '__package__', '__spec__', '_hashlib', 'algorithms_available', 'algorithms_guaranteed', 'blake2b', 'blake2s', 'md5', 'new', 'pbkdf2_hmac', 'scrypt', 'sha1', 'sha224', 'sha256', 'sha384', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512', 'sha512', 'shake_128', 'shake_256']
    md5 = hashlib.sha1()
    data = "hello world"
    md5.update(data.encode('utf-8'))
    # 计算 hash 值,拿到加密字符串
    print(md5.hexdigest())

def v():
    # 全局变量
    x = 0
    def demo():
        # 此时的 x 是局部变量
        x = 123
        print("函数内是局部变量 x = ", x)

    demo()
    print("函数外是全局变量 x= ", x)

    # len = len([])
    # def a():
    #     len = 1
    #     def b():
    #         len = 2
    #         print(len)
    #     b()
    # a()

def ddate():
    c = calendar.TextCalendar(calendar.SUNDAY)
    c.prmonth(2021, 9)

    dt = datetime.now()
    # 使用 datetime 的内置函数 timestamp()
    stamp = datetime.timestamp(dt)
    print(stamp)

    # t = time(hour=20, minute=20, second=40)
    # print(t, t.isoformat())


    # print('date.min:', date.min)
    # print('date.max:', date.max)
    # print('date.resolution:', date.resolution)
    # print('date.today():', date.today())
    # print('date.fromtimestamp():', date.fromtimestamp(time.time()))

    # x = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # print(x)
    # # 方向操作，字符串格式化成 time.struct_time
    # struct_time = time.strptime(x, "%Y-%m-%d %H:%M:%S")
    # print(struct_time)

# 装饰器
def run_time(func):
    # 这里的 wrapper 函数名可以为任意名称
    def wrapper(start):
        s_time = time.perf_counter()
        res = func(start)
        e_time = time.perf_counter()
        print(f"func --- {func.__name__}, runtime --- {e_time-s_time}")
        return res
    return wrapper

def eenumerate():
    # 输出 带下标的元组 数据
    weekdays = ['Mon', 'Tus', 'Wen', 'Thir']
    print(enumerate(weekdays))
    print(list(enumerate(weekdays)))

def rreduce():
    my_list = [1, 2, 3]

    def add(x, y):
        print(x,y)
        return x+y

    my_new_list = reduce(add, my_list, 4)
    print(my_list)
    print(my_new_list)

def llambda():
        
    my_list = [(1, 2), (3, 1), (4, 0), (11, 4)]
    my_list.sort(key=lambda x: x[1], reverse=True)
    print(my_list)


    sorted = lambda *args:None
    x = sorted([3,2,1])
    print(x)


    my_list = [lambda a: a**1, lambda b: b**2]
    fun = my_list[1]
    print(fun(2))

# += 写法
@run_time
def m0(start):
    s = 0
    for n in range(start, 100):
        s += n
    return (s)

# join 写法
def m1():
    l = []
    for n in range(0, 100000):
        l.append(str(n))
    s = ' '.join(l)

# pythonic 写法
def m2():
    s = ' '.join(map(str, range(0, 100000)))

def sstr():
    start_time = time.perf_counter()
    m2()
    end_time = time.perf_counter()
    print("代码运行时间为：", end_time-start_time)

def tperf_counter():
    id = [x for x in range(1, 10)]
    # 体重数据为了计算，也只能从 1 到 10000 了
    weight = [x for x in range(1, 10)]
    students = list(zip(id, weight))
    print(id, students)

    start_time = time.perf_counter()
    # 调用列表计算函数
    find_unique_weight(students)
    end_time = time.perf_counter()
    print("运算时间为：{}".format(end_time - start_time))

def find_unique_weight(students):
    # 声明一个统计集合
    unique_set = set()
    # 循环所有学生数据
    for id, weight in students:
        # 集合会自动过滤重复数据
        unique_set.add(weight)
    # 计算集合长度
    ret = len(unique_set)
    return ret

def ddict():
    my_dict = {}
    my_dict["A"] = "1"
    my_dict["B"] = "3"
    my_dict["C"] = "2"
    my_dict["D"] = "3"
    # my_dict["F"] ,不存在报错 keyError， 使用get,设置默认值
    print(my_dict.get("F", 'default'))

    for i in my_dict.items():
        print(i)
    sorted_dict = sorted(my_dict.items(), key=lambda x:x[1])
    print(sorted_dict)

def nnamedtuple():

    Point = namedtuple('Point', ['x', 'y'])
    p = Point(10, 20)
    p1 = Point(110, 120)
    print(p, p1)

def timit():
    # 测试效率？
    a = timeit.timeit('a=list()', number=10000000 )
    b = timeit.timeit('a=[]', number=10000000 )
    c = timeit.timeit('a=("a","b","c")', number=10000)
    d = timeit.timeit('b=["a","b","c"]', number=10000)
    print(a,b,c,d)

def tuple_append():
    # 
    my_old_tuple = (1, 2, "a", "b")
    my_new_tuple = ("c", "d", 1)

    my_tuple = my_old_tuple + my_new_tuple
    print(my_tuple, my_tuple[1:3], my_tuple[1:-2], my_tuple[-3:-1])

    my_list = list(my_tuple)
    print(my_list, my_list[0:3], my_list[-3:-1])

#r = redis.Redis(host='localhost', port= 6379)

# pool = redis.ConnectionPool(host='localhost', port=6379)
# r = redis.Redis(connection_pool=pool)
# print(r.get('note_1'))

if __name__ == '__main__':
    a = m0(1)
    print(a)