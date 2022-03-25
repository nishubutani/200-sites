# -*- coding: utf-8 -*-
import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision


class AxioshomesSpider(scrapy.Spider):
    name = 'axioshomes'
    allowed_domains = ['axioshomes.com']
    start_urls = ['http://axioshomes.com/']
    builderNumber = '14621'

    def parse(self, response):
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
        item['Street1'] = '975 Fee Drive'
        item['City'] = 'Sacramento'
        item['State'] = 'CA'
        item['ZIP'] = '95815'
        item['AreaCode'] = '916'
        item['Prefix'] = '614'
        item['Suffix'] = '9300'
        item['Extension'] = ""
        item['Email'] = 'support@axioshomes.com'
        item['SubDescription'] = 'Axios Homes, Inc. provides a two-year limited warranty on all of our homes.  That’s twice as long as the industry standard offered by our competitors!  Through our commitment to quality control as well as the high standards shared by our trade partners, we guarantee our homes to be free of defects in materials and workmanship.  Should a defect occur in any item covered by our warranty, Axios Homes, Inc. will repair or replace that item to the high standard with which your home was built.'
        item[
            'SubImage'] = 'http://users.neo.registeredsite.com/7/6/2/18070267/assets/wildflower-8205.jpg|http://users.neo.registeredsite.com/7/6/2/18070267/assets/Axios-46.jpg|http://users.neo.registeredsite.com/7/6/2/18070267/assets/Axios-5.jpg|http://users.neo.registeredsite.com/7/6/2/18070267/assets/Axios-3.jpg|http://users.neo.registeredsite.com/7/6/2/18070267/assets/wildflower-8142.jpg|http://users.neo.registeredsite.com/7/6/2/18070267/assets/Axios-6858353.jpg|http://users.neo.registeredsite.com/7/6/2/18070267/assets/unspecified-543331.jpeg'
        item['SubWebsite'] = response.url
        yield item

from scrapy.cmdline import execute
# execute("scrapy crawl axioshomes".split())

