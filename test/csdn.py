import requests
import re
import os
import time
import base64
import selenium
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def mkdir(path):
	folder = os.path.exists(path)
	if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
		print ("---  new folder...  ---", path)
	#else:
		#print ("---  There is this folder!  ---")

# 检查是否为图片类型
def check_image(content_type):
    if 'image' in content_type:
        return False
    else:
        return True
def dowmloadPic(html, keyword):
    #print (html)
    #pic_url = re.findall('"objURL":"(.*?)",', html, re.S)
    pic_url = re.findall('<img.*src="(.*?)"', html, re.S)
    #print (pic_url)

    if len(pic_url) > 0:
        filedir = './images/' + str(round(time.time() * 1000)) + '/'
        mkdir(filedir)
        i = 1
        for each in pic_url:
            reg = re.compile('.*(release|img-home|img-bss|side-toolbar).*')
            if re.match(reg, each):
                continue
            else:
                
                print('正在下载第' + str(i) + '张图片，图片地址:' + str(each))
                try:
                    reg = re.compile('.*(base64).*')
                    if re.match(reg, each):
                        # 1、信息提取
                        result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", each, re.DOTALL)
                        if result:
                            ext = result.groupdict().get("ext")
                            data = result.groupdict().get("data")
                        else:
                            raise Exception("Do not parse!")
                        # 2、base64解码
                        each = base64.urlsafe_b64decode(data)
                        #print (each)
                        filename = keyword + '_' + str(i) + '.jpg'
                        with open(filedir + filename, 'wb') as f:
                            f.write(each)
                    else:

                        pic = requests.get(each, timeout=10)
                        filename = keyword + '_' + str(i) + '.jpg'
                        # fp = open(filename, 'wb')
                        # fp.write(pic.content)
                        # fp.close()
                        with open(filedir + filename, 'wb') as f:
                            f.write(pic.content)
                except BaseException:
                    print('【错误】当前图片无法下载')
                    continue
                

                i += 1

                # #获得图片后缀
                # file_suffix = os.path.splitext(img_url)[1]
                # #拼接图片名（包含路径）
                # filename = '{}{}{}{}'.format(file_path,os.sep,file_name,file_suffix)
                # #下载图片，并保存到文件夹中
                # urllib.urlretrieve(img_url,filename=filename)

if __name__ == '__main__':
    #word = input("Input key word: ")
    #url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&ct=201326592&v=flip'
    keyword = str(round(time.time() * 1000))
    #url = input("url：")
    url="https://csdn.net/"
    header = {  # 模拟浏览器头部信息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    
    option = webdriver.ChromeOptions()
    # 不打开窗口 ， 静默模式
    option.add_argument('headless')
    # 防止打印一些无用的日志
    option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    driver = webdriver.Chrome(chrome_options=option)

 #   driver.implicitly_wait(10)  # 隐性等待和显性等待可以同时用，但要注意：等待的最长时间取两者之中的大者
    driver.get(url)
    
    sleep(3)  # 强制等待3秒再执行下一步

    dowmloadPic(driver.page_source, keyword)
    driver.quit()