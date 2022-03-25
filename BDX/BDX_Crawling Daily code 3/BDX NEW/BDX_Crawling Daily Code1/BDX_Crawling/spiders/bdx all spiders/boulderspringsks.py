

 # -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'boulderspringsks'
    allowed_domains = ['http://aa-newhomes.com/']
    # start_urls = ['http://aa-newhomes.com/']
    start_urls = ['https://www.boulderspringsks.com/villas-floor-plans.html']

    builderNumber = "62064"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        ab = response.xpath('//p[contains(text(),"BED")]/text()').extract()
        print(ab)



        # --------------------------------------------------------------------- #


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl boulderspringsks'.split())