# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'atlas_buildinggroup'
    allowed_domains = ['https://www.atlasbuildinggroup.com/']
    start_urls = ['https://www.atlasbuildinggroup.com']

    builderNumber = "62814"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()



        images = ''
        image = response.xpath('//div[@class="gallery-reel-item-src"]/img/@data-src').extract()
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
        item['Street1'] = '2026 N Beebe Blvd'
        item['City'] = 'Coeur d’Alene'
        item['State'] = 'ID'
        item['ZIP'] = '83814'
        item['AreaCode'] = '208'
        item['Prefix'] ='818'
        item['Suffix'] = '7941'
        item['Extension'] = ""
        item['Email'] = 'info@atlasbuildinggroup.com'
        item['SubDescription'] = 'Atlas Building Group was built in 2016 on a foundation of trusted friendship between Nick Forsberg and Kenny Debaene. They brought their unique set of skills to the company with their own history in the industry. Kenny has been in construction over 30 years and owned a concrete company for 20 years. Nick"s industry experience started when working for a local land developer back in 2006. After which, he worked in change management as the VP of performance strategy, traveling around the country for a couple of large publicly traded building material companies. Kristin Williams helps to keep the group organized through her experience with construction finance and accounting. Todd Best provides a point of contact for customer service and general assistance with the building process.'
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item


    # --------------------------------------------------------------------- #

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl atlas_buildinggroup'.split())