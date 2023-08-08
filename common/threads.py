import random
import threading, time, json
from queue import Queue
import util
from exp import SkipException
class ThreadCrawl(threading.Thread):
    """
    :param :thread_name 线程名称
    :param :func 线程要执行的函数
    """
    def __init__(self, thread_name, func, *args):
        # threading.Thread.__init__(self)
        # 调用父类初始化方法
        super(ThreadCrawl, self).__init__()
        self.threadName = thread_name
        self.func = func(*args)
        print('线程初始化', *args)
    def run(self):
        # runrun(self.threadName)
        print(self.threadName + '************启动************')
        self.func

s = 0
# 爬虫请求与解析入口
def runrun(thread_name):
    global s
    for x in range(3):
        s += x
        print('线程 - %s,s=%d '%(thread_name,s))
    # time.sleep(1)

def add(start, end):
    global s
    for x in range(start, end):
        s += 1
        # print('add,s=%d '%s)
            
def subs():
    global s
    for x in range(3):
        s -= x
        print('subs,s=%d '%s)

def func_a(func, *args, **kwargs):
  print(func(*args, **kwargs))
 
def func_b(*args):
  return args

def save_batch(no, start, end):
    # 这里因为接口，第一页返回数据1-15，第二页返回数据2-16，造成数据重复。
    # 所以 这里给offset 循环一次加上15
    size = 15 # 固定
    for i in range(start, end):
        # 反爬
        # time.sleep(1 + float(random.randint(1,100)) / 20)
        url = f'http://api.maoyan.com/mmdb/comments/movie/1263235.json?_v_=yes&offset={i*size+1}'
        print(f'No.{no} --------- {url}')
        
@util.run_time
def test():
    # 评论总数
    # 共30256条评论，每页15条，可爬2017页，随机预设【8】个线程，每个线程需爬取【288】页
    total = 1000
    # 接口 返回的评论条数
    size = 15
    # 取整的页数
    pages = round(total/size)
    # 每个线程的工作量
    # thrs = 2
    thrs = random.randint(2,10)
    works = round(pages / thrs)

    # 如果 线程*每个线程工作量<总页数，需要在启动一个线程
    if thrs * works < pages:
        thrs += 1

    # 多线程爬取
    l = []
    # 线程从1开始，各加1
    for i in range(1, thrs+1):
        if i == thrs and pages % works != 0:
            # 最后一个线程，不能超出可爬取的页数
            t = threading.Thread(target=save_batch, args=(i, works*(i-1), works*(i-1) + pages % works))
        else: 
            t = threading.Thread(target=save_batch, args=(i, works*(i-1), works*i))
        l.append(t)
        print("线程{} 启动".format(i))
        t.start()
        
    for p in l:
        p.join()

    print("多线程执行完成，爬取完毕")
    print(f'共{total}条评论，每页{size}条，可爬{pages}页，随机预设【{thrs}】个线程，每个线程需爬取【{works}】页')
# q.join()
# print("所有线程运行完毕")

def parse_ono_page(html):
    data = json.loads(html)['cmts'] #评论以json形式存储,故以json形式截取
    print(data)
    for item in data:
        yield { #该方法返回一个字典
            'comment':item['content'],
            'date':item['time'].split(' ')[0],
            'rate':item['score'],
            'city':item['cityName'],
            'nickname':item['nickName']
        }

def exp():
    try:
        a = 1/random.randint(0,3)
    except Exception:
        raise SkipException('解析JSON异常') 

def test_exp():
    for i in range(1, 6):
        try:
            exp()
        except SkipException as obj:
            continue
        print(i)


if __name__ == '__main__':
    test_exp()
    # func_a(func_b, 1, 2, 3)
    # parse_ono_page(html)
    test()
    # print(random.randint(1,10))
    # num = 100%6
    # print(num)
    # print(round(num))
    # print(int(num))