
# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'highland_builder'
    allowed_domains = ['highland-builders.com']
    start_urls = ['https://www.highland-builders.com/']
    builderNumber = 32628


    def parse(self, response):

        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = ''
        item2['City'] = 'West Bend'
        item2['State'] = 'WI'
        item2['ZIP'] = '00000'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "At Highland Builders, we're about as client focused as you can get. That means we're not a faceless contractor driven by the volume of houses we can build. And we don't take short-cuts on the biggest investment of your life. We're husbands and fathers who are reminded every day of how important home is. And when we work with you, we never forget that."
        item2['SubImage'] = "https://www.highland-builders.com/wp-content/uploads/2020/01/Prescotts_Highland_Builders_Ryan_Hainey_Photography_003_web.jpg|https://www.highland-builders.com/wp-content/uploads/2020/01/Prescotts_Highland_Builders_Ryan_Hainey_Photography_023_web.jpg|https://www.highland-builders.com/wp-content/uploads/2020/01/Prescotts_Highland_Builders_Ryan_Hainey_Photography_020_web.jpg|https://www.highland-builders.com/wp-content/uploads/2020/01/Prescotts_Highland_Builders_Ryan_Hainey_Photography_028_web.jpg"
        item2['SubWebsite'] = 'https://www.highland-builders.com/'
        item2['AmenityType'] = ''
        yield item2



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl highland_builder'.split())


