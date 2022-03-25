# -*- coding: utf-8 -*-
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision


class AsphaltplusincSpider(scrapy.Spider):
    name = 'asphaltPlusInc'
    allowed_domains = ['www.asphaltplusinc.com']
    start_urls = ['http://asphaltplusinc.com/country-meadow-subdivision/']

    builderNumber = "155399368437607976359111755051"

    def parse(self, response):

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] ='Country Meadow Subdivision'
        item['SubdivisionNumber'] = int(hashlib.md5(bytes(item['SubdivisionName'], "utf8")).hexdigest(), 16) % (10 ** 30)
        item['BuildOnYourLot'] = 1 if "build-on-your-lot" in str(response.url) else 0
        item['OutOfCommunity'] = 1
        item['Street1'] = "425 Johnson Lane"
        item['City'] = "Billings"
        item['State'] = "MT"
        item['ZIP'] = "59101"
        item['AreaCode'] = 406
        item['Prefix'] = 248
        item['Suffix'] = 5609
        item['Extension'] = ""
        item['Email'] = "office@asphaltplusinc.com"
        item['SubDescription'] = "|".join(response.xpath('//*[@id="content"]/div/div[1]//p[position()<last()]/text()').extract())
        item['SubImage'] = response.xpath('//*[@id="content"]/div/div[2]/p/a/img/@src').extract_first(default="")
        item['SubWebsite'] = response.url
        yield item


# from scrapy.cmdline import execute
# execute("scrapy crawl asphaltPlusInc".split())