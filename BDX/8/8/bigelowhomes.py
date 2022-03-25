# -*- coding: utf-8 -*-
import hashlib
import re

import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class BigelowhomesSpider(scrapy.Spider):
    name = 'bigelowhomes'
    allowed_domains = ['www.bigelowhomes.net']
    start_urls = ['http://www.bigelowhomes.net/']
    builderNumber = '57258'

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
        item['Street1'] = '4057 28TH ST. NW SUITE 100'
        item['City'] = 'ROCHESTER'
        item['State'] = 'MN'
        item['ZIP'] = '55901'
        item['AreaCode'] = '507'
        item['Prefix'] = '529'
        item['Suffix'] = '1161'
        item['Extension'] = ""
        item['Email'] = 'bigelow@bigelowhomes.net'
        item['SubDescription'] = "If anything in the homebuying process is as vital as finding the right home, it's finding the right community and the right lot. Will traveling in and out of the community be difficult? How close is it to shops and other daily needs of you and your family? Is it close to schools? Each Bigelow Home community has been carefully selected with our customers' needs in mind. Explore and discover which community will suit your lifestyle best.What do you want to see when you look out the windows of your new home? Whether its right near the entrance or tucked away in a quiet corner, the right lot makes a major difference on how you see your new neighborhood and the community you’ve chose to live. Our team will work with you to find the ideal location for your new home"
        image = ['http://www.bigelowhomes.net/images/banner1.jpg','http://www.bigelowhomes.net/images/banner2.jpg','http://www.bigelowhomes.net/images/banner3.jpg','http://www.bigelowhomes.net/images/banner4.jpg']
        item[
            'SubImage'] = '|'.join(image)
        item['SubWebsite'] = response.url
        yield item
