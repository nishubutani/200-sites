
# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'builddavinci'
    allowed_domains = ['builddavinci.com']
    start_urls = ['https://www.builddavinci.com/']
    builderNumber = 56854


    def parse(self, response):

        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = '3200 W. Clubhouse Dr. Suite #250'
        item2['City'] = 'Lehi'
        item2['State'] = 'UT'
        item2['ZIP'] = '84043'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "DaVinci Homes is a premier home builder in Utah. We know value is created through better design and increased quality, which is why we commission the finest subcontractors and designers in the state. DaVinci will build the home of your dreams with a custom plan and on the ideal lot, all of which can be selected directly from our site. We also offer our own portfolio of custom-designed home plans, personalized by a wide range of affordable options. DaVinci invites you to explore the many possibilities of custom home design and construction available to you through our comprehensive database of home plans so you can experience the Art of Living firsthand"
        item2['SubImage'] = "https://static.wixstatic.com/media/d24577_d13064878a194f6a92945fe98091460e~mv2.jpg|https://static.wixstatic.com/media/d24577_5c77303a5cea4176bc5cd489414b1555~mv2.jpg|https://static.wixstatic.com/media/d24577_75d2dfe5b1b5424191982cf8159a4ba6~mv2.jpg|https://static.wixstatic.com/media/d24577_7ab8f1b639ee4f2fb5ab991fc6acf49c~mv2.jpg"
        item2['SubWebsite'] = 'https://www.builddavinci.com/'
        item2['AmenityType'] = ''
        yield item2


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl builddavinci'.split())


