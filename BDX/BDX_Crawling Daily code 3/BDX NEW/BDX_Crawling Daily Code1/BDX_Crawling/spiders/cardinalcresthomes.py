
# -*- coding: utf-8 -*-
import json
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'cardinalcresthomes'
    allowed_domains = ['cardinalcresthomes.com']
    start_urls = ['https://www.cardinalcresthomes.com/']
    builderNumber = 49268


    def parse(self, response):

        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = '1539 SWIFT ST.'
        item2['City'] = 'KANSAS'
        item2['State'] = 'MO'
        item2['ZIP'] = '64116'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "Meet a custom home builder that provides true custom experiences. From the in house architectural services, to the step by step interior design consulting, we strive to make the home building process memorable. Cardinal Crest creates timeless homes that will focus equally on design and function. Utilizing the newest technologies we put as much emphasis on the aesthetics as the structural components to ensure a quality built home."
        item2['SubImage'] = "https://www.cardinalcresthomes.com/cache/media/511_10500-001-511-600-600.jpg|https://www.cardinalcresthomes.com/cache/media/1042_11950-002-1042-600-600.jpg|https://www.cardinalcresthomes.com/cache/media/5515_cc-exterior-13-5515-600-600.jpg|https://www.cardinalcresthomes.com/cache/media/3820_8905-001-3820-600-600.jpg|https://www.cardinalcresthomes.com/cache/media/5914_roundtwo-6-5914-600-600.jpg"
        item2['SubWebsite'] = 'https://www.cardinalcresthomes.com/'
        item2['AmenityType'] = ''
        yield item2

        link = 'https://www.cardinalcresthomes.com/projects/grid?page=1&method=single'
        yield scrapy.FormRequest(url=link,callback=self.parse3,dont_filter=True)

    def parse3(self,response):

        data = json.loads(response.text)
        size1 = len(data)
        for i in range(0, int(size1)):
            try:
                Type = 'SingleFamily'
            except Exception as e:
                Type = 'SingleFamily'
                print(e)

            try:
                PlanName = data['results'][i]['name']
            except Exception as e:
                PlanName = ''
                print(e)

            try:
                PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % PlanNumber, "wb")
                f.write(response.body)
                f.close()
            except Exception as e:
                print(e)

            try:
                SubdivisionNumber = self.builderNumber
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
                BasePrice = 0.00
            except Exception as e:
                print(e)

            try:
                BaseSqft = 0
                # BaseSqft = response.xpath('//strong[@class="total_heated_area"]/text()').extract_first(default='0')
                # if '_' in BaseSqft:
                #     BaseSqft = BaseSqft.split("-")[1]
                # BaseSqft = BaseSqft.replace(',', '')
                # BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]

            except Exception as e:
                print(e)

            try:
                Baths = data['results'][i]['project_bathrooms']
                Baths = re.findall(r"(\d+)", Baths)[0]
                if len(Baths) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0

            except Exception as e:
                Baths = 0
                print(e)

            try:
                Bedrooms = data['results'][i]['project_bathrooms']
                Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            except Exception as e:
                print(e)
                Bedrooms = 0

            try:
                # Garage = response.xpath('//strong[@class="garage"]/text()').extract_first('')
                # Garage = response.xpath(".//*[contains(text(),'Garages')]/../text()").extract_first(default='0')
                # Garage = re.findall(r"(\d+)", Garage)[0]
                Garage = "0"
            except Exception as e:
                print(e)
                Garage = "0"

            try:
                Description = ""
            except Exception as e:
                print(e)
                Description = ""

            try:
                ElevationImage = data['results'][i]['images']
                ElevationImage = "|".join(ElevationImage)
            except Exception as e:
                print(e)
                ElevationImage = ""

            try:
                PlanWebsite = 'https://www.cardinalcresthomes.com/'
            except Exception as e:
                print(e)

                # ----------------------- Don't change anything here --------------
            unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
                    10 ** 30)  # < -------- Changes here
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


        nxt_page = data['next_page']
        if nxt_page != '':
            nxt = f'https://www.cardinalcresthomes.com/projects/grid?page={nxt_page}&method=single'
            yield scrapy.FormRequest(url=nxt, callback=self.parse3, dont_filter=True)
        else:
            pass


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl cardinalcresthomes'.split())






