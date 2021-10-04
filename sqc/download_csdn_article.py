# 模块导入
import parsel 
import tomd # pip install tomd -i https://pypi.tuna.tsinghua.edu.cn/simple
import  re

from module_path import util, logging

# 把文章保存成markdown格式
def download_article(article_url):
    try:
        html = util.get_html(article_url)
        # print(html)

        # 把网页变成css选择器，解析网页
        sel = parsel.Selector(html)
        # 标题，内容
        title = sel.css('.title-article::text').get()
        content = sel.css('article').get()
        # print(title)
        # print(content)

        # 提取文章的内容与格式
        text = tomd.Tomd(content).markdown
        text = re.sub('<article.*?article>', "", text)  #正则表达式
        # print(text)

        filename = util.get_save_path('%s.md'%title)

        with open(filename, mode='w', encoding='utf-8') as f:
            f.write("#" + title)
            f.write(text)
    except Exception as e:
        print('失败>%s'%url)


if __name__ == '__main__':
    # print(util.get_save_path(filename='11.md'))
    # header = util.get_headers()
    # print(header)

    # 博客地址u'r'l,填入即可
    url = 'https://blog.csdn.net/mengchuan6666/article/details/120591747'
    download_article(url)
