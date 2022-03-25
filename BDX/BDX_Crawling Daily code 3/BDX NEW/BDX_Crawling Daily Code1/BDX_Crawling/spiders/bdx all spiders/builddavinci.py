



# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'builddavinci'
    allowed_domains = ['builddavinci.com']
    start_urls = ['https://www.builddavinci.com/']
    builderNumber = 56854


    def parse(self, response):


        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = '3200 W. Clubhouse Dr. Suite'
        item2['City'] = 'Lehi'
        item2['State'] = 'WI'
        item2['ZIP'] = '53597'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "DaVinci Homes is a premier home builder in Utah. We know value is created through better design and increased quality, which is why we commission the finest subcontractors and designers in the state."
        item2['SubImage'] = "https://static.wixstatic.com/media/d24577_d13064878a194f6a92945fe98091460e~mv2.jpg|https://static.wixstatic.com/media/d24577_75d2dfe5b1b5424191982cf8159a4ba6~mv2.jpg"
        item2['SubWebsite'] = 'https://www.builddavinci.com/'
        # item2['AmenityType'] = ''
        yield item2



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl builddavinci'.split())
