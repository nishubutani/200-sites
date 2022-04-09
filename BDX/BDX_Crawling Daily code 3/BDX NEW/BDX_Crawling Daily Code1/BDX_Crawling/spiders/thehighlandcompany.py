import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class HillCountrySpider(scrapy.Spider):
    name = 'thehighlandcompany'
    allowed_domains = []
    start_urls = ['https://www.thehighlandcompany.com/']
    builderNumber = 51658

    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '982 N. Winstead Avenue'
        item['City'] = 'Rocky Mount'
        item['State'] = 'NC'
        item['ZIP'] = '27804'
        item['AreaCode'] = ''
        item['Prefix'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = 'Since 1985, The Highland Company of Rocky Mount has been one of Eastern North Carolinas premier builders! Whether you are a first time home buyer, or looking to build for the first time, The Highland Company is committed and ready to go to work for you!'
        item['SubImage'] = 'https://www.thehighlandcompany.com/uploads/2/3/1/0/23106720/home-1_orig.jpg|https://www.thehighlandcompany.com/uploads/2/3/1/0/23106720/9652197_orig.jpg|https://www.thehighlandcompany.com/uploads/2/3/1/0/23106720/2800126_orig.jpg|https://www.thehighlandcompany.com/uploads/2/3/1/0/23106720/3797907_orig.jpg|https://www.thehighlandcompany.com/uploads/2/3/1/0/23106720/424972_orig.jpg|https://www.thehighlandcompany.com/uploads/2/3/1/0/23106720/5324209_orig.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item


if __name__ == '__main__':
    execute("scrapy crawl thehighlandcompany".split())