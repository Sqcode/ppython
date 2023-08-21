import sys, os
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '../common')))
import util
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText   # 定义邮件内容
from email.header import Header # 定义邮件标题
import smtplib
from email.mime.multipart import MIMEMultipart

import time
import datetime
from threading import Timer
import sys
from apscheduler.schedulers.blocking import BlockingScheduler
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import traceback
"""
1：循环+sleep方式适合简答测试，
2：timer可以实现定时任务，但是对定点任务来说，需要检查当前时间点；
3：schedule可以定点定时执行，但是需要在循环中检测任务，而且存在阻塞；
4：APScheduler框架更加强大，可以直接在里面添加定点与定时任务；
"""
def get_html():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'",
        "Referer": "https://www.baidu.com"
    }
    
    res = requests.get("https://s.weibo.com/top/summary?cate=realtimehot", headers=util.get_headers(localhost=False))
    print(res.text)
    # return analysis_html(res.text)

def analysis_html(html):
    soup = BeautifulSoup(html, 'lxml')
    data = soup.find(name="tbody")
    send_msgs = []
    print(data)
    if data:
        items = data.find_all(name='tr')  # 过滤到全部数据
        for item in items:
            top = item.find(attrs={"class": "td-01"}).text  # 排序
            if top == "":
                top = '置顶'
            content = item.find(attrs={"class": "td-02"})

            url = 'https://s.weibo.com/' + content.find('a')['href']
            # print(url)

            title_content = content.contents
            title = "" # 获取标题
            readers = ""
            if len(title_content) > 3:
                title = title_content[1].text
                readers = title_content[3].text
            else:
                title = title_content[1].text
                readers = "0"
            level = item.find(attrs={"class": "td-03"}).text  # 热度标签
            send_msgs.append ((top,url,title,readers,level))
        # print(send_msgs)
    return send_msgs

def selenium_get_html():
    url = "https://s.weibo.com/top/summary?cate=realtimehot"
    option = webdriver.ChromeOptions()
    # 不打开窗口 ， 静默模式
    # option.add_argument('--headless')
    option.headless = True

    # 防止打印一些无用的日志
    option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    driver = webdriver.Chrome(chrome_options=option)
    #driver.set_window_size(200,200)
    driver.get(url)
    driver.implicitly_wait(3) # 智能等待3秒

    locator = (By.CLASS_NAME, 'wbs-hotrank')

    try:
        # The presence_of_element_located condition is fulfilled when the element is just created, still not fully rendered. Accessing element in this early phase often causes to ElementNotInteractableException as you facing.
        wd = WebDriverWait(driver, 20, 0.5)
        wd.until(EC.visibility_of_element_located(locator))

        return analysis_html(driver.page_source)

    except BaseException as e:
        print ('repr(e):\t')
        #以下两步都是输出错误的具体位置的
        traceback.print_exc()
        print ('traceback.format_exc():\n%s' % traceback.format_exc())
    finally: 
        driver.quit()

def wb_send_email_param(server, sender, receivers):
    rq = time.strftime("%Y-%m-%d %H:%M:%S") # 发送时间
    from_addr = sender + server # 发送的邮箱
    # smtpserver="smtp.163.com" # 发送邮箱SMTP服务器地址
    smtpserver = "smtp.qq.com" # 发送邮箱SMTP服务器地址
    # password = "hbmfmxtfezekbcfa"# 密码，填写自己的密码即可，163邮箱和网页登录的邮箱不同
    password = "qaerbqssfcfpbebb"# 密码，填写自己的密码即可，163邮箱和网页登录的邮箱不同
    # 接收邮箱的账号
    # to_addr = receiver + server
    to_addrs = [from_addr]
    for rv in receivers:
        receiver = rv + server
        print(receiver)
        to_addrs.append(receiver)
    
    # 邮件的标题
    subject = f"{rq} 微博热搜"
    # 邮件html内容，需要把热搜的爬取到的数据进行格式化
    # data = get_html()
    data = selenium_get_html()

    if data:
        print("获取内容...", len(data))
        table = "<table>"
        for item in data:
            # table += f"<tr><td><font size='1' color='#f26d5f'>{item[0]}</font>:<a href='{item[1]}'><font size='2'>{item[2]}</font></a>---{item[3]}【{item[4]}】</td></tr>"
            str = ''
            if item[3]:
                str = f"---{item[3]}"
            if item[4]:
                str = f"---{item[3]}【{item[4]}】"
            # print(item[0], item[1], item[2], item[3], item[4], str)
            tr = ("<tr><td><font size='2' color='#f26d5f'>" + item[0]
            +"</font>:<a href='" + item[1] + "'><font size='3'>" + item[2] + "</font></a>" + str +"</td></tr>")
            
            table += tr
        table += "</table>"
        # print(table)
        content = table

        util.send_email(subject, content, receivers)
    else:
        print('未获取到内容')



