

# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'Wagoner_Homes'
    allowed_domains = ['wagonerhomes.com/']
    start_urls = ['https://wagonerhomes.com/']
    builderNumber = 999706109108107496764630555032

    def __init__(self):
        self.temp_list = []



    def parse(self, response):


        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = 'PO Box 58602'
        item2['City'] = 'Raleigh'
        item2['State'] = 'NC'
        item2['ZIP'] = '27658'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "With over 35 years of building custom homes in the Triangle, Jerry Wagoner has established a reputation that many local builders strive to have. Wagoner Homes success has been solely based on top notch quality and customer care while remaining attentive to the details."
        item2['SubImage'] = "https://wagonerhomes.com/wp-content/uploads/2021/02/HomeSliderSIze-1200x689_0007_Wagoner-Homes_Custom-Homes-In-Raleigh_02.jpg|https://wagonerhomes.com/wp-content/uploads/2021/02/HomeSliderSIze-1200x689_0006_Wagoner-Homes_Custom-Homes-In-Raleigh_03.jpg|https://wagonerhomes.com/wp-content/uploads/2021/02/HomeSliderSIze-1200x689_0005_Wagoner-Homes_Custom-Homes-In-Raleigh_04.jpg|https://wagonerhomes.com/wp-content/uploads/2021/02/HomeSliderSIze-1200x689_0008_Wagoner-Homes_Custom-Homes-In-Raleigh_01.jpg"
        item2['SubWebsite'] = 'https://wagonerhomes.com/'
        # item2['AmenityType'] = ''
        yield item2

        SubdivisionNumber = self.builderNumber
        unique = str("Plan Unknown") + str(SubdivisionNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['unique_number'] = unique_number
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = "Plan Unknown"
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = "Plan Unknown"
        item['PlanNotAvailable'] = 1
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0
        item['BaseSqft'] = 0
        item['Baths'] = 0
        item['HalfBaths'] = 0
        item['Bedrooms'] = 0
        item['Garage'] = 0
        item['Description'] = ""
        item['ElevationImage'] = ""
        item['PlanWebsite'] = ""
        yield item

        link = "https://wagonerhomes.com/available-homes/"
        yield scrapy.FormRequest(url=link,callback=self.spec_link,dont_filter=True,meta={'unique_number':unique_number})


    def spec_link(self,response):
        unique_number = response.meta['unique_number']
        # SubdivisionNumber = response.meta['SubdivisionNumber']
        links = response.xpath('//div[@class="group-homes"][1]//h4/a/@href').extract()
        for link in links:
            yield scrapy.FormRequest(url=link, callback=self.spec, dont_filter=True,meta={'unique_number':unique_number})

    def spec(self,response):
        unique_number = response.meta['unique_number']

        try:
            addd2 = response.xpath("//*[contains(text(),'Address:')]/../span/text()").get()
            print(addd2)
        except Exception as e:
            print(e)
            addd2 = ""


        try:
            SpecStreet1 = addd2.split(",")[0].replace("\n", "").replace("\t", "")
        except Exception as e:
            print(e)


        try:
            SpecC = addd2.split(",")[1].strip()
            SpecC = SpecC.split(",")[0].strip()
            SpecCity = SpecC
        except Exception as e:
            print(e)

        try:
            SpecState = addd2.split(",")[2]
            SpecState = SpecState.strip()
            SpecState = SpecState.split(" ")[0]
        except Exception as e:
            print(e)

        try:
            SpecZIP = addd2.split(",")[2].strip()
            SpecZIP = SpecZIP.strip()
            SpecZIP = SpecZIP.split(" ")[1]
        except Exception as e:
            SpecZIP = '00000'

        unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
        print(unique)
        SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

        f = open("html/%s.html" % SpecNumber, "wb")
        f.write(response.body)
        f.close()

        try:
            PlanNumber = self.builderNumber
        except Exception as e:
            print(e)

        try:
            SpecCountry = "USA"
        except Exception as e:
            print(e)

        price = '0'


        try:
            SpecBedrooms = response.xpath("//*[contains(text(),'Features:')]/../p/text()").extract_first('').strip().replace("\n", "").replace("\t", "")
            SpecBedrooms = re.findall(r"(.*?)BR",SpecBedrooms)[0]
            print(SpecBedrooms)
        except Exception as e:
            print(str(e))

        try:
            SpecBaths = response.xpath("//*[contains(text(),'Features:')]/../p/text()").extract_first('').strip().replace("\n", "").replace("\t", "")
            SpecBaths = re.findall(r"(.*?)BA",SpecBaths)[0]
            tmp = re.findall(r"(\d+)", SpecBaths)
            SpecBaths = tmp[0]
            if len(tmp) > 1:
                halfbath = 1
            else:
                halfbath = 0
        except Exception as e:
            print(str(e))

        try:
            SpecGarage = response.xpath("//*[contains(text(),'Features:')]/../p/text()").extract_first('')
            SpecGarage = re.findall(r"(\d+) Car Garage",SpecGarage)[0]

        except Exception as e:
            print(str(e))

        try:
            SpecSqft = response.xpath("//*[contains(text(),'sq. ft.')]/text()").extract_first('').strip().replace("\n", "").replace("\t", "").replace(",","")
            SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
        except Exception as e:
            print(str(e))

        try:
            MasterBedLocation = "Down"
        except Exception as e:
            print(e)

        try:
            SpecDescription = ""
        except Exception as e:
            print(e)

        try:
            image = response.xpath('//div[@class="home-image border-shadow"]/img/@src').extract_first('')
            ElevationImage = image
        except Exception as e:
            print(e)
            ElevationImage = ""


        try:
            SpecWebsite = response.url
        except Exception as e:
            print(e)



        item = BdxCrawlingItem_Spec()
        item['SpecNumber'] = SpecNumber
        item['PlanNumber'] = unique_number
        item['SpecStreet1'] = SpecStreet1
        item['SpecCity'] = SpecCity
        item['SpecState'] = SpecState
        item['SpecZIP'] = SpecZIP
        item['SpecCountry'] = SpecCountry
        item['SpecPrice'] = price
        item['SpecSqft'] = SpecSqft
        item['SpecBaths'] = SpecBaths
        item['SpecHalfBaths'] = halfbath
        item['SpecBedrooms'] = SpecBedrooms
        item['MasterBedLocation'] = MasterBedLocation
        item['SpecGarage'] = SpecGarage
        item['SpecDescription'] = SpecDescription
        item['SpecElevationImage'] = ElevationImage
        item['SpecWebsite'] = SpecWebsite
        yield item




if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl Wagoner_Homes'.split())


