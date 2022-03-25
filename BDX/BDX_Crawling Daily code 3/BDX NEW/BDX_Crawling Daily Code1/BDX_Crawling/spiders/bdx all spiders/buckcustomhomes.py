
# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'buckcustomhomes'
    allowed_domains = ['https://buckcustomhomes.com/']
    start_urls = ['https://buckcustomhomes.com/']

    builderNumber = "63681"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()


        images = ''
        image = response.xpath('//div[@class="fw-block-image-parent fw-overlay-1 fw-block-image-icon   "]/a/@href').extract()
        for i in image:
            print(i)
            images = images + i.replace("//www","https://www") + '|'
        images = images.strip('|')
        print(images)

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = 'PO Box 216'
        item['City'] = 'Ocean'
        item['State'] = 'NJ'
        item['ZIP'] = '08226'
        item['AreaCode'] = '609'
        item['Prefix'] ='317'
        item['Suffix'] = '3585'
        item['Extension'] = ""
        item['Email'] = 'info@buckcustomhomes.com'
        item['SubDescription'] = 'Buck Custom Homes, Founded by Michael Buck is committed to creating fine homes rich in detail and built with quality craftsmanship. Our philosophy is to produce unique shore residences tailored to exceed today"s standards by combining the best materials with flawless execution'
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl buckcustomhomes'.split())