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

#print(len(soup.select('div .article-item-box')))

# print(soup.select('.ui-pager'))
# pageBox = soup.select('#pageBox')[0]
# print(pageBox)
# print(pageBox.select('li'))

# 文章列表
def get_ats(html, ats):
    soup = BeautifulSoup(html, 'html.parser')
    box = soup.select('div .article-item-box')
    for i in range(len(box)):
        item = box[i]
        at = []
        # 标题
        a = item.select('a')[0]
        title = a.text.strip().replace('\n','').replace(',','，')
        titles = title.split('          ')
        at.append(titles[0])
        at.append(titles[1])
        at.append(a['href'])
        # print(title, title.split('          ')[1])
        ps = item.select('p')

        # 描述，时间，阅读，评论
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

#als = soup.find('article-list')
#print(als)

if __name__ == '__main__':
    # with open('./files/1631165674.csv','r') as f:
    #     print(f.read())
    ats = [['创作','标题','链接','描述','时间','阅读','评论']]
    for i in range(1,2):
        print(i)
        html = get_html(f'https://dream.blog.csdn.net/article/list/{i}')
        ats = get_ats(html, ats)
    #ats.append(['原创','标题','https://www.baidu.com','描述','时间','1231432','234324'])
    # print(ats)
    # wrt(ats)

    ex = excel()
    # with_url , 哪个下标内容带url，后面必须紧接着url
    ex.write_row(ats, with_url=1)
    #ex.wbac.cell(row=1, column=1).value = '=HYPERLINK("{}", "{}")'.format('https://www.baidu.com', "Link Name")
    ex.save()