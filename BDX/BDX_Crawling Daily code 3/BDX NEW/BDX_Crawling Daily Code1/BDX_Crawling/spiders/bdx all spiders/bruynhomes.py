

# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'bruynhomes'
    allowed_domains = ['bruynhomes.com']
    start_urls = ['http://www.bruynhomes.com/']
    builderNumber = 49501


    def parse(self, response):


        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = '5356 Plainfield Ave NE'
        item2['City'] = 'Liberty'
        item2['State'] = 'MI'
        item2['ZIP'] = '49525'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "Mike has a passion for development, with an addiction to housing. His experience includes horizontal development, vertical construction, and brokerage. Mike founded The Brookeview Group LLC in 2008 after managing the Kansas City office for a multi-state developer. A few years later, Mike founded The Real Estate Store LLC, a brokerage focused on residential, commercial, and investment sales. Both companies work in tandem to develop, build, and broker development indeopendtently and within trusted partnerships. With over 18 years of real estate and construction experience, Mike credits the core values of integrity, commitment, and trust as the reason for his success. He believes every project should begin with the end in mind, this unique approach ensures success for partners, investors, and end-users alike."
        item2['SubImage'] = ""
        item2['SubWebsite'] = ''
        # item2['AmenityType'] = ''
        yield item2



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl bruynhomes'.split())