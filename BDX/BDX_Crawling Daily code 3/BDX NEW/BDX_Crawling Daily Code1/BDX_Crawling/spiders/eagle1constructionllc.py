

# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'eagle1constructionllc'
    allowed_domains = ['eagle1constructionllc.com']
    start_urls = ['https://www.eagle1constructionllc.com/']
    builderNumber = 49280

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
        item2['Street1'] = '25 Buttrick Rd. Unit A1'
        item2['City'] = 'Londonderry'
        item2['State'] = 'NH'
        item2['ZIP'] = '03053'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "DHB Homes LLC’s developments include hundreds of single-family homes in many of New Hampshire’s finest communities, multi-family housing units in Boston, MA, beachfront condominiums in Salisbury, MA, several commercial office parks in Londonderry, NH, high-end waterfront town homes on Lake Winnipesaukee and a four-season resort community on the shores of beautiful Newfound Lake in Bristol, NH. We are currently building a 60-unit 55+ development in Salem, NH and continuing to build our ever-expanding rental portfolio in Southern New Hampshire."
        item2['SubImage'] = "https://www.dhbhomes.com/wp-content/uploads/2018/03/DHB-Photo-Project-23.jpg|https://www.dhbhomes.com/wp-content/uploads/2020/01/Truman-11-20-2019.jpg|https://www.dhbhomes.com/wp-content/uploads/2021/09/31Caymus.png"
        item2['SubWebsite'] = 'https://www.eagle1constructionllc.com/'
        item2['AmenityType'] = ''
        yield item2



        link = ['https://www.eagle1constructionllc.com/floorplan_category/floorplans/',"https://www.eagle1constructionllc.com/floorplan_category/floorplans/page/2/"]
        for li in link:
            yield scrapy.FormRequest(url=li, callback=self.plan_link, dont_filter=True)

    def plan_link(self, response):
        links = response.xpath('//div[@class="col-md-6 col-sm-12"][1]/a/@href').extract()
        for link in links:
            yield scrapy.FormRequest(url=link, callback=self.plan, dont_filter=True)

    def plan(self, response):
        try:
            Type = 'SingleFamily'
        except Exception as e:
            Type = 'SingleFamily'
            print(e)

        try:
            PlanName = response.xpath('//h2/span/text()').extract()[0].strip()
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

            BaseSqft = response.xpath("//*[contains(text(),'Base SqFt:')]/../text()").extract_first(default='0')
            BaseSqft = BaseSqft.split(':')[-1].strip()
            BaseSqft = BaseSqft.replace(',', '')
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]

        except Exception as e:
            print(e)

        try:
            Baths =response.xpath("//*[contains(text(),'Full Baths:')]/../text()").extract_first(default='0')
            Baths = re.findall(r"(\d+)", Baths)[0]

            if len(Baths) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0

        except Exception as e:
            Baths = 0
            print(e)

        try:
            Bedrooms = response.xpath("//*[contains(text(),'Bedrooms:')]/../text()").extract_first(default='0')
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)
            Bedrooms = 0

        try:

            Garage = response.xpath("//*[contains(text(),'Garages')]/../text()").extract_first(default='0')
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
            ElevationImage = response.xpath('//div[@class="fl-photo-content fl-photo-img-jpg"]/img/@src').extract_first(default='')
        except Exception as e:
            print(e)
            ElevationImage = ""

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

        temp_dict = {
            'PlanName': PlanName,
            'unique_number' : unique_number
        }
        self.temp_list.append(temp_dict)


        link = "https://www.eagle1constructionllc.com/property_category/available-homes/"
        yield scrapy.FormRequest(url=link,callback=self.spec_link,dont_filter=True,meta={'SubdivisionNumber':SubdivisionNumber})


    def spec_link(self,response):
        SubdivisionNumber = response.meta['SubdivisionNumber']
        links = response.xpath('//div[@class="col-md-6 col-sm-12"][1]/a/@href').extract()
        for link in links:
            yield scrapy.FormRequest(url='https://www.eagle1constructionllc.com/properties/104-nw-woodbury-drive/', callback=self.spec, dont_filter=True,meta={'SubdivisionNumber':SubdivisionNumber})

    def spec(self,response):

        try:
            SpecStreet1 = response.xpath('//h2/span[@class="title-text pp-primary-title"]/text()').extract_first('')
        except Exception as e:
            print(e)

        try:
            add = response.xpath('//h2/span[@class="title-text pp-secondary-title"]/text()').extract_first('')
            print(add)
        except Exception as e:
            print(e)

        try:
            SpecC = add.split(",")[0].strip()
            SpecCity = SpecC
        except Exception as e:
            print(e)

        try:
            SpecState = add.split(",")[1]
            SpecState = SpecState.strip()
            SpecState = SpecState.split(" ")[0]
        except Exception as e:
            print(e)

        try:
            SpecZIP = add.split(",")[1].strip()
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
            SpecBedrooms = response.xpath("//*[contains(text(),'Bedrooms:')]/../text()").extract_first('').strip().replace("\n", "").replace("\t", "")
            print(SpecBedrooms)
            SpecBedrooms = re.findall(r'(\d{1})', SpecBedrooms)[0]
        except Exception as e:
            print(str(e))

        try:
            SpecBaths = response.xpath("//*[contains(text(),'Full Baths:')]/../text()").extract_first('').strip().replace("\n", "").replace("\t", "")
            tmp = re.findall(r"(\d+)", SpecBaths)
            SpecBaths = tmp[0]
            if len(tmp) > 1:
                halfbath = 1
            else:
                halfbath = 0
        except Exception as e:
            print(str(e))

        try:
            SpecGarage = response.xpath("//*[contains(text(),'Garages')]/../text()").extract_first('')
            SpecGarage = SpecGarage.split("•")[2].split("•")[0]
            SpecGarage = re.findall(r'(\d{1})', SpecGarage)[0]
        except Exception as e:
            print(str(e))

        try:
            SpecSqft = response.xpath("//*[contains(text(),'Base SqFt:')]/../text()").extract_first('').strip().replace("\n", "").replace("\t", "").replace(",","")
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
            image = response.xpath('//div[@class="fl-photo-content fl-photo-img-jpg"]/img/@src').extract_first('')
            ElevationImage = image
        except Exception as e:
            print(e)

        try:
            old_planname = response.xpath("//*[contains(text(),'Floorplan:')]/../text()").extract_first('').replace('”','"').replace('”','"').strip()
            print(old_planname)
        except Exception as e:
            print(e)
            old_planname = ""

        # try:
        #     old_planname = int(hashlib.md5(bytes(old_planname, "utf8")).hexdigest(), 16) % (10 ** 30)
        #     f = open("html/%s.html" % old_planname, "wb")
        #     f.write(response.body)
        #     f.close()
        # except Exception as e:
        #     print(e)

        try:
            SpecWebsite = response.url
        except Exception as e:
            print(e)


        print(self.temp_list)
        for i in self.temp_list:

            PlanName= i['PlanName'].replace('”','"').replace('“','"').strip()
            print(PlanName,old_planname)
            unique_number = i['unique_number']


            if PlanName == old_planname:
                # ----------------------- Don't change anything here --------------------- #
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = PlanNumber
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

            else:
                PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
                SubdivisionNumber = self.builderNumber
                unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
                item = BdxCrawlingItem_Plan()
                item['Type'] = 'SingleFamily'
                item['PlanNumber'] = PlanNumber
                item['unique_number'] = unique_number  # < -------- Changes here
                item['SubdivisionNumber'] = SubdivisionNumber
                item['PlanName'] = PlanName
                item['PlanNotAvailable'] = '0'
                item['PlanTypeName'] = 'Single Family'
                item['BasePrice'] = '0'
                item['BaseSqft'] = ''
                item['Baths'] = ''
                item['HalfBaths'] = ''
                item['Bedrooms'] = ''
                item['Garage'] = ''
                item['Description'] = "Spacious Great Room w/ vaulted ceiling Hardwood floors in entry, kitchen, dining room and hall Island Kitchen w/ granite countertops walk-in pantry & double ovens Large Master Suite with walk-in shower,granite vanity, and walk-in closet Fully finished basement with 2 bedrooms and large family room Covered front porch and back deck,Front yard landscaping included"
                item['ElevationImage'] = "https://static.wixstatic.com/media/e05021_b779ac90ccb54a57a8e4993d131f547e.png/v1/fill/w_610,h_370,al_c,q_95/e05021_b779ac90ccb54a57a8e4993d131f547e.webp|https://static.wixstatic.com/media/e05021_4f2a224f116e8062504b23c973040d2f.png/v1/fill/w_610,h_370,al_c,q_95/e05021_4f2a224f116e8062504b23c973040d2f.webp|https://static.wixstatic.com/media/e05021_020ee1e5e8294075a2e8232a8ef04830.png/v1/fill/w_610,h_370,al_c,q_95/e05021_020ee1e5e8294075a2e8232a8ef04830.webp|https://static.wixstatic.com/media/e05021_7fc88e50993572892e6edc0de3480949.png/v1/fill/w_610,h_370,al_c,q_95/e05021_7fc88e50993572892e6edc0de3480949.webp|https://static.wixstatic.com/media/e05021_321c34a41c0398a94d9e528ebdb5d48a.png/v1/fill/w_615,h_313,al_c,q_85,usm_0.66_1.00_0.01/e05021_321c34a41c0398a94d9e528ebdb5d48a.webp"
                item['PlanWebsite'] = response.url
                yield item



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl eagle1constructionllc'.split())


