# -*- coding: utf-8 -*-
import hashlib
import re
import requests
from scrapy.http import HtmlResponse
import scrapy
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class AbbaRiverHomeSpider(scrapy.Spider):
    name = 'Abba_River_Home'
    allowed_domains = ['www.abbariverhomes.com']
    start_urls = ['https://www.providentresorts.com/sunset-vistas-beachfront-suites-tampa-and-treasure-island/about-sunset-vistas/amenities']

    builderNumber = "53901"

    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        amen = response.xpath('//div[@class="page-content"]/p/strong/text()').extract()
        print(amen)

        amen = "|".join(amen)
        print(amen)


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
        item['Street1'] = '2601 Cleburne Hwy'
        item['City'] = 'Cresson'
        item['State'] = 'TX'
        item['ZIP'] = '00000'
        item['AreaCode'] = '817'
        item['Prefix'] = '300'
        item['Suffix'] = '4352'
        item['Extension'] = ""
        item['Email'] = 'AbbaRiverHomes@yahoo.com'
        item['AmenityType'] = amen
        item['SubDescription'] = ''.join(response.xpath('//div[@id="pp-texttop"]/div//text()').extract()).strip()
        item['SubImage'] = '|'.join(response.xpath('//div[@class="nivoSlider"]/a/img/@src').extract())
        item['SubWebsite'] = response.url
        yield item

if __name__ == '__main__':

    from scrapy.cmdline import execute
    execute("scrapy crawl Abba_River_Home".split())
