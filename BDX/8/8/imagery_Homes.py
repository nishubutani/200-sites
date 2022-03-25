import hashlib
import json
import re

import requests
import scrapy
from scrapy.selector import Selector
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class ImageryHomesSpider(scrapy.Spider):
    name = 'imagery_Homes'
    allowed_domains = ['www.imageryhomes.com']
    start_urls = ['https://www.imageryhomes.com/Home.aspx']
    builderNumber = 33806

    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        item = BdxCrawlingItem_subdivision()
        imgs = response.xpath('//div[@class="slide-wrapper"]/div/img/@src').getall()
        img_list = []
        for img in imgs:
            image = 'https://www.imageryhomes.com' + str(img)
            img_list.append(image)
        SubImage = '|'.join(img_list)
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '1105 Michael Drive'
        item['City'] = 'Brookfield'
        item['State'] = 'WI'
        item['ZIP'] = '53045'
        item['AreaCode'] = '262'
        item['Prefix'] = '370'
        item['Suffix'] = '7121'
        item['Extension'] = ""
        item['Email'] = 'Info@BrownHomeConstruction.com'
        item['SubDescription'] = '''Imagery Homes is a custom home builder and remodeling company that provides high-end luxury without the high-end luxury price tag.   Our team of skilled craftsmen and designers will help "Elevate Your Quality of Life"! 
                                    Whether you’re building one of our existing home designs, or if you need a one-of-a-kind custom built home, Imagery Homes is recognized as one of the areas top builders.   Guiding homebuyers through a simple, step-by-step process, we enhance the building experience by providing design services, practical advice, flexible accommodations, and personalized hands-on oversight from start to finish.
                                    For those of you that would like to stay in your current home, but would like to update or refresh your home's appearance, we proudly offer a wide range of remodeling services. '''
        item['SubImage'] = SubImage
        item['SubWebsite'] = response.url
        yield item

# from scrapy.cmdline import execute
# execute("scrapy crawl imagery_Homes".split())
