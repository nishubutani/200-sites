# -*- coding: utf-8 -*-
import hashlib
import re
import requests
import scrapy
from decimal import Decimal
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class CelebrityCustomHomesSpider(scrapy.Spider):
    name = 'Celebrity_Custom_Homes'
    allowed_domains = ['http://www.celebrityhomescolorado.com/']
    start_urls = ['http://www.celebrityhomescolorado.com/']

    builderNumber = "52829"


    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #
        image1 = response.xpath('//*[@class="bg-image-full"]/img/@src').extract_first()
        image = '|'.join(response.xpath('//*[@class="h-fade"]/img/@src').extract())
        images = f"{image1}|{image}"
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = "10463 Park Meadows Dr., Suite 207"
        item['City'] = "Lone Tree"
        item['State'] = "CO"
        item['ZIP'] = "80124"
        item['AreaCode'] = "303"
        item['Prefix'] = "792"
        item['Suffix'] = "7357"
        item['Extension'] = ""
        item['Email'] = "info@celebritycommunities.com "
        item['SubDescription'] = response.xpath('//p/text()').extract_first().strip()
        item['SubImage'] = images
        item['SubWebsite'] = "https://www.celebrityhomescolorado.com/"
        yield item
        try:
            link = response.xpath('//*[contains(text(),"Home Plans")]/@href').extract_first()
            PlanDetails = {}
            yield scrapy.Request(url=link, callback=self.plans_details, meta={'sbdn': self.builderNumber, 'PlanDetails': PlanDetails}, dont_filter=True)
        except Exception as e:
            print(e)

    def plans_details(self, response):
        plandetails = response.meta['PlanDetails']
        Plan_selectors = response.xpath('//*[@class="kc_text_block"]/h3')
        for Plan_selector in Plan_selectors:
            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                SubdivisionNumber = response.meta['sbdn']
            except Exception as e:
                print(e)

            try:
                PlanName = ''.join(Plan_selector.xpath('./strong/text()').extract()).strip().replace(':','')
            except Exception as e:
                print(e)

            try:
                PlanNumber = int(hashlib.md5(bytes(response.url+PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % PlanNumber, "wb")
                f.write(response.body)
                f.close()
            except Exception as e:
                print(e)

            try:
                PlanNotAvailable = 0
            except Exception as e:
                print(e)

            try:
                PlanTypeName = 'Single Family'
            except Exception as e:
                print(e)

            try:
                BasePrice = '0'
            except Exception as e:
                print(e)

            try:
                Baths = Plan_selector.xpath('./../div[@class="innder_p_block"]/p[contains(text(),"bath")]/text()').extract_first().split(',')[1].strip().replace(' ½','.5')
                tmp1 = re.findall(r"[0-9]\.?[0-9]?", Baths)
                Baths = max(tmp1)
                tmp = re.findall(r"(\d+)", Baths)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                print(e)

            try:
                Bedrooms = str(Plan_selector.xpath('./../div[@class="innder_p_block"]/p[contains(text(),"bedrooms")]/text()').extract_first(default='0').strip()).replace(",","")
                Bedrooms = re.findall('(.*?) bedrooms', Bedrooms)[0]
                Bedrooms = re.findall(r'(\d+)', Bedrooms)[0]
            except Exception as e:
                print(e)

            try:
                Garage = Plan_selector.xpath('./../div[@class="innder_p_block"]/p[contains(text(),"car")]/text()').extract_first().split(',')[2]
                Garage = re.findall(r"(\d+)", Garage)
                Garage = max(Garage)
                BaseSqft = str(Plan_selector.xpath('./../div[@class="innder_p_block"]/p[contains(text(),"finished square feet")]/text()').extract_first(default='0').strip()).replace(",","")
                BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
            except Exception as e:
                print(e)

            try:
                Description = Plan_selector.xpath('./../div[@class="floor_descriptions"]/p/text()').extract_first().strip()
            except Exception as e:
                print(e)

            try:
                ElevationImage = Plan_selector.xpath('./../../..//img/@src').extract_first().strip()
            except Exception as e:
                print(e)

            try:
                PlanWebsite = response.url
            except Exception as e:
                print(e)

            SubdivisionNumber = SubdivisionNumber  # if subdivision is there
            # SubdivisionNumber = self.builderNumber #if subdivision is not available
            unique = str(PlanNumber) + str(SubdivisionNumber)
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            plandetails[PlanName] = unique_number
            item = BdxCrawlingItem_Plan()
            item['Type'] = Type
            item['PlanNumber'] = PlanNumber
            item['unique_number'] = unique_number
            item['SubdivisionNumber'] = SubdivisionNumber
            item['PlanName'] = PlanName
            item['PlanNotAvailable'] = PlanNotAvailable
            item['PlanTypeName'] = PlanTypeName
            item['BasePrice'] = BasePrice
            item['BaseSqft'] = BaseSqft
            item['Baths'] = Baths
            item['HalfBaths'] = HalfBaths
            item['Bedrooms'] = Bedrooms
            item['Garage'] = Garage
            item['Description'] = Description
            item['ElevationImage'] = ElevationImage
            item['PlanWebsite'] = PlanWebsite
            yield item

from scrapy.cmdline import execute
# execute("scrapy crawl Celebrity_Custom_Homes".split())