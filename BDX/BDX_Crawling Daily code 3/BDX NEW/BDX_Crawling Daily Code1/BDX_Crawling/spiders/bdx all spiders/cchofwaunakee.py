

# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'cchofwaunakee'
    allowed_domains = ['cchofwaunakee.com']
    start_urls = ['https://www.cchofwaunakee.com/']
    builderNumber = 53083


    def parse(self, response):


        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = '401 N. Century Avenue'
        item2['City'] = 'Waunakee'
        item2['State'] = 'WI'
        item2['ZIP'] = '53597'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "lassic Custom Homes of Waunakee, Inc. has a sound reputation in the construction industry confirmed by over 30 years of Wisconsin home building experience. Our expertise stems from residential and commercial construction, as well as residential and commercial remodeling. The team at Classic Custom Homes of Waunakee bring these talents together to provide our customers with an extraordinary home building experience."
        item2['SubImage'] = ""
        item2['SubWebsite'] = ''
        # item2['AmenityType'] = ''
        yield item2



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl cchofwaunakee'.split())