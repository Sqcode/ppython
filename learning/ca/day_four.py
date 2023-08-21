
import time
import os
import shutil
import logging

logging.basicConfig(filename = "out.txt",level=logging.DEBUG,format= "%(asctime)s %(levelname)s -- %(message)s")
logging.debug(111111111)

import subprocess

path = './images/logo.png'
# 打开计算器
# calc_pro = subprocess.Popen('calc.exe')
# 打开画板
# mspaint_pro = subprocess.Popen('mspaint.exe')

# 打开图片
mspaint_pro = subprocess.Popen(['start',  path], shell = True)



def oopen():
    file = 'ipporxy.txt'
    # shutil , 可以处理文件copy move..
    with open(file, mode="a",encoding="utf-8") as f:
        """
        : param mode: a - append, r - read only, w - write
        """
        f.write("111")
        # read = str , readlines = list[str]
        # a = f.read()
        # print(type(a))

def ppath():
    ret = os.path.relpath("C:\\")
    print(ret)

    print(time.asctime())

    print(time.localtime())

class Aargs():
    def show2(name, age, sex="男", *arg, **args):
        print("传入的参数可以循环打印")
        print(name)
        for key in args.items():
            print(key)
    # show2("橡皮擦", 18, "女", like=99)

    # def show(name,**args):
    #     print("传入的参数可以循环打印")
    #     print(name)
    #     for key in args.items():
    #         print(key)
    # show(name="橡皮擦", age=18)

    def show1(name,*arg):
        print("传入的参数可以循环打印")
        print(name)
        for key in arg:
            print(key)
    # show1("橡皮擦", 1,2,3)

def zzip():

    en_names = ["apple", "orange", "pear"]
    cn_names = ["苹果", "橘子", "梨"]

    zipData = zip(en_names, cn_names)

    # print(zipData)  # 打印 zipData
    # print(type(zipData))  # 打印 zipData 数据类型
    # print(list(zipData))  # 输出 zipData 中的数据内容

    s = zip(*zipData)
    for i in s:
        print(i)

    my_dict = {"red": "红色",
            "green": "绿色",
            "blue": "蓝色"}

    my_dict = {"red": "红色",
            "green": "绿色",
            "blue": "蓝色"}

    # 直接对 my_dict 进行遍历
    for item in my_dict:
        print(item)

    # 遍历 my_dict 的 items 方法
    for item in my_dict.items():
        print(item)

    # 遍历 my_dict 的 items 方法，并用 key 与 value 接收
    for key,value in my_dict.items():
        print("键:{}，值:{}".format(key,value))

def sset():
    my_set1 = {"apple", "orange", "pear", "banana", "food"}
    my_set2 = {"apple", "orange", "pear", "grape"}

    dif = my_set1 ^ my_set2
    print(dif)

