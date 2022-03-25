# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'vhco_homes'
    allowed_domains = ['https://vantagehomescolorado.com/']
    start_urls = ['https://vantagehomescolorado.com/']

    builderNumber = "13647"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()



        images = ''
        image = response.xpath('//div[@class="soliloquy-viewport"]/ul/li/img/@src').extract()
        for i in image:
            images = images + i + '|'
        images = images.strip('|')

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '5368 Deepwoods Court'
        item['City'] = 'Colorado Springs'
        item['State'] = 'CO'
        item['ZIP'] = '80921'
        item['AreaCode'] = '719'
        item['Prefix'] ='534'
        item['Suffix'] = '0984'
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = 'At Vantage Homes, we have mastered the art of listening. … From the day we opened our homebuilding company in Colorado Springs in 1983, our customers became our most important priority. Their input and perspective has enabled us to create imaginative new home designs that really work for the way they want to live.'
        item['SubImage'] = 'https://vantagehomescolorado.com/wp-content/uploads/1991-Walnut-Creek-Court-large-009-032-Exterior-Front-1498x1000-72dpi.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'https://vantagehomescolorado.com/floorplans/'
        yield scrapy.FormRequest(url=link, callback=self.parse2, dont_filter=True)

    def parse2(self, response):
        links = response.xpath('//a[@class="pp-post-link"]/@href').extract()
        print(links)
        for link in links:
            yield scrapy.FormRequest(url=link, callback=self.parse3, dont_filter=True)

    def parse3(self, response):

        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//h1[@class="fl-heading"]/span/text()').get()
        except Exception as e:
            PlanName = ''
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName + response.url, "utf8")).hexdigest(), 16) % (
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
            sqft = response.xpath("//h3[contains(text(),'TOTAL SQ. FT.')]/../p/span/text()").get()
            if '-' in sqft:
                sqft = sqft.split("-")[1]
            sqft = sqft.replace(',', '').strip()
            BaseSqft = re.findall(r"(\d+)", sqft)[0]

        except Exception as e:
            print(e)
            BaseSqft = '0'

        try:
            bath = response.xpath("//h3[contains(text(),'BATHROOMS')]/../p/span/text()").get()
            if '-' in bath:
                bath = bath.split("-")[1]
            tmp = re.findall(r"(\d+)", bath)
            Baths = tmp[0]
            if len(str(tmp)) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            print(e)


        try:
            Bedrooms = response.xpath("//h3[contains(text(),'BEDROOMS')]/../p/span/text()").get()
            if '-' in Bedrooms:
                Bedrooms = Bedrooms.split("-")[1]
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)

        try:
            Garage = response.xpath("//h3[contains(text(),'GARAGE')]/../p/span/text()").get()
            if '-' in Garage:
                Garage = Garage.split("-")[1]
            Garage = re.findall(r"(\d+)", Garage)[0]
            if not Garage:
                Garage = 0
        except Exception as e:
            Garage = 0
            print(e)

        try:
            desc = response.xpath('//div[@class="fl-module-content fl-node-content"]/p/text()').extract_first('')
            print(desc)
        except Exception as e:
            print(e)
            desc = ''

        try:
            images = []
            imagedata = response.xpath('//div[@aria-label="Slide 1"]/a/@href').getall()
            for id in imagedata:
                id = id
                images.append(id)
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
        item['Description'] = desc
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item

    # --------------------------------------------------------------------- #


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl vhco_homes'.split())