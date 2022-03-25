# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'amyx_homes'
    allowed_domains = ['http://amyxhomes.com/']
    start_urls = ['http://www.amyxhomes.com/']

    builderNumber = "62718"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()



        images = ''
        # image = response.xpath('//div[@class="tp-bgimg defaultimg"]/@src').extract()
        image = response.xpath('//li/img/@src').extract()
        for i in image:
            if 'wp-content/uploads/sites/50/4-slide.jpg' not in i:
                if 'sites/50/Avimor-Development-Boise.jpg' not in i:
                    images = images + i + '|'
        images = images.strip('|')

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '13967 W Wainwright Dr #102'
        item['City'] = 'Meridian'
        item['State'] = 'ID'
        item['ZIP'] = '83713'
        item['AreaCode'] = '208'
        item['Prefix'] ='939'
        item['Suffix'] = '5665'
        item['Extension'] = ""
        item['Email'] = 'Todd@AmyxHomes.com'
        item['SubDescription'] = 'Amyx Signature Homes has been a part of the Treasure Valley for over 46 years.Jim Amyx, a highly celebrated builder and developer, began the company with his father and grandfather in 1962. The Amyx name has since become a signature, representing homes of fine design, quality craftsmanship, and customer satisfaction.Todd Amyx, President of Amyx Signature Homes, is a Boise native and the fourth generation of Amyx builders, continuing a family tradition. Todd began his tenure as President almost 26 years ago and has introduced new vision and innovative design to the solid quality construction that built Amyx Signature Homes’ loyal reputation.Todd has grown not only with the company, but the Treasure Valley, in which he has a lifetime of deep respect. Todd Amyx is the past President (2004) of the local Building Contractors Association (BCA) and currently serves on the Board of Directors at both the local and national level in the perpetual effort to help form government regulation and maintain affordable housing for the public. The BCA has recognized Amyx Signature Homes through various awards, including The L. Wayne Terrell Award for both Todd Amyx (2004) and Jim Amyx (1968, 1969); and the Robert H. Vincent Builder of the Year award (Jim Amyx, 1976), and Todd Amyx in 2005.Todd is also a member of the Registered Master Builder Program, and is therefore pledged to build quality homes that meet the superior legal and ethical standards required by the criteria outlined in the Registered Master Builder Program.Home is near the heart of any family and a place of everyday living and special celebration. Amyx Signature Homes endeavors to build the best of all places for families to reside and celebrate living at its finest.'
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item


        link = 'http://amyxhomes.com/floor-plans/'
        yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)

    def parse2(self,response):
        links = response.xpath('//div[@style="margin-top: 10px;"]/a/@href').extract()
        for link in links:
            link = 'http://www.amyxhomes.com' + link
            yield scrapy.FormRequest(url=link,callback=self.parse3,dont_filter=True)
            # yield scrapy.FormRequest(url='http://www.amyxhomes.com/floor-plan-details/?id=243',callback=self.parse3,dont_filter=True)


    def parse3(self,response):

        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//h1/text()').get()
        except Exception as e:
            PlanName = ''
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName  + response.url, "utf8")).hexdigest(), 16) % (
                        10 ** 30)
        except Exception as e:
            PlanNumber = ''
            print(e)

        try:
            SubdivisionNumber = self.builderNumber
            print(SubdivisionNumber)
        except Exception as e:
            SubdivisionNumber = ''
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
            BasePrice = 0
        except Exception as e:
            print(e)

        try:
            sqft = response.xpath("//*[contains(text(),'Total Sq Ft:')]/../text()").get()
            sqft = sqft.replace(',', '').strip()
            BaseSqft = re.findall(r"(\d+)", sqft)[0]

        except Exception as e:
            print(e)

        try:
            bath = response.xpath("//*[contains(text(),'Baths:')]/../text()").get()
            tmp = re.findall(r"(\d+)", bath)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            print(e)

        try:
            Bedrooms = response.xpath("//*[contains(text(),'Beds:')]/../text()").get()
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)

        try:
            Garage = response.xpath("//*[contains(text(),'Garages:')]/../text()").get()
            Garage = re.findall(r"(\d+)", Garage)[0]
            if not Garage:
                Garage = 0
        except Exception as e:
            Garage = 0
            print(e)

        try:
            # Description = response.xpath('//h2[contains(text(),"Description")]/../div/p/text()').extract()[1:]
            Description = response.xpath('//div[@class="tabcontent"]/h2[contains(text(),"Description")]/../div/p/text()').extract()
            if Description != []:
                Description = "".join(Description)
                print(Description)
            else:
                Description = ''

        except Exception as e:
            print(e)
            Description = ''

        try:
            images = []

            im1 = response.xpath('//img[contains(@src,"uplo")]/@src/../../@href').extract_first('')
            if im1!= '':
                images.append(im1)

            img1 = response.xpath("//div/img[contains(@src,'uplo')]/@src").extract_first('')
            if img1 != '':
                images.append(img1)

            imagedata = response.xpath("//img[contains(@src,'uplo')]/@src").getall()
            for id in imagedata:
                id = id
                if 'wp-content' not in id:
                    images.append(id)


            gallary_images = response.xpath('//div[@class="ngg-gallery-thumbnail"]/a/@href').getall()
            print(gallary_images)
            if gallary_images != []:
                for gal in gallary_images:
                    images.append(gal)


            ElevationImage = "|".join(images)
        except Exception as e:
            print(e)

        try:
            PlanWebsite = response.url
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


        ##--------------------------------------------------------------------- #

        link = 'http://amyxhomes.com/available-homes/'
        yield scrapy.FormRequest(url=link,callback=self.home,dont_filter=True)


    def home(self,response):
        links = response.xpath('//div[@style="margin-top: 10px;"]/a/@href').extract()
        for link in links:
            link = 'http://www.amyxhomes.com' + link
            yield scrapy.FormRequest(url=link,callback=self.home_data,dont_filter=True)

    def home_data(self,response):


        address = response.xpath('//div[@class="Overflow"]/h2/text()').get(default='')
        try:
            try:
                SpecStreet1 = address.split(',')[0].replace("Way Boise","").strip()
            except Exception as e:
                print(e)
                SpecStreet1 = ''

            SpecCity = 'Way Boise'

            SpecState = address.split(',')[1].strip().split(" ")[0].strip()

            SpecZIP = address.split(',')[1].strip().split(" ")[1].strip()
            unique = SpecStreet1 + SpecCity + SpecState + SpecZIP + response.url
            SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

            f = open("html/%s.html" % SpecNumber, "wb")
            f.write(response.body)
            f.close()

        except Exception as e:
            print(e)

        try:
            SpecCountry = "USA"
        except Exception as e:
            print(e)

        try:
            SpecPrice = response.xpath("//*[contains(text(),'Price:')]/../text()").get()
            SpecPrice = SpecPrice.replace(",", "")
            SpecPrice = re.findall(r"(\d+)", SpecPrice)[0]
        except Exception as e:
            print(e)
            SpecPrice = 0

        try:
            SpecSqft = response.xpath("//*[contains(text(),'SqFt:')]/../text()").extract_first('')
            SpecSqft = SpecSqft.replace(",", "")
            SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
        except Exception as e:
            print(e)
            SpecSqft = 0

        try:
            SpecBaths = response.xpath("//*[contains(text(),'Baths:')]/../text()").get(default='').strip()
            tmp = re.findall(r'(\d+)', SpecBaths)
            print(SpecBaths)
            SpecBaths = SpecBaths[0]
            if len(tmp) > 1:
                SpecHalfBaths = 1
            else:
                SpecHalfBaths = 0
        except Exception as e:
            print(e)

        try:
            SpecBedrooms = response.xpath("//*[contains(text(),'Beds:')]/../text()").get(default='').strip()
            SpecBedrooms = ''.join(re.findall(r'(\d+)', SpecBedrooms))
        except Exception as e:
            print(e)
            SpecBedrooms = ''

        try:
            SpecGarage = response.xpath("//*[contains(text(),'Garages:')]/../text()").get(default='').strip()
            SpecGarage = ''.join(re.findall(r'(\d+)', SpecGarage))
            print(SpecGarage)
        except Exception as e:
            print(e)
            SpecGarage = ""

        try:
            MasterBedLocation = "Down"
        except Exception as e:
            print(e)

        try:
            SpecDescription = response.xpath("//h3[contains(text(),'Description')]/following-sibling::text()").extract_first('').replace("\n","").replace("\t","")
            print(SpecDescription)
        except Exception as e:
            print(e)

        try:
            SpecWebsite = response.url
        except Exception as e:
            print(e)

        try:
            images = []
            # imagedata = response.xpath('//div[@class="galleria-image"]/img/@src').extract()
            imagedata = response.xpath('//div[@id="galleria"]/a/@href').extract()
            for id in imagedata:
                id = id
                images.append(id)
            ElevationImage = images
            print(ElevationImage)
            SpecElevationImage = images
        except Exception as e:
            print(e)

        item = BdxCrawlingItem_Plan()
        unique = str("Plan Unknown") + str(self.builderNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
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

        # ----------------------- Don't change anything here ---------------- #
        item = BdxCrawlingItem_Spec()
        item['SpecNumber'] = SpecNumber
        item['PlanNumber'] = unique_number
        item['SpecStreet1'] = SpecStreet1
        item['SpecCity'] = SpecCity
        item['SpecState'] = SpecState
        item['SpecZIP'] = SpecZIP
        item['SpecCountry'] = SpecCountry
        item['SpecPrice'] = SpecPrice
        item['SpecSqft'] = SpecSqft
        item['SpecBaths'] = SpecBaths
        item['SpecHalfBaths'] = SpecHalfBaths
        item['SpecBedrooms'] = SpecBedrooms
        item['MasterBedLocation'] = MasterBedLocation
        item['SpecGarage'] = SpecGarage
        item['SpecDescription'] = SpecDescription
        item['SpecElevationImage'] = "|".join(SpecElevationImage)
        item['SpecWebsite'] = SpecWebsite
        yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl amyx_homes'.split())