import hashlib

import scrapy
import re
import json
import os
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, \
    BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision
import requests
from scrapy.http import HtmlResponse
from scrapy.cmdline import execute


class AffordableHomesSuperCenter(scrapy.Spider):
    name = 'AffordableHomesSuperCenter'
    allowed_domains = []
    start_urls = ['https://www.affordablehomessupercenter.com/']
    builderNumber = '62135'

    def parse(self,response):
        try:
            SubDescription = ''.join(response.xpath('//*[@class="elementor-element elementor-element-5fd61103 elementor-widget elementor-widget-text-editor"]//p//text()').extract()).strip()
            SubImage = '|'.join(response.xpath('//*[@class="fp-card-image lazyload"]/@data-bg').extract())
            item = BdxCrawlingItem_subdivision()
            item['sub_Status'] = "Active"
            item['SubdivisionNumber'] = ''
            item['BuilderNumber'] = self.builderNumber
            item['SubdivisionName'] = "No Sub Division"
            item['BuildOnYourLot'] = 0
            item['OutOfCommunity'] = 0
            item['Street1'] = '10223 US Hwy 49 N'
            item['City'] = 'Brookland'
            item['State'] = 'AR'
            item['ZIP'] = '72417'
            item['AreaCode'] = '870'
            item['Prefix'] = "932"
            item['Suffix'] = "5692"
            item['Extension'] = ""
            item['Email'] = "info@affordablehomessupercenter.com"
            item['SubDescription'] = SubDescription
            item['SubImage'] = SubImage
            item['SubWebsite'] = response.url
            item['AmenityType'] = ''
            yield item
        except Exception as e:
            print(e)

        url = ["https://www.affordablehomessupercenter.com/floor-plans/","https://www.affordablehomessupercenter.com/inventory/"]
        for i in url:
            link = i
            yield scrapy.FormRequest(url=link, callback=self.firstlevel, dont_filter=True,
                                     meta={'SubDescription': SubDescription,'SubImage':SubImage})

    def firstlevel(self, response):
        SubDescription = response.meta['SubDescription']
        # ElevationImage = response.xpath('//*[@class="fp-card-image lazyload"]/@data-bg').extract()
        SubImage = response.meta['SubImage']
        try:
            divs = response.xpath('//*[contains(text(),"Info")]/../a/@href').extract()
            for i in divs:
                link = "https://www.affordablehomessupercenter.com" + i
                yield scrapy.FormRequest(url='https://www.affordablehomessupercenter.com/plan/228480/ascend/the-pursuit-2860h22a1a/', callback=self.secondlevel, dont_filter=True,
                                         meta={'SubDescription': SubDescription, 'SubImage': SubImage})
            next = "https://www.affordablehomessupercenter.com" + response.xpath('//*[contains(text(),"→")]/../a/@href').extract_first()
            yield scrapy.FormRequest(url=next, callback=self.firstlevel, dont_filter=True,
                                     meta={'SubDescription': SubDescription, 'SubImage': SubImage})
        except Exception as e:
            print(e)

    def secondlevel(self, response):

        try:
            Type = "SingleFamily"
        except Exception as e:
            Type = ""
            print(e)

        try:
            PlanName = ''.join(response.xpath('//h1[@class="elementor-heading-title elementor-size-default"]//text()').extract())
        except Exception as e:
            PlanName = ""
            print(e)

        try:
            PlanNumber1 = str(PlanName) + str(response.url)
            PlanNumber = int(hashlib.md5(bytes(PlanNumber1, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % PlanNumber, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
            print(e)

        try:
            BasePrice = '0'
        except Exception as e:
            BasePrice = '0'
            print(e)

        try:
            BaseSqft = response.xpath('//*[contains(text(),"Sq. Ft.")]/.//text()').extract_first().strip().split("Sq. Ft.")[0]
            # if int(BaseSqft) <= 500:
            #     BaseSqft = "0"
            # else:
            #     BaseSqft = BaseSqft
        except Exception as e:
            BaseSqft = "0"
            print(e)

        try:
            Baths = response.xpath('//*[contains(text(),"Baths")]/./text()').extract_first().strip().split("Baths")[0]
            if "." in Baths:
                Baths = Baths.split(".")[0]
                HalfBaths = "1"
            else:
                HalfBaths = "0"
        except Exception as e:
            Baths = "0"
            print(e)

        try:
            Bedrooms = response.xpath('//*[contains(text(),"Beds")]/./text()').extract_first().strip().split("Beds")[0]
        except Exception as e:
            Bedrooms = "0"
            print(e)

        try:
            Garage = "0"
        except Exception as e:
            Garage = "0"
            print(e)
        #
        try:
            Description = ''.join(response.xpath('//*[@class="elementor-element elementor-element-2a4bc742 elementor-widget elementor-widget-text-editor"]//text()').extract()).strip().replace("′", "")
            # if len(Description) <= 15:
            #     Description = response.meta['SubDescript"ion']"
            # # elif Description == "":
            #     Description = response.meta['SubDescription']

        except Exception as e:
            Description = ""
            print(e)

        try:
            ElevationImage = response.xpath('//*[@class="gallery-icon "]//a/@href').extract()
            if ElevationImage != []:
                ElevationImage = "|".join(ElevationImage)

        except Exception as e:
            ElevationImage = ""
            print(e)
        unique = str(PlanName)+ str(self.builderNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['Type'] = Type
        item['PlanNumber'] = PlanNumber
        item['SubdivisionNumber'] = self.builderNumber
        item['PlanName'] = PlanName
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = "Single Family"
        item['BasePrice'] = BasePrice
        item['BaseSqft'] = BaseSqft
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = Description
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = response.url
        item['unique_number'] = unique_number
        yield item

if __name__ == '__main__':
    execute("scrapy crawl AffordableHomesSuperCenter".split())