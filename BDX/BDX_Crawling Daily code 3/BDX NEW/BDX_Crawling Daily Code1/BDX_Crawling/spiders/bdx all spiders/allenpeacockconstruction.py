
# -*- coding: utf-8 -*-
import hashlib
import re
import time

import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class allenpeacockconstruction(scrapy.Spider):
    name = 'allenpeacockconstruction'
    allowed_domains = ['https://buydestinyhomes.com/']
    start_urls = ['https://buydestinyhomes.com//']

    builderNumber = "62676"

    def parse(self, response):

        images = ''
        image = response.xpath('//div[@class="cycle-slideshow"]/img/@src').extract()
        for i in image:
            images = images + i + '|'
        images = images.strip('|')

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '1530 George Drive'
        item['City'] = 'Douglas'
        item['State'] = 'GA'
        item['ZIP'] = '31535'
        item['AreaCode'] = '912'
        item['Prefix'] = '384'
        item['Suffix'] = '8144'
        item['Extension'] = ""
        item['Email'] = 'peacockconst@windstream.net'
        item['SubDescription'] = 'With Every Peacock built home you can rest assured that you are covered in case something is discovered as less than perfect. Explore the interactive image to check what is covered, how it is covered, and to see that you have coverage long enough to be confident that your build is just what you ordered. Select 1 Year, 2 Year, and 10 Year to get items covered for that period. There is information behind every plus sign so start now and discover that a Peacock home is a home you can depend on being built right.'
        item['SubImage'] = 'http://allenpeacockconstruction.com/images/contactus400.jpg|http://allenpeacockconstruction.com/indexedimages/400/12_04_18_1221_4f897.jpg|'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item




if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl allenpeacockconstruction'.split())


