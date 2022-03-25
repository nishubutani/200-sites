


# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class vtshomeshomesSpider(scrapy.Spider):
    name = 'garrisonhomes'
    allowed_domains = []
    start_urls = ['https://www.garrisonhomes.com/portfolio/']

    builderNumber = "25992"

    def parse(self, response):
        print('--------------------')

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        imagess = []
        images = response.xpath('//a[@class="x-div portfolio-item-link"]/div/div/@data-bg').extract()
        for imag in images:
            print(imag)
            imagess.append(imag)
        imagess = "|".join(imagess)
        print(imagess)


        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = '51152'
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '19413 Jingle Shell Way'
        item['City'] = 'Lewes'
        item['State'] = 'DE'
        item['ZIP'] = '19958'
        item['AreaCode'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Prefix'] = ""
        item['Email'] = ''
        item['SubDescription'] = "For over 20 years, Garrison Homes has fine-tuned every aspect of the home building process. We ensure each home is built exactly as the customer desires, and we ensure the project stays on time and within budget. We’re confident that you will be at ease throughout the construction of your new home"
        item['SubImage'] = imagess
        item['SubWebsite'] = 'https://www.garrisonhomes.com/'
        item['AmenityType'] = ''
        yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl garrisonhomes".split())