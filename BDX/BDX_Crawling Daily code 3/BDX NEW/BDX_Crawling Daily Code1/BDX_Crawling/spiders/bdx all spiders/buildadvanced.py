
# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'buildadvanced'
    allowed_domains = ['https://buildadvanced.com/']
    start_urls = ['https://buildimmaculate.com/']

    # builderNumber = "169997824428359468527692220082"
    builderNumber = "24008"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()


        # images = ''
        # image = response.xpath('//div[@class="widget animated fadeInUpShort"]//img[@class="lazy loaded"]').extract()
        # for i in image:
        #     images = images + i + '|'
        # images = images.strip('|')

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '4854 Southwest 91 Court'
        item['City'] = 'Gainesville'
        item['State'] = 'FL'
        item['ZIP'] = '32608'
        item['AreaCode'] = '352'
        item['Prefix'] ='379'
        item['Suffix'] = '0898'
        item['Extension'] = ""
        item['Email'] = 'info@buildadvanced.com'
        item['SubDescription'] = 'You may find a plan on our website that can be modified especially for you; or, you may choose to use pictures, fragments of plans and your imagination to allow us to help you to create a plan that is truly unique. Either way, Advanced Building Concepts designs, builds and tailors your home to your needs, desires and budget.'
        item['SubImage'] = 'https://buildadvanced.com/wp-content/uploads/2020/11/print_13638SW6thRd_15-600x450.jpg|https://buildadvanced.com/wp-content/uploads/2020/11/print_13638SW6thRd_01-600x450.jpg|https://buildadvanced.com/wp-content/uploads/2020/11/print_13638SW6thRd_03-600x450.jpg|https://buildadvanced.com/wp-content/uploads/2020/11/print_13638SW6thRd_05-600x450.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item



    # --------------------------------------------------------------------- #

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl buildadvanced'.split())