def wb_send_email():
    server = '@qq.com'
    sender = '627758338'
    # , '367269243'
    receivers = ['570300991']

    rq = time.strftime("%Y-%m-%d %H:%M:%S") # 发送时间
    from_addr = sender + server # 发送的邮箱
    # smtpserver="smtp.163.com" # 发送邮箱SMTP服务器地址
    smtpserver = "smtp.qq.com" # 发送邮箱SMTP服务器地址
    # password = "hbmfmxtfezekbcfa"# 密码，填写自己的密码即可，163邮箱和网页登录的邮箱不同
    password = "qaerbqssfcfpbebb"# 密码，填写自己的密码即可，163邮箱和网页登录的邮箱不同
    # 接收邮箱的账号
    # to_addr = receiver + server
    to_addrs = [from_addr]
    for rv in receivers:
        receiver = rv + server
        print(receiver)
        to_addrs.append(receiver)
    
    # 邮件的标题
    subject = f"{rq} 微博热搜"
    # 邮件html内容，需要把热搜的爬取到的数据进行格式化
    data = get_html()
    print("获取内容...", len(data))
    table = "<table>"
    for item in data:
        # table += f"<tr><td>{item[0]}:<a href='{item[1]}'>{item[2]}</a>---{item[3]}【{item[4]}】</td></tr>"
        str = ''
        if item[3]:
            str = f"---{item[3]}"
        if item[4]:
            str = f"---{item[3]}【{item[4]}】"
        # print(item[0], item[1], item[2], item[3], item[4], str)
        tr = ("<tr><td><font size='2' color='#f26d5f'>" + item[0]
        +"</font>:<a href='" + item[1] + "'><font size='3'>" + item[2] + "</font></a>" + str +"</td></tr>")
        
        table += tr
    table += "</table>"
    # print(table)
    content = table
    msg = MIMEText(content, 'html', 'utf-8') # 邮件的正文
    msg['Subject'] = Header(subject, 'utf-8') # 邮件的标题
    msg['From'] = from_addr # 邮件发送方
    # msg['To'] = to_addr # 邮件接收方，发送给一人
    msg['To']=','.join(to_addrs)# 邮件接收方，发送给多人

    smtp = smtplib.SMTP_SSL(smtpserver, 465)# SSL协议端口号要使用465
    smtp.helo(smtpserver) # helo向邮箱标识用户身份
    smtp.ehlo(smtpserver) # 服务器返回结果确认
    smtp.login(from_addr, password)# 登录邮箱服务器，输入自己的账号和密码

    print("发送中...")
    smtp.sendmail(from_addr, to_addrs, msg.as_string())# 邮件发送多人
    # smtp.sendmail(from_addr, to_addr, msg.as_string())# 发送给个人的邮件
    smtp.quit()
    print("发送完毕")

def func():
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    print('do func  time :',ts)

def func2():
    #耗时2S
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    print('do func2 time：',ts)
    time.sleep(2)

def clearJobs():
    print(scheduler.get_jobs())
    scheduler.remove_job(func_name)
    # print(scheduler.get_jobs())
    if len(scheduler.get_jobs()) == 0:
        scheduler.shutdown()

def doScheduler(func, seconds, times):
    global scheduler, func_name
    func_name = func.__name__
    # 创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    
    # 清除
    sTimer = Timer(seconds * times + 2, clearJobs)
    sTimer.start()

    # 添加任务,时间间隔seconds
    scheduler.add_job(func, 'interval', seconds = seconds, id = func_name)
    # scheduler.add_job(getJobs(func_name), 'interval', seconds = 5, id = 'getJobs')
    scheduler.start()
    # print(func_name, scheduler.get_jobs())


if __name__ == '__main__':
    # selenium_get_html()
    # get_html() #'2770404149',
    # wb_send_email()
    #, '1070197073',  '1297932368','367269243', '445418932'
    # wb_send_email_param('@qq.com', '627758338', ['570300991', '367269243'])
    wb_send_email_param('@qq.com', '627758338', ['570300991'])
    # doScheduler(wb_send_email, 60, 2)

    # print(wb_send_email('@qq.com', '627758338', ['570300991', '367269243']).__name__)
    # funcName = sys._getframe().f_back.f_code.co_name #获取调用函数名
    # lineNumber = sys._getframe().f_back.f_lineno #获取行号
    # print(sys._getframe().f_code.co_name) # 获取当前函数名
    # sTimer = Timer(2, getJobs)
    # sTimer.start()
