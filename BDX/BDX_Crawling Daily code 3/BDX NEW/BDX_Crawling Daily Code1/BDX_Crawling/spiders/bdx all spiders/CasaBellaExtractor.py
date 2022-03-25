# -*- coding: utf-8 -*-
import hashlib
import re
import os
import scrapy
from scrapy.cmdline import execute
from BDX_Crawling.export_xml import genxml
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision


class CasabellaextractorSpider(scrapy.Spider):
    name = 'CasaBellaExtractor'
    allowed_domains = ['www.casabellanm.com']
    start_urls = ['http://www.casabellanm.com/']
    builderNumber = 919323714075623547930045788819

    def parse(self, response):
        # ----------------------------------------------------------------- #
        # subdivision == > Builders communities
        # Plans == > available plans in that communities
        # specs == > available Homes in plans

        # ----------------------- Don't change anything here -------------- #

        # item = BdxCrawlingItem_Corporation()
        # item['CorporateBuilderNumber'] = inp.CorporateBuilderNumber
        # item['CorporateName'] = inp.CorporateName
        # item['CorporateState'] = inp.CorporateState
        # yield item
        #
        # item1 = BdxCrawlingItem_Builder()
        # item1['BuilderNumber'] = int(hashlib.md5(bytes(inp.BuilderWebsite, "utf8")).hexdigest(), 16) % (10 ** 30)
        # item1['BrandName'] = inp.BrandName
        # item1['BrandLogo_Med'] = 'http:'+response.xpath(
        #     '//img[@alt="Casa Bella Construction"]/@src').extract_first(default="")
        # item1['ReportingName'] = inp.ReportingName
        # item1['DefaultLeadsEmail'] = inp.DefaultLeadsEmail
        # item1['BuilderWebsite'] = inp.BuilderWebsite
        # item1['CorporateBuilderNumber'] = inp.CorporateBuilderNumber
        # yield item1

        # ----------------------------------------------------------------- #

        # In case you can't able to find any communities, then please use this line of code, and reference this SubdivisionNumber in All Plans

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = response.xpath('//h1[@data-content-field="site-title"]/a/img/@alt').extract_first()
        item['SubdivisionNumber'] = int(hashlib.md5(bytes(item['SubdivisionName'], "utf8")).hexdigest(), 16) % (10 ** 30)
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 1

        # enter any address you fond on the website.
        Street1 = 'PO BOX 30425'
        item['Street1'] = Street1
        item['City'] = 'ALBUQUERQUE'
        item['State'] = 'NM'
        item['ZIP'] = '87199'
        item['AreaCode'] = '505'
        item['Prefix'] = '385'
        item['Suffix'] = '0606'
        item['Extension'] = ''
        item['Email'] = 'd@casabellanm.com'
        item['SubDescription'] = response.xpath('normalize-space(//h2[contains(text(),"Mission Statement")]/following-sibling::p/text())').extract_first(default='')
        # SubImage = re
        item['SubImage'] = ''
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl CasaBellaExtractor --nolog'.split())