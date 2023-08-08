import scrapy
from scrapy import FormRequest
import json

from items import MyspiderItem
class GaokaoSpider(scrapy.Spider):
    name = 'GaoKao'
    allowed_domains = ['gaokaopai.com']
    start_url = 'http://www.gaokaopai.com/rank-index.html'

    def __init__(self):
        self.headers = {
            "User-Agent":"自己找个UA",
            "X-Requested-With":"XMLHttpRequest"
        }

    # 需要重写start_requests() 方法
    def start_requests(self):
        for page in range(0,2):
            form_data = {
                "otype": "4",
                "city":"",
                "start":str(25*page),
                "amount": "25"
            }

            request = FormRequest(self.start_url,headers=self.headers,formdata=form_data,callback=self.parse)
            yield request

    def parse(self, response):
        print(response.body)
        print(response.url)
        print(response.body_as_unicode())
