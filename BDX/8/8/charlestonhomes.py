import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class CharlestonHomesSpider(scrapy.Spider):
    name = 'charlestonhomes'
    allowed_domains = []
    start_urls = ['https://www.charlestonhomesomaha.com/']
    builderNumber = 52303

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
        item['Street1'] = '3803 NORTH 153RD STREET, STE 200'
        item['City'] = 'OMAHA'
        item['State'] = 'NE'
        item['ZIP'] = '68116'
        item['AreaCode'] = '402'
        item['Prefix'] ='933'
        item['Suffix'] = '7224'
        item['Extension'] = ""
        item['Email'] =''
        item['SubDescription'] ='I’ve received a ton of compliments on the home and wanted to thank you and the entire Charleston team for a truly beautiful home. Thank you!'
        item['SubImage']= 'https://www.charlestonhomesomaha.com/wp-content/uploads/2017/09/Edgebrook-Model-Slide-1-100x50.jpg'
        item['SubWebsite'] = response.url
        yield item

# execute("scrapy crawl charlestonhomes".split())