
# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'lindberghproperties'
    allowed_domains = ['https://lindberghproperties.com/']
    start_urls = ['https://www.lindberghproperties.com/']

    builderNumber = "372381131645426700306955805013"

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
        item['Street1'] = 'P.O. Box 29318 St.'
        item['City'] = 'Louis'
        item['State'] = 'MO'
        item['ZIP'] = '63126'
        item['AreaCode'] = '314'
        item['Prefix'] ='965'
        item['Suffix'] = '3638'
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = 'Lindbergh Properties Construction has been involved in the planning, development, and building of new communities and homes in the Greater St. Louis Metropolitan area for over 30 years. We are dedicated to value and customer service. We have earned an award-winning reputation for our service and guidance to our customers. Whether it is selecting the perfect floor plan or securing financing, we are there every step of the way.'
        item['SubImage'] = 'https://www.lindberghproperties.com/wp-content/uploads/2017/08/0Slide1.jpg|https://www.lindberghproperties.com/wp-content/uploads/2017/08/0Slide2.jpg|https://www.lindberghproperties.com/wp-content/uploads/2017/08/0Slide3.jpg|https://www.lindberghproperties.com/wp-content/uploads/2017/08/0Slide5.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        # --------------------------------------------------------------------- #


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl lindberghproperties'.split())