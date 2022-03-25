


# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'anthonythomas_builders'
    allowed_domains = ['http://anthonythomasbuilders.com/']
    start_urls = ['http://anthonythomasbuilders.com/anthony-thomas-builders-photo-gallery/ranch-homes-by-anthony-thomas-builders/']

    builderNumber = "62734"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        images = ''
        image = response.xpath('//dt[@class="gallery-icon landscape"]/a/@href').extract()
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
        item['Street1'] = '1208 HWY 83'
        item['City'] = 'Hartland'
        item['State'] = 'WI'
        item['ZIP'] = '53029'
        item['AreaCode'] = '262'
        item['Prefix'] ='367'
        item['Suffix'] = '8884'
        item['Extension'] = ""
        item['Email'] = 'info@anthonythomasbuilders.com'
        # item['Email'] = ''
        item['SubDescription'] = 'Anthony’s support at home comes from his wife Jill and their children, Tyler, Cade, Tanner & Kallyn. Coming back to Southeastern Wisconsin to start his own business was already decided in 1992 while he and Jill were living in the western suburbs of Chicago. Anthony had worked for two very large building firms in the Chicagoland area and had the responsibility for building hundreds of homes under corporate rules and procedures. While wearing all of the hats as an estimator, contract negotiator and general manager of construction, the final decisions affecting quality & homeowner satisfaction were still made by the company owners. It was time to control those decisions and get back to meeting the client’s needs and wants.'
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item


        # --------------------------------------------------------------------- #


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl anthonythomas_builders'.split())

    # minOccurs = "0"