# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
import requests
from scrapy.http import HtmlResponse
class casabellaconstructionSpider(scrapy.Spider):
    name = 'casabellaconstruction'
    allowed_domains = ['casabellaconstruction.com']
    start_urls = ['https://casabellaconstruction.com/']

    builderNumber = "529443120563621281917374561655"

    def parse(self, response):
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
        item['Street1'] = "10502 N Ambassador Dr Ste 230"
        item['City'] = "Kansas City"
        item['State'] = "MO"
        item['ZIP'] = "64153"
        item['AreaCode'] = "816"
        item['Prefix'] = "436"
        item['Suffix'] = "9969"
        item['Extension'] = ""
        item['Email'] = "amberjury@yahoo.com"
        item['SubDescription'] = "Casa Bella Construction has earned a reputation as one of the Kansas City metro area’s premier custom home builders. They are consistent winners of the Home Builder’s Associations’ American Dream Grand Award, Pick of the Parade, and Distinctive Design and Plan contests. They have also won many Kansas City Home and Gardens and Kansas City at Home publications’ Model of the Year Awards."
        item['SubImage'] = ""
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        # In case you have found the communities (subdivision) and Homes (Specs) but you are not able to find the plan details then,
        # please use this line of code, and reference this unique_number  in All Home(Specs)


        url = ['https://casabellaconstruction.com/home-plans/']
        for u in url:
            yield scrapy.Request(url=u, callback=self.plan_link,dont_filter=True)



    def plan_link(self,response):
        links = response.xpath('//div[@class="banner-layers container"]/a/@href').getall()
        for link in links:
            yield scrapy.Request(url=link,callback=self.plan_detail,dont_filter=True)


    def plan_detail(self,response):

        try:
            PlanName = response.xpath('//div[@class="text-inner text-center"]/h1/text()').get()
            PlanName = PlanName.strip()
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
            BasePrice = 0
        except Exception as e:
            print(e)

        try:

            BaseSqft = 0
        except Exception as e:
            print("BaseSqft: ", e)
        try:
            planbeds = response.xpath('//div[@class="text-inner text-center"]/p/text()[2]').get()
            planbeds = re.sub('<[^<]+?>', '', str(planbeds)).strip()
            if planbeds == '':
                planbeds = 0
        except Exception as e:
            print("planbeds: ", e)
        try:
            planbath = response.xpath('//div[@class="text-inner text-center"]/p/text()[2]').get()
            planbath = re.sub('<[^<]+?>', '', str(planbath))
            tmp = re.findall(r"(\d+)", planbath)
            planbath = tmp[0]
            print("Bathrooms ----> ",planbath)
            if len(tmp) > 1:
                planHalfBaths = 1
                print(planHalfBaths)
            else:
                planHalfBaths = 0
                # print(planHalfBaths)
            # print(planbath)
        except Exception as e:
            print("planbath: ", e)
        try:
            # cargarage = response.xpath('//*[contains(text(),"Garages:")]/../text()').get()
            # cargarage = re.sub('<[^<]+?>', '', str(cargarage))
            cargarage = 0
        except Exception as e:
            print("cargarage: ", e)
        try:
            PlanImage = []
            PImage1 = response.xpath('//div[@class="img-inner image-cover dark"]/img/@src').getall()
            PImage2 = response.xpath('//div[@class="box-image"]//img/@src').getall()
            PImage = PImage1 + PImage2
            for p in PImage:
                # PlanImages = "".join(re.findall(r'background-image:url(\(.*?)\)',p, re.DOTALL)).strip('(')
                PlanImage.append(p)
            PlanImage ="|".join(PlanImage)
        except Exception as e:
            print("SpecElevationImage: ", e)
        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)
        unique = str(PlanNumber) + str(self.builderNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
                10 ** 30)  # < -------- Changes here

        # SubdivisionNumber = SubdivisionNumber  # if subdivision is there
        SubdivisionNumber = self.builderNumber #if subdivision is not available
        unique = str(PlanNumber)+str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = PlanName
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = BasePrice
        item['BaseSqft'] = BaseSqft
        item['Baths'] = planbath
        item['HalfBaths'] = planHalfBaths
        item['Bedrooms'] = planbeds
        item['Garage'] = 0
        item['Description'] = "Casa Bella Construction has earned a reputation as one of the Kansas City metro area’s premier custom home builders."
        item['ElevationImage'] = PlanImage
        item['PlanWebsite'] = PlanWebsite
        yield item


        # ------------------------------------------- Extract Homedetails ------------------------------ #

    def Detail(self, response):


        #------------------------------------- Extracting Plans ------------------------- #
        datablock = response.xpath('//*[@class="accordion"]/div')

        for data in datablock:

            PlanName = data.xpath('./a/span/text()').extract_first()
            BaseSqft = 0

            basefeet = ''.join(data.xpath('./div/div/div/div/p/text()').extract())

            try:
                Baths_temp = ''.join(re.findall(r'(\d.\d+) baths',basefeet)) or ''.join(re.findall(r'(\d+) baths',basefeet))

                if '.' in Baths_temp:
                    Baths = Baths_temp[0]
                    HalfBaths = 1
                else:
                    Baths = Baths_temp
                    HalfBaths = 0
            except Exception as e:
                try:
                    if not Baths:
                        Baths = 0
                        HalfBaths = 0
                except Exception as e:
                    if Baths == "":
                        Baths = 0
                        HalfBaths = 0

            try:
                Bedrooms = re.findall(' (\d+) bedrooms', basefeet)[0]
                if not Bedrooms:
                    Bedrooms = 0
            except Exception as e:
                Bedrooms = 0

            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
            except Exception as e:
                print(e)

            # try:
            #     SubdivisionNumber = response.meta['sbdn']
            # except Exception as e:
            #     print(e)

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
                # print(BasePrice)
                # BasePrice = re.findall(r"(\d+)", BasePrice)[0]
            except Exception as e:
                print(e)

            try:
                Garage = 0
            except Exception as e:
                print(e)

            try:
                Description = ''
            except Exception as e:
                print(str(e))

            try:
                ElevationImage = data.xpath('./div/div/div/div//img/@src').extract()

                if ElevationImage != []:
                    ElevationImage = "|".join(ElevationImage)
                else:
                    ElevationImage = ''


                while ElevationImage.startswith('|'):
                    ElevationImage = ElevationImage[1:]
                while ElevationImage.endswith('|'):
                    ElevationImage = ElevationImage[:-1]

            except Exception as e:
                print(e)

            try:
                PlanWebsite = response.url
            except Exception as e:
                print(e)

            if Baths == '':
                Baths = 0

            # ----------------------- Don't change anything here --------------

            unique = str(PlanNumber)  # < -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
            item = BdxCrawlingItem_Plan()
            item['Type'] = Type
            item['PlanNumber'] = PlanNumber
            item['unique_number'] = unique_number  # < -------- Changes here
            item['PlanName'] = PlanName

            item['SubdivisionNumber'] = self.builderNumber

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


from scrapy.cmdline import execute
if __name__ == '__main__':
    execute("scrapy crawl casabellaconstruction".split())