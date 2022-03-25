# -*- coding: utf-8 -*-

import re

import scrapy
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision


class betterbuiltnwfSpider(scrapy.Spider):
    name = 'betterbuiltnwf'
    allowed_domains = []
    start_urls = ['http://www.betterbuiltnwf.com/']
    builderNumber = 54046
    count = 0

    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        SubImage = ' , '.join(response.xpath('//ul[@class="slides"]/li/div[2]/@style').extract()).replace('"background-image: url(&quot;','').replace('&quot;); max-width: 100%; height: 442px;" data-imgwidth="1800"></div>','').replace('url(','').replace(');max-width:100%;height:650px;filter:','').replace("progid:DXImageTransform.Microsoft.AlphaImageLoader(src='","").replace("sizingMethod='scale')'; , background-image:","").replace("sizingMethod='scale');-ms-filter:","").replace("sizingMethod='scale')';","")
        # img_ls = []
        # for i in SubImage:
        #     img = re.findall(r'&quot;(.*?)&quot;', i)
        #     img_ls.append(img)
        # image1 = " , ".join(SubImage)
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = 'BetterBuilt of Northwest Florida 210 Government Avenue'
        item['City'] = 'Niceville'
        item['State'] = 'FL'
        item['ZIP'] = '32578'
        item['AreaCode'] = '850'
        item['Prefix'] = '729'
        item['Suffix'] = '2484'
        item['Extension'] = ""
        item['Email'] = 'info@betterbuiltnwf.com'
        item['SubDescription'] = '''As one of the most experienced and respected luxury home builders on Northwest Florida's Emerald Coast, BetterBuilt prides itself in building homes to the highest standards of workmanship, design, and engineering. BetterBuilt is not just our name—it is our mission.'''
        # item['SubImage'] = response.xpath('//ul[@class="slides"]/li/div[2]/@style').extract()
        item['SubImage'] = SubImage
        item['SubWebsite'] = response.url
        yield item

        url = 'http://www.betterbuiltnwf.com/'
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.Plans_link)


    def Plans_link(self,response):
        urls = response.xpath('//ul[@class="fusion-megamenu "]/li/ul/li/a/@href').extract()
        for i in urls:
            url = str(i)
            print('PLANS------------------->',url)
            yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.Plans_Details)

    def Plans_Details(self, response):

        Type = 'SingleFamily'

        PlanName = response.xpath('//div[@class="fusion-page-title-captions"]/h1/text()').extract_first().strip()

        PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)

        SubdivisionNumber = self.builderNumber

        PlanNotAvailable = 0

        PlanTypeName = 'Single Family'

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)
        #
        Bedrooms = response.xpath('//div[@class="table-2"]/table/tbody/tr[5]/td[2]/text()').extract_first()
        a = response.xpath('//div[@class="table-2"]/table/tbody/tr[6]/td[2]/text()').extract_first()
        Baths = a[0]
        Bath = re.findall(r"(\d+)", a)
        tmp = Bath
        if len(tmp) > 1:
            HalfBaths = 1
        else:
            HalfBaths = 0

        if '½' in a:
            HalfBaths = 1
        try:
            Garage = response.xpath('//div[@class="table-2"]/table/tbody/tr[7]/td[2]/text()').extract_first()
            Garage = re.findall(r"(\d+)", Garage)
            Garage = Garage[0]
        except:
            Garage = 0
        try:
            BaseSqft = response.xpath('//div[@class="table-2"]/table/tbody/tr[2]/td[2]/text()').extract_first().replace(',','')
        except:
            BaseSqft = 0
        try:
            if response.xpath('//div[@class="fusion-column-wrapper"]/p[1]/text()').getall() !=None:
                Description = ''.join(response.xpath('//div[@class="fusion-column-wrapper"]/p[1]/text()').extract()).strip().replace('\\x80', '').replace('\\xE2', '').replace('\\xB2', '')
            else:
                Description = 0
        except:
            Description = 0
        #
        try:
            ElevationImage1 = '|'.join(response.xpath('//ul[@class="slides"]/li/span/img/@src').extract())
            ElevationImage2 = response.xpath('//ul[@class="fusion-carousel-holder"]/li/div/div/a/@href').extract()
            EI2 = []
            for i in ElevationImage2:
                img = 'http://www.betterbuiltnwf.com' + str(i)
                EI2.append(img)

            ElevationImage = ElevationImage1 + '|'.join(EI2)
            # ElevationImage = '|'.join(EI2)
        except Exception as e:
            ElevationImage = 0
            print(str(e))
        #
        try:
            Price1  = response.xpath('//div[@class="table-2"]/table/tbody/tr[8]/td[2]/text()').get().replace('$','').replace(',','')
            Price = re.findall(r"(\d+)", Price1)
            if Price == []:
                BasePrice = 0
            else:
                BasePrice = str(Price)
        except:
            BasePrice = 0

        if 'Family Traditions' in PlanName:
            Bedrooms = 7
            Baths = 7
            HalfBaths = 1
            Garage = 1
            BasePrice = 2795000
        if 'Allamanda “B”' in PlanName:
            Bedrooms = 4
            Baths = 4
            HalfBaths = 0
            Garage = 1
            BasePrice = 600
        if 'Family Ties' in PlanName:
            Bedrooms = 5
            Baths = 5
            HalfBaths = 1
            Garage = 1
            BasePrice = 1375000
        if 'Tupelo' in PlanName:
            Bedrooms = 4
            Baths = 2
            HalfBaths = 1
            Garage = 0
            BasePrice = 500
        if 'Sanibel' in PlanName:
            Bedrooms = 3
            Baths = 3
            HalfBaths = 1
            Garage = 2
            BasePrice = 600
        if 'The Gathering' in PlanName:
            Bedrooms = 4
            Baths = 4
            HalfBaths = 0
            Garage = 0
            BasePrice = 860000
        if 'Hideaway' in PlanName:
            Bedrooms = 4
            Baths = 4
            HalfBaths = 0
            Garage = 0
            BasePrice = 895000

        unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['Type'] = Type
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number  # < -------- Changes here
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

        #

#
# from scrapy.cmdline import execute
# execute("scrapy crawl betterbuiltnwf".split())