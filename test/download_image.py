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

# 创建图片文件夹
def mkdir(path):
	if len(path) == 0 :
		path = './images/' + str(round(time.time() * 1000)) + '/'
	folder = os.path.exists(path)
	if not folder:                   # if not , then created
		os.makedirs(path)            # makedirs
		print ("---  new folder...  ---", path)
	#else:
		#print ("---  There is this folder!  ---")
	return path

# 检查是否为图片类型
def check_image(content_type):
    # Content-Type: image/jpeg
    if 'image' in content_type:
        return True
    else:
        return False

# 下载图片，imgUrl图片连接、name保存的名称、保存的图片路径
def downloadImage(imgUrl, name, path):
    # create image target file
    # mkdir(str(path))
    # filename
    filename = str(name) + '.jpg'

    print('下载图片:' + str(imgUrl))
    try:
        # 是否是base64的图片
        reg = re.compile('.*(base64).*')
        if re.match(reg, imgUrl):
            # 1、信息提取
            result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", imgUrl, re.DOTALL)
            if result:
                ext = result.groupdict().get("ext")
                data = result.groupdict().get("data")
            else:
                raise Exception("Do not parse!")
            # 2、base64解码
            imgUrl = base64.urlsafe_b64decode(data)
            with open(path + filename, 'wb') as f:
                f.write(imgUrl)
        else:
            img_file = requests.get(imgUrl, timeout=10)
            if check_image(img_file.headers['Content-Type']):
                with open(path + filename, 'wb') as f:
                    f.write(img_file.content)
            else:
                print ('{}, 不是image格式'.format(imgUrl))
    except BaseException:
        print('【错误】当前图片无法下载')
        driver.quit()

    
def dowmloadPic(html, keyword):
    #list = re.findall('<img.+?src=\"(.*?)\"\s+alt="(.*?)"', html, re.S)
    list = driver.find_elements_by_tag_name('img')
    if 'baidu' in url:
        list = re.findall('"objURL":"(.*?)",', html, re.S)
    
    #print (list)
    #for item in list:
    #    print (item.get_attribute('src'))
    if len(list) > 0:
        filedir = './images/' + str(round(time.time() * 1000)) + '/'
        mkdir(str(filedir))
        i = 1
        for item in list:
            print('准备下载第' + str(i) + '张图片')

            if 'baidu' in url:
                reg = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
                if re.match(reg, url):
                    downloadImage(item, keyword + str(i), filedir)
            else:
                try:
                    imgUrl = item.get_attribute('src')
                    # 相对路径
                    if 'http' not in imgUrl:
                        print (imgUrl)
                        # 绝对路径
                        imgUrl = url + imgUrl
                        
                    if item.get_attribute('alt'):
                        name = item.get_attribute('alt')
                    else:
                        name = i
                    #print (name, imgUrl)
                    
                    downloadImage(imgUrl, name, filedir)
                    
                except BaseException as e:
                    print(e)
                    continue
            i += 1
        

if __name__ == '__main__':
    
    url="http://2t6y.mydown.com/yuanqidesktop/tianji.html?softid=585&tid1=133&tid2=1001&tod1=6855"
    url="https://desk.zol.com.cn/"
    url="http://www.jj20.com/bz/nxxz/shxz/329474.html"
    url="http://www.jj20.com/bz/ktmh/dmrw/324467_2.html"

    keyword = input("Input key word: ")
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + keyword + '&ct=201326592&v=flip'

    header = {  # 模拟浏览器头部信息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    
    option = webdriver.ChromeOptions()
    # 不打开窗口 ， 静默模式
    option.add_argument('headless')
    # 防止打印一些无用的日志
    option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    driver = webdriver.Chrome(chrome_options=option)
    # driver.implicitly_wait(10)  # 隐性等待和显性等待可以同时用，但要注意：等待的最长时间取两者之中的大者
    driver.get(url)
    
    sleep(3)  # 强制等待3秒再执行下一步
    dowmloadPic(driver.page_source, keyword)
    driver.quit()