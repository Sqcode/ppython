import sys, os
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '../common')))
import util
import requests
import json
import time
import random
import slide_selenium
from bs4 import BeautifulSoup

# 解析一页数据
def parse_ono_page(html):
    data = json.loads(html)['cmts'] #评论以json形式存储,故以json形式截取
    #data = json.loads(html)['hcmts'] #评论以json形式存储,故以json形式截取
    for item in data:
        yield { #该方法返回一个字典
            'comment':item['content'],
            'date':item['time'].split(' ')[0],
            'rate':item['score'],
            'city':item['cityName'],
            'nickname':item['nickName']
        }

def parse_ono_pages(html):
    # 总数
    total = json.loads(html)['total']
    return total

# {"approve":0,"assistAwardInfo":{"avatar":"","celebrityId":0,"celebrityName":"","rank":0,"title":""},"avatarurl":"https://img.meituan.net/maoyanuser/0d20974fe7a2dcb726680f4d94493b8511096.png","cityName":"北京","content":"刘德华演技在线，画面真美，剧情太烂！","id":1143035845,"isMajor":false,"juryLevel":0,"movieId":341516,"nick":"zhangsq0812","nickName":"zhangsq0812","oppose":0,"pro":false,"reply":0,"score":0.5,"spoiler":0,"startTime":"2021-09-10 11:55:57","supportComment":true,"supportLike":true,"sureViewed":1,"tagList":{"fixed":[{"id":2,"name":"购票差评"},{"id":4,"name":"购票"}]},"time":"2021-09-10 11:55","userId":220211944,"userLevel":0,"vipType":0}
#保存数据到文本文档
def save_to_txt(html, filepath):
    print(filepath)
    for item in parse_ono_page(html):
        print(item)
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

def scrawl(url, filepath=os.path.join(__dir__, f'../files/{str(round(time.time() * 1000))}.txt'), valid=False):
    print(f'正在爬取{url}')
    html = util.get_html(url)
    save_to_txt(html, filepath)

def valid(html):
    times = 1
    while(True):
        soup = BeautifulSoup(html, 'html.parser')
        titles = soup.select('title')
        # print(titles)
        if len(titles) > 0:
            title = titles[0].text
            if '验证' in title:
                slide_selenium.selenium_get_html(url)
                time.sleep(1)
                html = util.get_html(url)
            times += 1
        else: 
            break
        if times > 3:
            raise MyException('error')

def get_movie_name(movie_id):
    html = util.get_html(f'http://api.maoyan.com/mmdb/movie/v5/{movie_id}.json')
    data = json.loads(html)['data']['movie']
    return data

def get_movies(keyword):
    html = util.get_html(f'https://maoyan.com/ajax/suggest?kw={keyword}')
    # print(html)
    mvs = json.loads(html)['movies']['list']
    print(mvs)
    if (len(mvs) == 0):
        raise MyException(f'找不到{keyword}')
    return mvs[0]

class MyException(Exception): #让MyException类继承Exception
    def __init__(self,msg):
        self.msg = msg

def do_scrawl(url, movie_name=f'movie{str(round(time.time() * 1000))}'):
    # 这里因为接口，第一页返回数据1-15，第二页返回数据2-16，造成数据重复。
    # 所以 这里给offset 循环一次加上15
    size = 15 # 固定
    try:
        # scrawl(url, util.JarProjectPath.project_root_path('py') + 'files/m.txt', valid=True)
        html = util.get_html(url)
        print('第一次 进行反复循环，检测是否需要验证')
        # 第一次 进行反复循环，检测是否需要验证
        valid(html)
        total = parse_ono_pages(html)
    except MyException as obj:
        print(obj)

    pages = round(total/15)
    print(f'共{total}条，可爬{pages}页')

    root_path = util.JarProjectPath.project_root_path('py')
    for i in range(2, 5):
        # 反爬
        time.sleep(1 + float(random.randint(1,100)) / 20) 
        url = f'http://m.maoyan.com/mmdb/comments/movie/1263235.json?_v_=yes&offset={(i-1)*size+1}'
        scrawl(url, root_path + f'files/{movie_name}.txt')

def scrawl_mv(keyword):
    try:
        mv = get_movies(keyword)
    except MyException as e :
        print(e)
    
    movie_id = mv['id']
    movie_name = mv['nm']
    print(type(mv), movie_id, movie_name)
    url = f'http://m.maoyan.com/mmdb/comments/movie/{movie_id}.json?_v_=yes&offset=1'
    
    do_scrawl(url, movie_name)
    print(url)


if __name__ =='__main__':
    # mv = get_movie_name('1263235')
    # print(type(mv))
    # print(mv['nm'])
    # mv = get_movies('失控玩家')
    scrawl_mv('失控玩家')
