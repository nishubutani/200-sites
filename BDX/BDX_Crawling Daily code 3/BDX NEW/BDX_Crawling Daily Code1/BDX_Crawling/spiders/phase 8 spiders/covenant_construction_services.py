# -*- coding: utf-8 -*-
import hashlib
import re
import requests
import scrapy
from decimal import Decimal
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class CovenantConstructionServicesSpider(scrapy.Spider):
    name = 'Covenant_Construction_Services'
    allowed_domains = ['https://www.ccs-homes.com/']
    start_urls = ['https://www.ccs-homes.com/']

    builderNumber = "49165"


    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #
        image1 = '|'.join(response.urljoin("https:" + i) for i in
                                  response.xpath('//*[@data-title="Slide"]/@data-thumb').extract())
        image2 = '|'.join(response.xpath('//*[@class="epl-blog-image"]/img/@src').extract())
        image3 = '|'.join(response.xpath('//*[@class="fusion-carousel-item"]//img/@src').extract())
        images = f"{image1}|{image2}|{image3}"
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = "2635 Berkshire Parkway, Suite 202"
        item['City'] = "Clive"
        item['State'] = "IA"
        item['ZIP'] = "50325"
        item['AreaCode'] = "515"
        item['Prefix'] = "216"
        item['Suffix'] = "1017"
        item['Extension'] = ""
        item['Email'] = "alans@ccsvet.com"
        item['SubDescription'] = response.xpath('//*[contains(text(),"WHO WE ARE")]/../p/text()').extract_first().strip()
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        yield item

        try:
            link = response.xpath('//*[contains(text(),"Floor Plans")]/../@href').extract_first()
            PlanDetails = {}
            yield scrapy.Request(url=link,callback=self.parse_plan,meta={'sbdn':self.builderNumber,'PlanDetails':PlanDetails},dont_filter=True)
        except Exception as e:
            print(e)

    def parse_plan(self,response):
        PN = response.meta['PlanDetails']
        sbdn = response.meta['sbdn']
        links = response.xpath('//*[@class="heading-link"]/@href').extract()
        for link in links:
            link = "https://www.ccs-homes.com/floor-plans" + link
            yield scrapy.Request(url=str(link), callback=self.plans_details, dont_filter=True, meta={"PN": PN,"sbdn": sbdn})

    def plans_details(self, response):
        try:
            plandetails = response.meta['PN']
            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                PlanName = response.xpath('//h1/text()').extract_first(default='').strip()
            except Exception as e:
                print(e)

            try:
                PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
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
                Baths = '0'
                tmp = re.findall(r"(\d+)", Baths)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                print(e)

            try:
                Bedrooms = '0'
            except Exception as e:
                print(e)

            try:
                Garage = '0'
                BaseSqft = str(response.xpath('//*[contains(text(),"Base SqFt:")]/text()').extract_first(default='0').strip()).replace(",", "")
                BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
            except Exception as e:
                print(e)

            try:
                Description = "As a flexible builder, CCS Homes will accommodate your home plan or help you develop and design a plan that meets your goals. We have knowledgeable people positioned and excited to take you through your custom design and selection process. Creating a personalized new home from your vision is our passion."
            except Exception as e:
                print(e)

            try:
                ElevationImage = '|'.join(response.xpath('//*[@class="fusion-carousel-item"]//img/@src').extract())
                ElevationImage = ElevationImage.strip('|')
            except Exception as e:
                print(e)

            try:
                PlanWebsite = response.url
            except Exception as e:
                print(e)

            # SubdivisionNumber = SubdivisionNumber  # if subdivision is there
            SubdivisionNumber = self.builderNumber #if subdivision is not available
            unique = str(PlanNumber) + str(SubdivisionNumber)
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            plandetails[PlanName] = unique_number
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
            item['Baths'] = Baths
            item['HalfBaths'] = HalfBaths
            item['Bedrooms'] = Bedrooms
            item['Garage'] = Garage
            item['Description'] = Description
            item['ElevationImage'] = ElevationImage
            item['PlanWebsite'] = PlanWebsite
            yield item
        except Exception as e:
            print(e)

        try:
            home_links = response.xpath('//*[contains(text(),"Homes For Sale")]/../@href').extract()
            for home_link in home_links:
                yield scrapy.Request(url=str(home_link), callback=self.home_list, dont_filter=True,meta={"PN": plandetails, "sbdn": response.meta['sbdn'],'unique_number':unique_number})
        except Exception as e:
            print(e)

        try:
            sale_home = self.start_urls[0] + response.xpath('//*[contains(text(),"For Sale")]/../@href').extract_first()
            res_h = requests.get(url=sale_home)
            response_h = HtmlResponse(url=res_h.url, body=res_h.content)
            link_selectors = response_h.xpath('//div[contains(@id,"post-")]//h3/a')
            for link_selector in link_selectors:
                link = link_selector.xpath('./@href').extract_first()
                name = link_selector.xpath('./text()').extract_first()
                if not 'SOLD' in name:
                    yield scrapy.Request(url=str(link), callback=self.home_list, dont_filter=True,
                                         meta={"PN": plandetails, "sbdn": response.meta['sbdn'],
                                               'unique_number': unique_number})
                else:
                    print("SOLD HOUSE")
        except Exception as e:
            print(e)

    def home_list(self,response):
        if not response.xpath('//h3[contains(text(),"Nothing found, please check back later.")]'):
            PlanNumber = ''
            unique_number = response.meta['unique_number']
            PN = response.meta['PN']
            SpecStreet1 = response.xpath('//*[@class="item-street"]/text()').extract_first()
            if ',' in SpecStreet1:
                SpecStreet1 = SpecStreet1.replace(',','')
            SpecCity = response.xpath('//*[@class="item-suburb"]/text()').extract_first().strip()
            SpecState = response.xpath('//*[@class="item-state"]/text()').extract_first().strip()
            SpecZIP = response.xpath('//*[@class="item-pcode"]/text()').extract_first().strip()

            unique = SpecStreet1 + SpecCity + SpecState + SpecZIP + str(response.url)
            SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            Plan_Name1 = response.xpath('//*[contains(text(),"Floor Plan ")]/@onclick').extract_first()
            for name,value in PN.items():
                name_list = name.split()
                for n in name_list:
                    if n in Plan_Name1:
                        Plan_Name = name
                        PlanNumber = PN[Plan_Name]
                        break
            if PlanNumber == '':
                PlanNumber = unique_number
            try:
                SpecCountry = "USA"
            except Exception as e:
                print(e)

            try:
                SpecPrice1 = response.xpath('//*[@class="page-price"]/text()').extract_first(default='0').strip().replace(',','')
                SpecPrice = re.findall(r"(\d+)", SpecPrice1)[0]
            except Exception as e:
                print(e)

            try:
                SpecSqft = response.xpath('//*[@class="land-size"]/text()').extract_first(default='0').strip().replace(',','')
                SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
            except Exception as e:
                print(e)

            try:
                SpecBaths = response.xpath('//*[@class="bathrooms"]/text()').extract_first(default='0').strip().replace(',','')
                tmp = re.findall(r"(\d+)", SpecBaths)
                SpecBaths = tmp[0]
                if len(tmp) > 1:
                    SpecHalfBaths = 1
                else:
                    SpecHalfBaths = 0
            except Exception as e:
                print(e)

            try:
                SpecBedrooms = response.xpath('//*[@class="bedrooms"]/text()').extract_first(default='0').strip().replace(',','')
                SpecBedrooms = re.findall(r"(\d+)", SpecBedrooms)[0]
            except Exception as e:
                print(e)

            try:
                SpecGarage = response.xpath('//*[@class="garage"]/text()').extract_first(default='0').strip().replace(',','')
                SpecGarage = re.findall(r"(\d+)", SpecGarage)[0]
            except Exception as e:
                print(e)

            try:
                MasterBedLocation = "Down"
            except Exception as e:
                print(e)

            try:
                SpecDescription = ''
            except Exception as e:
                print(e)

            try:
                ElevationImage = response.xpath('//*[@class="fusion-carousel-item"]//img/@src').extract()
                SpecElevationImage = '|'.join(ElevationImage)
            except Exception as e:
                print(e)

            try:
                SpecWebsite = response.url
            except Exception as e:
                print(e)

            try:
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
            except Exception as e:
                print(e)



from scrapy.cmdline import execute
# execute("scrapy crawl Covenant_Construction_Services".split())