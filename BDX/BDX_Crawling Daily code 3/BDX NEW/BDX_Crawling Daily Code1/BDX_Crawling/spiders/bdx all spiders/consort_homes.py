

# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'consort_homes'
    allowed_domains = ['consort-homes.com/']
    start_urls = ['https://consort-homes.com/']
    builderNumber = 327159950172746484835538322752

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
        item2['Street1'] = '16141 Swingley Ridge Road'
        item2['City'] = 'Chesterfield'
        item2['State'] = 'MO'
        item2['ZIP'] = '63017'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "The Consort Homes story is rich in St. Louis homebuilding history beginning more than 85 years ago with the founder of The Jones Company, John E. Jones. Those who know the St. Louis area probably know the name Bob Jones, who was the son of John E. Jones"
        item2['SubImage'] = "https://consort-homes.com/wp-content/uploads/2015/05/model_391-699x428.jpg|https://consort-homes.com/wp-content/uploads/2019/01/WP-Display-Sierra-01-a-699x428.jpg"
        item2['SubWebsite'] = 'https://wagonerhomes.com/'
        item2['AmenityType'] = ''
        yield item2



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl consort_homes'.split())


