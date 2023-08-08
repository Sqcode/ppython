import parsel, tomd, re
# pip install tomd -i https://pypi.tuna.tsinghua.edu.cn/simple
from module_path import util, logging

# 把文章保存为markdown
def download_article(url):
    try:
        html = util.get_html(url)
        # 把网页变成css选择器，解析网页
        sel = parsel.Selector(html)
        # 标题，内容
        title = sel.css('.title-article::text').get()
        content = sel.css('article').get()

        # 提取文章的内容与格式
        text = tomd.Tomd(content).markdown
        text = re.sub('<article.*?article>', "", text)
        # 获取后，标题中带有<a>..</a>的去掉
        text = re.sub('<a.*</a>', "", text)

        """
        将图片下载 下来，替换文章中的csdn链接
        """
        imgs = re.findall('<img.*?>', text)

        root_path = util.JarProjectPath.project_root_path()
        # 创建文件夹
        folder = util.mkdir(path='%s/files/%s'%(root_path, title))
            
        for i in range(len(imgs)):
            # 获取图片地址
            url = re.search(r'.*src="(.*?)"', imgs[i]).group(1)
            # print(imgs[i])
            # 下载图片，返回本地路径
            filepath = util.download_img(url, filename='%s_%d'%(title, i), filedir=folder)
            # 替换文章中的链接
            text = text.replace(imgs[i], '<img src="%s" >'%filepath)

        # 保存文章路径
        filename = '%s/files/%s.md'%(root_path, title)
        # 保存
        with open(filename, mode='w', encoding='utf-8') as f:
            f.write("#" + title)
            f.write(text)
    
    except Exception as e:
        logging.debug(e)
        print('失败>%s'%url)


if __name__ == '__main__':
    # 博客地址url，问号后的参数可以都删掉
    url = 'https://blog.csdn.net/jasonsong2008/article/details/87801529'
    download_article(url)

    # text = '11<a id="1903__10__4__John_Vincent_Atanasoff__24"></a>'
    # text = re.sub('<a.*</a>', "", text)
    # print(text)
