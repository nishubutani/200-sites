

# -*- coding: utf-8 -*-
import json
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'homeprowv'
    allowed_domains = ['homeprowv.com']
    start_urls = ['http://www.homeprowv.com/']
    builderNumber = 51343


    def parse(self, response):


        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = self.builderNumber
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = '2201 Jefferson Avenue'
        item2['City'] = 'Point Pleasant'
        item2['State'] = 'WV'
        item2['ZIP'] = '25550'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "Home Pro Custom Builders has proudly served the area for more than 10 years. We work closely with our clients to bring their ideas and dreams to life."
        item2['SubImage'] = "http://www.homeprowv.com/data/slideShowFiles/Slide0.jpg|http://www.homeprowv.com/data/Albums/The_Advantage_Louisville/large/Living3-sm.jpg|http://www.homeprowv.com/data/Albums/The_Shelton_Creek/large/Living1-sm.jpg"
        item2['SubWebsite'] = 'https://www.dhbhomes.com/'
        item2['AmenityType'] = ''
        yield item2

        link = 'https://api.ritz-craft.com/api/floorplanglobalcontent/search?iBedMin=1&iBedMax=6&iBathMin=1&HideWithInactiveCollection=true&iBathMax=6&sPlanName=&iRId=3&OrderBy=name+asc&Filters=active%3Dtrue&ExcludedCId=9&pageSize=200&pageNumber=1'
        yield scrapy.FormRequest(url=link, callback=self.plan, dont_filter=True)

    def plan(self, response):
        data = json.loads(response.text)
        lan = len(data)

        for i in range(0,lan):


            try:
                Type = 'SingleFamily'
            except Exception as e:
                Type = 'SingleFamily'
                print(e)

            try:
                PlanName = data[i]['name']
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

                BaseSqft = data[i]['sqFt']
                BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]

            except Exception as e:
                print(e)

            try:
                Baths = data[i]['bathMax']
                if Baths == None:
                    Baths = data[i]['bathMin']
                Bath = re.findall(r"(\d+)", Baths)
                Baths = Bath[0]
                if len(Bath) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0

            except Exception as e:
                Baths = 0
                print(e)

            try:

                Bedrooms = data[i]['bedMax']
                if Bedrooms == None:
                    Bedrooms = data[i]['bedMin']
                Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            except Exception as e:
                print(e)
                Bedrooms = 0

            try:

                Garage = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*-car", response.text.lower())[0]
                Garage = Garage.replace("three", "3").replace("four", "4").replace("two", "2")
                Garage = re.findall(r"(\d+)", Garage)[0]

            except Exception as e:
                print(e)
                Garage = "0"

            try:
                Description = ''
            except Exception as e:
                print(e)
                Description = ""

            try:
                ElevationImage = []
                ElevationImage1 = data[i]['imgOriginal']
                ElevationImage1 = 'https://globalcontent.ritz-craft.com/' + ElevationImage1
                ElevationImage1 = ElevationImage1.replace(" ","%20")
                ElevationImage.append(ElevationImage1)


                ElevationImage2 = data[i]['images']
                len_ElevationImage = len(ElevationImage2)
                for j in range(0,len_ElevationImage):
                    ElevationImage22 = data[i]['images'][j]['photoOriginal']
                    ElevationImage22 = 'https://globalcontent.ritz-craft.com/' + ElevationImage22
                    ElevationImage22 = ElevationImage22.replace(" ", "%20")
                    ElevationImage.append(ElevationImage22)


                ElevationImage = "|".join(ElevationImage)


            except Exception as e:
                print(e)
                ElevationImage = ""

            try:
                PlanWebsite = 'http://www.homeprowv.com/modular-floor-plan.asp?altdb=true#/detail/' + str(data[i]['id'])
            except Exception as e:
                print(e)

            # ----------------------- Don't change anything here --------------
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


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl homeprowv'.split())


