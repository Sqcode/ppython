import sys, os
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '../')))
# print(__dir__, sys.path)
from util import get_html, check_ip_port, check_proxy
from lxml import etree

def ip66():
    url = "http://www.66ip.cn/1.html"
    text = get_html(url)
    ip_xpath = '//table/tr[position()>1]/td[1]/text()'
    port_xpath = '//table/tr[position()>1]/td[2]/text()'
    ret = format_html(text, ip_xpath, port_xpath)
    print(ret)

def ip3366():
    url = "https://proxy.ip3366.net/free/?action=china&page=1"
    text = get_html(url)
    ip_xpath = '//td[@data-title="IP"]/text()'
    port_xpath = '//td[@data-title="PORT"]/text()'
    ret = format_html(text, ip_xpath, port_xpath)
    print(ret)

def ip_huan():
    url = "https://ip.ihuan.me/?page=b97827cc"
    text = get_html(url)
    ip_xpath = '//tbody/tr/td[1]/a/text()'
    port_xpath = '//tbody/tr/td[2]/text()'
    ret = format_html(text, ip_xpath, port_xpath)
    print(ret)

def ip_kuai():
    url = "https://www.kuaidaili.com/free/inha/2/"
    text = get_html(url)
    ip_xpath = '//td[@data-title="IP"]/text()'
    port_xpath = '//td[@data-title="PORT"]/text()'
    ret = format_html(text, ip_xpath, port_xpath)
    print(ret)

def ip_jiangxi():
    url = "https://ip.jiangxianli.com/?page=1"
    text = get_html(url)
    ip_xpath = '//tbody/tr[position()!=7]/td[1]/text()'
    port_xpath = '//tbody/tr[position()!=7]/td[2]/text()'
    ret = format_html(text, ip_xpath, port_xpath)
    print(ret)

def ip_kaixin():
    url = "http://www.kxdaili.com/dailiip/1/1.html"
    text = get_html(url)
    ip_xpath = '//tbody/tr/td[1]/text()'
    port_xpath = '//tbody/tr/td[2]/text()'
    ret = format_html(text, ip_xpath, port_xpath)
    print(ret)

def ip_nima():
    url = "http://www.nimadaili.com/putong/1/"
    text = get_html(url)
    ip_xpath = '//tbody/tr/td[1]/text()'
    ret = format_html_ext(text, ip_xpath)
    print(ret)

# 扩展HTML解析函数
def format_html_ext(text, ip_xpath):
    # 待返回的IP与端口列表
    ret = []
    html = etree.HTML(text)
    ips = html.xpath(ip_xpath)
    print(ips)
    for ip in ips:

        item_dict = {
            "ip": ip.split(":")[0],
            "port": ip.split(":")[1]
        }
        ret.append(item_dict)

    return ret

# 代理IP网站源码获取部分
def ip89():
    url = "https://www.89ip.cn/index_1.html"
    text = get_html(url)
    ip_xpath = '//tbody/tr/td[1]/text()'
    port_xpath = '//tbody/tr/td[2]/text()'
    ret = format_html(text, ip_xpath, port_xpath)
    return ret

# HTML解析部分
def format_html(text, ip_xpath, port_xpath):
    # 待返回的IP与端口列表
    ret = []
    html = etree.HTML(text)
    ips = html.xpath(ip_xpath)
    ports = html.xpath(port_xpath)
    # 测试，正式运行删除本部分代码
    # print(ips,ports)
    ip_port = zip(ips, ports)
    for ip, port in ip_port:
        item_dict = {
            "ip": ip.strip(), # 防止出现 \n \t 等空格类字符
            "port": port.strip()
        }
        ret.append(item_dict)

    return ret

if __name__ == '__main__':

    print(1)
    # ip_port = ip89()
    # print(ip_port)
    # check_proxy(ip_port)

    # n = int(input())
    #     # print(n)
    #     for i in range(n):
    #         s = int(input())
    #         print(f"s= {s}")

