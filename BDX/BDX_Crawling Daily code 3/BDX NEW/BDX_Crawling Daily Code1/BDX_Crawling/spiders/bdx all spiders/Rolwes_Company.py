# -*- coding: utf-8 -*-
import hashlib
import re
import time

import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class Rolwes_CompanySpider(scrapy.Spider):
    name = 'Rolwes_Company'
    allowed_domains = ['rolwesco.com']
    start_urls = ['http://rolwesco.com/']

    builderNumber = "283642830766554092828081401890"
    counter = 0
    status = False

    def parse(self, response):

        # images = ''
        # image = response.xpath('//div[@class="cycle-slideshow"]/img/@src').extract()
        # for i in image:
        #     images = images + i + '|'
        # images = images.strip('|')
        #
        # item = BdxCrawlingItem_subdivision()
        # item['sub_Status'] = "Active"
        # item['SubdivisionNumber'] = ''
        # item['BuilderNumber'] = self.builderNumber
        # item['SubdivisionName'] = "No Sub Division"
        # item['BuildOnYourLot'] = 0
        # item['OutOfCommunity'] = 0
        # item['Street1'] = '9101 Mile 6 Rd'
        # item['City'] = 'Ballwin'
        # item['State'] = 'MO'
        # item['ZIP'] = '63021'
        # item['AreaCode'] = '314'
        # item['Prefix'] = '821'
        # item['Suffix'] = '9601'
        # item['Extension'] = ""
        # item['Email'] = 'info@RolwesCo.com'
        # item['SubDescription'] = 'We have a new home that’s just right for you. Explore our new home communities throughout the St. Louis area or if you need to move NOW, check out our move-in ready homes. Read what our buyers say about Rolwes Company, their favorite St. Louis new home builders. Hear what owner Greg Rolwes says about his personal promise to deliver a superior experience to your home-buying process.'
        # item['SubImage'] = images
        # item['SubWebsite'] = response.url
        # item['AmenityType'] = ''
        # yield item

        community=response.xpath('//a[contains(text(),"Our Communities")]//@href').extract_first()
        yield scrapy.FormRequest(url=community,callback=self.community,dont_filter=True)


    def community(self,response):
        homes = []
        homess = response.xpath('//div[@class="w33 columns"]/a/@href').getall()
        img = response.xpath('//div[@class="w33 columns"]/a/following-sibling::p/strong[2]/text()').getall()

        for homess, img in zip(homess, img):
            if 'SOLD' in img or 'Coming Soon!' in img:
                print("hii")
            else:
                print(homess)
                # print(type(homess))
                yield scrapy.FormRequest(url=homess,callback=self.communites,dont_filter=True)

    def communites(self,response):
        subdivisonName = response.xpath('//div[@class="container"]//h1//text()|//div[@class="green-title"]//h1//text()').extract_first()
        if subdivisonName!='Your Land Our Plan®':

            subdivisonNumber = int(hashlib.md5(bytes(subdivisonName+response.url,"utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % subdivisonNumber, "wb")
            f.write(response.body)
            f.close()

            try:
                phone = response.xpath('//div[@class="gray-box blue"]/p/text()').extract_first('').replace("\r","").replace("\n","").strip()
                # print(phone)
            except Exception as e:
                print(e)
                phone=''

            if phone != '':
                areacode = phone.split(")")[0].replace("(","")
                # print(areacode)

                prefix = phone.split(".")[0].split(")")[1].strip()
                # print(prefix)

                suffix = phone.split(".")[1].strip()
                # print(suffix)

            else:
                areacode = ''
                prefix = ''
                suffix = ''

            a = []
            # aminity = ''.join(response.xpath('//*[@class="ll-features-content__half right col-md-1of2"]/ul[1]/li/text()').extract())
            try:
                aminity = ''.join(response.xpath('//div[@class="w70 columns"]//text()').getall())
                aminity = aminity.title()
            except Exception as e:
                print(e)

            amenity_list = ["Pool", "Playground", "GolfCourse", "Tennis", "Soccer", "Volleyball", "Basketball",
                            "Baseball", "Views", "Lake", "Pond", "Marina", "Beach", "WaterfrontLots", "Park",
                            "Trails", "Greenbelt", "Clubhouse", "CommunityCenter"]
            for i in amenity_list:
                # print(i)
                if i in aminity:
                    # print(i)
                    a.append(i)
            ab = '|'.join(a)

            address=response.xpath('//div[@class="gray-box blue"]//a[contains(text(),"Directions")]//@href').get().split('/')[5]
            item2 = BdxCrawlingItem_subdivision()
            item2['sub_Status'] = "Active"
            item2['SubdivisionName'] = subdivisonName
            item2['SubdivisionNumber'] = subdivisonNumber
            item2['BuilderNumber'] = self.builderNumber
            item2['BuildOnYourLot'] = 0
            item2['OutOfCommunity'] = 1
            item2['Street1'] = address.split('+')[0].replace(',','')
            item2['City'] = address.split('+')[1].replace(',','')
            item2['State'] = address.split('+')[2].replace(',','')
            item2['ZIP'] = address.split('+')[3].replace(',','')
            item2['AreaCode'] = areacode
            item2['Prefix'] = prefix
            item2['Suffix'] = suffix
            item2['Extension'] = ""
            item2['Email'] = response.xpath('//a[contains(text(),"@")]/text()').get()
            item2['SubDescription'] = "".join(response.xpath('//div[@class="sec"]//p//text()').extract()[0:3])
            item2['AmenityType'] = ab
            image=[]
            img=response.xpath('//div[@class="cycle-pager"]/following-sibling::img//@src').getall()
            for im in img:
                image.append(im)
            image='|'.join(image)
            item2['SubImage'] = image
            item2['SubWebsite'] =response.url
            yield item2


            homes=[]
            homess = response.xpath('//div[@class="w50 columns row"]/a/@href').getall()
            img=response.xpath('//div[@class="w50 columns row"]/a/img/@src').getall()

            for homess,img in zip (homess,img):
                if 'Sold' in img:
                    print()
                else:
                    homes.append(homess)
            plan = response.xpath('//div[@class="w50 columns"]/a/@href').getall()
            if plan != []:
                for pl in plan:
                    yield scrapy.FormRequest(url=pl,callback=self.plan,dont_filter=True,meta={'subdivisonNumber':item2['SubdivisionNumber'],'subdivisonName':item2['SubdivisionName'],'homes':homes})
                    # yield scrapy.FormRequest(url='https://rolwesco.com/floorplans/rochester/',callback=self.plan,dont_filter=True,meta={'subdivisonNumber':item2['SubdivisionNumber'],'subdivisonName':item2['SubdivisionName'],'homes':homes})

            else:
                for link in homes:
                    print(link)
                    yield scrapy.FormRequest(url=link,callback=self.fakeplan,dont_filter=True,meta={'subdivisonNumber':item2['SubdivisionNumber'],'subdivisonName':item2['SubdivisionName'],'homes':homes})
        else:
            print()
    def plan(self,response):

        subdivisonNumber=response.meta['subdivisonNumber']
        subdivisonName=response.meta['subdivisonName']
        unique = str(subdivisonNumber) + str(response.url)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['unique_number'] = unique_number
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
        item['SubdivisionNumber'] = subdivisonNumber
        item['PlanName'] = response.xpath('//div[@class="green-title"]//h1/text()').get()
        item['PlanNotAvailable'] = 1
        item['PlanTypeName'] = "Single Family"
        try:
            BasePrice = response.xpath('//span[contains(text(),"Price:")]/../text()').get()
            BasePrice = BasePrice.replace(",","")
            BasePrice = re.findall(r"(\d+)", BasePrice)[0]
        except Exception as e:
            print(e)
            BasePrice = '0'

        item['BasePrice'] = BasePrice
        item['BaseSqft'] = 0
        bath=response.xpath('//span[contains(text(),"Baths:")]/../text()').get(default='')
        if '.' in bath:
            item['HalfBaths'] = 1
            item['Baths'] =bath.split('.')[0]
        else:
            item['HalfBaths'] = 0
            item['Baths'] = bath

        item['Bedrooms'] = response.xpath('//span[contains(text(),"Beds:")]/../text()').get(default='').strip()
        item['Garage'] = response.xpath('//span[contains(text(),"Garage:")]/../text()').get(default='').strip()
        item['Description'] = response.xpath('//div[@class="w70 columns"]/p/text()').get(default='').strip()
        image=[]
        img=response.xpath('//div[@class="cycle-pager"]/following-sibling::img/@src|//div[@class="w50 columns"]/a/@href').getall()
        for im in img:
            image.append(im)
        image='|'.join(image)
        item['ElevationImage'] = image
        item['PlanWebsite'] = response.url
        yield item

        try:
            homes=response.meta['homes']
        except Exception:
            homes = []
        for home in homes:
            yield scrapy.FormRequest(url=home, callback=self.HomesDetails, dont_filter=True,
                                     meta={'PN': item['unique_number'],'subdivisonName':subdivisonName,'subdivisonNumber':subdivisonNumber})


    def HomesDetails(self, response):

        # # subdivisonNumber = response.meta['subdivisonNumber']
        # item = BdxCrawlingItem_Plan()
        # unique = str("Plan Unknown") + str(self.builderNumber)
        # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        # item['unique_number'] = unique_number
        # item['Type'] = "SingleFamily"
        # item['PlanNumber'] = "Plan Unknown"
        # item['SubdivisionNumber'] = self.builderNumber
        # item['PlanName'] = "Plan Unknown"
        # item['PlanNotAvailable'] = 1
        # item['PlanTypeName'] = "Single Family"
        # item['BasePrice'] = 0
        # item['BaseSqft'] = 0
        # item['Baths'] = 0
        # item['HalfBaths'] = 0
        # item['Bedrooms'] = 0
        # item['Garage'] = 0
        # item['Description'] = ""
        # item['ElevationImage'] = ""
        # item['PlanWebsite'] = ""
        # yield item


        # Plan_name=response.xpath('//span[contains(text(),"Floor Plan:")]/../text()').get().strip().lower()
        image = []
        img = response.xpath('//div[@class="cycle-pager"]/following-sibling::img/@src|//div[@class="w50 columns"]/a/@href').getall()
        for im in img:
            image.append(im)
        SpecElevationImage = '|'.join(image)

        temptemp = response.xpath('//h1/text()').extract_first()
        print(temptemp)

        if temptemp == 'Chapelwood / ':
            address = response.xpath('//div[@class="gray-box blue"]//*[contains(text(),"Directions / Map")]//@href').get(
                default='').split('=')[-1]
            try:
                Home_Name = response.xpath('//div[@class="green-title"]//span//text()').get()
                SpecStreet1 = address.split('+')[0]
                SpecCity = address.split('+')[1]
                SpecState = address.split('+')[2]
                SpecZIP = address.split('+')[3]
                unique = SpecStreet1 + SpecCity + SpecState + SpecZIP + Home_Name
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()

            except Exception as e:
                print(e)

            try:
                # time.sleep(3)
                # PlanNumber =
                Plan = '567694329444975300706626788411'
            except Exception as e:
                print(e)

            try:
                SpecCountry = "USA"
            except Exception as e:
                print(e)

            try:
                SpecPrice = response.xpath('//span[contains(text(),"Priced:")]/../text()').get().replace(',',
                                                                                                         '').replace(
                    '$', '').replace('Call for Price', '').strip()
            except Exception as e:
                print(e)
                SpecPrice = 0
            if SpecPrice == '':
                SpecPrice = 0
            try:
                SpecSqft = 0
            except Exception as e:
                SpecSqft = 0

            bath = response.xpath('//span[contains(text(),"Baths:")]/../text()').get(default='')
            if '.' in bath:
                SpecHalfBaths = 1
                SpecBaths = bath.split('.')[0]
            else:
                SpecHalfBaths = 0
                SpecBaths = bath

            SpecBedrooms = response.xpath('//span[contains(text(),"Beds:")]/../text()').get(default='').strip()
            SpecGarage = response.xpath('//span[contains(text(),"Garage:")]/../text()').get(default='').strip()

            try:
                MasterBedLocation = "Down"
            except Exception as e:
                print(e)

            try:
                SpecDescription = response.xpath('//div[@class="w70 columns"]/p//text()').get()
            except Exception as e:
                print(e)

            try:
                SpecWebsite = response.url
            except Exception as e:
                print(e)

            # ----------------------- Don't change anything here ---------------- #
            item = BdxCrawlingItem_Spec()
            item['SpecNumber'] = SpecNumber
            item['PlanNumber'] = Plan
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
            item['SpecElevationImage'] = SpecElevationImage
            item['SpecWebsite'] = SpecWebsite
            yield item

        # if 'sold' in SpecElevationImage:
        #     print('home sold')
        # else:
        #     address=response.xpath('//div[@class="gray-box blue"]//*[contains(text(),"Directions / Map")]//@href').get(default='').split('=')[-1]
        #     try:
        #         Home_Name=response.xpath('//div[@class="green-title"]//span//text()').get()
        #         SpecStreet1 = address.split('+')[0]
        #         SpecCity = address.split('+')[1]
        #         SpecState = address.split('+')[2]
        #         SpecZIP = address.split('+')[3]
        #         unique = SpecStreet1 + SpecCity + SpecState + SpecZIP + Home_Name
        #         SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        #
        #         f = open("html/%s.html" % SpecNumber, "wb")
        #         f.write(response.body)
        #         f.close()
        #
        #     except Exception as e:
        #         print(e)
        #
        #     try:
        #         # time.sleep(3)
        #         # PlanNumber =
        #         Plan =  unique_number
        #     except Exception as e:
        #         print(e)
        #
        #     try:
        #         SpecCountry = "USA"
        #     except Exception as e:
        #         print(e)
        #
        #     try:
        #         SpecPrice = response.xpath('//span[contains(text(),"Priced:")]/../text()').get().replace(',','').replace('$','').replace('Call for Price','').strip()
        #     except Exception as e:
        #         print(e)
        #         SpecPrice=0
        #     if SpecPrice =='':
        #         SpecPrice = 0
        #     try:
        #         SpecSqft = 0
        #     except Exception as e:
        #         SpecSqft = 0
        #
        #     bath = response.xpath('//span[contains(text(),"Baths:")]/../text()').get(default='')
        #     if '.' in bath:
        #         SpecHalfBaths = 1
        #         SpecBaths = bath.split('.')[0]
        #     else:
        #         SpecHalfBaths = 0
        #         SpecBaths=bath
        #
        #     SpecBedrooms= response.xpath('//span[contains(text(),"Beds:")]/../text()').get(default='').strip()
        #     SpecGarage = response.xpath('//span[contains(text(),"Garage:")]/../text()').get(default='').strip()
        #
        #     try:
        #         MasterBedLocation = "Down"
        #     except Exception as e:
        #         print(e)
        #
        #
        #     try:
        #         SpecDescription =response.xpath('//div[@class="w70 columns"]/p//text()').get()
        #     except Exception as e:
        #         print(e)
        #
        #
        #     try:
        #         SpecWebsite = response.url
        #     except Exception as e:
        #         print(e)
        #
        #     # ----------------------- Don't change anything here ---------------- #
        #     item = BdxCrawlingItem_Spec()
        #     item['SpecNumber'] = SpecNumber
        #     item['PlanNumber'] = Plan
        #     item['SpecStreet1'] = SpecStreet1
        #     item['SpecCity'] = SpecCity
        #     item['SpecState'] = SpecState
        #     item['SpecZIP'] = SpecZIP
        #     item['SpecCountry'] = SpecCountry
        #     item['SpecPrice'] = SpecPrice
        #     item['SpecSqft'] = SpecSqft
        #     item['SpecBaths'] = SpecBaths
        #     item['SpecHalfBaths'] = SpecHalfBaths
        #     item['SpecBedrooms'] = SpecBedrooms
        #     item['MasterBedLocation'] = MasterBedLocation
        #     item['SpecGarage'] = SpecGarage
        #     item['SpecDescription'] = SpecDescription
        #     item['SpecElevationImage'] = SpecElevationImage
        #     item['SpecWebsite'] = SpecWebsite
        #     yield item

    def fakeplan(self, response):
        subdivisonNumber = response.meta['subdivisonNumber']
        item = BdxCrawlingItem_Plan()
        unique = str("Plan Unknown") + str(self.builderNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item['unique_number'] = unique_number
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = "Plan Unknown"
        item['SubdivisionNumber'] = subdivisonNumber
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

        image = []
        img = response.xpath(
            '//div[@class="cycle-pager"]/following-sibling::img/@src|//div[@class="w50 columns"]/a/@href').getall()
        for im in img:
            image.append(im)
        SpecElevationImage = '|'.join(image)
        if 'sold' in SpecElevationImage:
            print('home sold')
        else:

            address = response.xpath('//div[@class="gray-box blue"]//*[contains(text(),"Directions / Map")]//@href').get(
                default='').split('=')[-1]
            try:
                Home_Name = response.xpath('//div[@class="green-title"]//span//text()').get()
                SpecStreet1 = address.split('+')[0]
                SpecCity = address.split('+')[1]
                SpecState = address.split('+')[2]
                SpecZIP = address.split('+')[3]
                unique = SpecStreet1 + SpecCity + SpecState + SpecZIP + Home_Name
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()

            except Exception as e:
                print(e)

            try:
                # time.sleep(3)
                Plan = unique_number
            except Exception as e:
                print(e)

            try:
                SpecCountry = "USA"
            except Exception as e:
                print(e)

            try:
                SpecPrice = response.xpath('//span[contains(text(),"Priced:")]/../text()').get().replace(',',
                                                                                                         '').replace(
                    '$', '').replace('Call for Price', '').strip()
            except Exception as e:
                print(e)
                SpecPrice = 0
            if SpecPrice == '':
                SpecPrice = 0
            try:
                SpecSqft = 0
            except Exception as e:
                SpecSqft = 0

            bath = response.xpath('//span[contains(text(),"Baths:")]/../text()').get(default='')
            if '.' in bath:
                SpecHalfBaths = 1
                SpecBaths = bath.split('.')[0]
            else:
                SpecHalfBaths = 0
                SpecBaths = bath

            SpecBedrooms = response.xpath('//span[contains(text(),"Beds:")]/../text()').get(default='').strip()
            SpecGarage = response.xpath('//span[contains(text(),"Garage:")]/../text()').get(default='').strip()

            try:
                MasterBedLocation = "Down"
            except Exception as e:
                print(e)

            try:
                SpecDescription = response.xpath('//div[@class="w70 columns"]/p//text()').get()
            except Exception as e:
                print(e)

            try:
                SpecWebsite = response.url
            except Exception as e:
                print(e)

            # ----------------------- Don't change anything here ---------------- #
            item = BdxCrawlingItem_Spec()
            item['SpecNumber'] = SpecNumber
            item['PlanNumber'] = Plan
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
            item['SpecElevationImage'] = SpecElevationImage
            item['SpecWebsite'] = SpecWebsite
            yield item

            # --------------------------------------------------------------------- #


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl Rolwes_Company'.split())

