

# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'trenthomes'
    allowed_domains = ['trenthomes.net']
    start_urls = ['https://www.trenthomes.net/']
    builderNumber = 51076


    def parse(self, response):


        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = '918 Meridian St'
        item2['City'] = 'Huntsville'
        item2['State'] = 'AL'
        item2['ZIP'] = '35801'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "Kent Brown and Trish Neal have been in the Huntsville area building business for over 20 years. They have extensive experience building custom homes, speculative building and remodeling.We believe in relationship building, getting to know the customer to help determine their goals in the construction process and staying within the budgeted amount agreed upon. We apply our beliefs in honesty, commitment to excellence and customer satisfaction to build the best possible home we can in a timely fashion."
        item2['SubImage'] = "https://www.trenthomes.net/uploadimage/158815184551629.jpg|https://www.trenthomes.net/uploadimage/158904626493526.jpg|https://www.trenthomes.net/uploadimage/158904626429926.jpg|https://www.trenthomes.net/uploadimage/158904626483934.jpg|https://www.trenthomes.net/uploadimage/158904631684685.jpg"
        item2['SubWebsite'] = ''
        # item2['AmenityType'] = ''
        yield item2




if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl trenthomes'.split())