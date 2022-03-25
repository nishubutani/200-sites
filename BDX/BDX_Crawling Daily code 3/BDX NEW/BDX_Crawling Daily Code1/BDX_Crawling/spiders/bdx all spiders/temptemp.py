# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from scrapy.cmdline import execute
from scrapy.utils.response import open_in_browser

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class valleybuildersSpider(scrapy.Spider):
    name = 'temptemp'
    allowed_domains = ['www.2valleybuilders.com/']
    start_urls = ['http://2valleybuilders.com/']
    builderNumber = 62028


    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = "2 VALLEY BUILDERS"
        item['City'] = "Windsor"
        item['State'] = "CO"
        item['ZIP'] = "80634"
        item['AreaCode'] = "970"
        item['Prefix'] = "396"
        item['Suffix'] = "1516"
        item['Extension'] = ""
        item['Email'] = "2valleybuilders@gmail.com"
        item['SubDescription'] = ""
        item['SubImage'] = "http://2valleybuilders.com/img/2ValleyBuilders-ItsPersonal-Family.jpg|http://2valleybuilders.com/img/Banner_Avail_17v2.jpg|http://2valleybuilders.com/img/stmichaelssign_index.jpg"
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl temptemp'.split())