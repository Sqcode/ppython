import requests
import threading
from queue import Queue
from lxml import etree
import time
import random

# 初始化一个队列
q = Queue(maxsize=0)
# 批量添加数据
for page in range(1, 2):
    q.put('https://www.huaroo.net/d/pg_{}/'.format(page))

# 获取头文件，其中的 uas 自行设置
def get_headers():
    uas = [
        "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
        "Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)"
    ]
    ua = random.choice(uas)
    headers = {
        "user-agent": ua,
        "referer": "https://www.baidu.com"
    }
    return headers

# 格式化数据
def format(text):
    element = etree.HTML(text)
    # print(element)
    article_list = element.xpath('//div[contains(@class,"article_list")]')
    # print(article_list)
    wait_save_str = ""
    # 通过 xpath 提取数据
    for article in article_list:

        title = article.xpath("./a/div/div[@class='article_title']/text()")[0].strip()
        hospital = article.xpath("./a/div/div[@class='hospital_list_content mt10 oh']/div[1]/text()")[0].strip()
        duties = article.xpath("./a/div/div[@class='hospital_list_content mt10 oh']/div[2]/text()")[0].strip()
        practice = article.xpath("./a/div/div[@class='hospital_list_content mt10 oh']/div[3]/text()")[0].strip()
        project = article.xpath("./a/div/div[@class='hospital_list_content mt10 oh']/div[4]/text()")[0].strip()
        wait_save_str += f"{title},{hospital},{duties},{practice},{project}\n"
    save(wait_save_str)

# 储存数据
def save(wait_save_str):
    with open('./医美.csv', 'a+', encoding='utf-8') as f:
        f.write(wait_save_str)
    print(wait_save_str, "---保存成功")


# 爬虫请求与解析入口
def run():
    while q.qsize() > 0:
        url = q.get()
        # print(url)
        q.task_done()
        res = requests.get(url=url, headers=get_headers(), timeout=10)
        format(res.text)



l = []
for i in range(2):
    t = threading.Thread(target=run)
    l.append(t)
    t.start()

for p in l:
    p.join()

print("多线程执行完毕")

q.join()
print("所有线程运行完毕")
