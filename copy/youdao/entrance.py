import hashlib
import time
import random
import requests
def generate_salt_sign(translate):
    # var t = n.md5(navigator.appVersion)
    app_version = "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    bv = hashlib.md5(app_version.encode(encoding='UTF-8')).hexdigest()
    # r = "" + (new Date).getTime()
    salt = str(int(round(time.time(),3)*1000))
    # i = r + parseInt(10 * Math.random(), 10);
    lts = salt[:-1]

    # sign: n.md5("fanyideskweb" + e + i + "1L5ja}w$puC.v_Kz3@yYn")
    sign = hashlib.md5(("fanyideskweb"+translate+salt+"Y2FYu%TNSbMCxc3t2u^XT").encode(encoding='utf-8')).hexdigest()

# salt: 16304848224258
# sign: 42ffa0ac520d673a11ccb7e4629565cf
# lts: 1630484822425
# bv: 89e18957825871c419be045180c67d3b

    return salt,sign,lts,bv

def params():
    data = {}
    translate = '橡皮擦'
    client = 'fanyideskweb'
    data['i'] = translate
    data['from'] = 'AUTO'
    data['to'] = 'AUTO'
    data['smartresult'] = 'dict'
    data['client'] = client

    data['salt'],data['sign'],data['lts'],data['bv'] = generate_salt_sign(translate)
    data['doctype'] = 'json'
    data['version'] = '2.1'
    data['keyfrom'] = 'fanyi.web'
    data['action'] = 'FY_BY_DEFAULT'
    # data['typoResult'] = 'false'
    print('data', data)
    return data
def tran():
    data = params()
    headers = {}
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    headers["Referer"] = "http://fanyi.youdao.com/"
    headers["Cookie"] = "OUTFOX_SEARCH_USER_ID=-1868577286@222.222.147.75;"

    with requests.post("https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule",headers=headers,data=data) as res:
        print(res.text)

if __name__ == '__main__':
    lts = str(int(round(time.time(),3)*1000))
    print(lts, lts[:-1])
    tran()
