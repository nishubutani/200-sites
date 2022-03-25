# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'aclee_construction'
    allowed_domains = ['https://www.acleeconstruction.com/']
    start_urls = ['https://www.acleeconstruction.com/home-gallery/']

    builderNumber = "62112"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()



        images = ''
        image = response.xpath('//div[@class="et_pb_gallery_image landscape"]/a//@href').extract()
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
        item['Street1'] = '915 Juniper Rd.'
        item['City'] = 'Four Oaks'
        item['State'] = 'NC '
        item['ZIP'] = '27524'
        item['AreaCode'] = '919'
        item['Prefix'] ='207'
        item['Suffix'] = '6080'
        item['Extension'] = ""
        item['Email'] = 'ashley@acleeconstruction.com'
        item['SubDescription'] = 'AC Lee Construction believes everyone should live better. We are a full service, custom building and design construction company. Our philosophy can be summarized in one word – compassion. We want to know you and learn about your project goals so we can deliver beautiful results.'
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl aclee_construction'.split())