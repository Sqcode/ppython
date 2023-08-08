import re,hashlib,requests,json, time
from requests.utils import dict_from_cookiejar
# from loguru import logger
appKey = '12574478'
def get_sign(ck, page, size, x):
    # 获取时间戳
    date = int(time.time() * 1000)
    # mm_110807073_1262350149_109959000489
    # data_s = '{"pNum": %s,"pSize": 2,"refpid":"mm_26632258_3504122_32538762",' % 1
    data_s = '{"pNum": %d,"pSize": %d,"refpid":"mm_26632258_3504122_32538762",' % (page, size)
    # data_tm = r'"variableMap":"{\"q\":\"手机\",\"navigator\":true,\"usertype\":\"1\",\"union_lens\":\"recoveryid:201_11.11.43.24_685807_1619341742886;prepvid:201_11.27.89.99_473565_1619342131641\",\"recoveryId\":\"201_11.186.139.24_536838_1619342621063\"}","qieId":"34374","spm":"a2e1u.19484427.29996460","app_pvid":"201_11.186.139.24_536838_1619342621063","ctm":"spm-url:a2e1u.19484427.filter.6;page_url:https%3A%2F%2Fai.taobao.com%2Fsearch%2Findex.htm%3Fkey%3D%25E4%25B8%25B8%25E7%25BE%258E%26pid%3Dmm_110807073_1262350149_109959000489%26union_lens%3Drecoveryid%253A201_11.11.43.24_685807_1619341742886%253Bprepvid%253A201_11.27.89.99_473565_1619342131641%26spm%3Da2e1u.19484427.filter.6%26usertype%3D1%26pnum%3D0"}'.replace('手机',x)
    data_tm = r'"variableMap":"{\"q\":\"手机\",\"navigator\":false,\"clk1\":\"25b8f4d10e5d19d5a1b4c05c0cda428b\",\"union_lens\":\"recoveryid:201_11.20.200.89_16797742_1632624677134;prepvid:201_11.20.207.176_16801805_1632625096923\",\"recoveryId\":\"201_11.175.96.106_16839576_1632632392630\"}","qieId":"36308","spm":"a2e0b.20350158.31919782","app_pvid":"201_11.175.96.106_16839576_1632632392630","ctm":"spm-url:a2e0b.20350158.31919782.1;page_url:https%3A%2F%2Fuland.taobao.com%2Fsem%2Ftbsearch%3Frefpid%3Dmm_26632258_3504122_32538762%26keyword%3Dadidas%2520yeezy%2520boost%26clk1%3D25b8f4d10e5d19d5a1b4c05c0cda428b%26upsId%3D25b8f4d10e5d19d5a1b4c05c0cda428b%26spm%3Da2e0b.20350158.31919782.1%26pid%3Dmm_26632258_3504122_32538762%26union_lens%3Drecoveryid%253A201_11.20.200.89_16797742_1632624677134%253Bprepvid%253A201_11.20.207.176_16801805_1632625096923%26pnum%3D1"}'.replace('手机',x)
 
    data_s = data_s + data_tm
    # 获取token
    token = re.findall(r"_m_h5_tk=(.*?);", ck)
    token = ''.join([i.split("_")[0] for i in token])
    
    # 运算sign加密
    pre_sign = token + '&' + str(date) + '&' + appKey + '&' + data_s
    sign = hashlib.md5(pre_sign.encode(encoding='UTF-8')).hexdigest()
    # print('cookies', ck)
    # print("sign计算成功>>>>%s" % sign)
    return date, data_s, sign
 
def get_cookies():
    url = 'https://h5api.m.taobao.com/h5/mtop.alimama.union.xt.en.api.entry/1.0/?jsv=2.5.1&appKey=12574478&t=1622426487791&sign=7771a311a65bbb533c3f3d4534d50f5e&api=mtop.alimama.union.xt.en.api.entry&v=1.0&AntiCreep=true&timeout=20000&AntiFlood=true&type=jsonp&dataType=jsonp&callback=mtopjsonp2&data=%7B%22floorId%22%3A195%2C%22count%22%3A10%2C%22p4pPid%22%3A%22430748_1006%22%2C%22spm%22%3A%22a2e1u.19484427.29996459%22%2C%22app_pvid%22%3A%22201_11.11.62.22_407060_1622426486844%22%2C%22ctm%22%3A%22spm-url%3Aa231o.13503973.search.1%3Bpage_url%3Ahttps%253A%252F%252Fai.taobao.com%252Fsearch%252Findex.htm%253Fspm%253Da231o.13503973.search.1%2526key%253D%2525E4%2525B8%2525B8%2525E7%2525BE%25258E%2526pid%253Dmm_110807073_1262350149_109959000489%2526union_lens%253Drecoveryid%25253A201_11.11.62.22_399283_1622423612735%25253Bprepvid%25253A201_11.11.62.22_399283_1622423612735%22%2C%22variableMap%22%3A%22%7B%5C%22union_lens%5C%22%3A%5C%22recoveryid%3A201_11.11.62.22_399283_1622423612735%3Bprepvid%3A201_11.11.62.22_399283_1622423612735%5C%22%2C%5C%22recoveryId%5C%22%3A%5C%22201_11.11.62.22_407060_1622426486844%5C%22%7D%22%7D'
    headers = {
        'referer': 'https://ai.taobao.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
    }
    res = requests.get(url, headers=headers).cookies
    cook = dict_from_cookiejar(res)
    cooks = ''
    for i, k in cook.items():
        cooks += i + '=' + k + ';'
    
    return cooks

