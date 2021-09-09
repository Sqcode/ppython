
from codecs import utf_16_be_decode
import requests
from bs4 import BeautifulSoup
import bs4
import re

url = 'http://news.baidu.com/'
# https://www.csdn.net/

header = {  # 模拟浏览器头部信息
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}
cookie={
    "BIDUPSID=700C9D09A9A9CE337D4D0809750ADA86; PSTM=1622697748; BAIDUID=EE1286C707089C0A235C6604C415CC0A:FG=1; __yjs_duid=1_4fa1bc9de85bd3682d78d1cbd97ebc791622704218460; channel=baidusearch; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; MCITY=-178%3A; H_PS_PSSID=34099_31254_34004_34073_33607_34106_34135_22159; delPer=0; PSINO=5; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BAIDUID_BFESS=4CF9ED528E735D0F4F9A82F90BFA87E1:FG=1; BA_HECTOR=810ka0a184a02l0k7l1gd7r1s0q; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1623725764,1624233589,1624254915,1624501312; BK_SEARCHLOG=%7B%22key%22%3A%5B%22%E7%8C%AA%22%5D%7D; Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a=1624501414; BKWPF=3; ab_sr=1.0.1_ODgwMWIzNDliZmM3MDE4MGQ3MzUzOWE5ZjdjNDhhMWYzMDA4ODk2YTFjOWMyYjU3YTk5MjY4ZGQ3NzczNzk5ZTMzYTVlMmU3YjI0Njk1M2U1YzdlN2VjYWFjYjlkOGU2YTY3OGM3ZWQwYTEwNzhkNGFhNzU1ZTMwNGQ0YjIyMTExNmI2NGNiMmI0ZjdlMzJkODkyYmQ5M2YwMWQwNjAzMg=="
}
def url_open(url):
    req=requests.get(url, headers=header)
    html=req.text
    return html

r = requests.get(url, headers=header)
#r.encoding=utf_16_be_decode
if r.status_code == requests.codes.ok:
    print(r.status_code)  # 响应码
    #print(r.headers)  # 响应头
    #print(r.headers.get('content-type'))  # 推荐使用这种获取方式，获取其中的某个字段
    html = r.text
    #print (html)
    soup = BeautifulSoup(html, 'html.parser')
    
    # 获取右边的图片
    # for item in soup.find_all('img'):
    #     print (item)
    #     #print (item.get('src'))
    #     src = item.get('src')
    #     filename=src.split('/')[-1] #get the last member of arr,that is the name
    #     with open(filename,'wb') as f:
    #         img = url_open(src+'jpg')
    #         f.write(img)

    

    # 获取的热点要闻
    for item in soup.select('div #pane-news li'):
        #print(item)
        result = list()
        for item1 in item.select('a'):
            #print(item1)
            if item1.string:
                result.append(item1.string)
        print(','.join(result))
        print("-----------------------------------------------")
else:
    r.raise_for_status()

# 加入请求头，获取cookies
# r = requests.get(url, headers=header)
# # 遍历出所有的cookie字段的值
# for cookie in r.cookies.keys():
#     print (cookie+':'+r.cookies.get(cookie))

# 自定义cookies
# cookies = dict(name='s',age='1')
# r = requests.get(url, headers=header, cookies=cookies)
# print (r.text)

