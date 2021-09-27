import sys, os
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '../common')))
# print(__dir__)
from util import get_html
from excel import excel
# 爬取csdn博主文章，并保存？
import time
from bs4 import BeautifulSoup

# 文章列表
def get_ats(html, ats):
    """
    :param :html 网页源码
    :param :ats  即将要导出excel的内容
    """
    soup = BeautifulSoup(html, 'html.parser')
    box = soup.select('div .article-item-box')
    if box:
        for i in range(len(box)):
            item = box[i]
            at = []
            # 标题
            a = item.select('a')[0]
            # 避免标题/文章头内容的，\t\n && 英文逗号，影响csv的分割，这里替换掉
            title = a.text.strip().replace('\n','').replace(',','，')
            titles = title.split('          ')
            at.append(titles[0])
            at.append(titles[1])
            at.append(a['href'])
            # print(title, title.split('          ')[1])
            ps = item.select('p')

            # 文章头，时间，阅读，评论
            for i in range(len(ps)):
                if i == 1:
                    for j in ps[i].select('span'):
                        at.append(j.text)
                else:
                    at.append(ps[i].text.strip().replace(',','，'))
            # print(at)
            ats.append(at)
    return ats

# 保存
def wrt(ats):
    name = str(round(time.time()))
    with open(f'./files/{name}.csv', 'a+', encoding='utf-8') as f:
        for i in range(len(ats)):
            f.write(','.join(ats[i]))
            f.write('\n')
        #print(','.join(i))

if __name__ == '__main__':
    # 表头
    ats = [['创作','标题','链接','文章头','时间','阅读','评论']]

    
    # 博主首页链接，擦姐的域名，很强。带有一个dream，普通人就是 https://blog.csdn.net/博主名称
    blog_url = 'https://dream.blog.csdn.net'
    # blog_url = 'https://blog.csdn.net/博主名称'
    
    # 自行查看，博主首页文章的页数
    pages = 2

    # 循环获取每一页
    for i in range(1, pages+1):
        url = f'{blog_url}/article/list/{i}'
        print(f'爬取。。。{url}')
        html = get_html(url)
        ats = get_ats(html, ats)

    # 保存csv，保存后如若用excel打开，则需先用记事本打开，另存为 ANSI ， 才不会乱码
    # wrt(ats)

    # 保存excel
    ex = excel()
    # with_url , 哪一列下标内容带url，ats数组改列后面必须紧接着url
    ex.write_row(ats, with_url=1)
    #ex.wbac.cell(row=1, column=1).value = '=HYPERLINK("{}", "{}")'.format('https://www.baidu.com', "Link Name")
    ex.save()