import os, time, requests, random, telnetlib, json, pypinyin, cv2
from re import M
from bs4 import BeautifulSoup
from email.mime.text import MIMEText   # 定义邮件内容
from email.header import Header # 定义邮件标题
import smtplib
import numpy as np
import matplotlib.pylab as plt
__dir__ = os.path.dirname(os.path.abspath(__file__))
# print(__dir__)
from exp import MyException
import logging
logging.basicConfig(filename = "out.txt",level=logging.DEBUG,format= "%(asctime)s %(levelname)s -- %(message)s",encoding='utf-8')

# 获取请求头
def get_headers(localhost=True, refer="https://www.baidu.com", host=None, cookie=None):
	ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
	if not localhost:
		uas = [
			"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
			"Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
			"Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)",
			"Baiduspider-image+(+http://www.baidu.com/search/spider.htm)",
			"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
			"Mozilla/5.0 (compatible; Googlebot-Image/1.0; +http://www.google.com/bot.html)",
			"Sogou web spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)",
			"Sogou News Spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)",
			"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);",
			"Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
			"Sosospider+(+http://help.soso.com/webspider.htm)",
			"Mozilla/5.0 (compatible; Yahoo! Slurp China; http://misc.yahoo.com.cn/help.html)"
		]
		ua = random.choice(uas)
	headers = {
		"User-Agent": ua,
		"Referer": refer,
		"Host": host,
		"cookie": cookie
	}
	return headers

# 获取html
def get_html(url, ret_type="text", timeout=50, encoding="utf-8", cookie=None):
	headers = get_headers(cookie=cookie)
	res = requests.get(url, headers=headers, timeout=timeout)
	res.encoding = encoding
	# print(res.status_code)
	# print(res.text)
	if ret_type == "text":
		return res.text
	elif ret_type == "image":
		return res.content
	elif ret_type == "json":
		return res.json()

# 创建文件夹
def mkdir(path=os.path.join(__dir__, '../images/%s'%str(round(time.time() * 1000)) + '/')):
	"""
	新建图片文件夹
	:param path: The file path - 文件路径 
	"""
	ext = os.path.exists(path)
	#判断是否存在文件夹如果不存在则创建为文件夹
	if not ext:
		os.makedirs(path)
		print ("---  new folder...  ---", path)
	#else:
		#print ("---  There is this folder!  ---")
	return '%s/'%path

def download_img(src, filename=str(round(time.time() * 1000)), filedir=os.path.join(__dir__, '../images/'), domain=None):
	"""
	图片下载
	:param src: The image http url - 图片链接
	:param filename: file name - 名称。默认当前时间戳
	:param filedir: file saved dir - 保存目录。默认当前文件，文件夹images
	:param domain: website domain - 图片前缀域名
	"""
	if domain is not None:
		src = domain + src
	pic = requests.get(src, timeout=20)
	# 去掉链接后面的参数
	src = src.split('?')[0]

	filepath = filedir + filename + src[-4:]
	if pic.status_code == 200:
		with open(filepath, 'wb') as f:
			f.write(pic.content)

	return filepath

# 代理检测函数
def check_ip_port(ip_port):
    for item in ip_port:
        ip = item["ip"]
        port = item["port"]
        try:
            tn = telnetlib.Telnet(ip, port=port, timeout=2)
        except:
            print('[-] ip:{}:{}'.format(ip, port))
        else:
            print('[+] ip:{}:{}'.format(ip, port))
            with open('ipporxy.txt','a') as f:
                f.write(ip+':'+port+'\n')
    print("阶段性检测完毕")

# 代理检测函数
def check_proxy(ip_port):
	for item in ip_port:
		ip = item["ip"]
		port = item["port"]
		url = 'https://api.ipify.org/?format=json'
		proxies= {
			"http":"http://{}:{}".format(ip, port),
			"https":"https://{}:{}".format(ip, port),
		}
		try:
			res = requests.get(url, proxies=proxies, timeout=3).json()
			print(res)
			if 'ip' in res:
				print(res['ip'])
		except Exception as e:
			print(e)

# 获取当前项目根路径
class JarProjectPath:
    @staticmethod
    def project_root_path(project_name=None):
        """
        获取当前项目根路径
        :param project_name:
        :return: 根路径
        """
        PROJECT_NAME = 'py' if project_name is None else project_name
        project_path = os.path.abspath(os.path.dirname(__file__))
        root_path = project_path[:project_path.find("{}\\".format(PROJECT_NAME)) + len("{}\\".format(PROJECT_NAME))]
        # print('当前项目名称：{}\r\n当前项目根路径：{}'.format(PROJECT_NAME, root_path))
        return root_path

# 装饰器，函数运行时间
def run_time(func):
    # 这里的 wrapper 函数名可以为任意名称
    def wrapper(*args):
        s_time = time.perf_counter()
        res = func(*args)
        e_time = time.perf_counter()
        print(f"func --- {func.__name__}, runtime --- {e_time-s_time}")
        return res
    return wrapper

# 不带声调的(style=pypinyin.NORMAL)
def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s

# 带声调的(默认)
def yinjie(word):
    s = ''
    # heteronym=True开启多音字
    for i in pypinyin.pinyin(word, heteronym=True):
        s = s + ''.join(i) + " "
    return s

