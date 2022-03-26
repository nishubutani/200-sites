# -*- coding: utf-8 -*-
import json
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'trickconstruction'
    allowed_domains = ['harlowbuilders.net']
    start_urls = ['https://www.trickconstruction.com/']
    builderNumber = 19900


    def parse(self, response):

        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = '1305 TWIN OAKS ROAD EAST'
        item2['City'] = 'NORTHPORT'
        item2['State'] = 'AL'
        item2['ZIP'] = '35473'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "Trick Construction encourages and supports an affirmative advertising and marketing program in which there are no barriers to obtaining housing because of race, color, religion, sex, handicap, familial status, or national origin. All residential real estate information on this website is subject to the Federal Fair Housing Act Title VIII of the Civil Rights Act of 1968, as amended, which makes it illegal to advertise any preference, limitation, or discrimination because of race, color, religion, sex, handicap, familial states, or national origin, or intention to make any such preference, limitation or discrimination.Your state or local jurisdiction may impose additional requirements. We are committed to the letter and spirit of the United States policy for the achievement of equal housing opportunity"
        item2['SubImage'] = "https://images.squarespace-cdn.com/content/v1/5caf31a7755be20933430199/1555877738378-6N2GN5CJOZN5RDJSE5P8/002+No+Name.JPG?format=1500w|https://images.squarespace-cdn.com/content/v1/5caf31a7755be20933430199/1555877750537-9LHZNWBHWZVKIWAXIA39/007+%282%29No+Name.JPG?format=1500w|https://images.squarespace-cdn.com/content/v1/5caf31a7755be20933430199/1555877760218-CCY3Y2KWHV7JW8D2J4ZF/008TNR+294.JPG?format=1500w|https://images.squarespace-cdn.com/content/v1/5caf31a7755be20933430199/1555877762775-JANBFOCDYPL0HDVOYTTL/15+MGMimosa+Gard.jpg?format=1500w|https://images.squarespace-cdn.com/content/v1/5caf31a7755be20933430199/1555877778619-MUPF2RSXYB3TZHUO1XUG/44ROY+front.JPG?format=1500w|https://images.squarespace-cdn.com/content/v1/5caf31a7755be20933430199/1555877780909-CLTJIPZ3AXWBOOEK5OUK/50+Easton+Place+elev.jpg?format=1500w"
        item2['SubWebsite'] = 'https://www.trickconstruction.com/'
        item2['AmenityType'] = ''
        yield item2

        link = 'https://www.designbasics.com/plan-library/?pg=0&search-type=library&client=aaron@trickconstruction.com'
        yield scrapy.FormRequest(url=link, callback=self.plan, dont_filter=True)


    def plan(self, response):

        links = response.xpath('//div[@class="plan-result img"]/a/@href').extract()
        for link in links:
            link = 'https://www.designbasics.com' + str(link)
            yield scrapy.FormRequest(url=link,callback=self.plan_details,dont_filter=True)

        nxt_link = response.xpath("//span[contains(text(),'Next')]/../@href").extract_first('')
        print(nxt_link)
        if nxt_link != '':
            nxt_link = 'https://www.designbasics.com/plan-library/' + nxt_link
            yield scrapy.FormRequest(url=nxt_link,callback=self.plan,dont_filter=True)
        else:
            pass

    def plan_details(self,response):

        try:
            Type = 'SingleFamily'
        except Exception as e:
            Type = 'SingleFamily'
            print(e)

        try:
            PlanName = response.xpath('//h1[@class="entry-title main_title"]/text()').extract_first('').strip()
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

            BaseSqft = response.xpath('//strong[@class="total_heated_area"]/text()').extract_first(default='0')
            if '_' in BaseSqft:
                BaseSqft = BaseSqft.split("-")[1]
            BaseSqft = BaseSqft.replace(',', '')
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]

        except Exception as e:
            print(e)

        try:
            Baths = response.xpath('//strong[@class="bathrooms"]/text()').extract_first(
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
            Bedrooms = response.xpath('//strong[@class="bedrooms"]/text()').extract_first(default='0')
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)
            Bedrooms = 0

        try:
            Garage = response.xpath('//strong[@class="garage"]/text()').extract_first('')
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
            ElevationImage = response.xpath('//span[@class="et_pb_image_wrap "]/img/@src').extract()
            ElevationImage = "|".join(ElevationImage)
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

        spec_link = 'https://api.myownmls.com/property/getProperties?userId=12&sortField=id&sortOrder=DESC&status=!Sold&deleted=false&&bathrooms=1-x&bedrooms=1-x&price=5000-50000000&pageNumber=1'
        yield scrapy.FormRequest(url=spec_link,callback=self.spec_details,dont_filter=True)

    def spec_details(self,response):

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

        data = json.loads(response.text)
        for i in range(0,5):
            try:
                SpecStreet1 = data['data'][i]['street']
            except Exception as e:
                print(e)

            try:
                SpecCity = data['data'][i]['city']
            except Exception as e:
                print(e)

            try:
                SpecState =data['data'][i]['state']
            except Exception as e:
                print(e)

            try:
                SpecZIP = data['data'][i]['zipcode']
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

            try:
                price = data['data'][i]['price']
                price = re.findall(r"(\d+)", price)[0]
            except Exception as e:
                print(e)

            try:
                SpecBedrooms = data['data'][i]['price']
                SpecBedrooms = re.findall(r"(\d+)", SpecBedrooms)[0]
                print(SpecBedrooms)
            except Exception as e:
                print(str(e))

            try:
                SpecBaths = data['data'][0]['bathrooms']
                tmp = re.findall(r"(\d+)", SpecBaths)
                SpecBaths = tmp[0]
                if len(tmp) > 1:
                    halfbath = 1
                else:
                    halfbath = 0
            except Exception as e:
                print(str(e))

            try:
                SpecGarage = data['data'][i]['garagebays']
                # SpecGarage = re.findall(r"(\d+) Car Garage",SpecGarage)[0]
            except Exception as e:
                print(str(e))

            try:
                SpecSqft = data['data'][i]['squarefeet']
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
                image = data['data'][i]['photos']
                ElevationImage = "|".join(image)
            except Exception as e:
                print(e)
                ElevationImage = ""


            web = 'https://www.trickconstruction.com/property?mlsid=' + str(data['data'][i]['id']) + '&address=' + SpecStreet1.replace(" ","_") + "_" + SpecCity + "_" + SpecState + "_" + SpecZIP
            print(web)

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
    execute('scrapy crawl trickconstruction'.split())





