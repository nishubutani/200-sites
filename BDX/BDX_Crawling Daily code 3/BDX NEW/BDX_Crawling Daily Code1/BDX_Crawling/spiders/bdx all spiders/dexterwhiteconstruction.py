# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'dexterwhiteconstruction'
    allowed_domains = ['dexterwhiteconstruction.com/']
    start_urls = ['http://dexterwhiteconstruction.com//']

    builderNumber = "691128069770652644700407639480"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        add = response.xpath('//p[@id="contact"]/text()').extract_first(default='').strip().split(',')
        Street1 = add[0]
        City = add[1]
        State = add[2].strip().split(' ')[0]
        ZIP = add[2].strip().split(' ')[1]

        contact = response.xpath('//p[@id="contact"]/a[1]/text()').extract_first(default='').strip().split('.')



        images = ''
        image = response.xpath('//*[contains(@src,"https://dexterwhiteconstruction.com/wp-content/uploads/media/projects")]/@src').extract()
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
        item['Street1'] = Street1
        item['City'] = City
        item['State'] = State
        item['ZIP'] = ZIP
        item['AreaCode'] = contact[0]
        item['Prefix'] = contact[1]
        item['Suffix'] = contact[2]
        item['Extension'] = ""
        item['Email'] = response.xpath('//p[@id="contact"]/a[2]/text()').extract_first(default='').strip()
        item['SubDescription'] = "".join(response.xpath('//*[@id="tradition-of-excellence"]//p//text()').extract())
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item


        # --------------------------------------------------------------------- #


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl dexterwhiteconstruction'.split())