def data(ck, page, size, keyword):
    date, data_s, sign = get_sign(ck, page, size, keyword)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        "cookie": ck}
    params = {
        'jsv': '2.5.1',
        'appKey': '12574478',
        't': date,
        'sign': sign,
        'api': 'mtop.alimama.union.xt.en.api.entry',
        'v': '1.0',
        'AntiCreep': 'true',
        'timeout': '20000',
        'AntiFlood': 'true',
        'type': 'jsonp',
        'dataType': 'jsonp',
        'callback': 'mtopjsonp2',
        'data': data_s
    }
    return headers, params

def run(pages, size, keyword):
    # cookie
    ck = get_cookies()
    # headers, params = data(ck, word)
    url = 'https://h5api.m.taobao.com/h5/mtop.alimama.union.xt.en.api.entry/1.0/'
    for page in range(1, pages):
        headers, params = data(ck, page, size, keyword)
        #  data_s={"pNum":2,"pSize":"60","refpid":"mm_26632258_3504122_32538762","variableMap":"{\"q\":\"adidas yeezy boost\",\"navigator\":false,\"clk1\":\"25b8f4d10e5d19d5a1b4c05c0cda428b\",\"union_lens\":\"recoveryid:201_11.20.200.89_16797742_1632624677134;prepvid:201_11.20.207.176_16801805_1632625096923\",\"recoveryId\":\"201_11.0.174.53_16801750_1632625790037\"}","qieId":"36308","spm":"a2e0b.20350158.31919782","app_pvid":"201_11.0.174.53_16801750_1632625790037","ctm":"spm-url:a2e0b.20350158.search.1;page_url:https%3A%2F%2Fuland.taobao.com%2Fsem%2Ftbsearch%3Frefpid%3Dmm_26632258_3504122_32538762%26keyword%3Dadidas%2520yeezy%2520boost%26clk1%3D25b8f4d10e5d19d5a1b4c05c0cda428b%26upsId%3D25b8f4d10e5d19d5a1b4c05c0cda428b%26spm%3Da2e0b.20350158.search.1%26pid%3Dmm_26632258_3504122_32538762%26union_lens%3Drecoveryid%253A201_11.20.200.89_16797742_1632624677134%253Bprepvid%253A201_11.20.207.176_16801805_1632625096923"}
        res = requests.get(url, headers=headers, params=params, timeout=30).content.decode('utf-8')
        # print(res)
        res_json = json.loads(str(res).replace('mtopjsonp2', '').replace('(', '').replace(')', ''))
        # print(a)
        if res_json['data']: 
            resultList = res_json['data']['recommend']['resultList']
            for x in resultList:
                print(f"产品名称：{x['itemName']} 店名：{x['shopTitle']}")
                # print(f"产品名称：{x['itemName']}，店名：{x['shopTitle']},卖家小名:{x['sellerNickName']},促销价格：{x['promotionPrice']},原价：{x['price']},月销量：{x['monthSellCount']}件，产地：{x['provcity']},网址:{x['url']}")
 
        # for x in a:
        #     print(
        #         f"产品名称：{str(x['itemName']).replace('<span class=H>','').replace('</span>','')}， 副标题：{x['subTitle']}, 卖家小名:{x['nick']}, 促销价格：{x['promotionPrice']}, 原价：{x['price']}, 月销量：{x['monthSellCount']}件, 网址:https{x['url']}, pic_url:https{x['pic']}")
 
if __name__=='__main__':

    # 页数，每页多少，关键字
    run(4, 10, '电脑')#可设置页数和商品名字

    # print('{"pNum": %d,"pSize": %d,"refpid":"mm_26632258_3504122_32538762",' % (1,2)10