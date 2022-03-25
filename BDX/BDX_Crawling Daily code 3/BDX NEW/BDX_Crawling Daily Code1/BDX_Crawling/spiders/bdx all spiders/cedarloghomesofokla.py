

# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class vtshomeshomesSpider(scrapy.Spider):
    name = 'cedarloghomesofokla'
    allowed_domains = []
    start_urls = ['https://cedarloghomesofokla.com/']


    builderNumber = "24298"

    def parse(self, response):
        print('--------------------')



        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = '51152'
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = 'OK-150'
        item['City'] = 'Checotah'
        item['State'] = 'OK'
        item['ZIP'] = '74426'
        item['AreaCode'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Prefix'] = ""
        item['Email'] = ''
        item['SubDescription'] = "We are a small family business in Oklahoma, representing Katahdin Cedar Log Homes. We have experience in working with customers to design the custom log homes they've envisioned. We have several log home building crews who will work with you to build your dream home"
        item['SubImage'] = "https://img1.wsimg.com/isteam/ip/1d8ea83e-5850-4978-a2e4-8087500ed566/a55dc703-204b-43ec-9540-17e9c7871074.jpg|https://img1.wsimg.com/isteam/ip/1d8ea83e-5850-4978-a2e4-8087500ed566/159a7f07-f184-4756-808c-90e5391f8c6d.jpg/:/rs=w:1300,h:800|https://img1.wsimg.com/isteam/ip/1d8ea83e-5850-4978-a2e4-8087500ed566/adc5fcd4-35f3-4f6e-a622-b4dd56292add.jpg/:/rs=w:1300,h:800|https://img1.wsimg.com/isteam/ip/1d8ea83e-5850-4978-a2e4-8087500ed566/c2faa853-cfb5-4753-b74d-643261bd3703.jpg/:/rs=w:1300,h:800|https://img1.wsimg.com/isteam/ip/1d8ea83e-5850-4978-a2e4-8087500ed566/fd70fd26-42f2-4d14-b2a3-869f59d70110.jpg/:/rs=w:1300,h:800|https://img1.wsimg.com/isteam/ip/1d8ea83e-5850-4978-a2e4-8087500ed566/4160f8a9-7f61-40af-b911-b309c453deeb.jpg/:/rs=w:1300,h:800|https://img1.wsimg.com/isteam/ip/1d8ea83e-5850-4978-a2e4-8087500ed566/6226a918-68ce-4637-8b3e-3a4cddd588e8.jpg/:/rs=w:1300,h:800"
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link= 'https://cedarloghomesofokla.com/floor-plans'
        yield scrapy.Request(url=link, callback=self.parse2)

    def parse2(self,response):

        #------------- need to change from here ---#


        'Senator ~ 1725 sq.ft. ~ 3 bedrroms/2 baths'
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
            Baths = response.xpath("//*[contains(text(),'Baths')]/../text()").extract_first(default='0').strip().replace(",", "")
            Baths = Baths.split(" ")[0]
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
            Bedrooms = response.xpath("//*[contains(text(),'Beds')]/../text()").extract_first(default='0').strip().replace(",", "")
            Bedrooms = Bedrooms.split(" ")[0]
            print(Bedrooms)
        except Exception as e:
            print(e)

        try:
            Garage = response.xpath("//*[contains(text(),'Garage')]/../text()").extract_first(default='0').strip().replace(",", "")
            Garage = Garage.split(" ")[0]
            Garage = re.findall(r"(\d+)", Garage)[0]
            print(Garage)
        except Exception as e:
            print(e)
            Garage = 0.0


        try:
            BaseSqft = response.xpath("//*[contains(text(),'SqF')]/../text()").extract_first(
                default='0').strip().replace(",", "")
            BaseSqft = BaseSqft.split(" ")[0]
            print(BaseSqft)

        except Exception as e:
            print(e)

        try:
            Description = response.xpath("//h2/following-sibling::div/p[2]/text()").extract_first('')

            print(Description)
        except Exception as e:
            Description = ''

        try:
            images = []
            image1 = response.xpath('//li/@data-thumb').extract_first('')
            image2 = response.xpath("//img[contains(@src,'https://biltmoreco.visualwebb4.com/files')]/@src").extract()
            if image1 != "":
                images.append(image1)
            if image2 != []:
                for im in image2:
                    images.append(im)
            ElevationImage = "".join(images)
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
    execute("scrapy crawl cedarloghomesofokla".split())