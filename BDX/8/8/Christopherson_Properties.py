
# -*- coding: utf-8 -*-
import hashlib
import re

import requests
import scrapy
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class ChristophersonPropertiesSpider(scrapy.Spider):
    name = 'christopherson_properties'
    allowed_domains = ['christophersonhomes.com']
    start_urls = ['https://christophersonproperties.net/']

    builderNumber = "11947"


    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #
        image = '|'.join(response.xpath('//*[contains(@style,"background:")]/@style').extract())
        image = '|'.join(re.findall(r'\((.*?)\)',image))
        images = image.strip('|')
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = "565 W College Ave"
        item['City'] = "Santa Rosa"
        item['State'] = "CA"
        item['ZIP'] = "95401"
        item['AreaCode'] = "707"
        item['Prefix'] = "584"
        item['Suffix'] = "6377"
        item['Extension'] = ""
        item['Email'] = ""
        item['SubDescription'] = "Deeply embedded in the Sonoma County real estate and construction community for over 40 years, the Christopherson family knows how to make things happen. Whether it is buying your next home or selling the one you live in now, we know this market.Each Sonoma County real estate team member brings years of expertise to the various aspects of the business. Combined with unsurpassed personal attention, we’ll be offering a Real Estate experience like no other.Our six local real estate agents and brokers are dedicated to help our clients in various ways if you decide not to rebuild. We can find you a replacement home or sell your lot, or find another lot where Christopherson Builders can construct your dream home."
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        yield item
        try:
            link = response.xpath('//*[contains(text(),"Properties")]/@href').extract_first()
            plandetains = {}
            yield scrapy.Request(url=link,callback=self.plans_details,meta={'sbdn':self.builderNumber,'PlanDetails':plandetains},dont_filter=True)
        except Exception as e:
            print(e)

    def plans_details(self,response):
        plandetails = response.meta['PlanDetails']
        unique = str("Plan Unknown") + str(self.builderNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['unique_number'] = unique_number
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = "Plan Unknown"
        item['SubdivisionNumber'] = self.builderNumber
        item['PlanName'] = "Plan Unknown"
        item['PlanNotAvailable'] = 1
        item['PlanTypeName'] = 'Single Family'
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
        try:
            home_links = response.xpath('//*[@class="availability available"]/../../@href').extract()
            for home_link in home_links:
                yield scrapy.Request(url=home_link,callback=self.HomesDetails,meta={'unique_number':unique_number,'PN':plandetails},dont_filter=True)
        except Exception as e:
            print(e)
        try:
            New_Homes = response.xpath('//*[contains(text(),"New Homes")]/@href').extract_first()
            res_home = requests.get(url=New_Homes)
            response_home = HtmlResponse(url=res_home.url, body=res_home.content)
            new_home_links = response_home.xpath('//*[@class="availability available"]/../../@href').extract()
            for new_home_link in new_home_links:
                yield scrapy.Request(url=new_home_link,callback=self.HomesDetails,meta={'unique_number':unique_number,'PN':plandetails},dont_filter=True)
        except Exception as e:
            print(e)

    def HomesDetails(self, response):
        PN = response.meta['PN']
        unique_number = response.meta['unique_number']
        PlanNumber = unique_number
        SpecStreet1 = response.xpath('//h1/text()[1]').extract_first().strip()
        address = response.xpath('//h1/text()[2]').extract_first().strip()
        try:
            SpecCity = address.split(',')[0].strip()
        except Exception as e:
            print(e)
        try:
            SpecState = address.split(',')[1].split()[0].strip()
            if SpecState == "California":
                SpecState = "CA"
            else:
                print("other state")
        except Exception as e:
            print(e)
        try:
            SpecZIP = address.split(',')[1].split()[1].strip()
        except Exception as e:
            SpecZIP = '00000'
            print(e)

        try:
            unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
            SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % SpecNumber, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
            print(e)

        try:
            SpecCountry = "USA"
        except Exception as e:
            print(e)

        try:
            SpecPrice = response.xpath('//*[@class="price"]//text()').extract_first().replace('$','').replace(',','')
        except Exception as e:
            print(e)

        try:
            SpecSqft = str(response.xpath('//*[contains(text(),"sq ft")]/text()').extract_first(default='0').strip()).replace(",", "")
            SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
        except Exception as e:
            SpecSqft = '0'
            print(e)

        try:
            SpecBaths = str(response.xpath('//*[contains(text(),"Bathrooms")]/..//span/text()').extract_first(default='0').strip()).replace(",", "")
            tmp = re.findall(r"(\d+)", SpecBaths)
            SpecBaths = tmp[0]
            if len(tmp) > 1:
                SpecHalfBaths = 1
            else:
                SpecHalfBaths = 0
        except Exception as e:
            print(e)

        try:
            SpecBedrooms = str(response.xpath('//*[contains(text(),"Bedrooms")]/..//span/text()').extract_first(default='0').strip()).replace(",", "")
            SpecBedrooms = re.findall(r'(\d+)', SpecBedrooms)[0]
        except Exception as e:
            print(e)

        try:
            MasterBedLocation = "Down"
        except Exception as e:
            print(e)

        try:
            SpecGarage = response.xpath('//*[contains(text(),"Garage")]/..//span/text()').extract_first(default='0')
            SpecGarage = re.findall(r"(\d+)", SpecGarage)[0]
        except Exception as e:
            SpecGarage = '0'
            print(e)

        try:
            if response.xpath('//*[contains(text(),"Description")]/../p/text()'):
                SpecDescription = response.xpath('//*[contains(text(),"Description")]/../p/text()').extract_first(default='').strip()
            elif response.xpath('//*[contains(text(),"Property Features")]/../ul/li/text()'):
                SpecDescription = ''.join(response.xpath('//*[contains(text(),"Property Features")]/../ul/li/text()').extract()).strip()
            else:
                SpecDescription = "These brand new Christopherson designed and built homes are currently in different stages of construction and will be coming on the market soon. Each home is value-engineered and newly designed. Contact our agents to view the homes and floor plans."
        except Exception as e:
            print(e)

        try:
            ElevationImage = '|'.join(response.xpath('//*[@class="planGalleryItem"]/a/@href').extract())
            SpecElevationImage = ElevationImage.strip('|')
        except Exception as e:
            print(e)

        try:
            SpecWebsite = response.url
        except Exception as e:
            print(e)

            # ----------------------- Don't change anything here ---------------- #
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


from scrapy.cmdline import execute
# execute("scrapy crawl christopherson_properties".split())