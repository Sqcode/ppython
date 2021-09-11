from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import traceback
import time
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
    # 防止打印一些无用的日志
    option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    driver = webdriver.Chrome(chrome_options=option)
    # driver.set_window_size(200,200)
    # driver.maximize_window()

    driver.get(url)

    locator = (By.ID, 'yodaMoveingBar')
    try:
        a = WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located(locator))

        # yodaMoveingBar = driver.find_element_by_id("yodaMoveingBar")
        # print(yodaMoveingBar.size)
        #driver.find_element_by_id("yodaBox")

        # 发现滑块
        yodaBox = driver.find_element_by_id("yodaBox")
        # print(yodaBox.size)
        # 滑块区域
        source = driver.find_element_by_id("yodaBoxWrapper")
        # print(source.size)
        # 拖拽滑块，从左侧拖拽到右侧
        ActionChains(driver).drag_and_drop_by_offset(yodaBox, source.size["width"], source.size["height"]).perform()
        
    except BaseException as e:
        print ('repr(e):\t')
        #以下两步都是输出错误的具体位置的
        traceback.print_exc()
        print ('traceback.format_exc():\n%s' % traceback.format_exc())
    finally: 
        time.sleep(2)
        driver.quit()

if __name__ =='__main__':
    url = 'http://m.maoyan.com/mmdb/comments/movie/1263235.json?_v_=yes&offset=1'
    # 验证滑块
    selenium_get_html(url)