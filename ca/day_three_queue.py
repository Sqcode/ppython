import threading, queue, time

# 初始化一个队列
q = queue.Queue(maxsize=0)
# 生产者
def producer(name):
    course_num = 1
    while True:
        q.put('制作的第 {} 套课程'.format(course_num))
        print("{} 制作的第 {} 套课程".format(name, course_num))
        course_num += 1
        time.sleep(5)
# 消费者
def consumer(name):
    while True:
        print('{} 购买了 {}'.format(name, q.get()))
        time.sleep(1)
        q.task_done()

# 开启三个进程
t1 = threading.Thread(target=producer, args=('橡皮擦',))
t2 = threading.Thread(target=consumer, args=('CSDN 账户 A',))
t3 = threading.Thread(target=consumer, args=('CSDN 账户 B',))

t1.start()
# t2.start()
# t3.start()

# # 初始化一个空队列，不限制长度
# q = queue.Queue()

# def worker():
#     while True:
#         item = q.get()
#         print(f'正在执行： {item}, 完成： {item}')
#         # 发送任务完成的命令
#         q.task_done()

# # 开启多线程
# threading.Thread(target=worker, daemon=True).start()

# # 设置 30 个 put
# for item in range(30):
#     q.put(item)

# print('所有的任务已经完成\n', end='')

# # 阻塞，直到所有任务完成
# q.join()
# print('所有任务完成')


# http://www.netbian.com/mei/index.htm