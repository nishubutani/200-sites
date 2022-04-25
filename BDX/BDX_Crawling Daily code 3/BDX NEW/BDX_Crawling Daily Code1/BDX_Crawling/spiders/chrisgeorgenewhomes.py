
# -*- coding: utf-8 -*-
import json
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'chrisgeorgenewhomes'
    allowed_domains = ['cardinalcresthomes.com']
    start_urls = ['https://www.cardinalcresthomes.com/']
    builderNumber = 49270


    def parse(self, response):

        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = '128 Boston Post Road'
        item2['City'] = 'Lyme'
        item2['State'] = 'CT'
        item2['ZIP'] = '06333'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "We believe that beautiful homes begin with customers who want to love the home in which they live … customers who don’t want to settle for a pre-owned house that doesn’t fit their needs or taste. Our philosophy for well over 30 years has been to build a well designed, quality constructed house that is a joy to live in A house that our customers are proud to call Home."
        item2['SubImage'] = "http://www.chrisgeorgenewhomes.com/images/photos/about-us/101_Daigle-On-Front-Porch.jpg|http://www.chrisgeorgenewhomes.com/lib/image.asp?ImageID=267542&ImageType=0|http://www.chrisgeorgenewhomes.com/lib/image.asp?ImageID=267401&ImageType=0"
        item2['SubWebsite'] = 'https://www.cardinalcresthomes.com/'
        item2['AmenityType'] = ''
        yield item2

        link = 'http://www.chrisgeorgenewhomes.com/docs/inventory/models-floorplans.asp'
        yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)

    def parse2(self, response):
        links = response.xpath('//span[@class="category-center"]/../@href').extract()[2:]
        for link in links:
            link = 'http://www.chrisgeorgenewhomes.com/docs/inventory/' + link
            print(link)
            yield scrapy.FormRequest(url=link,callback=self.parse3,dont_filter=True)


    def parse3(self, response):
        links = response.xpath('//a[@class="listing-div"]/@href').extract()
        for link in links:
            link = 'http://www.chrisgeorgenewhomes.com/docs/inventory/' + link
            print(link)
            yield scrapy.FormRequest(url=link,callback=self.parse4,dont_filter=True)

            # break

    def parse4(self,response):

        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//h1/text()').extract_first(
                default='').strip()
            print(PlanName)
        except Exception as e:
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
            print(PlanName)
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
            Baths = response.xpath("//*[contains(text(),'Bath')]/following-sibling::div/text()").extract_first(default='0').strip().replace(",","")
            # if '+' in Baths:
            #     Baths = Baths.split("+")
            Baths = re.findall(r"(\d+)", Baths)
            Bath = Baths[0]
            print(Baths)
            if len(Baths) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            print(e)

        try:
            Bedrooms = response.xpath("//*[contains(text(),'Bed')]/following-sibling::div/text()").extract_first(default='0').strip().replace(",","")
            print(Bedrooms)
        except Exception as e:
            print(e)

        try:
            Garage = response.xpath("//*[contains(text(),'Garage')]/text()").extract_first(default='0').strip().replace(",","")
            Garage = re.findall(r"(\d+)", Garage)[0]
            print(Garage)
        except Exception as e:
            print(e)
            Garage = 0.0

        try:
            BaseSqft = response.xpath("//*[contains(text(),'SQ.')]/text()").extract_first(
                default='0').strip().replace(",", "")
            BaseSqft = BaseSqft.split(" ")[0]
            print(BaseSqft)

        except Exception as e:
            print(e)

        try:
            Description = "".join(response.xpath('//div[@class="detailsInfo"]/text()').extract()).strip()

            print(Description)
        except Exception as e:
            Description = ''

        try:
            images = []
            image1 = response.xpath('//div[@id="plan_images"]//a/@href').extract()
            if image1 != []:
                for im in image1:
                    im = 'http://www.chrisgeorgenewhomes.com' + im
                    images.append(im)

            ElevationImage = "|".join(images)
            print(ElevationImage)
        except Exception as e:
            print(e)
            ElevationImage = ''

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

            # SubdivisionNumber = SubdivisionNumber #if subdivision is there
        SubdivisionNumber = self.builderNumber  # if subdivision is not available
        unique = str(PlanName) + str(SubdivisionNumber)
        print(unique)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

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
        item['Baths'] = Bath
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = Description
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl chrisgeorgenewhomes'.split())






