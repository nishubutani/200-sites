
# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'bradfordcommunities'
    allowed_domains = ['bradfordcommunities.com']
    start_urls = ['http://www.bradfordcommunities.com/']
    builderNumber = 5819419335688426705717577677

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
        item2['Street1'] = '313 Ray Street'
        item2['City'] = 'Pleasanton'
        item2['State'] = 'CA'
        item2['ZIP'] = '94566'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "We create neighborhoods that encourage vitality and connectivity among the people who live there. In choosing desirable locations, we create communities that provide comfort, safety, security and peace of mind. And, by listening to our home buyers, we create places that match their specific lifestyles, needs and desires. Blend all this with an unrelenting commitment to quality and our passion for delivering the best possible living experience and you’ll see that Bradford Communities is setting a new standard for delivering the American Dream."
        item2['SubImage'] = "http://www.bradfordcommunities.com/wordpress/wp-content/uploads/2016/10/podva-comm-img.jpg"
        item2['SubWebsite'] = 'http://www.bradfordcommunities.com/'
        # item2['AmenityType'] = ''
        yield item2



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl bradfordcommunities'.split())


