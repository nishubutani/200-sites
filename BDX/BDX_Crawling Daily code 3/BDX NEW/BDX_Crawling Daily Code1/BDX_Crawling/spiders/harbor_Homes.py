import re

import scrapy
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision



class HarborHomesSpider(scrapy.Spider):
    name = 'harbor_Homes'
    # allowed_domains = ['www.harborhomes.net']
    start_urls = ['https://harborhomes.net/']
    builderNumber = 27844

    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        SubImage1 = re.findall(r"background-image: url(.*?)'><div class='container'>", response.text)
        Image = []
        for img in SubImage1:
            image = 'https://harborhomes.net/' + str(img).replace('(','').replace(')','')
            Image.append(image)
        Image = '|'.join(Image)

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '480 Merchant Dr'
        item['City'] = 'Norman'
        item['State'] = 'OK'
        item['ZIP'] = '73069'
        item['AreaCode'] = '405'
        item['Prefix'] = '790'
        item['Suffix'] = '0629'
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = '''Harbor Homes is a family owned custom new home builder.  The company started in 1997.Harbor Homes has one of the finest corporate office among all builders in the Oklahoma City metro with a state of the art custom design center.Harbor Homes is an industry leader and well respected among our peers, banks, and developers.Harbor Homes has been in business for 23 years and built over 700 homes for Oklahoma families. We received the award as “2015 Best Home Builder in Oklahoma”.  We have been a top builder in the Oklahoma City area since 1998 as recorded by the Journal Record.  We received the Excellence in manufacturing award in 2013.  Harbor Homes is a member of the BASCO and also a member of the Better Business Bureau and has maintained an A+ rating since joining the BBB in 2005.'''
        item['SubImage'] = Image
        item['SubWebsite'] = response.url
        yield item

if __name__ == '__main__':

    from scrapy.cmdline import execute
    execute("scrapy crawl harbor_Homes".split())