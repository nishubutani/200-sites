# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'woodbrookhomesllc'
    allowed_domains = ['woodbrookhomesllc.com']
    start_urls = ['http://www.woodbrookhomesllc.com/']
    builderNumber = 50817


    def parse(self, response):


        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = '23 Revere Court'
        item2['City'] = 'Princeton Junction'
        item2['State'] = 'NJ'
        item2['ZIP'] = '08550'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "Woodbrook Homes LLC is the culmination of almost thirty years of experience in the homebuilding industry by its principal Tom Rockoff. He has combined knowledge and expertise along with personal service in creating Woodbrook Homes. Complete dedication to building quality homes with superb workmanship is the hallmark of the company."
        item2['SubImage'] = "http://www.woodbrookhomesllc.com/images/gallery_page/Gallery_110_2.jpg|http://www.woodbrookhomesllc.com/images/gallery_page/Gallery_117.jpg|http://www.woodbrookhomesllc.com/images/gallery_page/Gallery_115_7.jpg|http://www.woodbrookhomesllc.com/images/gallery_page/Gallery_32.jpg"
        item2['SubWebsite'] = ''
        # item2['AmenityType'] = ''
        yield item2




if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl woodbrookhomesllc'.split())