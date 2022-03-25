

# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'dunreehomes'
    allowed_domains = ['dunreehomes.com/']
    start_urls = ['https://dunreehomes.com/']
    builderNumber = 173657954026217782940436413671

    def __init__(self):
        self.temp_list = []



    def parse(self, response):


        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = '19839 Mulroy Circle'
        item2['City'] = 'Tinley'
        item2['State'] = 'IL'
        item2['ZIP'] = '60487'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "Dunree Homes brings more than twenty years of homebuilding experience to Chicago and its surrounding suburbs. With a reputation for superior quality and the utmost attention to detail, Dunree Homes is known for providing trusted customer service throughout every aspect of the process— from architectural planning and construction to interior design"
        item2['SubImage'] = "https://images.squarespace-cdn.com/content/v1/57a152273e00bec21a8afa21/1476825245292-QX0UAG31F9RER1A9HDYL/0001.jpg?format=750w|https://images.squarespace-cdn.com/content/v1/57a152273e00bec21a8afa21/1498699517985-XEH5A29XQKG15PPUROBD/Screen+Shot+2017-06-28+at+8.23.57+PM.png?format=1000w|https://images.squarespace-cdn.com/content/v1/57a152273e00bec21a8afa21/1478721110078-0CXXFF0RBV5X5D4H5X0B/4144+and+4148+N.+Whipple+Chicago+Il+60618+New+Construction.jpg?format=1500w"
        item2['SubWebsite'] = 'https://wagonerhomes.com/'
        # item2['AmenityType'] = ''
        yield item2




if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl dunreehomes'.split())


