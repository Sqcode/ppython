import requests
import re
import os
import time

def mkdir(path):
	folder = os.path.exists(path)
	if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
		print ("---  new folder...  ---", path)
	#else:
		#print ("---  There is this folder!  ---")

def dowmloadPic(html, keyword):
    #print (html)
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)
    if len(pic_url) > 0:
        filedir = './images/' + str(round(time.time() * 1000)) + '/'
        mkdir(filedir)
        i = 1
        for each in pic_url:
            reg = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
            if re.match(reg, url):
                print('正在下载第' + str(i) + '张图片，图片地址:' + str(each))
                
                try:
                    pic = requests.get(each, timeout=10)
                except BaseException:
                    print('【错误】当前图片无法下载')
                    continue
                # filename = keyword + '_' + str(i) + '.png'
                filename = str(i) + '.png'
                with open(filedir + filename, 'wb') as f:
                    f.write(pic.content)

                i += 1
                if i == 11:
                    break
if __name__ == '__main__':
    word = input("Input key word: ")
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&ct=201326592&v=flip'
    header = {  # 模拟浏览器头部信息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    result = requests.get(url, headers=header)
    dowmloadPic(result.text, word)