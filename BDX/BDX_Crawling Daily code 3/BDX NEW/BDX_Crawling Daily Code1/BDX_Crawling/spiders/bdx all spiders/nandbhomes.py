# -*- coding: utf-8 -*-
import hashlib
import re

import requests
import scrapy
from lxml import html
from scrapy.utils.response import open_in_browser

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class nandbhomesSpider(scrapy.Spider):
    name = 'nandbhomes'
    allowed_domains = []
    # start_urls = ['https://www.nandbhomes.com/']

    builderNumber = "47119414900787008606791295359"

    def start_requests(self):
        url = "https://www.nandbhomes.com/"
        yield scrapy.FormRequest(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = self.builderNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = "14201 I-27"
        item['City'] = "Amarillo"
        item['State'] = "TX"
        item['ZIP'] = "79119"
        item['AreaCode'] = "806"
        item['Prefix'] = "681"
        item['Suffix'] = "8198"
        item['Extension'] = ""
        item['Email'] = "office@nandbhomes.com"
        item['SubDescription'] = "First-time homebuyers prefer our home building methodology because it’s not your typical cookie-cutter starter home. If you don’t like a standard feature that we offer, you can upgrade your floor plan as much as you want."
        item['SubImage'] = ""
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        # ------------------- If NO Plan Found found ---------------------- #

        # In case you have found the communities (subdivision) and Homes (Specs) but you are not able to find the plan details then,
        # please use this line of code, and reference this unique_number  in All Home(Specs)

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
        item['Baths'] = 0
        item['HalfBaths'] = 0
        item['Bedrooms'] = 0
        item['Garage'] = 0
        item['Description'] = ""
        item['ElevationImage'] = ""
        item['PlanWebsite'] = ""
        yield item


        # specs_links = response.xpath('//section[@class="nb-footer"]/div/div/div[3]/ul/li[2]/a/@href').extract_first()
        spec_link = 'https://www.nandbhomes.com/new-homes/'
        yield scrapy.Request(url=spec_link, callback=self.HomesDetails, meta={"PN": unique_number})

    def HomesDetails(self, response):

        # ------------------------------------------- Extract Homedetails ------------------------------ #
        divs = response.xpath('//table[@class="table table-striped row-numbered"]//tr')
        for div in divs:


            try:
                address = div.xpath('./td[2]/text()').extract()
                statecityzipcode = address[1].strip().split()


                SpecStreet1 = address[0].strip()
                SpecCity = statecityzipcode[0]
                SpecState = statecityzipcode[1]
                SpecZIP = statecityzipcode[2]

                unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()

            except Exception as e:
                print(e)

            try:
                PlanNumber = response.meta['PN']
            except Exception as e:
                print(e)

            try:
                SpecCountry = "USA"
            except Exception as e:
                print(e)

            try:
                SpecPrice = div.xpath('./td[6]/text()').extract_first().strip().replace(',','').replace('$','')

            except Exception as e:
                print(e)

            try:
                SpecSqftgarages = div.xpath('./td[5]/text()').extract()
                SpecSqft = SpecSqftgarages[1].replace("sq ft",'').strip().replace(',','').strip()
            except Exception as e:
                SpecSqft = 0

            try:
                SpecBathsbeds = div.xpath('./td[4]/text()').extract()
                SpecBaths = SpecBathsbeds[1].replace('Bathrooms','').strip()
                SpecHalfBaths = 0
            except Exception as e:
                SpecBaths = 0
                SpecHalfBaths = 0

            try:
                SpecBedrooms = SpecBathsbeds[0].replace('Bedrooms','').strip()
            except Exception as e:
                SpecBedrooms = 0

            try:
                MasterBedLocation = "Down"
            except Exception as e:
                print(e)

            try:
                SpecGarage = SpecSqftgarages[0].replace('Car Garage','').strip()
            except Exception as e:
                SpecGarage = 0

            try:
                tempdescurl = div.xpath('./td[3]/a/@href').extract_first()
                r = requests.get(tempdescurl)
                res = html.fromstring(r.text)
                SpecDescriptiontmp = ''.join(res.xpath('//p[@class="lead"]/text()'))
                SpecDescription = re.sub('\s+', ' ', re.sub('\r|\n|\t', ' ', SpecDescriptiontmp)).strip()
            except Exception as e:
                print(e)

            try:
                SpecElevationImage = ''
            except Exception as e:
                print(e)

            try:
                SpecWebsite = tempdescurl
            except Exception as e:
                print(e)


            # ----------------------- Don't change anything here ---------------- #

            if len(SpecZIP) != 4:
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
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = SpecGarage
                item['SpecDescription'] = SpecDescription
                item['SpecElevationImage'] = SpecElevationImage
                item['SpecWebsite'] = SpecWebsite
                yield item


        # --------------------------------------------------------------------- #

        # ------------------- If communities found ---------------------- #

        # ------------------- Creating Communities ---------------------- #

    # def parse1(self,response):
    #     divs = response.xpath('//section[@class="nb-footer"]/div/div/div[2]/ul/li[5]/a|//section[@class="nb-footer"]/div/div/div[2]/ul/li[8]/a')
    #     for div in divs:
    #         name = div.xpath('./text()').extract_first()
    #         link = div.xpath('./@href').extract_first()
    #         yield scrapy.Request(url=link,callback=self.home1details,meta={'name':name})
    #
    # def home1details(self,response):
    #
    #     subdivisonName = response.meta['name']
    #     subdivisonNumber = int(hashlib.md5(bytes(subdivisonName,"utf8")).hexdigest(), 16) % (10 ** 30)
    #
    #     f = open("html/%s.html" % subdivisonNumber, "wb")
    #     f.write(response.body)
    #     f.close()
    #     adresstmp = response.xpath('//p[@class="address"]/text()').extract_first().strip().split(",")
    #
    #     item2 = BdxCrawlingItem_subdivision()
    #     item2['sub_Status'] = "Active"
    #     item2['SubdivisionName'] = subdivisonName
    #     item2['SubdivisionNumber'] = subdivisonNumber
    #     item2['BuilderNumber'] = self.builderNumber
    #     item2['BuildOnYourLot'] = 0
    #     item2['OutOfCommunity'] = 1
    #     item2['Street1'] = adresstmp[0].strip()
    #     item2['City'] = adresstmp[1].strip()
    #     statezip = adresstmp[2].strip().split()
    #     item2['State'] = statezip[0].strip()
    #     item2['ZIP'] = statezip[1].strip()
    #     item2['AreaCode'] = "806"
    #     item2['Prefix'] = "681"
    #     item2['Suffix'] = "8198"
    #     item2['Extension'] = ""
    #     item2['Email'] = ''
    #     item2['SubDescription'] = response.xpath('//p[@class="lead"]/text()').extract_first(default="")
    #     item2['SubImage'] = "|".join(response.xpath('//div[@class="sidepix"]/img/@src').extract())
    #     item2['SubWebsite'] = response.url
    #     yield item2



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl nandbhomes".split())