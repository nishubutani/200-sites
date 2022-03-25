# -*- coding: utf-8 -*-
import scrapy
import hashlib
import re
import scrapy
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class WestridgeBuilderSpider(scrapy.Spider):
    name = 'westridge_builder'
    allowed_domains = ['www.westridgebuilders.com']
    start_urls = ['https://www.westridgebuilders.com']
    builderNumber = "14059"

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
        item['Street1'] = 'N8 W22520-L Johnson Dr'
        item['City'] = 'Waukesha'
        item['State'] = 'WI'
        item['ZIP'] = '53186'
        item['AreaCode'] = "262"
        item['Prefix'] = "547"
        item['Suffix'] = "0326"
        item['Extension'] = ""
        item['Email'] = "builder@warringhomes.com"
        item['SubDescription'] = 'The Finest in Luxury Home Design and New Home Construction'