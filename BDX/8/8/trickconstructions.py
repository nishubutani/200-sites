import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class trickconstructionSpider(scrapy.Spider):
    name = 'trickconstructions'
    allowed_domains = []
    start_urls = ['https://www.trickconstruction.com/']
    builderNumber = 19900

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
        item['Street1'] = '1305 TWIN OAKS ROAD EAST'
        item['City'] = ' NORTHPORT'
        item['State'] = 'AL'
        item['ZIP'] = '35473'
        item['AreaCode'] = ''
        item['Prefix'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] = 'FREDTRICK@TRICKCONSTRUCTION.COM'
        item[
            'SubDescription'] = 'Trick Construction encourages and supports an affirmative advertising and marketing program in which there are no barriers to obtaining housing because of race, color, religion, sex, handicap, familial status, or national origin. All residential real estate information on this website is subject to the Federal Fair Housing Act Title VIII of the Civil Rights Act of 1968, as amended, which makes it illegal to advertise "any preference, limitation, or discrimination because of race, color, religion, sex, handicap, familial states, or national origin, or intention to make any such preference, limitation or discrimination." Your state or local jurisdiction may impose additional requirements. We are committed to the letter and spirit of the United States policy for the achievement of equal housing opportunity.'
        item[
            'SubImage'] = ''
        item['SubWebsite'] = response.url
        yield item

        unique = str("Plan Unknown") + str(self.builderNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['unique_number'] = unique_number
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = "Plan Unknown"
        item['SubdivisionNumber'] = self.builderNumber
        item['PlanName'] = "Plan Unknown"
        item['PlanNotAvailable'] = 1
        item['PlanTypeName'] = "Single Family"
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

        for i in range(0,19):
            if i == 1:
                Street1 = '13128 Garden Creek Lane Northport'
                City = 'Northport'
                State = 'AL'
                Zip = '35475'
                Price = '244900'
                sqft = '1796'
                bath = '2'
                bed = '3'
                garage = 0
                MasterBedLocation = "Down"
                image = 'https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589561452656-243-Hidden-Meadows-13128-Garden-Creek-Lane-1.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1592170920146-13128%20Garden%20Creek.jpg'
                website = 'https://www.trickconstruction.com/property?mlsid=58&address=13128_Garden_Creek_Lane_Northport_AL_35475'
                unique = str("Plan Unknown")+str(self.builderNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                unique = str(Street1) + str(City) + str(State) + str(Zip)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = unique_number
                item['SpecStreet1'] = Street1
                item['SpecCity'] = City
                item['SpecState'] = State
                item['SpecZIP'] = Zip
                item['SpecCountry'] = 'USA'
                item['SpecPrice'] = Price
                item['SpecSqft'] = sqft
                item['SpecBaths'] = bath
                item['SpecHalfBaths'] = 0
                item['SpecBedrooms'] = bed
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = garage
                item['SpecDescription'] = ''
                item['SpecElevationImage'] = image
                item['SpecWebsite'] = website
                yield item
            elif i == 2:
                Street1 = '1821 Willow Oak Circle Tuscaloosa'
                City = 'Tuscaloosa'
                State = 'AL'
                Zip = '35405'
                Price = '309900'
                sqft = '2307'
                bath = '3'
                bed = '4'
                garage = 0
                MasterBedLocation = "Down"
                image = 'https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589561235826-19-Laurelwood-1821-Willow-Oak-Circle-1.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1592170941165-1821%20Willow%20Oak%20Circle%20.001.jpg'
                website = 'https://www.trickconstruction.com/property?mlsid=57&address=1821_Willow_Oak_Circle_Tuscaloosa_AL_35405'
                unique = str("Plan Unknown") + str(self.builderNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                unique = str(Street1) + str(City) + str(State) + str(Zip)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = unique_number
                item['SpecStreet1'] = Street1
                item['SpecCity'] = City
                item['SpecState'] = State
                item['SpecZIP'] = Zip
                item['SpecCountry'] = 'USA'
                item['SpecPrice'] = Price
                item['SpecSqft'] = sqft
                item['SpecBaths'] = bath
                item['SpecHalfBaths'] = 0
                item['SpecBedrooms'] = bed
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = garage
                item['SpecDescription'] = ''
                item['SpecElevationImage'] = image
                item['SpecWebsite'] = website
                yield item
            elif i == 3:
                Street1 = '4602 Jamie Ln'
                City = 'Moundville'
                State = 'AL'
                Zip = '35474'
                Price = '299900'
                sqft = '2401'
                bath = '2'
                bed = '4'
                garage = 0
                MasterBedLocation = "Down"
                image = 'https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589561102023-21%2BGrayson%2BParc-4602-Jamie-Lane-1.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1592170957034-4602%20Jamie%20Lane.jpg'
                website = 'https://www.trickconstruction.com/property?mlsid=56&address=4602_Jamie_Ln_Moundville_AL_35474'
                unique = str("Plan Unknown") + str(self.builderNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                unique = str(Street1) + str(City) + str(State) + str(Zip)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = unique_number
                item['SpecStreet1'] = Street1
                item['SpecCity'] = City
                item['SpecState'] = State
                item['SpecZIP'] = Zip
                item['SpecCountry'] = 'USA'
                item['SpecPrice'] = Price
                item['SpecSqft'] = sqft
                item['SpecBaths'] = bath
                item['SpecHalfBaths'] = 0
                item['SpecBedrooms'] = bed
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = garage
                item['SpecDescription'] = ''
                item['SpecElevationImage'] = image
                item['SpecWebsite'] = website
                yield item
            elif i == 4:
                Street1 = '13139 Garden Creek Lane Northport'
                City = 'Northport'
                State = 'AL'
                Zip = '35473'
                Price = '244900'
                sqft = '1823'
                bath = '2'
                bed = '4'
                garage = 0
                MasterBedLocation = "Down"
                image = 'https://myownmls.s3.us-east-2.amazonaws.com/uploads/1592170973571-13139%20Garden%20Creek%20.001.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589560433035-214%2BHidden%2BMeadows%2B13139%2BGarden%2BCreek%2BLane-1.jpg'
                website = 'https://www.trickconstruction.com/property?mlsid=55&address=13139_Garden_Creek_Lane_Northport_AL_35473'
                unique = str("Plan Unknown") + str(self.builderNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                unique = str(Street1) + str(City) + str(State) + str(Zip)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = unique_number
                item['SpecStreet1'] = Street1
                item['SpecCity'] = City
                item['SpecState'] = State
                item['SpecZIP'] = Zip
                item['SpecCountry'] = 'USA'
                item['SpecPrice'] = Price
                item['SpecSqft'] = sqft
                item['SpecBaths'] = bath
                item['SpecHalfBaths'] = 0
                item['SpecBedrooms'] = bed
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = garage
                item['SpecDescription'] = ''
                item['SpecElevationImage'] = image
                item['SpecWebsite'] = website
                yield item
            elif i == 5:
                Street1 = 'Arborway Circle Tuscaloosa'
                City = 'Tuscaloosa'
                State = 'AL'
                Zip = '35405'
                Price = '309900'
                sqft = '2400'
                bath = '3'
                bed = '4'
                garage = 0
                MasterBedLocation = "Down"
                image = 'https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589560128355-46%2BLaurelwood%2BArborway%2BCircle-1.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1592170988233-1670%20Arborway%20Circle%20.001.jpg'
                website = 'https://www.trickconstruction.com/property?mlsid=54&address=Arborway_Circle_Tuscaloosa_AL_35405'
                unique = str("Plan Unknown") + str(self.builderNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                unique = str(Street1) + str(City) + str(State) + str(Zip)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = unique_number
                item['SpecStreet1'] = Street1
                item['SpecCity'] = City
                item['SpecState'] = State
                item['SpecZIP'] = Zip
                item['SpecCountry'] = 'USA'
                item['SpecPrice'] = Price
                item['SpecSqft'] = sqft
                item['SpecBaths'] = bath
                item['SpecHalfBaths'] = 0
                item['SpecBedrooms'] = bed
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = garage
                item['SpecDescription'] = ''
                item['SpecElevationImage'] = image
                item['SpecWebsite'] = website
                yield item
            elif i == 6:
                Street1 = '1591 Arborway Circle Tuscaloosa'
                City = 'Tuscaloosa'
                State = 'AL'
                Zip = '35405'
                Price = '309900'
                sqft = '2330'
                bath = '3'
                bed = '4'
                garage = 0
                MasterBedLocation = "Down"
                image = 'https://myownmls.s3.us-east-2.amazonaws.com/uploads/1592171006658-1591%20Arborway%20Circle.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589559917298-10%2BLaurelwood%2B1591%2BArborway%2BCircle-1.jpg'
                website = 'https://www.trickconstruction.com/property?mlsid=53&address=1591_Arborway_Circle_Tuscaloosa_AL_35405'
                unique = str("Plan Unknown") + str(self.builderNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                unique = str(Street1) + str(City) + str(State) + str(Zip)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = unique_number
                item['SpecStreet1'] = Street1
                item['SpecCity'] = City
                item['SpecState'] = State
                item['SpecZIP'] = Zip
                item['SpecCountry'] = 'USA'
                item['SpecPrice'] = Price
                item['SpecSqft'] = sqft
                item['SpecBaths'] = bath
                item['SpecHalfBaths'] = 0
                item['SpecBedrooms'] = bed
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = garage
                item['SpecDescription'] = ''
                item['SpecElevationImage'] = image
                item['SpecWebsite'] = website
                yield item
            elif i == 7:
                Street1 = 'Arborway Circle'
                City = 'Tuscaloosa'
                State = 'AL'
                Zip = '35405'
                Price = '309900'
                sqft = '2400'
                bath = '3'
                bed = '4'
                garage = 0
                MasterBedLocation = "Down"
                image = 'https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589559792012-11%2BLaurelwood%2BArborway%2BCircle-1.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1592171037004-1585%20Arborway%20Circle%20.001.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1592171037008-1585%20Arborway%20Circle.jpg'
                website = 'https://www.trickconstruction.com/property?mlsid=52&address=Arborway_Circle_Tuscaloosa_AL_35405'
                unique = str("Plan Unknown") + str(self.builderNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                unique = str(Street1) + str(City) + str(State) + str(Zip)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = unique_number
                item['SpecStreet1'] = Street1
                item['SpecCity'] = City
                item['SpecState'] = State
                item['SpecZIP'] = Zip
                item['SpecCountry'] = 'USA'
                item['SpecPrice'] = Price
                item['SpecSqft'] = sqft
                item['SpecBaths'] = bath
                item['SpecHalfBaths'] = 0
                item['SpecBedrooms'] = bed
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = garage
                item['SpecDescription'] = ''
                item['SpecElevationImage'] = image
                item['SpecWebsite'] = website
                yield item
            elif i == 8:
                Street1 = '12997 Rolling Meadows Cir'
                City = 'Northport'
                State = 'AL'
                Zip = '35473'
                Price = '244900'
                sqft = '1823'
                bath = '2'
                bed = '3'
                garage = 0
                MasterBedLocation = "Down"
                image = 'https://myownmls.s3.us-east-2.amazonaws.com/uploads/1592171060692-12997%20Rolling%20Meadows%20.001.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589487976260-12997-Rollling-Meadows-Circle-1.jpg'
                website = 'https://www.trickconstruction.com/property?mlsid=51&address=12997_Rolling_Meadows_Cir_Northport_AL_35473'
                unique = str("Plan Unknown") + str(self.builderNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                unique = str(Street1) + str(City) + str(State) + str(Zip)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = unique_number
                item['SpecStreet1'] = Street1
                item['SpecCity'] = City
                item['SpecState'] = State
                item['SpecZIP'] = Zip
                item['SpecCountry'] = 'USA'
                item['SpecPrice'] = Price
                item['SpecSqft'] = sqft
                item['SpecBaths'] = bath
                item['SpecHalfBaths'] = 0
                item['SpecBedrooms'] = bed
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = garage
                item['SpecDescription'] = ''
                item['SpecElevationImage'] = image
                item['SpecWebsite'] = website
                yield item
            elif i == 9:
                Street1 = '13134 Garden Creek Ln'
                City = 'Northport'
                State = 'AL'
                Zip = '35473'
                Price = '244900'
                sqft = '1818'
                bath = '4'
                bed = '2'
                garage = 0
                MasterBedLocation = "Down"
                image = 'https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589487688930-13134%2BGarden%2BCreek%2BLn-1.jpg'
                website = 'https://www.trickconstruction.com/property?mlsid=50&address=13134_Garden_Creek_Ln_Northport_AL_35473'
                unique = str("Plan Unknown") + str(self.builderNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                unique = str(Street1) + str(City) + str(State) + str(Zip)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = unique_number
                item['SpecStreet1'] = Street1
                item['SpecCity'] = City
                item['SpecState'] = State
                item['SpecZIP'] = Zip
                item['SpecCountry'] = 'USA'
                item['SpecPrice'] = Price
                item['SpecSqft'] = sqft
                item['SpecBaths'] = bath
                item['SpecHalfBaths'] = 0
                item['SpecBedrooms'] = bed
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = garage
                item['SpecDescription'] = ''
                item['SpecElevationImage'] = image
                item['SpecWebsite'] = website
                yield item
            elif i == 10:
                Street1 = '13003 Rolling Meadows Cir'
                City = 'Northport'
                State = 'AL'
                Zip = '35473'
                Price = '244900'
                sqft = '1823'
                bath = '3'
                bed = '4'
                garage = 0
                MasterBedLocation = "Down"
                image = 'https://myownmls.s3.us-east-2.amazonaws.com/uploads/1592171264732-13003%20Rolling%20Meadows%20.001-min.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589487328485-13003%2BRolling%2BMeadows%2BCir-1.jpg'
                website = 'https://www.trickconstruction.com/property?mlsid=49&address=13003_Rolling_Meadows_Cir_Northport_AL_35473'
                unique = str("Plan Unknown") + str(self.builderNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                unique = str(Street1) + str(City) + str(State) + str(Zip)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = unique_number
                item['SpecStreet1'] = Street1
                item['SpecCity'] = City
                item['SpecState'] = State
                item['SpecZIP'] = Zip
                item['SpecCountry'] = 'USA'
                item['SpecPrice'] = Price
                item['SpecSqft'] = sqft
                item['SpecBaths'] = bath
                item['SpecHalfBaths'] = 0
                item['SpecBedrooms'] = bed
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = garage
                item['SpecDescription'] = ''
                item['SpecElevationImage'] = image
                item['SpecWebsite'] = website
                yield item
            elif i == 11:
                Street1 = '13917 Darden Ave'
                City = 'Northport'
                State = 'AL'
                Zip = '35475'
                Price = '309900'
                sqft = '2354'
                bath = '3'
                bed = '4'
                garage = 0
                MasterBedLocation = "Down"
                image = 'https://myownmls.s3.us-east-2.amazonaws.com/uploads/1592171354276-13917%20Darden%20Ave%20.004-min.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1592171354273-13917%20Darden%20Ave%20.001-min.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589484336973-13917-Darden-Ave.jpg'
                website = 'https://www.trickconstruction.com/property?mlsid=48&address=13917_Darden_Ave_Northport_AL_35475'
                unique = str("Plan Unknown") + str(self.builderNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                unique = str(Street1) + str(City) + str(State) + str(Zip)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = unique_number
                item['SpecStreet1'] = Street1
                item['SpecCity'] = City
                item['SpecState'] = State
                item['SpecZIP'] = Zip
                item['SpecCountry'] = 'USA'
                item['SpecPrice'] = Price
                item['SpecSqft'] = sqft
                item['SpecBaths'] = bath
                item['SpecHalfBaths'] = 0
                item['SpecBedrooms'] = bed
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = garage
                item['SpecDescription'] = ''
                item['SpecElevationImage'] = image
                item['SpecWebsite'] = website
                yield item
            elif i == 12:
                Street1 = '5720 Shirleywood Pkwy'
                City = 'Northport'
                State = 'AL'
                Zip = '35473'
                Price = '265900'
                sqft = '1800'
                bath = '2'
                bed = '3'
                garage = 0
                MasterBedLocation = "Down"
                image = 'https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589484085702-5720-shirleywood-pkwy-1.jpg'
                website = 'https://www.trickconstruction.com/property?mlsid=47&address=5720_Shirleywood_Pkwy_Northport_AL_35473'
                unique = str("Plan Unknown") + str(self.builderNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                unique = str(Street1) + str(City) + str(State) + str(Zip)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = unique_number
                item['SpecStreet1'] = Street1
                item['SpecCity'] = City
                item['SpecState'] = State
                item['SpecZIP'] = Zip
                item['SpecCountry'] = 'USA'
                item['SpecPrice'] = Price
                item['SpecSqft'] = sqft
                item['SpecBaths'] = bath
                item['SpecHalfBaths'] = 0
                item['SpecBedrooms'] = bed
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = garage
                item['SpecDescription'] = ''
                item['SpecElevationImage'] = image
                item['SpecWebsite'] = website
                yield item
            elif i == 13:
                Street1 = '13921 Darden Ave'
                City = 'Northport'
                State = 'AL'
                Zip = '35475'
                Price = '309900'
                sqft = '2354'
                bath = '3'
                bed = '4'
                garage = 0
                MasterBedLocation = "Down"
                image = 'https://myownmls.s3.us-east-2.amazonaws.com/uploads/1592171393464-13921%20Darden%20Ave%20.01-min.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589483808703-13921-Darden-Ave-1.jpg'
                website = 'https://www.trickconstruction.com/property?mlsid=46&address=13921_Darden_Ave_Northport_AL_35475'
                unique = str("Plan Unknown") + str(self.builderNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                unique = str(Street1) + str(City) + str(State) + str(Zip)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = unique_number
                item['SpecStreet1'] = Street1
                item['SpecCity'] = City
                item['SpecState'] = State
                item['SpecZIP'] = Zip
                item['SpecCountry'] = 'USA'
                item['SpecPrice'] = Price
                item['SpecSqft'] = sqft
                item['SpecBaths'] = bath
                item['SpecHalfBaths'] = 0
                item['SpecBedrooms'] = bed
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = garage
                item['SpecDescription'] = ''
                item['SpecElevationImage'] = image
                item['SpecWebsite'] = website
                yield item
            elif i == 14:
                Street1 = '13163 Garden Creek Ln'
                City = 'Northport'
                State = 'AL'
                Zip = '35473'
                Price = '246400'
                sqft = '1796'
                bath = '2'
                bed = '3'
                garage = 0
                MasterBedLocation = "Down"
                image = 'https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589553543562-13163-Garden-Creek-Ln-1.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589553543568-13163-Garden-Creek-Ln-2.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589553543578-13163-Garden-Creek-Ln-3.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589553543579-13163-Garden-Creek-Ln-4.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589553543589-13163-Garden-Creek-Ln-5.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589553543593-13163-Garden-Creek-Ln-6.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589553543600-13163-Garden-Creek-Ln-7.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589553543603-13163-Garden-Creek-Ln-8.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589553543607-13163-Garden-Creek-Ln-9.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589553543607-13163-Garden-Creek-Ln-10.jpg|https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589553543615-13163-Garden-Creek-Ln-11.jpg'
                website = 'https://www.trickconstruction.com/property?mlsid=45&address=13163_Garden_Creek_Ln_Northport_AL_35473'
                unique = str("Plan Unknown") + str(self.builderNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                unique = str(Street1) + str(City) + str(State) + str(Zip)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = unique_number
                item['SpecStreet1'] = Street1
                item['SpecCity'] = City
                item['SpecState'] = State
                item['SpecZIP'] = Zip
                item['SpecCountry'] = 'USA'
                item['SpecPrice'] = Price
                item['SpecSqft'] = sqft
                item['SpecBaths'] = bath
                item['SpecHalfBaths'] = 0
                item['SpecBedrooms'] = bed
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = garage
                item['SpecDescription'] = ''
                item['SpecElevationImage'] = image
                item['SpecWebsite'] = website
                yield item
            elif i == 15:
                Street1 = '13978 Knoll Pointe Dr'
                City = 'Northport'
                State = 'AL'
                Zip = '35475'
                Price = '259900'
                sqft = '1800'
                bath = '2'
                bed = '3'
                garage = 0
                MasterBedLocation = "Down"
                image = 'https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589483139804-13978%2BKNOLL%2BPOINTE%2BDR%2BGP%2B619%2BFRONT%2BELEVATION-min.jpeg'
                website = 'https://www.trickconstruction.com/property?mlsid=44&address=13978_Knoll_Pointe_Dr_Northport_AL_35475'
                unique = str("Plan Unknown") + str(self.builderNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                unique = str(Street1) + str(City) + str(State) + str(Zip)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = unique_number
                item['SpecStreet1'] = Street1
                item['SpecCity'] = City
                item['SpecState'] = State
                item['SpecZIP'] = Zip
                item['SpecCountry'] = 'USA'
                item['SpecPrice'] = Price
                item['SpecSqft'] = sqft
                item['SpecBaths'] = bath
                item['SpecHalfBaths'] = 0
                item['SpecBedrooms'] = bed
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = garage
                item['SpecDescription'] = ''
                item['SpecElevationImage'] = image
                item['SpecWebsite'] = website
                yield item
            elif i == 16:
                Street1 = '3604 Wagon Way Dr'
                City = 'Northport'
                State = 'AL'
                Zip = '35473'
                Price = '269900'
                sqft = '1890'
                bath = '2'
                bed = '3'
                garage = 0
                MasterBedLocation = "Down"
                image = 'https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589482734953-3604-wagon-way-dr-1.jpg'
                website = 'https://www.trickconstruction.com/property?mlsid=43&address=3604_Wagon_Way_Dr_Northport_AL_35473'
                unique = str("Plan Unknown") + str(self.builderNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                unique = str(Street1) + str(City) + str(State) + str(Zip)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = unique_number
                item['SpecStreet1'] = Street1
                item['SpecCity'] = City
                item['SpecState'] = State
                item['SpecZIP'] = Zip
                item['SpecCountry'] = 'USA'
                item['SpecPrice'] = Price
                item['SpecSqft'] = sqft
                item['SpecBaths'] = bath
                item['SpecHalfBaths'] = 0
                item['SpecBedrooms'] = bed
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = garage
                item['SpecDescription'] = ''
                item['SpecElevationImage'] = image
                item['SpecWebsite'] = website
                yield item
            elif i == 17:
                Street1 = '4138 Richmond Street'
                City = 'Northport'
                State = 'AL'
                Zip = '35473'
                Price = '249900'
                sqft = '1790'
                bath = '2'
                bed = '3'
                garage = 0
                MasterBedLocation = "Down"
                image = 'https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589288636806-4138%2BRICHMOND%2BST%2BCNW%2B47%2BFRONT%2BELEVATION-min.jpg'
                website = 'https://www.trickconstruction.com/property?mlsid=42&address=4138_Richmond_Street_Northport_AL_35473'
                unique = str("Plan Unknown") + str(self.builderNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                unique = str(Street1) + str(City) + str(State) + str(Zip)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = unique_number
                item['SpecStreet1'] = Street1
                item['SpecCity'] = City
                item['SpecState'] = State
                item['SpecZIP'] = Zip
                item['SpecCountry'] = 'USA'
                item['SpecPrice'] = Price
                item['SpecSqft'] = sqft
                item['SpecBaths'] = bath
                item['SpecHalfBaths'] = 0
                item['SpecBedrooms'] = bed
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = garage
                item['SpecDescription'] = ''
                item['SpecElevationImage'] = image
                item['SpecWebsite'] = website
                yield item
            elif i == 18:
                Street1 = '4145 Richmond St'
                City = 'Northport'
                State = 'AL'
                Zip = '35473'
                Price = '249900'
                sqft = '1825'
                bath = '2'
                bed = '3'
                garage = 0
                MasterBedLocation = "Down"
                image = 'https://myownmls.s3.us-east-2.amazonaws.com/uploads/1589288158783-4145%2BRICHMOND%2BST%2BCNW%2B69%2BFRONT%2BELEVATION%2B1.jpg'
                website = 'https://www.trickconstruction.com/property?mlsid=41&address=4145_Richmond_St_Northport_AL_35473'
                unique = str("Plan Unknown") + str(self.builderNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                unique = str(Street1) + str(City) + str(State) + str(Zip)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
    # ----------------------- Don't change anything here ---------------- #
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = unique_number
                item['SpecStreet1'] = Street1
                item['SpecCity'] = City
                item['SpecState'] = State
                item['SpecZIP'] = Zip
                item['SpecCountry'] = 'USA'
                item['SpecPrice'] = Price
                item['SpecSqft'] = sqft
                item['SpecBaths'] = bath
                item['SpecHalfBaths'] = 0
                item['SpecBedrooms'] = bed
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = garage
                item['SpecDescription'] = ''
                item['SpecElevationImage'] = image
                item['SpecWebsite'] = website
                yield item
# execute("scrapy crawl trickconstructions".split())