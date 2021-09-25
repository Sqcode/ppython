import sys, os
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '../common')))
import util, maoyan_jieba
from exp import SkipException
import requests, json, time, random, slide_selenium, threading
from bs4 import BeautifulSoup

# 解析一页数据
def parse_ono_page(html):
    try:
        data = json.loads(html)['cmts'] #评论以json形式存储,故以json形式截取
    except Exception:
        raise SkipException('json解析错误，获取不到cmts') 
    #data = json.loads(html)['hcmts'] #评论以json形式存储,故以json形式截取
    for item in data:
        yield { #该方法返回一个字典
            'comment':item['content'],
            'date':item['time'].split(' ')[0],
            'rate':item['score'],
            'city':item['cityName'],
            'nickname':item['nickName']
        }

# 返回评论总数
def parse_ono_pages(html):
    # 总数
    total = json.loads(html)['total']
    return total

# {"approve":0,"assistAwardInfo":{"avatar":"","celebrityId":0,"celebrityName":"","rank":0,"title":""},"avatarurl":"https://img.meituan.net/maoyanuser/0d20974fe7a2dcb726680f4d94493b8511096.png","cityName":"北京","content":"刘德华演技在线，画面真美，剧情太烂！","id":1143035845,"isMajor":false,"juryLevel":0,"movieId":341516,"nick":"zhangsq0812","nickName":"zhangsq0812","oppose":0,"pro":false,"reply":0,"score":0.5,"spoiler":0,"startTime":"2021-09-10 11:55:57","supportComment":true,"supportLike":true,"sureViewed":1,"tagList":{"fixed":[{"id":2,"name":"购票差评"},{"id":4,"name":"购票"}]},"time":"2021-09-10 11:55","userId":220211944,"userLevel":0,"vipType":0}
#保存数据到文本文档
def save_to_txt(url, filepath=os.path.join(__dir__, f'../files/{str(round(time.time() * 1000))}.txt')):
    html = util.get_html(url)
    # print(filepath)
    try:
        cmts = parse_ono_page(html)
    except Exception:
        raise SkipException('解析JSON异常') 
    
    for item in cmts:
        # print(item)
        with open(filepath,'a',encoding='utf-8') as f:
            f.write(item['date'] + ',' + item['nickname'] + ',' + item['city'] + ',' +str(item['rate'])+','+item['comment']+'\n')

# 获取的评论可能有重复，为了最终统计的真实性，需做去重处理
def delete_repeat(old,new):
    oldfile = open(old,'r',encoding='UTF-8')
    newfile = open(new,'w',encoding='UTF-8')
    content_list = oldfile.readlines() #读取的数据集
    content_alreadly_ditinct = [] #存储不重复的评论数据
    for line in content_list:
        if line not in content_alreadly_ditinct: #评论不重复
            newfile.write(line+'\n')
            content_alreadly_ditinct.append(line)

# 获取网页，并保存至txt
def scrawl(url):
    print(f'正在爬取{url}')
    html = util.get_html(url)
    save_to_txt(html)

# 第一次访问 可能需要人工验证，滑块
@util.run_time
def valid(html, url):
    times = 1
    while(True):
        soup = BeautifulSoup(html, 'html.parser')
        titles = soup.select('title')
        print(titles)
        if len(titles) > 0:
            title = titles[0].text
            if '验证' in title:
                slide_selenium.selenium_get_html(url)
                time.sleep(1)
                html = util.get_html(url)
                times += 1
            else:
                break
        else: 
            break
            # return html
        if times > 3:
            raise SkipException('无法通过滑块验证，error')
    return util.get_html(url)

# 通过id，获取电影名称
@util.run_time
def get_movie_name(movie_id):
    """
    :param :movie_id - 电影id
    """
    html = util.get_html(f'http://api.maoyan.com/mmdb/movie/v5/{movie_id}.json')
    data = json.loads(html)['data']['movie']
    return data

# 通过关键字，返回电影列表。只返回第一个
def get_movies(keyword):
    html = util.get_html(f'https://maoyan.com/ajax/suggest?kw={keyword}')
    # print(html)
    mvs = json.loads(html)['movies']['list']
    # print(mvs)
    if (len(mvs) == 0):
        raise SkipException(f'找不到{keyword}')
    return mvs[0]

