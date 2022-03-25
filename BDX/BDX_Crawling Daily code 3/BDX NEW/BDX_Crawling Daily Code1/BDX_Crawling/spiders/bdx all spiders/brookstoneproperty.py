# -*- coding: utf-8 -*-
import hashlib
import re
import json
import scrapy
# from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
import requests
# from scrapy.http import HtmlResponse


class brookstonepropertySpider(scrapy.Spider):
    name = 'brookstoneproperty'
    # allowed_domains = []
    start_urls = ['https://www.brookstoneproperty.com/']

    builderNumber = 63677

    def parse(self, response, **kwargs):

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
        item['Street1'] = "5302 51st Ave S"
        item['City'] = "Fargo"
        item['State'] = "ND"
        item['ZIP'] = "58104"
        item['AreaCode'] = "701"
        item['Prefix'] = "532"
        item['Suffix'] = "0898"
        item['Extension'] = ""
        item['Email'] = 'hello@brookstoneproperty.com'  # From Contact Us page
        item['SubDescription'] = "When you decide to build a home with Brookstone Property, you are choosing a home builder in Fargo, ND that is extremely hands-on during the building process. You are putting your trust in our team of professionals to build your new home that will be the backdrop where all your memories are created. It’s our mission to build our homes with excellence and our expertise and dedication will show in every step of the home building process."[:1500]
        item['SubImage'] = "|".join(response.xpath('//img/@src').getall())
        item['SubWebsite'] = response.url
        item['AmenityType'] = ""
        yield item

        floor_plans_page = response.xpath('//*[contains(text(),"Home Plan")]/@href').get()
        yield scrapy.FormRequest(url=floor_plans_page, method="GET", callback=self.parse2)

        # home_page = "https://www.brookstoneproperty.com/our-homes/available-homes/"
        #
        # yield scrapy.FormRequest(url=home_page, method="GET", callback=self.parse5)

    def parse2(self, response):

        links = response.xpath('//*[contains(text(),"View")]/../@href').getall()

        for link in links:
            yield scrapy.FormRequest(url=link, method="GET", callback=self.parse3)

    def parse3(self, response):

        try:
            plan_name = response.xpath('//h1/text()').get(default="")
        except Exception as e:
            print("Error in Plan name", e)

        try:
            plan_number = int(hashlib.md5(bytes(plan_name, 'utf-8')).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print("error in the plan number", e)

        try:
            basesqft = int(response.xpath('//*[contains(text(),"Square Feet")]/text()').get(default="0").split()[0])
        except Exception as e:
            print("Error in base sqft", e)

        try:
            bedrooms = response.xpath('//*[contains(text(),"Bedroom")]/text()').get(default="0").split()[0]
        except Exception as e:
            print("Error in bedrooms", e)

        try:
            fullbaths = response.xpath('//*[contains(text(),"Bathroom")]/text()').get(default="0").split()[0]
            if len(fullbaths) > 1:
                halfbath = 1
                fullbaths = fullbaths[0]
            else:
                halfbath = 0
                fullbaths = fullbaths[0]
        except Exception as e:
            print("Error in bath rooms", e)

        try:
            garage = response.xpath('//*[contains(text(),"Stall Garage")]/text()').get(default="0").split()[0]
        except Exception as e:
            print("Error in garage", e)
            garage = 0

        try:
            desc = "".join(response.xpath('//*[@class="fl-rich-text"]//text()').getall()).strip()
        except Exception as e:
            print("Error in Desc", e)

        try:
            images = "|".join(response.xpath('//*[@class="uabb-gallery-img"]/@src').getall())
        except Exception as e:
            print("Error in Images", e)

        unique = str(plan_number)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = plan_number
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = self.builderNumber
        item['PlanName'] = plan_name
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0
        item['BaseSqft'] = basesqft
        item['Baths'] = fullbaths
        item['HalfBaths'] = halfbath
        item['Bedrooms'] = bedrooms
        item['Garage'] = garage
        item['Description'] = desc
        item['ElevationImage'] = images
        item['PlanWebsite'] = response.url
        yield item

        home_available = response.xpath('//*[@itemid]/@itemid').getall()

        for home in home_available:
            # link = home.xpath('.//a/@href').get()
            yield scrapy.FormRequest(url=home, method="GET", callback=self.parse4, meta={"uniqui_number": unique_number, "PlanNumber": plan_number})

        home_page = "https://www.brookstoneproperty.com/our-homes/available-homes/"
        yield scrapy.FormRequest(url=home_page, method="GET", callback=self.parse5)



    def parse4(self, response):

        PlanNumber = response.meta['uniqui_number']

        try:
            SpecStreet1 = response.xpath('//*[contains(text(),"Address:")]//following::text()[1]').get(default="").strip()
            if not SpecStreet1:
                SpecStreet1 = response.xpath('//*[@class="fl-heading-text"]//text()').get(default="").strip()
        except Exception as e:
            print("Error in Spec Street", e)

        try:
            SpecCity = response.xpath('//*[contains(text(),"City:")]//following::text()[1]').get(default="").strip()
        except Exception as e:
            print("Error in Spec City",e)

        try:
            SpecState = response.xpath('//*[contains(text(),"State:")]//following::text()[1]').get(default="").strip()
        except Exception as e:
            print("Error in Spec City", e)

        try:
            SpecZIP = response.xpath('//*[contains(text(),"ZIP:")]//following::text()[1]').get(default="00000").strip()
        except Exception as e:
            print("Error in Zip Code", e)

        try:
            SpecPrice = response.xpath('//*[contains(text(),"Price:")]//following::text()[1]').get(default="0").strip().replace("$", "").replace(",", "")
        except Exception as e:
            print("Error in Spec Price", e)

        try:
            unique = SpecStreet1 + SpecCity + SpecState + SpecZIP + SpecPrice
            SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        SpecCountry = "USA"

        try:
            SpecSqft = int(response.xpath('//*[contains(text(),"Square Feet:")]/following::text()[1]').get(default="0").strip())
        except Exception as e:
            print("Error in SpecSqft", e)

        try:
            SpecBaths = response.xpath('//*[contains(text(),"Bathrooms:")]//following::text()[1]').get(default="0").strip()
            if len(SpecBaths) > 1:
                SpecHalfBaths = 1
                SpecBaths = SpecBaths[0]
            else:
                SpecHalfBaths = 0
                SpecBaths = SpecBaths[0]
        except Exception as e:
            print("Error in SpecBaths", e)

        try:
            SpecBedrooms = response.xpath('//*[contains(text(),"Bedrooms:")]/following::text()[1]').get(default="0").strip()
        except Exception as e:
            print("Error in Bed Room", e)

        try:
            SpecDescription = response.xpath('//*[@class="fl-module-content fl-node-content"]/p/text()').get(default="").strip()
        except Exception as e:
            print("Error in Description", e)

        try:
            SpecElevationImage = "|".join(response.xpath('//*[@itemprop="image"]/@src').getall())
        except Exception as e:
            print("Error in Images", e)

        try:
            SpecWebsite = response.url
        except Exception as e:
            print("Error in Website URl", e)

        item = BdxCrawlingItem_Spec()
        item['SpecNumber'] = SpecNumber
        item['PlanNumber'] = PlanNumber
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
        item['MasterBedLocation'] = 'Down'
        item['SpecGarage'] = 0
        item['SpecDescription'] = SpecDescription[0:1500]
        item['SpecElevationImage'] = SpecElevationImage
        item['SpecWebsite'] = SpecWebsite
        yield item

    def parse5(self, response):

        links = response.xpath('//*[@target="_self"]/@href').getall()
        for link in links:
            if "home" in link:
                yield scrapy.FormRequest(url=link, method="GET", callback=self.parse5half)

    def parse5half(self, response):
        links = response.xpath('//*[@target="_self"]/@href').getall()

        for link in links:
            yield scrapy.FormRequest(url=link, method="GET", callback=self.parse6)

    def parse6(self, response):
        home_available = response.xpath('//*[@itemprop="blogPost"]')
        for home in home_available:
            if home.xpath('.//*[@class="listing-text"]'):
                if home.xpath('.//*[@class="listing-text"]//text()').get().lower() == "sold":
                    pass
                else:
                    link = home.xpath('.//a[@class ="more-link view-listing"]/@href').get()
                    yield scrapy.FormRequest(url=link, method="GET", callback=self.homes)
            else:
                link = home.xpath('.//a/@href').get()
                yield scrapy.FormRequest(url=link, method="GET", callback=self.homes)

    def homes(self, response):

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
        item['Baths'] = 1
        item['HalfBaths'] = 0
        item['Bedrooms'] = 1
        item['Garage'] = 0
        item['Description'] = ""
        item['ElevationImage'] = ""
        item['PlanWebsite'] = ""
        yield item

        try:
            SpecStreet1 = response.xpath('//*[contains(text(),"Address:")]//following::text()[1]').get(default="").strip()
            if not SpecStreet1:
                SpecStreet1 = response.xpath('//*[@class="fl-heading-text"]//text()').get(default="").strip()
        except Exception as e:
            print("Error in Spec Street", e)

        try:
            SpecCity = response.xpath('//*[contains(text(),"City:")]//following::text()[1]').get(default="").strip()
        except Exception as e:
            print("Error in Spec City", e)

        try:
            SpecState = response.xpath('//*[contains(text(),"State:")]//following::text()[1]').get(default="").strip()
        except Exception as e:
            print("Error in Spec City", e)

        try:
            SpecZIP = response.xpath('//*[contains(text(),"ZIP:")]//following::text()[1]').get(default="00000").strip()
        except Exception as e:
            print("Error in Zip Code", e)

        try:
            SpecPrice = response.xpath('//*[contains(text(),"Price:")]//following::text()[1]').get(default="0").strip().replace("$", "").replace(",", "")
        except Exception as e:
            print("Error in Spec Price", e)

        try:
            unique = SpecStreet1 + SpecCity + SpecState + SpecZIP + SpecPrice
            SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        SpecCountry = "USA"

        try:
            SpecSqft = int(response.xpath('//*[contains(text(),"Square Feet:")]/following::text()[1]').get(default="0").strip())
        except Exception as e:
            print("Error in SpecSqft", e)

        try:
            SpecBaths = response.xpath('//*[contains(text(),"Bathrooms:")]//following::text()[1]').get(default="0").strip()
            if len(SpecBaths) > 1:
                SpecHalfBaths = 1
                SpecBaths = SpecBaths[0]
            else:
                SpecHalfBaths = 0
                SpecBaths = SpecBaths[0]
        except Exception as e:
            print("Error in SpecBaths", e)

        try:
            SpecBedrooms = response.xpath('//*[contains(text(),"Bedrooms:")]/following::text()[1]').get(default="0").strip()
        except Exception as e:
            print("Error in Bed Room", e)

        try:
            SpecDescription = response.xpath('//*[@class="fl-module-content fl-node-content"]/p/text()').get().strip()
        except Exception as e:
            try:
                SpecDescription = "".join(response.xpath('//*[@class="fl-module-content fl-node-content"]/text()').getall()).strip()
            except Exception as e:
                print("Error in Description", e)

        try:
            SpecElevationImage = "|".join(response.xpath('//*[@itemprop="image"]/@src').getall())
        except Exception as e:
            print("Error in Images", e)

        try:
            SpecWebsite = response.url
        except Exception as e:
            print("Error in Website URl", e)

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
        item['MasterBedLocation'] = 'Down'
        item['SpecGarage'] = 0
        item['SpecDescription'] = SpecDescription[0:1500]
        item['SpecElevationImage'] = SpecElevationImage
        item['SpecWebsite'] = SpecWebsite
        yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl {}".format(brookstonepropertySpider.name).split())
