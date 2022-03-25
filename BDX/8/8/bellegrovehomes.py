# -*- coding: utf-8 -*-
import os
import hashlib
import re

import scrapy
import requests
from scrapy.http import HtmlResponse

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan


class BellGrovehomesSpider(scrapy.Spider):
    name = 'bellgrovehomes'
    allowed_domains = []
    start_urls = ['https://www.example.com']

    builderNumber = '11777'

    def parse(self, response):
        imgs = [
            'http://bellegrovehomes.com/wp-content/uploads/2014/09/plain-house.jpg',
            'http://bellegrovehomes.com/wp-content/uploads/2014/09/Patio-Brick.jpg',
            'http://bellegrovehomes.com/wp-content/uploads/2014/09/DiningRoom-BelleGrove.jpg',
            'http://bellegrovehomes.com/wp-content/uploads/2014/11/004-e1415587411219.jpg'
        ]

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '34 Defense Street, Suite 300'
        item['City'] = 'Annapolis'
        item['State'] = 'MD'
        item['ZIP'] = '21401'
        item['AreaCode'] = '410'
        item['Prefix'] = '224'
        item['Suffix'] = '1411'
        item['Extension'] = ""
        item['Email'] = "BGH@BELLEGROVEHOMES.COM"
        item['SubDescription'] = "Since 1941, Belle Grove Homes has successfully served our customers and community. Belle Grove Homes is dedicated to quality construction and professional customer service. We pride ourselves with innovation in the building materials and in our floor plans designed to meet your family’s day to day needs without losing the custom features that make our designs unique.Organization and teamwork are Belle Grove’s keys to success. We understand that proven systems and working relationships are crucial to the management of the many variables in construction and real estate. Coordination with customers, engineers, architects, designers, suppliers, tradespeople, government & the local community are critical to the building process.Belle Grove stays informed of current issues and have been active members of the Home Builder Association of Maryland for 70+ years, Associated Builders & Contractors for 30+ years and Anne Arundel County Association of Realtors for 40+ years."
        item['SubImage'] = '|'.join(imgs)
        item['SubWebsite'] = "http://bellegrovehomes.com/"
        yield item

# from scrapy.cmdline import execute
# execute("scrapy crawl bellgrovehomes".split())