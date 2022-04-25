

# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'bruynhomes'
    allowed_domains = ['bruynhomes.com']
    start_urls = ['http://www.bruynhomes.com/']
    builderNumber = 49501

    def parse(self, response):

        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = '5356 Plainfield Ave NE'
        item2['City'] = 'Liberty'
        item2['State'] = 'MI'
        item2['ZIP'] = '49525'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "Mike has a passion for development, with an addiction to housing. His experience includes horizontal development, vertical construction, and brokerage. Mike founded The Brookeview Group LLC in 2008 after managing the Kansas City office for a multi-state developer. A few years later, Mike founded The Real Estate Store LLC, a brokerage focused on residential, commercial, and investment sales. Both companies work in tandem to develop, build, and broker development indeopendtently and within trusted partnerships. With over 18 years of real estate and construction experience, Mike credits the core values of integrity, commitment, and trust as the reason for his success. He believes every project should begin with the end in mind, this unique approach ensures success for partners, investors, and end-users alike."
        item2['SubImage'] = "https://bruynhomes.com/wp-content/uploads/2021/02/DSC_5309-1024x630.jpg|https://bruynhomes.com/wp-content/uploads/2021/02/DSC_5286-1024x630.jpg|https://bruynhomes.com/wp-content/uploads/2021/02/DSC_5338-1024x630.jpg|https://bruynhomes.com/wp-content/uploads/2018/01/img_6834_2-1030x686.jpg|https://bruynhomes.com/wp-content/uploads/2018/02/img_6828-1030x687.gif|https://bruynhomes.com/wp-content/uploads/2021/02/DSC_5286-1024x630.jpg|"
        item2['SubWebsite'] = 'https://bruynhomes.com/'
        item2['AmenityType'] = ''
        yield item2

        SubdivisionNumber = self.builderNumber  # if subdivision is not available
        planname = "1790 Solitude"
        PlanNumber = int(hashlib.md5(bytes(planname, "utf8")).hexdigest(), 16) % (10 ** 30)
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = planname
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = ""
        item['BaseSqft'] = ""
        item['Baths'] = "2"
        item['HalfBaths'] = "1"
        item['Bedrooms'] = "3"
        item['Garage'] = ""
        item['Description'] = ""
        item['ElevationImage'] = "https://bruynhomes.com/wp-content/uploads/2022/03/IMG_4733.jpg"
        item['PlanWebsite'] = response.url
        yield item

        SubdivisionNumber = self.builderNumber  # if subdivision is not available
        planname = "1733 Solitude"
        PlanNumber = int(hashlib.md5(bytes(planname, "utf8")).hexdigest(), 16) % (10 ** 30)
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = planname
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = ""
        item['BaseSqft'] = ""
        item['Baths'] = "2"
        item['HalfBaths'] = "1"
        item['Bedrooms'] = "4"
        item['Garage'] = ""
        item['Description'] = ""
        item['ElevationImage'] = "https://bruynhomes.com/wp-content/uploads/2021/10/Cambridge-Front-Elevation-Small-2-scaled.jpg"
        item['PlanWebsite'] = response.url
        yield item

        link = 'https://bruynhomes.com/gallery-features/'
        yield scrapy.FormRequest(url=link, callback=self.parse2, dont_filter=True)

    def parse2(self, response):
        links = response.xpath('//span[@class="avia_iconbox_title"]/../../a[contains(@href,"https://bruynhomes.com")]/@href').extract()
        for link in links:
            yield scrapy.FormRequest(url=link, callback=self.parse3, dont_filter=True)

    def parse3(self, response):
        try:
            PlanName = response.xpath('//h3/text()').extract_first('')
            print(PlanName)
        except Exception as e:
            print("PlanName: ", e)
        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = self.builderNumber
            print(SubdivisionNumber)
        except Exception as e:
            print(str(e))

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
            print(str(e))

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)
        try:
            Bedroo = response.xpath('//*[contains(text(),"Bedrooms:")]/../following-sibling::td/text()').extract_first('').replace("\n", "").strip()
            Bedrooms = re.findall(r"(\d+)", Bedroo)[0]
            # Bedrooms = Bedroom.split(' Bed')[0].strip()

        except Exception as e:
            Bedrooms = 0
            print("Bedrooms: ", e)

        try:
            Bathroo = response.xpath('//*[contains(text(),"Bathrooms:")]/../following-sibling::td/text()').extract_first('').strip().replace("\n","").strip()
            tmp = re.findall(r"(\d+)", Bathroo)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0

        except Exception as e:
            Baths = 0
            print("Baths: ", e)

        try:
            desc = response.xpath(
                '//div[@class="md:flex items-center"]//p/text()|//div[@class="w-full"]/p/text()').extract_first('')
            print(desc)
        except Exception as e:
            print(e)
            desc = ''

        try:
            Garage = response.xpath(
                '//div[@class="text z-t-20 z-text-white"]/text()[6]').extract_first('').strip().replace(',', '')
            Garage = re.findall(r"(\d+)", Garage)[0]
        except Exception as e:
            print("Garage: ", e)
            Garage = 0

        try:
            BaseSqft = response.xpath('//*[contains(text(),"Square Footage:")]/../following-sibling::td/text()').extract_first('').strip().replace(',', '')
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
        except Exception as e:
            print("BaseSQFT: ", e)

        try:
            ElevationImages = []
            ElevationImage2 = response.xpath("//ul[@class='avia-slideshow-inner']//li/div/div/following-sibling::img/@src").extract()
            if ElevationImage2 != []:
                for image in ElevationImage2:
                    ElevationImage2 =  image
                    ElevationImages.append(ElevationImage2)
            ElevationImage = "|".join(ElevationImages)

        except Exception as e:
            print(str(e))

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
        item['Description'] = desc
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl bruynhomes'.split())