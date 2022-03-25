import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header

class DannysullivanconstructionComSpider(scrapy.Spider):
    name = 'highlandBuilders'
    allowed_domains = []
    start_urls = ['https://highlandbuilding.com/']
    builderNumber = 32626


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
        item['Street1'] = '14012 Redhills Rd'
        item['City'] = 'Beaverdam'
        item['State'] = 'VA'
        item['ZIP'] = '23015'
        item['AreaCode'] = '804'
        item['Prefix'] ='409'
        item['Suffix'] = '4460'
        item['Extension'] = ""
        item['Email'] ='kevin@highlandbuilding.com'
        item['SubDescription'] ='Would you rather have a templated home with a few customized options or a truly custom-built home that will satisfy all your needs and desires? If you want a fully customizable home, Highland Builders is the choice for you. We’re an established builder in the Greater Richmond area. We’ll guide you through the entire home building process – from brainstorming design ideas to addressing any concerns long after your home has been built.'
        item['SubImage']= 'https://highlandbuilding.com/wp-content/uploads/2020/01/slider-2.jpg|https://highlandbuilding.com/wp-content/uploads/2020/01/slider-1.jpg|https://highlandbuilding.com/wp-content/uploads/2020/01/slider-3.jpg|https://highlandbuilding.com/wp-content/uploads/2020/01/manakin-sabot_2017_davis-cook-10.jpeg'
        item['SubWebsite'] = response.url
        yield item

from scrapy.cmdline import execute
if __name__ == '__main__':
    execute("scrapy crawl highlandBuilders".split())