# 爬url
@util.run_time
def do_scrawl(url, movie_name=f'movie{str(round(time.time() * 1000))}'):
    """
    :param :url 要爬取的链接
    :param :movie_name 电影名称，保存txt文件名
    """
    try:
        html = util.get_html(url)
        print('第一次 进行反复循环，检测是否需要验证')
        # 第一次 进行反复循环，检测是否需要验证
        html = valid(html, url)
    except SkipException as obj:
        print(obj)
        sys.exit(1)
    # print(html)
    # 评论总数
    total = parse_ono_pages(html)
    # 发现接口只返回1000条
    if total > 1000:
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

    root_path = util.JarProjectPath.project_root_path('py')
    filepath = root_path + f'files/{movie_name}.txt'
    print(f'共{total}条评论，每页{size}条，可爬{pages}页，随机预设【{thrs}】个线程，每个线程需爬取【{works}】页')
    # 多线程爬取
    l = []
    # 线程从1开始，各加1
    for i in range(1, thrs+1):
        if i == thrs and pages % works != 0:
            # 最后一个线程，不能超出可爬取的页数
            t = threading.Thread(target=save_batch, args=(i, works*(i-1), works*(i-1) + pages % works, filepath))
        else: 
            t = threading.Thread(target=save_batch, args=(i, works*(i-1), works*i, filepath))
        l.append(t)
        print("线程{} 启动".format(i))
        t.start()
        
    for p in l:
        p.join()

    print("多线程执行完成，爬取完毕")
    print(f'共{total}条评论，每页{size}条，可爬{pages}页，随机预设【{thrs}】个线程，每个线程需爬取【{works}】页')

# 爬取，XX电影
def scrawl_mv(keyword):
    try:
        mv = get_movies(keyword)
    except SkipException as e :
        print(e)
    
    movie_id = mv['id']
    movie_name = mv['nm']
    print(type(mv), movie_id, movie_name)
    url = f'http://api.maoyan.com/mmdb/comments/movie/{movie_id}.json?_v_=yes&offset=1'
    print(f'正在爬取 --- 【{movie_name}】====第一页======= {url}')
    do_scrawl(url, movie_name)

# 多线程爬取
def save_batch(no, start, end, filepath):
    # 这里因为接口，第一页返回数据1-15，第二页返回数据2-16，造成数据重复。
    # 所以 这里给offset 循环一次加上15
    size = 15 # 固定
    for i in range(start, end):
        # 反爬
        time.sleep(1 + float(random.randint(1,100)) / 20)
        url = f'http://api.maoyan.com/mmdb/comments/movie/1263235.json?_v_=yes&offset={i*size+1}'
        print(f'Thread.{no} >>> 正在保存 --- {url}')
        try:
            save_to_txt(url, filepath)
        except SkipException as obj:
            continue

# 测试
@util.run_time
def thread_test(movie_name):
    # 评论总数
    total = 1530
    # 接口 返回的评论条数
    size = 15
    # 取整的页数
    pages = round(total/size)
    # 每个线程的工作量
    works = 50

    # 最大线程数
    r = int(pages / works) + 1 if pages % works > 0 else 0
    print(f'共{total}条评论，每页{size}条，可爬{pages}页，预设每个线程爬取【{works}】页，需要【{r}】个线程')
    
    root_path = util.JarProjectPath.project_root_path('py')
    filepath = root_path + f'files/{movie_name}.txt'

    # l = []
    # for i in range(1, r+1):
    #     if i == r:
    #         # 最后一个线程，不能超出可爬取的页数
    #         t = ThreadCrawl(str(i), save_batch, works*(i-1), works*(i-1) + pages % works, filepath)
    #     else: 
    #         t = ThreadCrawl(str(i), save_batch, works*(i-1), works*i, filepath)
    #     l.append(t)
    #     t.start()

    # for p in l:
    #     p.join()

    print("多线程执行完成，爬取完毕")

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
        print(f'线程{self.threadName}：************启动************')
        self.func
        
if __name__ =='__main__':
    # print(get_movies('怒火·重案'))
    movie_name = '我的青春有个你'
    scrawl_mv(movie_name)

    filepath = f'files/{movie_name}.txt'
    
    if os.path.exists(filepath):
        print(os.path.abspath(filepath))
        maoyan_jieba.analysis(os.path.abspath(filepath))
