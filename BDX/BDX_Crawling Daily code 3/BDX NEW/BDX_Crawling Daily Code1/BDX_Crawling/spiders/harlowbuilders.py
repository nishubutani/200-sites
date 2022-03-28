

# -*- coding: utf-8 -*-
import json
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'harlowbuilders'
    allowed_domains = ['harlowbuilders.net']
    start_urls = ['https://www.harlowbuilders.net/']
    builderNumber = 27918


    def parse(self, response):


        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = '701 North Market Street'
        item2['City'] = 'Troy'
        item2['State'] = 'OH'
        item2['ZIP'] = '45373'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "Home Pro Custom Builders has proudly served the area for more than 10 years. We work closely with our clients to bring their ideas and dreams to life."
        item2['SubImage'] = "https://www.harlowbuilders.net/wp-content/gallery/exterior/2801-Stonebridge-1.jpg|https://www.harlowbuilders.net/wp-content/gallery/exterior/2834-Stonebridge-1.jpg|https://www.harlowbuilders.net/wp-content/gallery/exterior/2870-Stonebridge-1.jpg|https://www.harlowbuilders.net/wp-content/gallery/exterior/640-Rosecrest-1.jpg|https://www.harlowbuilders.net/wp-content/gallery/exterior/2741-Stonebridge-1.jpg|https://www.harlowbuilders.net/wp-content/gallery/exterior/639-Sedgwick-1.jpg"
        item2['SubWebsite'] = 'https://www.harlowbuilders.net/'
        item2['AmenityType'] = ''
        yield item2

        link = 'https://www.harlowbuilders.net/our-homes/the-competitor-series/'
        yield scrapy.FormRequest(url=link, callback=self.plan, dont_filter=True)


    def plan(self, response):

        links = response.xpath('//a[@class="chb-view-button"]/@href').extract()
        for link in links:
            print(link)
            yield scrapy.FormRequest(url=link,callback=self.plan_details,dont_filter=True)

    def plan_details(self,response):

        try:
            Type = 'SingleFamily'
        except Exception as e:
            Type = 'SingleFamily'
            print(e)

        try:
            PlanName = response.xpath("//h1/text()").extract_first('').strip()
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

            BaseSqft = response.xpath("//*[contains(text(),'Sq Ft')]/text()").extract_first(default='0')
            # BaseSqft = BaseSqft.split(':')[-1].strip()
            if '_' in BaseSqft:
                BaseSqft = BaseSqft.split("-")[1]

            BaseSqft = BaseSqft.replace(',', '')
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]

        except Exception as e:
            print(e)

        try:
            Baths = response.xpath("//*[contains(text(),'BATH')]/text()").extract_first(
                default='0')
            Baths = re.findall(r"(\d+)", Baths)[0]

            if len(Baths) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0

        except Exception as e:
            Baths = 0
            print(e)

        try:
            Bedrooms = response.xpath("//*[contains(text(),'BED')]/text()").extract_first(default='0')
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)
            Bedrooms = 0

        try:
            Garage = response.xpath("//*[contains(text(),'Car Garage')]/text()").extract_first('')
            # Garage = response.xpath(".//*[contains(text(),'Garages')]/../text()").extract_first(default='0')
            Garage = re.findall(r"(\d+)", Garage)[0]

        except Exception as e:
            print(e)
            Garage = "0"

        try:
            Description = ""
        except Exception as e:
            print(e)
            Description = ""

        try:
            ElevationImage = response.xpath("//div[@class='et_pb_module et_pb_image et_pb_image_0']/a/@href").extract_first(default='')
        except Exception as e:
            print(e)
            ElevationImage = ""

        try:
            PlanWebsite = response.url
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


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl harlowbuilders'.split())





