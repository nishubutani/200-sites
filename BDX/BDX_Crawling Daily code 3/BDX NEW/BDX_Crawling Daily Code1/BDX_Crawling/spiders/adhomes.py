# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class ZemanhomesSpider(scrapy.Spider):
    name = 'adhomes'
    allowed_domains = []
    start_urls = ['http://www.adhomes.com/']

    builderNumber = "51330"

    def parse(self, response):
        print('--------------------')
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #


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
        item['Street1'] = '1953 Garden Ave.,'
        item['City'] = 'Eugene'
        item['State'] = 'OR'
        item['ZIP'] = '97403'
        item['AreaCode'] = ''
        item['Prefix'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = "Anslow & DeGeneault, Inc. (A & D) is a full service design and construction firm; active in Eugene-Springfield and surrounding areas since 1985. Owners Gordon Anslow and Allen DeGeneault invite you to spend a moment here to learn more about their background, and the services they offer"
        item['SubImage'] = 'https://www.adhomes.com/wp-content/uploads/Meadowgrove-Ext-Corner-View-RS-scaled.jpg|https://www.adhomes.com/wp-content/uploads/Cumberland-Street-View.jpg|https://www.adhomes.com/wp-content/uploads/Osprey-Street-View-scaled.jpg|https://www.adhomes.com/wp-content/uploads/Osprey-Park-Aerial-res-mid.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        PlanName,BaseSqft,Bedrooms,Baths,HalfBaths,Garage,Description,ElevationImage = 'THE FRENCHGLEN','',"3","2","","2","3 Bedrooms, 2 Baths plus Office. Open floor plan with covered Front Porch and Rear Patio. Over sized 2-car Garage w/ opener & keypad. Plank floor in Entry, Great Room, Dining Room, Kitchen, and Office. Large walk-in-shower in Owner's Bath. Quartz solid surface counter tops in Kitchen. Gas fireplace.","https://www.adhomes.com/wp-content/uploads/Frenchglen-Color-Ren-640w-2.png"
        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        SubdivisionNumber = self.builderNumber  # if subdivision is not available
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = PlanName
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0.00
        item['BaseSqft'] = BaseSqft
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = Description
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = response.url
        yield item

        PlanName, BaseSqft, Bedrooms, Baths, HalfBaths, Garage, Description, ElevationImage = 'THE CLOVERDALE', '', "3", "2", "", "0", "Open floor plan great room, ideal for entertaining. 3 bedroom, 2 bathrooms. Wood floors in entry, great room, dining room, and kitchen. Quartz solid surface counter tops. Air conditioning included. Fully landscaped and fenced yard with sprinkler system.", "https://www.adhomes.com/wp-content/uploads/Cloverdale-Color-Rend-2.png"
        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        SubdivisionNumber = self.builderNumber  # if subdivision is not available
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = PlanName
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0.00
        item['BaseSqft'] = BaseSqft
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = Description
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = response.url
        yield item

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl adhomes".split())