import re
import scrapy
from scrapy.http import HtmlResponse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


C=0 #Count of Crawled documents (used to ID next document)
Links = set()#Set of Crawled URLs

#A Function which gets a url and normalize it, to avoid duplication of crawling
def normalize(url):
    if url[4]=='s':
        url = url[:4]+url[5:]
    s = url.find("#")
    if s!=-1:
        url = url[:s]
    if url[-1]=='/':
        url = url[:-1]
    return url
    

class SpiderTwo(CrawlSpider):
    name = "two"
    allowed_domains = ["ucl.ac.uk"]
    start_urls = ["http://www.ucl.ac.uk/"]
    rules = (
     Rule(LinkExtractor(allow=('')),follow= True,callback='parse_page'),
     )
        

    def parse_page(self, response):
        global C,Links
        url = normalize(response.url)
        
        #Don't crawl:
        #1) Non html documents
        #2) Redirection or not found URLs
        #3) Non UCL URLs
        #4) Same document another time
        #5) If the page requires login
        if not isinstance(response, HtmlResponse) or response.status != 200 or not re.match("http.*ucl\.ac\.uk.*",url) or url in Links or "login" in url:
            return
        Links.add(url)
        filename = str(C)+'.txt'
        C=C+1
        with open("url/"+filename, 'wb') as f:#Save URL in url/C.txt
            f.write(url)
        with open("doc/"+filename, 'wb') as f:#Save html in doc/C.txt
            f.write(response.body)
        with open("links/"+filename, 'wb') as f:#Save the set of out links in links/C.txt
            outLinks = set()
            for href in response.css("a::attr('href')"):
                try:
                    link = response.urljoin(href.extract())
                    norm = normalize(link)
                    if(re.match("http.*ucl\.ac\.uk.*",link) and norm not in outLinks):
                        outLinks.add(norm)
                except:
                    pass
            for x in outLinks:
                try:
                    f.write(x+"\n")
                except:
                    pass
        

   
