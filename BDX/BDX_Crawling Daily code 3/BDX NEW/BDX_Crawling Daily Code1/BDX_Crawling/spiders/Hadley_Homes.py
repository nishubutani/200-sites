import hashlib
import json
import re

import requests
import scrapy
from scrapy.selector import Selector
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision


class HadleyHomesSpider(scrapy.Spider):
    name = 'Hadley_Homes'
    allowed_domains = ['www.hadleyhomebuilder.com']
    start_urls = ['http://www.hadleyhomebuilder.com/']
    builderNumber = 52931

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
        item['Street1'] = '56861 Grand River Ave. P.O. Box 328'
        item['City'] = 'New Hudson'
        item['State'] = 'MI'
        item['ZIP'] = '48165'
        item['AreaCode'] = '248'
        item['Prefix'] = '437'
        item['Suffix'] = '1728'
        item['Extension'] = ""
        item['Email'] = 'info@hadleyhomebuilder.com'
        item['SubDescription'] = "Hadley Home Builders, Inc. is a locally owned and operated residential construction company specializing in new construction. We are small enough for the personal touch and large enough for you to be confident the work will be done in a timely and professional manner. Our number one priority is our customer's satisfaction and we achieve that through quality craftsmanship and first class service."
        item['SubWebsite'] = response.url
        img_link = 'http://www.hadleyhomebuilder.com' + str(response.xpath('//ul[@class="uk-subnav uk-subnav-line"]/li[2]/a/@href').get())
        response = requests.request("GET", img_link)
        res1 = Selector(text=response.text)
        imgs = res1.xpath('//a[@class="uk-position-cover"]/@href').getall()
        img = []
        for i in imgs:
            image = 'http://www.hadleyhomebuilder.com' + str(i)
            img.append(image)
        img = '|'.join(img)
        item['SubImage'] = img
        item['AmenityType'] = ''

        yield item

        url = 'http://www.hadleyhomebuilder.com/index.php/home-plans'
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.Plans)

    def Plans(self,response):
        links = response.xpath('//a[@class="uk-button"]/@href').getall()
        for link in links:
            url = 'http://www.hadleyhomebuilder.com' + str(link)
            yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.Plan_data)

    def Plan_data(self, response):
        Type = 'SingleFamily'
        try:
            PlanName = response.xpath('//div[@class="uk-width-medium-1-2 uk-text-center"]/h2/text()').get()
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        except:
            PlanName = response.xpath('//div[@class="uk-width-1-2 uk-text-center"]/h2/text()').get()
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        SubdivisionNumber = self.builderNumber
        unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        PlanNotAvailable = 0
        PlanTypeName = 'Single Family'

        url = response.url

        # image = data1["items"][i]["image"]
        sbbg = response.xpath('//div[@class="uk-width-medium-1-2 uk-text-center"]/h3/text()').get()
        if sbbg != None:

            sqft = re.findall(r'at (.*?) s.f.',sbbg)[0]

            Bedrooms = re.findall(r'Bath, (.*?) Bedroom',sbbg)[0]

            bathrooms = re.findall(r', (.*?) Bath,',sbbg)[0]
            Bath = re.findall(r"(\d+)", bathrooms)
            Baths = Bath[0]
            tmp = Bath
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0


            try:
                if PlanName == 'The Pentwater':
                    Garage = 3
                else:
                    Garage = re.findall(r'Opional (.*?) Car Garage',sbbg)[0]
            except:
                Garage = 0
        else :
            sbbg = response.xpath('//div[@class="uk-width-1-2 uk-text-center"]/h3/text()').get()
            sqft = re.findall(r'at (.*?) s.f.', sbbg)[0]

            Bedrooms = re.findall(r'Bath, (.*?) Bedroom', sbbg)[0]

            bathrooms = re.findall(r', (.*?) Bath,', sbbg)[0]
            Bath = re.findall(r"(\d+)", bathrooms)
            Baths = Bath[0]
            tmp = Bath
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0

            try:
                if PlanName == 'The Pentwater':
                    Garage = 3
                else:
                    Garage = re.findall(r'Opional (.*?) Car Garage', sbbg)[0]
            except:
                Garage = 0


        Description = response.xpath('//div[@class="uk-width-1-2 uk-text-center"]/p[2]/text()').get()
        if Description != None:
            Description = Description
        else:
            Description = "We’re the Custom Home Builder dedicated to your complete satisfaction. Hadley Home Builders, Inc. is a locally owned and operated residential construction company specializing in new construction. We are small enough for the personal touch and large enough for you to be confident the work will be done in a timely and professional manner. Our number one priority is our customer's satisfaction and we achieve that through quality craftsmanship and first class service."

        imgs = response.xpath('//img/@src').getall()[2:]
        images = []
        for img in imgs:
            image = 'http://www.hadleyhomebuilder.com' + str(img)
            images.append(image)
        Elevationimage = '|'.join(images)

        BasePrice = 0

        # unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['Type'] = Type
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number  # < -------- Changes here
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = PlanName
        item['PlanNotAvailable'] = PlanNotAvailable
        item['PlanTypeName'] = PlanTypeName
        item['BasePrice'] = BasePrice
        item['BaseSqft'] = str(sqft)
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = Description
        item['ElevationImage'] = Elevationimage
        item['PlanWebsite'] = url
        yield item



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl Hadley_Homes".split())
