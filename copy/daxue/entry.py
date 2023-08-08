import scrapy
from scrapy import Request,Selector

class SchoolSpider(scrapy.Spider):
    name = 'School'
    allowed_domains = ['daxue.eol.cn']
    start_urls = ['https://daxue.eol.cn/mingdan.shtml']

    def parse(self, response):
        select = Selector(response)
        links = select.css(".province>a")
        
        for item in links:
            name = item.css("::text").extract_first()
            link = item.css("::attr(href)").extract_first()

            if name in ["河南","山东"]:
                yield Request(link,callback=self.parse_he_shan,meta={"name" : name})
            else:
                yield Request(link,callback=self.parse_school,meta={"name" : name})
    # 专门为河南和山东编写的提取方法
    def parse_he_shan(self,response):
        name = response.meta["name"]
        data = response.css(".table-x tr")
        for item in data:
            school_name = item.css("td:not(.tmax)::text").extract()

            if len(school_name)>0:
                for s in school_name:
                    if len(s.strip())>0:
                        if len(s.split("."))==1:
                            last_name = s.split(".")[0]
                        else:
                            last_name = s.split(".")[1]  # 最终获取到的名字
                        yield {
                            "city_name": name,
                            "school_name": last_name,
                            "code": "",
                            "department": "",
                            "location": "",
                            "subject": "",
                            "private": ""
                        }

    # 通用学校提取
    def parse_school(self,response):
        name = response.meta["name"]

        schools = response.css(".table-x tr")[2:]

        for item in schools:
            school_name = item.css("td:nth-child(2)::text").extract_first()
            code =  item.css("td:nth-child(3)::text").extract_first()
            department = item.css("td:nth-child(4)::text").extract_first()
            location = item.css("td:nth-child(5)::text").extract_first()
            subject = item.css("td:nth-child(6)::text").extract_first()
            private = item.css("td:nth-child(7)::text").extract_first()
            yield {
                "city_name":name,
                "school_name":school_name,
                "code":code,
                "department":department,
                "location":location,
                "subject":subject,
                "private":private
            }
