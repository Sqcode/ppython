import scrapy


class CarsSpider(scrapy.Spider):
    name = 'cars'
    allowed_domains = ['12365auto.com']
    start_urls = ['http://12365auto.com/']

    def parse(self, response):
        name_car = response.xpath(".//div[@class='in_cxsx_b'][1]/div[@class='in_wxc'][1]/dl[1]/dt/a/text()")
        item = {}
        item['name'] = name_car.extract()
        yield item
