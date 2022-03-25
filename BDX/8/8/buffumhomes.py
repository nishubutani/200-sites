# -*- coding: utf-8 -*-
import hashlib
import re
import json
import requests
from scrapy.http import HtmlResponse
import scrapy
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from lxml import html
import datetime
import html2text


class buffumhomes(scrapy.Spider):
    name = 'buffumhomes'
    allowed_domains = ['']
    start_urls = ['https://buffumhomes.com/']
    builderNumber = 49502

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
        item['Street1'] = '144 44th St SW'
        item['City'] = 'Grand Rapids'
        item['State'] = 'MI'
        item['ZIP'] = '49548'
        item['AreaCode'] = '616'
        item['Prefix'] = '538'
        item['Suffix'] = '4663'
        item['Extension'] = ""
        item['Email'] = 'josh@buffumhomes.com'
        item[
            'SubDescription'] = 'With over 25 years of experience in new home construction, Buffum Homes has become one of the best value and quality driven builders in Grand Rapids. Our customers may choose from a variety of our award-winning floor plans, or a new plan can be drawn to be completely customized to meet your needs. Homes can be built on our lots, in one of our communities, or on one you choose or own. We offer a no-hassle construction financing option as well, so that you don’t have to worry about a construction loan.'
        item['SubImage'] = 'https://buffumhomes.com/wp-content/uploads/2016/09/Buffum-Homes-Logo.png'
        item['SubWebsite'] = response.url
        yield item
        yield scrapy.Request(url='https://buffumhomes.com/availablehomes/', dont_filter=True,
                             callback=self.HomesDetails)

    def HomesDetails(self, response):
        unique = str("Plan Unknown") + str(self.builderNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['unique_number'] = unique_number
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = "Plan Unknown"
        item['SubdivisionNumber'] = self.builderNumber
        item['PlanName'] = "Plan Unknown"
        item['PlanNotAvailable'] = 1
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0
        item['BaseSqft'] = 0
        item['Baths'] = 0
        item['HalfBaths'] = 0
        item['Bedrooms'] = 0
        item['Garage'] = 0
        item[
            'Description'] = 'With over 25 years of experience in new home construction, Buffum Homes has become one of the best value and quality driven builders in Grand Rapids. Our customers may choose from a variety of our award-winning floor plans, or a new plan can be drawn to be completely customized to meet your needs. Homes can be built on our lots, in one of our communities, or on one you choose or own. We offer a no-hassle construction financing option as well, so that you don’t have to worry about a construction loan.'
        item['ElevationImage'] = ""
        item['PlanWebsite'] = ""
        yield item

        for i in range(1,4):
            if i == 1:
                try:
                    SpecStreet1 = "1700 Gloryfield Drive SW"
                    SpecCity = 'Byron Center'
                    SpecState = 'MI'
                    SpecZIP = '49315'
                    unique = str(SpecStreet1) + str(SpecCity) + str(SpecState) + str(SpecZIP)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()

                    item = BdxCrawlingItem_Spec()
                    item['SpecNumber'] = SpecNumber
                    item['PlanNumber'] = unique_number
                    item['SpecStreet1'] = SpecStreet1
                    item['SpecCity'] = SpecCity
                    item['SpecState'] = SpecState
                    item['SpecZIP'] = SpecZIP
                    item['SpecCountry'] = 'USA'
                    item['SpecPrice'] = '464900'
                    item['SpecSqft'] = '2225'
                    item['SpecBaths'] = '3'
                    item['SpecHalfBaths'] = '0'
                    item['SpecBedrooms'] = '3'
                    item['MasterBedLocation'] = "Down"
                    item['SpecGarage'] = '0'
                    item[
                        'SpecDescription'] = 'With over 25 years of experience in new home construction, Buffum Homes has become one of the best value and quality driven builders in Grand Rapids. Our customers may choose from a variety of our award-winning floor plans, or a new plan can be drawn to be completely customized to meet your needs. Homes can be built on our lots, in one of our communities, or on one you choose or own. We offer a no-hassle construction financing option as well, so that you don’t have to worry about a construction loan.'
                    item['SpecElevationImage'] = 'https://cdn1.photos.sparkplatform.com/ric/20200916202859919400000000.jpg'
                    item['SpecWebsite'] = 'https://buffumhomes.com/availablehomes/'
                    yield item
                except Exception as e:
                    print('1: ',e)

            elif i == 2:
                try:
                    SpecStreet1 = "5578 Stonebridge Drive SW"
                    SpecCity = 'Grandville'
                    SpecState = 'MI'
                    SpecZIP = '49418'
                    unique = str(SpecStreet1) + str(SpecCity) + str(SpecState) + str(SpecZIP)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()

                    item = BdxCrawlingItem_Spec()
                    item['SpecNumber'] = SpecNumber
                    item['PlanNumber'] = unique_number
                    item['SpecStreet1'] = SpecStreet1
                    item['SpecCity'] = SpecCity
                    item['SpecState'] = SpecState
                    item['SpecZIP'] = SpecZIP
                    item['SpecCountry'] = 'USA'
                    item['SpecPrice'] = '522900'
                    item['SpecSqft'] = '2556'
                    item['SpecBaths'] = '3'
                    item['SpecHalfBaths'] = '0'
                    item['SpecBedrooms'] = '4'
                    item['MasterBedLocation'] = "Down"
                    item['SpecGarage'] = '0'
                    item[
                        'SpecDescription'] = 'With over 25 years of experience in new home construction, Buffum Homes has become one of the best value and quality driven builders in Grand Rapids. Our customers may choose from a variety of our award-winning floor plans, or a new plan can be drawn to be completely customized to meet your needs. Homes can be built on our lots, in one of our communities, or on one you choose or own. We offer a no-hassle construction financing option as well, so that you don’t have to worry about a construction loan.'
                    item[
                        'SpecElevationImage'] = 'https://cdn1.photos.sparkplatform.com/ric/20200716000003638849000000.jpg'
                    item['SpecWebsite'] = 'https://buffumhomes.com/availablehomes/'
                    yield item
                except Exception as e:
                    print('2: ', e)

            elif i == 3:
                try:
                    SpecStreet1 = "5668 Stonebridge Drive"
                    SpecCity = 'Grandville'
                    SpecState = 'MI'
                    SpecZIP = '49418'
                    unique = str(SpecStreet1) + str(SpecCity) + str(SpecState) + str(SpecZIP)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()

                    item = BdxCrawlingItem_Spec()
                    item['SpecNumber'] = SpecNumber
                    item['PlanNumber'] = unique_number
                    item['SpecStreet1'] = SpecStreet1
                    item['SpecCity'] = SpecCity
                    item['SpecState'] = SpecState
                    item['SpecZIP'] = SpecZIP
                    item['SpecCountry'] = 'USA'
                    item['SpecPrice'] = '537900'
                    item['SpecSqft'] = '2407'
                    item['SpecBaths'] = '3'
                    item['SpecHalfBaths'] = '0'
                    item['SpecBedrooms'] = '4'
                    item['MasterBedLocation'] = "Down"
                    item['SpecGarage'] = '0'
                    item[
                        'SpecDescription'] = 'With over 25 years of experience in new home construction, Buffum Homes has become one of the best value and quality driven builders in Grand Rapids. Our customers may choose from a variety of our award-winning floor plans, or a new plan can be drawn to be completely customized to meet your needs. Homes can be built on our lots, in one of our communities, or on one you choose or own. We offer a no-hassle construction financing option as well, so that you don’t have to worry about a construction loan.'
                    item[
                        'SpecElevationImage'] = 'https://cdn1.photos.sparkplatform.com/ric/20200716164533261893000000.jpg'
                    item['SpecWebsite'] = 'https://buffumhomes.com/availablehomes/'
                    yield item
                except Exception as e:
                    print('3: ', e)

#
# from scrapy.cmdline import execute
# execute("scrapy crawl buffumhomes".split())
