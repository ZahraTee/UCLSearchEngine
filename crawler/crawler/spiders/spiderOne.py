import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

C=0

class SpiderOne(CrawlSpider):
    name = "one"
    allowed_domains = ["ucl.ac.uk"]
    start_urls = ["http://www.ucl.ac.uk/"]
    rules = (
     Rule(LinkExtractor(allow=('')),follow= True,callback='parse_page'),
     )
        

    def parse_page(self, response):
        global C
        filename = str(C)+'.txt'
        C=C+1
        with open("url/"+filename, 'wb') as f:
            f.write(response.url)
        with open("doc/"+filename, 'wb') as f:
            f.write(response.body)
        with open("links/"+filename, 'wb') as f:
            for href in response.css("a::attr('href')"):
                link = response.urljoin(href.extract())
                if(re.match(".*ucl\.ac\.uk.*",link)):
                    f.write(link+"\n")
        

   
