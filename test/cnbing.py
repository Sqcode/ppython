import sys, os
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '../common')))
# print(__dir__)
from util import mkdir

import requests
import traceback
import selenium
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import re
import os
import time
from bs4 import BeautifulSoup


# 微软bing的背景图片

url = "https://cn.bing.com/"

option = webdriver.ChromeOptions()
# 不打开窗口 ， 静默模式
# option.add_argument('headless')
# 防止打印一些无用的日志
option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
driver = webdriver.Chrome(chrome_options=option)
#driver.set_window_size(200,200)

driver.get(url)


locator = (By.CLASS_NAME, 'img_cont')
img = ""

try:
    a = WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located(locator))
    #print ("WebDriverWait", a)
    filedir = mkdir()
    for i in range(8):
        #/th?id=OHR.Heliodoxa_ZH-CN9872355419_UHD.jpg&rf=LaDigue_UHD.jpg&pid=hp&w=1920&h=1080&rs=1&c=4
        # 可以去更改w,h
        #imgs =  re.findall('data-ultra-definition-src="(.*?)"', driver.page_source)

        # bgDiv = driver.find_element_by_id('bgDiv')
        bgDiv = driver.find_element_by_class_name('img_cont')
        #print (bgDiv.get_attribute("style"))
        #print (bgDiv.value_of_css_property('background-image'))
        imgUrl = bgDiv.value_of_css_property('background-image')[5:-2]
        # title = driver.find_element_by_id('sh_cp').get_attribute("title").split("(")[0]

        title = driver.find_element_by_class_name('title')
        print (title.text, imgUrl)
        
        filename = title.text + ".jpg"
            
        pic = requests.get(imgUrl, timeout=10)

        if pic.status_code == 200:
            if img != imgUrl:
                with open(filedir + filename, 'wb') as f:
                    f.write(pic.content)
            
        #sh_igr 下一个，sh_igl 上一个
        #driver.find_element_by_id('sh_igl').click() #下一页
        sh_igl = driver.find_element_by_id('leftNav') #上一页
        ActionChains(driver).click(sh_igl).perform()

        # 第一次等待久一点
        if i == 0:
            time.sleep(2)
            ActionChains(driver).click(sh_igl).perform()
        else:
            time.sleep(1)
except BaseException as e:
    print ('repr(e):\t')
    #以下两步都是输出错误的具体位置的
    traceback.print_exc()
    print ('traceback.format_exc():\n%s' % traceback.format_exc())
finally: 
    driver.quit()
#if __name__ == "__main__":
    #print (1)