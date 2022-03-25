

# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
# from BDX_Crawling.spiders.input8 import mainstreethomes_input as inp
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision


class MainstreethomesCrawlerSpider(scrapy.Spider):
    name = 'darshit'
    allowed_domains = ['www.mainstreethome.com']
    start_urls = ['https://mainstreet-homes.com/']

    builderNumber = "62025"


    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

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
        item['Street1'] = "1310 S. Main Street, Suite 12"
        item['City'] = "Ann Arbor"
        item['State'] = "MI"
        item['ZIP'] = "48104"
        item['AreaCode'] = "734"
        item['Prefix'] = "531"
        item['Suffix'] = "6477"
        item['Extension'] = ""
        item['Email'] = "joe@mainstreethomes.com"
        item['SubDescription'] = "At Main Street Homes, we use only the best materials and work with the most talented architects, designers, and tradespeople. We use a systematic process that makes the whole experience easy for our clients. We provide an on-site selections center with professional design and selections services. We include what other builders consider upgrades. And because no two families are the same, each Main Street-built home is distinctively different.And you could say each Main Street-built home is distinctively Michigan, too, designed to complement the unique beauty, culture, and energy of this corner of the world. As a custom home builder in Michigan, our staff live and work in greater Ann Arbor, and we know you’ll love coming home to this area as much as we do!Get to know our team, and see what our clients have to say about us. Then give us a call so we can show you in person how we’ll put our home building philosophy to work for you."
        item['SubImage'] = '|'.join(response.xpath('//ul[@class="slides"]//img/@src').extract())
        item['SubWebsite'] = "https://mainstreet-homes.com/"
        item['AmenityType'] = ""
        yield item

        # --------------------------------------------------------------------- #


if __name__ == '__main__':

    from scrapy.cmdline import execute
    execute('scrapy crawl darshit'.split())