# 发送邮件，QQ
def send_email(data, receivers, server='@qq.com', sender='627758338'):
	"""
	:param :data 要发送的内容
	:param :receivers 接受人数组
	 example - wb_send_email_param(['570300991'])
	"""
	rq = time.strftime("%Y-%m-%d %H:%M:%S") # 发送时间
	from_addr = sender + server # 发送的邮箱
	# smtpserver="smtp.163.com" # 发送邮箱SMTP服务器地址
	smtpserver = "smtp.qq.com" # 发送邮箱SMTP服务器地址
	# password = "hbmfmxtfezekbcfa"# 密码，填写自己的密码即可，163邮箱和网页登录的邮箱不同
	password = "qaerbqssfcfpbebb"# 密码，填写自己的密码即可，163邮箱和网页登录的邮箱不同
	# 接收邮箱的账号
	# to_addr = receiver + server
	to_addrs = []
	for rv in receivers:
		receiver = rv + server
		print(receiver)
		to_addrs.append(receiver)

	# 邮件的标题
	subject = f"{rq} 微博热搜"
	# 发送内容
	if data:
		msg = MIMEText(data, 'html', 'utf-8') # 邮件的正文
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
	else:
		print('未获取到内容')

def plt_show(images, titles):
    for i in range(len(images)):
        plt.subplot(3, 3, i+1)
        # print(isinstance(titles[i], list))
        if isinstance(titles[i], list):
            # print(titles[i][1])
            if titles[i][1]:
                b, g, r = cv2.split(images[i])
                srcImage_new = cv2.merge([r, g, b])
                plt.imshow(srcImage_new)
        else:
            plt.imshow(images[i], 'gray')
        plt.title(titles[i] if titles[i] else i)
        plt.xticks([])
        plt.yticks([])

    plt.show()

def file_exist(filepath):
	if not os.path.exists(filepath):
		raise MyException('文件不存在')
	return True

# 如果有提供原始路径，则最后文件保存至原路径目录下。若无，则项目根目录的files下。
def get_save_path(filename=None, origin_filepath=None, suffix=None, file_prefix='', path=None):
	"""
	:param filename:	传入文件问，直接拼接项目根目录+文件名
	:param origin_filepath:	原文件路径
	:param suffix	即将要保存为的文件格式后缀
	:param file_prefix:	保存的文件前缀
	:param path:	文件保存的根路径
	"""
	# 是否传入 存储的根路径。默认项目根
	if path is None:
		path = f"{JarProjectPath.project_root_path()}/files"

	# 是否直接指定文件名
	if filename is not None:
		file = f"{path}/{filename}"
	else:
		# 通过原始文件名，文件保存至该同级目录
		if origin_filepath is not None:
			path, file = os.path.split(origin_filepath)[:2]
			# print(os.path.split(origin_filepath), path,'---------', file)
			spx = file.split('.')
			# print(spx)
			# suffix = suffix if suffix else '.%s'%spx[1]
			file = f"{path}/{spx[0]}_{str(round(time.time() * 1000))}{suffix if suffix else '.%s'%spx[1]}"
		else:
			# 没有原始文件名，则传入要保存的后缀
			if suffix is None:
				raise MyException('文件后缀不能为空，请传入要保存为的文件后缀格式suffix=（.***）')
			file = f"{path}/{'%s'%file_prefix if file_prefix else ''}_{str(round(time.time() * 1000))}{suffix}"
	
	logging.info('文件保存至>%s'%file)
	return file

if __name__ == "__main__":
	path6 = 'C:/Users/dyjx/Desktop/py/images/1629353489174/sf_3.png'
	# print(get_save_path(suffix='.jpg', file_prefix='1111'))
	url = 'https://img-blog.csdnimg.cn/20211003092556847.png?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBA5oiR5pivc3ByaW5nbWVuZw==,size_13,color_FFFFFF,t_70,g_se,x_16'
	download_img(url, str(1), r'c:\Users\dyjx\Desktop\py\111')


	# print(url.split('?')[0])
	# print(JarProjectPath.project_root_path())
	# print(file_exist(r'static/logo.png'))
	# video_mask(r'static/dcf.mp4')
	# video_to_gif(r'static/dcf.mp4')
	# send_email('1111', ['570300991'])
	# print(pinyin('怒火·重案'))
	# print(5 + float(random.randint(1,100)) /20)

	# html = get_html('http://www.netbian.com/mei/index.htm', encoding='gbk')
	# soup = BeautifulSoup(html, 'html.parser')
	# print(soup.select('title'), soup.select('title')[0].text)
	# title = soup.select('title')[0].text
	# print('美女' in title, title.find('美女'))

	# print(html.find('doctype'))
	# print(html[0,2])
	# start = html.find('<title>')
	# end = html.find('</title>')
	# print(type(start), start, type(end), end)
	# print(html[start, end])
	# print(type(html.title))
	#check_ip_port([{'ip': '202.109.157.60', 'port': '9000'}])
	#check_ip_port([{'ip': '192.168.179.129', 'port': '52856'}])
	# check_proxy([{'ip': '192.168.17.131', 'port': '8989'}])
	#check_proxy([{'ip': '222.74.202.231', 'port': '8080'}])
	# 222.74.202.231:8080
	# get_html('http://www.netbian.com/mei/index.htm', encoding='gbk')
	# mkdir()
	#str = 'url("https://cn.bing.com/th?id=OHR.Heliodoxa_ZH-CN9872355419_1920x1080.jpg&rf=LaDigue_1920x1080.jpg&pid=hp")'
	#print (str[5:-2], str[-4:])