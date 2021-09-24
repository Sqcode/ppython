from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import traceback
import time
import random, sys
# driver = webdriver.Firefox()
# # 浏览器最大化
# driver.maximize_window()
# # 打开注册页面
# driver.get('https://reg.taobao.com/member/reg/fill_mobile.htm')

# navigator.appVersion
def selenium_get_html(url="http://m.maoyan.com/mmdb/comments/movie/341516.json?_v_=yes&offset=1"):
    # url = "http://m.maoyan.com/mmdb/comments/movie/341516.json?_v_=yes&offset=1"
    option = webdriver.ChromeOptions()
    # 不打开窗口 ， 静默模式
    # option.add_argument('headless')
    # 禁用js
    # prefs = {
    #     'profile.default_content_setting_values': {
    #         'images': 2,
    #         'javascript':2
    #     }
    # }
    # option.add_experimental_option('prefs', prefs)
    # 防止打印一些无用的日志
    option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    driver = webdriver.Chrome(chrome_options=option)
    # driver.set_window_size(200,200)
    # driver.maximize_window()

    driver.get(url)

    locator = (By.ID, 'yodaMoveingBar')
    try:
        a = WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located(locator))
        time.sleep(1)
        # 发现滑块
        yodaBox = driver.find_element_by_id("yodaBox")
        # print(yodaBox.size)
        # 滑块区域
        source = driver.find_element_by_id("yodaBoxWrapper")
        # print(source.size, source.size["width"], type(source.size["width"]))

        ActionChains(driver).drag_and_drop_by_offset(yodaBox, source.size["width"], source.size["height"]).perform()
        # 将长度分成3分 拖拽
        # width = source.size["width"] / 3
        # # 拖拽滑块，从左侧拖拽到右侧
        # for i in range(1, 4):
        #     ActionChains(driver).drag_and_drop_by_offset(yodaBox, width*i, source.size["height"]).perform()
    except TimeoutException as e :
        print('等待超时...')
        sys.exit(1)
    except BaseException as e:
        print ('repr(e):\t')
        #以下两步都是输出错误的具体位置的
        traceback.print_exc()
        print ('traceback.format_exc():\n%s' % traceback.format_exc())
    finally: 
        time.sleep(12)
        driver.quit()
        return print(driver.current_url)   # current_url 方法可以得到当前页面的URL

if __name__ =='__main__':
    url = 'http://m.maoyan.com/mmdb/comments/movie/1263235.json?_v_=yes&offset=1'
    # 验证滑块
    a = selenium_get_html(url)
    print(a)

    # https://verify.meituan.com/v2/web/general_page?action=spiderindefence&requestCode=634671d53328468baf84568ef214b43e&platform=1000&adaptor=auto&succCallbackUrl=https%3A%2F%2Foptimus-mtsi.meituan.com%2Foptimus%2FverifyResult%3ForiginUrl%3Dhttp%253A%252F%252Fm.maoyan.com%252Fmmdb%252Fcomments%252Fmovie%252F1263235.json%253F_v_%253Dyes%2526offset%253D1