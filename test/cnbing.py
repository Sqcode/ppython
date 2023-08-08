import sys, os
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '../common')))
# sys.path.append(os.path.abspath(os.path.join(__dir__, './common'))) # 打包，放当前目录
# print(__dir__)
from util import mkdir
import requests
import traceback
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import os
import time
from bs4 import BeautifulSoup
# coding:utf-8
from PIL import Image

import logging
logging.basicConfig(filename = "out.txt",level=logging.DEBUG,format= "%(asctime)s %(levelname)s -- %(message)s")

desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
print(desktop_path)

# 微软bing的背景图片

url = "https://cn.bing.com/"

option = webdriver.ChromeOptions()
# 不打开窗口 ， 静默模式
# option.add_argument('--headless')
option.headless = True

# 防止打印一些无用的日志
option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
driver = webdriver.Chrome(chrome_options=option)
#driver.set_window_size(200,200)
driver.get(url)
# driver.implicitly_wait(3) # 智能等待3秒

locator = (By.CLASS_NAME, 'img_cont')
img = ""
try:
    # The presence_of_element_located condition is fulfilled when the element is just created, still not fully rendered. Accessing element in this early phase often causes to ElementNotInteractableException as you facing.
    wd = WebDriverWait(driver, 20, 0.5)
    wd.until(EC.visibility_of_element_located(locator))
    # a = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(locator))
    #print ("WebDriverWait", a)
    

    filedir = mkdir(desktop_path + '/' + str(round(time.time() * 1000)))
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

        # title = driver.find_element_by_class_name('title default_pointer_cs')
        title = driver.find_elements_by_css_selector(".mc_caro .musCard .musCardCont .title")
        # title = driver.find_element_by_id('headline')
#vs_cont > div.mc_caro.default_cursor_cs > div.musCard.default_cursor_cs.focusin > div.musCardCont.default_cursor_cs > h3 > a
        title_text = title[0].text

        print (title_text, imgUrl)
        logging.debug(title_text, imgUrl)

        # print (title., imgUrl)
        filename = title_text + ".webp"
        file_url = filedir + filename
        if title_text: 
            pic = requests.get(imgUrl, timeout=10)
            if pic.status_code == 200 and img != imgUrl:
                with open(file_url, 'wb') as f:
                    f.write(pic.content)
                time.sleep(1)
                # 保存成功后，转一下jpg
                im = Image.open(file_url)
                if im.mode == "RGBA":
                    im.load()  # required for png.split()
                    background = Image.new("RGB", im.size, (255, 255, 255))
                    background.paste(im, mask=im.split()[3])
                save_name = file_url.replace('webp', 'jpg')
                # 此处会保存到源filename路径下
                im.save('{}'.format(save_name), 'JPEG')
                    
            
        #sh_igr 下一个，sh_igl 上一个
        #driver.find_element_by_id('sh_igl').click() #下一页
        wd.until(EC.visibility_of_element_located((By.ID, "leftNav")))

        sh_igl = driver.find_element_by_id('leftNav') #上一页
        ActionChains(driver).click(sh_igl).perform()

        # 第一次等待久一点
        if i == 0:
            time.sleep(3)
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