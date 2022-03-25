


# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'celticbuilthomes'
    allowed_domains = ['celticbuilthomes.net']
    start_urls = ['https://celticbuilthomes.com/']
    builderNumber = 51334


    def parse(self, response):

        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = '1101 Chemawa Rd N'
        item2['City'] = 'Keizer'
        item2['State'] = 'OR'
        item2['ZIP'] = '97303'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "Celtic Homes built our house last June. We love it! From the foundation to the last touches on the house we could count on Jason to help us, answer my tons of text messages & support us any way he could. He was available to meet us whenever we wanted to walk through the construction. He & I looked at several floor plans for our lot and he was great at getting back to me via email to help us choose one that met our needs."
        item2['SubImage'] = "https://celticbuilthomes.com/wp-content/uploads/fpo-cta-full-width.jpg"
        item2['SubWebsite'] = 'https://celticbuilthomes.com/'
        # item2['AmenityType'] = ''
        yield item2

        link = 'https://celticbuilthomes.com/house-plans/'
        yield scrapy.FormRequest(url=link,callback=self.plan_link,dont_filter=True)

    def plan_link(self,response):
        links = response.xpath('//a[@class="row plan"]/@href').extract()
        for link in links:
            yield scrapy.FormRequest(url=link,callback=self.plan,dont_filter=True)

    def plan(self,response):
        try:
            Type = 'SingleFamily'
        except Exception as e:
            Type = 'SingleFamily'
            print(e)

        try:
            PlanName = response.xpath('//h1/text()').extract()[0].strip()
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
            BaseSqft = response.xpath('//i[@class="fa fa-expand"]/following-sibling::div/text()').extract_first(default='0')
            BaseSqft = BaseSqft.split(':')[-1].strip()
            BaseSqft = BaseSqft.replace(',', '')

        except Exception as e:
            print(e)

        try:
            Baths = response.xpath('//i[@class="fa fa-shower"]/following-sibling::div/text()').extract_first(default='0')
            Baths = re.findall(r"(\d+)", Baths)[0]
            print(Baths)
            if len(Baths) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0

        except Exception as e:
            Baths = 0
            print(e)

        try:
            Bedrooms = response.xpath('//i[@class="fa fa-bed"]/following-sibling::div/text()').extract_first(default='0')
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)
            Bedrooms = 0

        try:
            Garage = response.xpath('//i[@class="fa fa-car"]/following-sibling::div/text()').extract_first("")
            Garage = re.findall(r"(\d+)", Garage)[0]
        except Exception as e:
            print(e)
            Garage = "0"

        try:
            Description = ''
        except Exception as e:
            print(e)

        try:
            ElevationImage = response.xpath('//div[@class="slick-track"]//img/@src').extract_first(default='')
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



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl celticbuilthomes'.split())
