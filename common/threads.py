import random
import threading, time
from queue import Queue
import util
class ThreadCrawl(threading.Thread):
    """
    :param :thread_name 线程名称
    :param :func 线程要执行的函数
    """
    def __init__(self, thread_name, func):
        # threading.Thread.__init__(self)
        # 调用父类初始化方法
        super(ThreadCrawl, self).__init__()
        self.threadName = thread_name
        self.func = func
        print(thread_name, func)
    def run(self):
        # runrun(self.threadName)
        print(self.threadName + '************启动************')
        self.func()

s = 0
# 爬虫请求与解析入口
def runrun(thread_name):
    global s
    for x in range(3):
        s += x
        print('线程 - %s,s=%d '%(thread_name,s))
    # time.sleep(1)

def add():
    global s
    for x in range(3):
        s += x
        print('add,s=%d '%s)
            
def subs():
    global s
    for x in range(3):
        s -= x
        print('subs,s=%d '%s)

def func_a(func, *args, **kwargs):
  print(func(*args, **kwargs))
 
def func_b(*args):
  return args

@util.run_time
def test():
    total = 10
    works = 3

    r = int(total / works) + 1 if total % works > 0 else 0

    l = []
    for i in range(1, r+1):
        t = ThreadCrawl(str(i), subs)
        # t = threading.Thread(target=run)
        l.append(t)
        
        t.start()
        # print(f'线程{i}启动~')
    # print(total / works, total % works)
    # print(int(total / works) + 1 if total % works > 0 else 0)

    for p in l:
        p.join()

    print("多线程执行完毕")

    sum = 0
    for i in range(4):
        for j in range(3):
            sum += j
            # print('sum,sum=%d '%sum)

    print(f's={s}, sum={sum}')
# q.join()
# print("所有线程运行完毕")

if __name__ == '__main__':
    # func_a(func_b, 1, 2, 3)
    test()
    # print(1)
    # num = 100%6
    # print(num)
    # print(round(num))
    # print(int(num))