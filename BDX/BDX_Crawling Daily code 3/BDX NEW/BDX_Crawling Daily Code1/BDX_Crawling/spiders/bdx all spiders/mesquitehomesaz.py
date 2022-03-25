

# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'mesquitehomesaz'
    allowed_domains = ['mesquitehomesaz.com/']
    start_urls = ['http://mesquitehomesaz.com/']
    builderNumber = 173657954026217782940436413671

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
        item2['Street1'] = '345 E. Congress'
        item2['City'] = 'Tucson'
        item2['State'] = 'AZ'
        item2['ZIP'] = '85701'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = ""
        item2['SubImage'] = "http://mesquitehomesaz.com/Portals/94364/images/snapshot-02.png"
        item2['SubWebsite'] = 'https://wagonerhomes.com/'
        # item2['AmenityType'] = ''
        yield item2




if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl mesquitehomesaz'.split())


