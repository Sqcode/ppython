import os, time, requests, random, telnetlib

def get_headers(localhost=True, refer="https://www.baidu.com", host=None):

	ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
	if not localhost:
		uas = [
			"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
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
		"Host": host
	}
	return headers

def get_html(url, ret_type="text", timeout=50, encoding="utf-8"):
	headers = get_headers()
	res = requests.get(url, headers=headers, timeout=timeout)
	res.encoding = encoding
	# print(res.text)
	if ret_type == "text":
		return res.text
	elif ret_type == "image":
		return res.content
	elif ret_type == "json":
		return res.json()

# 创建图片文件夹
def mkdir(path='./images/' + str(round(time.time() * 1000)) + '/'):
	"""
	新建图片文件夹
	:param:path The file path - 文件路径 
	"""
	folder = os.path.exists(path)
	if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
		print ("---  new folder...  ---", path)
	#else:
		#print ("---  There is this folder!  ---")
	return path

def download_img(src, filename=str(round(time.time() * 1000)), filedir='./images/', domain=None):
	"""
	图片下载
	:param:src The image http url - 图片链接
	:param:filename file name - 名称。默认当前时间戳
	:param:filedir file saved dir - 保存目录。默认当前文件，文件夹images
	:param:domain website domain - 图片前缀域名
	"""
	if domain is not None:
		src = domain + src
	pic = requests.get(src, timeout=20)
	if pic.status_code == 200:
		with open(filedir + filename + src[-4:], 'wb') as f:
			f.write(pic.content)

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

if __name__ == "__main__":
	#check_ip_port([{'ip': '202.109.157.60', 'port': '9000'}])
	#check_ip_port([{'ip': '192.168.179.129', 'port': '52856'}])
	# check_proxy([{'ip': '192.168.17.131', 'port': '8989'}])
	check_proxy([{'ip': '222.74.202.231', 'port': '8080'}])
	# 222.74.202.231:8080
	# get_html('http://www.netbian.com/mei/index.htm', encoding='gbk')
	#mkdir(")
	#str = 'url("https://cn.bing.com/th?id=OHR.Heliodoxa_ZH-CN9872355419_1920x1080.jpg&rf=LaDigue_1920x1080.jpg&pid=hp")'
	#print (str[5:-2], str[-4:])