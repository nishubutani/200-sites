# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class GrandCherrySpider(scrapy.Spider):
    name = 'grand_cherry'
    allowed_domains = ['grandcherry.com']
    start_urls = ['http://www.grandcherry.com']
    builderNumber = "123839220840978789482500090921"

    def parse(self, response):

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        images = ''
        image = response.xpath('//*[contains(@src,"images/navigation/headers")]/@src').extract()
        for i in image:
            images = images + self.start_urls[0] + i + '|'
        images = images.strip('|')

        images2 = ''
        image2 = response.xpath('//*[contains(@src,"images/ga")]/@src').extract()
        for i in image2:
            images2 = images2 + self.start_urls[0] + i + '|'
        images2 = images2.strip('|')

        finalimage = images2 + images


        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = '210 Little Lake Dr., Suite 11'
        item2['City'] = 'Ann Arbor'
        item2['State'] = 'MI'
        item2['ZIP'] = '48103'
        item2['AreaCode'] = '231'
        item2['Prefix'] = "421"
        item2['Suffix'] = "8726"
        item2['Extension'] = ""
        item2['Email'] = "info@grandcherry.com"
        item2['SubDescription'] = "Grand Cherry Builders has more than 30 years of experience in custom building, and new home construction. With our knowledge, experience and professionalism we are able to deliver results our unique clientele expect for their biggest investment— their dream home. We take a full-service, personal approach to every project. We are fully licensed (Michigan builders license #2102146237) and fully insured. Customer satisfaction and open, honest communication are top priorities for everyone at our company. We specialize in:Custom, Year-Round Homes,Vacation Homes,Project Management"
        item2['SubImage'] = finalimage
        item2['SubWebsite'] = ''
        item2['AmenityType'] = ""
        yield item2

        # -------------------------------------------------------------------- #

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl grand_cherry'.split())