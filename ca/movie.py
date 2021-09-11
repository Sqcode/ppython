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
# 解析一页数据
def parse_ono_page(html):
    data = json.loads(html)['cmts'] #评论以json形式存储,故以json形式截取
    #data = json.loads(html)['hcmts'] #评论以json形式存储,故以json形式截取
    # 总数
    total = json.loads(html)['total']
    for item in data:
        yield{ #该方法返回一个字典
            'comment':item['content'],
            'date':item['time'].split(' ')[0],
            'rate':item['score'],
            'city':item['cityName'],
            'nickname':item['nickName']
        }
# {"approve":0,"assistAwardInfo":{"avatar":"","celebrityId":0,"celebrityName":"","rank":0,"title":""},"avatarurl":"https://img.meituan.net/maoyanuser/0d20974fe7a2dcb726680f4d94493b8511096.png","cityName":"北京","content":"刘德华演技在线，画面真美，剧情太烂！","id":1143035845,"isMajor":false,"juryLevel":0,"movieId":341516,"nick":"zhangsq0812","nickName":"zhangsq0812","oppose":0,"pro":false,"reply":0,"score":0.5,"spoiler":0,"startTime":"2021-09-10 11:55:57","supportComment":true,"supportLike":true,"sureViewed":1,"tagList":{"fixed":[{"id":2,"name":"购票差评"},{"id":4,"name":"购票"}]},"time":"2021-09-10 11:55","userId":220211944,"userLevel":0,"vipType":0}
#保存数据到文本文档
def save_to_txt(html):
    # for i in range(1, 2):
    #     url='http://m.maoyan.com/mmdb/comments/movie/341516.json?_v_=yes&offset=' + str(i)
    #     html = get_one_page(url)
    path = os.path.join(__dir__, '../files/movie1263235.txt')
    for item in parse_ono_page(html):
        print(item)
        with open(path,'a',encoding='utf-8') as f:
            f.write(item['date'] + ',' + item['nickname'] + ',' + item['city'] + ',' +str(item['rate'])+','+item['comment']+'\n')
    #反爬
    time.sleep(5 + float(random.randint(1,100)) /20) 

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

if __name__ =='__main__':
    url = 'http://m.maoyan.com/mmdb/comments/movie/1263235.json?_v_=yes&offset=1'
    # 验证滑块
    # slide_selenium.selenium_get_html(url)
    # time.sleep(2)

    # 验证完再请求
    # html = util.get_html(url)
    # print(html) str(round(time.time() * 1000))

    for i in range(1, 20):
        time.sleep(1)
        url = 'http://m.maoyan.com/mmdb/comments/movie/1263235.json?_v_=yes&offset=' + str(i)
        print(f'正在爬取{url}')
        html = util.get_html(url)
        save_to_txt(html)

    # save_to_txt(html)
    # save_to_txt()
    # delete_repeat(r'狄仁杰.txt', r'狄仁杰_new.txt')
