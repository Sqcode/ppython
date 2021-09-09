import queue
import threading
import requests

CRAWL_EXIT = False
url_format = "https://tuchong.com/tags/西湖/"
headers = {  # 模拟浏览器头部信息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
class ThreadCrawl(threading.Thread):
    def __init__(self, thread_name, page_queue, data_queue):
        # threading.Thread.__init__(self)
        # 调用父类初始化方法
        super(ThreadCrawl, self).__init__()
        self.threadName = thread_name
        self.page_queue = page_queue
        self.data_queue = data_queue
    def run(self):
        print(self.threadName + ' 启动************')
        while not CRAWL_EXIT:
            try:
                global tag, url, headers, img_format  # 把全局的值拿过来
                # 队列为空 产生异常
                page = self.page_queue.get(block=False)   # 从里面获取值
                spider_url = url_format.format('tag',page,3)   # 拼接要爬取的URL
                # print(spider_url)
            except:
                break

            timeout = 4   # 合格地方是尝试获取3次，3次都失败，就跳出
            while timeout > 0:
                timeout -= 1
                try:
                    with requests.Session() as s:
                        response = s.get(spider_url, headers=headers, timeout=3)
                        json_data = response.json()
                        print('json_data', json_data)
                        if json_data is not None:
                            imgs = json_data["postList"]
                            for i in imgs:
                                imgs = i["images"]
                                for img in imgs:
                                    print('img --- ', img)
                                    # img = img_format.format(img["user_id"],img["img_id"])
                                    # self.data_queue.put(img)  # 捕获到图片链接，之后，存入一个新的队列里面，等待下一步的操作

                    break

                except Exception as e:
                    print(e)


            if timeout <= 0:
                print('time out!')

def main():
    page_queue = queue.Queue(10)
    for i in range(1,10):
        page_queue.put(i)

    # print(page_queue.qsize(), page_queue.empty(),
    # page_queue.full())

    data_queue = queue.Queue()
    # 记录线程的列表
    thread_crawl = []
    # 每次开启4个线程
    craw_list = ['采集线程1号','采集线程2号']
    for thread_name in craw_list:
        c_thread = ThreadCrawl(thread_name, page_queue, data_queue)
        c_thread.start()
        thread_crawl.append(c_thread)

    # 等待page_queue队列为空，也就是等待之前的操作执行完毕
    while not page_queue.empty():
        pass

    

if __name__ == '__main__':
    main()