# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class ChrisJacksonBuilderSpider(scrapy.Spider):
    name = 'chris_jackson_builder'
    allowed_domains = ['http://chrisjacksonbuilders.com/']
    start_urls = ['http://chrisjacksonbuilders.com/']

    builderNumber = "54574"


    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #
        image = '|'.join(response.xpath('//li/a/img/@src').extract())
        images = image.strip('|')
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = "2700 Old Rosebud Road"
        item['City'] = "Lexington"
        item['State'] = "KY"
        item['ZIP'] = "40509"
        item['AreaCode'] = "859"
        item['Prefix'] = "230"
        item['Suffix'] = "5493"
        item['Extension'] = ""
        item['Email'] = ""
        item['SubDescription'] = ''.join(response.xpath('//*[@class="vs_text"]/p//text()').extract()).strip()
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        yield item


from scrapy.cmdline import execute
# execute("scrapy crawl chris_jackson_builder".split())