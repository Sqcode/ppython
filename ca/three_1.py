import sys, os
# 将工具类util放入搜索路径里，否则无法引入
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '../')))
# print(__dir__, sys.path)
from util import get_html, mkdir, download_img

import requests, re
from bs4 import BeautifulSoup


def climb_netbian(res, domain=''):
    # print(res.text)
    soup = BeautifulSoup(res, 'html.parser')
    imgs = soup.find_all('img')
    print(len(imgs))
    for item in imgs:
        alt = item.get('alt')
        if alt is None:
            continue
        src = item.get('src')
        print (alt, src)
        #print (src[-4:])

        download_img(src, filename=alt, domain=domain)

def netbian(name, mode=None):
    
    # urls = [f"http://www.netbian.com/mei/index_{i}.htm" for i in range(2, 201)]
    # url = "http://www.netbian.com/mei/index.htm"
    # urls.insert(0, url)

    domain = 'http://www.netbian.com'
    # 4k 后缀html,普通htm
    point = 'htm'
    if mode == '4k':
        domain = 'https://pic.netbian.com'
        point = 'html'
        name = mode+name
    
    # 保存到一整个文件夹
    filedir = mkdir()
    for i in range(1, 3):
        if i == 1:
            url = f'{domain}/{name}'  # /index.htm
        else:
            url = f'{domain}/{name}/index_{i}.{point}'
        print(url)
        climb_netbian(get_html(url, encoding='gbk'), filedir, domain)
        #climb_netbian(get_html(url, encoding='gbk'), domain)

error_list = []

# 获取全部奥特曼详情页
def get_aoteman_list(html):
    start_index = '<ul class="lists">'
    start = html.find(start_index)
    html = html[start:]
    links = re.findall('<li class="item"><a href="(.*)">', html)
    # links = list(set(links))
    links = [f"http://www.ultramanclub.com/allultraman/{i.split('/')[1]}/" for i in set(links)]
    return links

def get_image(url, filedir='images'):
    print(url)
    try:
        # 网页访问速度慢，需要设置 timeout
        res = get_html(url, encoding='gb2312', timeout=15)
        # 获取详情页标题，作为图片文件名
        title = re.search('<title>(.*?)\[', res).group(1)
        # 获取图片短连接地址
        image_short = re.search(
            '<figure class="image tile">[.\s]*?<img src="(.*?)"', res).group(1)
        # 拼接完整图片地址
        img_url = "http://www.ultramanclub.com/allultraman/" + image_short[3:]
        # 获取图片数据
        img_data = requests.get(img_url).content
        print(f"正在爬取{title}")
        if title is not None and image_short is not None:
            with open(filedir + title + '.png', 'wb') as f:
                f.write(img_data)
            # with open(f"images/{title}.png", "wb") as f:
            #     f.write(img_data)

    except Exception as e:
        print("*"*100)
        print(url)
        print("请求异常", e)

        error_list.append(url)

# 爬虫入口
def aoteman():
    url = "http://www.ultramanclub.com/allultraman/"
    try:
        # 网页访问速度慢，需要设置 timeout
        res = get_html(url, encoding='gb2312')
        return get_aoteman_list(res)

    except Exception as e:
        print("请求异常", e)

if __name__ == '__main__':
    # aotemans = aoteman()
    # print(aotemans)
    # filedir = mkdir()
    # for detail in aoteman():
    #     get_image(detail, filedir)

    # while len(error_list) > 0:
    #     print("再次爬取")
    #     detail = error_list.pop()
    #     get_image(detail)

    # print("奥特曼图片数据爬取完毕")
    netbian('dongwu', mode='4k')
    
    #res = get_html('http://www.netbian.com/mei/index.htm', encoding='gbk')

    #main(res)