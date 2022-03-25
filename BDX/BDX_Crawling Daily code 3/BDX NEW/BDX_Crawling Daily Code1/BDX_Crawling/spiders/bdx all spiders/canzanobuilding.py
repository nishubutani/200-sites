
# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'canzanobuilding'
    allowed_domains = ['canzanobuilding.com']
    start_urls = ['http://canzanobuilding.com/']
    builderNumber = 235661454696196808504913514980

    def __init__(self):
        self.temp_list = []


    def parse(self, response):


        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = '32233 Schoolcraft #110'
        item2['City'] = 'Livonia'
        item2['State'] = 'MI'
        item2['ZIP'] = '48150'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "Canzano Building Company Inc. and JDM Building Company LLC are two of the premier builders of single family homes in southeast Michigan. We have been in the construction business for over two decades and have a long-standing reputation for personal integrity, honesty and dependability in the construction of our homes. Every home we build has a character that is shaped on our customers' needs and wishes "
        item2['SubImage'] = "http://canzanobuilding.com/images/h1.jpg"
        item2['SubWebsite'] = 'http://canzanobuilding.com/'
        # item2['AmenityType'] = ''
        yield item2



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl canzanobuilding'.split())




