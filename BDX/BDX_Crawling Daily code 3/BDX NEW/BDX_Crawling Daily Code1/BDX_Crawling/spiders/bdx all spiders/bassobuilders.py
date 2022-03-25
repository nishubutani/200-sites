



# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'bassobuilders'
    allowed_domains = ['bassobuilders.com']
    start_urls = ['http://www.bassobuilders.com']
    builderNumber = 13853


    def parse(self, response):


        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = '405 Skyline Drive'
        item2['City'] = 'Lake Geneva'
        item2['State'] = 'WI'
        item2['ZIP'] = '53147'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "BASSO BUILDERS has been serving Lake Geneva and its surrounding communities for over 40 years. From remodels to single family homes to multi family units, we provide personalized professional service to ensure you receive superior quality and exceptional value."
        item2['SubImage'] = "http://www.bassobuilders.com/wp-content/uploads/2021/07/IMG_0435-1030x687-1.jpg|http://www.bassobuilders.com/wp-content/uploads/2021/07/IMG_8015_6_7_8_9_tonemapped-X2-1030x687-1.jpg|http://www.bassobuilders.com/wp-content/uploads/2021/07/IMG_0405-X2-1030x687-1.jpg"
        item2['SubWebsite'] = ''
        # item2['AmenityType'] = ''
        yield item2




if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl bassobuilders'.split())