#         yield scrapy.FormRequest(url=response.url, callback=self.homelist)
#
#     def homelist(self,response):
#         unique = str("Plan Unknown") + str(self.builderNumber)  # < -------- Changes here
#         unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
#         item = BdxCrawlingItem_Plan()
#         item['unique_number'] = unique_number
#         item['Type'] = "SingleFamily"
#         item['PlanNumber'] = "Plan Unknown"
#         item['SubdivisionNumber'] = self.builderNumber
#         item['PlanName'] = "Plan Unknown"
#         item['PlanNotAvailable'] = 1
#         item['PlanTypeName'] = 'Single Family'
#         item['BasePrice'] = 0
#         item['BaseSqft'] = 0
#         item['Baths'] = 0
#         item['HalfBaths'] = 0
#         item['Bedrooms'] = 0
#         item['Garage'] = 0
#         item['Description'] = ""
#         item['ElevationImage'] = ""
#         item['PlanWebsite'] = ""
#         yield item
#
#         home_link = 'http://www.bigelowhomes.net/tour.php'
#
#         yield scrapy.FormRequest(url=home_link,callback=self.HomesDetails,meta={'PN':unique_number})
#
#     def HomesDetails(self,response):
#         global PlanNumber, SpecPrice, SpecSqft, SpecBaths, SpecHalfBaths, SpecBedrooms, SpecGarage
#         table = response.xpath('//*[@class="resultItem"]')
#         for t in table:
#
#             try:
#                 PlanNumber = response.meta['PN']
#             except Exception as e:
#                 print(e)
#
#
#
#             SpecCity = t.xpath('.//SPAN[contains(text(),"SQFT")]/text()').get().strip()
#
#
#             try:
#                 SpecPrice = t.xpath('.//SPAN[contains(text(),"PRICE")]/text()').get()
#             except Exception as e:
#                 print(e)
#
#             try:
#                 SpecSqft = t.xpath('.//SPAN[contains(text(),"SQFT")]/text()').get().strip()
#
#             except Exception as e:
#                 print(e)
#
#             try:
#                 # SpecBaths = str(response.xpath('normalize-space(//*[contains(text(),"Bathrooms")]/following-sibling::text())').extract_first(default='0').strip()).replace(",", "")
#                 tmp = t.xpath('.//SPAN[contains(text(),"BR")]/text()').get().strip()
#                 SpecBaths = tmp[0]
#                 if len(tmp) > 1:
#                     SpecHalfBaths = 1
#                 else:
#                     SpecHalfBaths = 0
#             except Exception as e:
#                 print(e)
#
#             try:
#                 SpecBedrooms = t.xpath('.//SPAN[contains(text(),"BA")]/text()').get().strip()
#             except Exception as e:
#                 print(e)
#
#
#
#             try:
#                 SpecGarage = t.xpath('.//SPAN[contains(text(),"GAR")]/text()').get().strip()
#             except Exception as e:
#                 print(e)
#
#             u = t.xpath('.//@onclick').get()
#
#             next_data = re.findall(r"('\d+')",u)[0]
#
#             next_data_url = f'http://www.bigelowhomes.net/tour.php?modelID={next_data}'
#
#             yield scrapy.FormRequest(url=next_data_url,callback=self.final,meta={'PlanNumber':PlanNumber,'SpecPrice':SpecPrice,'SpecSqft':SpecSqft,'SpecBaths':SpecBaths,'SpecHalfBaths':SpecHalfBaths,
#                             'SpecBedrooms':SpecBedrooms,'SpecGarage':SpecGarage,'SpecCity':SpecCity})
#
#     def final(self,response):
#         global SpecStreet1, SpecNumber, SpecCountry, MasterBedLocation, SpecDescription, SpecElevationImage, SpecWebsite
#         PlanNumber = response.meta['PlanNumber']
#         SpecPrice = response.meta['PlanNumber']
#         SpecSqft = response.meta['PlanNumber']
#         SpecBaths = response.meta['PlanNumber']
#         SpecBedrooms = response.meta['SpecBedrooms']
#         SpecHalfBaths = response.meta['SpecHalfBaths']
#         SpecGarage = response.meta['SpecGarage']
#         SpecCity = response.meta['SpecCity']
#
#         try:
#             SpecDescription = 'In today’s day and age, everything is visual – we invite you to look, see, touch and feel the difference in the homes we build at Bigelow Homes. Our model homes are designed to showcase the latest trends and features, and to showcase the benefits of the design, layout, and options available to you, our homebuyer.We invite you to browse through each home online to help filter what you desire most in your next home. Next, explore all of the Bigelow homes for sale in Southeastern Minnesota in person by contacting any member of our team to set up a time convenient for you. Start your new home search today!'
#         except Exception as e:
#             print(e)
#
#         try:
#             SpecStreet1 = response.xpath('normalize-space(//strong[contains(text(),"Address:")]/following-sibling::text()').extract_first(default='').strip()
#         except Exception as e:
#             print(e)
#
#         try:
#             image = ['http://www.bigelowhomes.net/images/box-3.png','http://www.bigelowhomes.net/images/box-2.png','http://www.bigelowhomes.net/images/box-1.png']
#
#             SpecElevationImage = '|'.join(image)
#         except Exception as e:
#             print(e)
#
#         try:
#             MasterBedLocation = "Down"
#         except Exception as e:
#             print(e)
#
#         SpecState = 'MN'
#         SpecZIP = '00000'
#
#         try:
#             unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
#             SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
#             f = open("html/%s.html" % SpecNumber, "wb")
#             f.write(response.body)
#             f.close()
#         except Exception as e:
#             print(e)
#
#         try:
#             SpecCountry = "USA"
#         except Exception as e:
#             print(e)
#
#         try:
#             SpecWebsite = response.url
#         except Exception as e:
#             print(e)
#
#                 # ----------------------- Don't change anything here ---------------- #
#             item = BdxCrawlingItem_Spec()
#             item['SpecNumber'] = SpecNumber
#             item['PlanNumber'] = PlanNumber
#             item['SpecStreet1'] = SpecStreet1
#             item['SpecCity'] = SpecCity
#             item['SpecState'] = SpecState
#             item['SpecZIP'] = SpecZIP
#             item['SpecCountry'] = SpecCountry
#             item['SpecPrice'] = SpecPrice
#             item['SpecSqft'] = SpecSqft
#             item['SpecBaths'] = SpecBaths
#             item['SpecHalfBaths'] = SpecHalfBaths
#             item['SpecBedrooms'] = SpecBedrooms
#             item['MasterBedLocation'] = MasterBedLocation
#             item['SpecGarage'] = SpecGarage
#             item['SpecDescription'] = SpecDescription
#             item['SpecElevationImage'] = SpecElevationImage
#             item['SpecWebsite'] = SpecWebsite
#             yield item
#
from scrapy.cmdline import execute
# execute("scrapy crawl bigelowhomes".split())

