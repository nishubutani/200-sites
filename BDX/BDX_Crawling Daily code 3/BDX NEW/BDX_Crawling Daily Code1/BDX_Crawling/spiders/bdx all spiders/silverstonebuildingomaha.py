# -*- coding: utf-8 -*-
import copy
import re
import os
import json
import hashlib
from pprint import pprint

import requests
import scrapy
from lxml import html

from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class BaumannbuildingSpider(scrapy.Spider):
    name = 'silverstonebuildingomaha'
    allowed_domains = ['silverstonebuildingomaha.com']
    start_urls = ['http://www.silverstonebuildingomaha.com/']

    builderNumber = '462773800289259035977981963001'

    #comm_dic = dict()

    def parse(self, response):

        try:
            # --------------------- TO the Communities page -------- #
            link = 'http://www.silverstonebuildingomaha.com/subdivisions/default.aspx'
            yield scrapy.Request(url=link, callback=self.communities_list,meta={'BN': self.builderNumber})
        except Exception as e:
            print(e)

    def communities_list(self, response):

        # -------------------- fetch all the Communities ----- #
        try:
            links = response.xpath('//*[@class="col-sm-6 col-md-4 subdivisions-clear"]/div/a/@href').getall()
            for lnk in links:
                link = 'http://www.silverstonebuildingomaha.com/subdivisions/'+lnk
                yield scrapy.Request(url=str(link), callback=self.process_communities, meta=response.meta)
        except Exception as e:
            print(e)

    def process_communities(self, response):

        # ---------------------------Extracting Communities Details ------------------------------------ #
        try:
            SubDescription = response.xpath('//span[@style="line-height:2;"]/../p/text()').get()
            if not SubDescription:
                SubDescription = ''
        except Exception as e:
            print(e)

        try:
            sub_Status = 'Active'
        except Exception as e:
            print(e)

        try:
            BuilderNumber = response.meta['BN']
        except Exception as e:
            print(e)

        try:
            SubdivisionName = response.xpath('//*[@id="dlistSubdivisions_ctl00_lblSubdivisionName"]/text()').get()
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = int(hashlib.md5(bytes(SubdivisionName, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        try:
            BuildOnYourLot = 1 if "build-on-your-lot" in str(response.url) else 0
        except Exception as e:
            print(e)

        try:
            OutOfCommunity = 1
        except Exception as e:
            print(e)

        try:
            address = response.xpath('//h4/text()').get()
            City = address.split(',')[1].strip()
            Street1 = address.split(',')[0].strip()
            statezip = address.split(',')[2].strip()
            State = statezip.split(' ')[0].strip()
            ZIP = statezip.split(' ')[1].strip()
        except Exception as e:
            print(e)

        try:
            Email = 'Silverstone@PinPointHomeSales.com'
        except Exception as e:
            print(e)

        try:
            phone = response.xpath('//strong[contains(text(),"Agent:")]/../following-sibling::td/text()').extract()[1]
            AreaCode = phone.split('-')[0].strip()
            Prefix = phone.split('-')[1].strip()
            Suffix = phone.split('-')[2].strip()
            Extension = ""
        except Exception as e:
            AreaCode = Prefix = Suffix = Extension = ""

        try:
            SubImage = 'http://www.silverstonebuildingomaha.com' + str(response.xpath('//*[@rel="fancybox"]/img/@src').get())
        except Exception as e:
            print(e)

        try:
            SubWebsite = response.url
        except Exception as e:
            print(e)

        f = open("html/%s.html" % SubdivisionNumber, "wb")
        f.write(response.body)
        f.close()

        # ----------------------- Don't change anything here --------------
        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = sub_Status
        item2['SubdivisionNumber'] = SubdivisionNumber
        item2['BuilderNumber'] = BuilderNumber
        item2['SubdivisionName'] = SubdivisionName
        item2['BuildOnYourLot'] = BuildOnYourLot
        item2['OutOfCommunity'] = OutOfCommunity
        item2['Street1'] = Street1
        item2['City'] = City
        item2['State'] = State
        item2['ZIP'] = ZIP
        item2['AreaCode'] = AreaCode
        item2['Prefix'] = Prefix
        item2['Suffix'] = Suffix
        item2['Extension'] = Extension
        item2['Email'] = Email
        item2['SubDescription'] = SubDescription[0:2000]
        item2['SubImage'] = SubImage
        item2['SubWebsite'] = SubWebsite
        item2['AmenityType'] = ''

        yield item2

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = 'No Sub Division'
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '7416 N 171st Street'
        item['City'] = 'Bennington'
        item['State'] = 'NE'
        item['ZIP'] = '68007'
        item['AreaCode'] = '402'
        item['Prefix'] = "965"
        item['Suffix'] = "1848"
        item['Extension'] = ""
        item['Email'] = "Silverstone@PinPointHomeSales.com"
        r = requests.get('http://www.silverstonebuildingomaha.com/default.aspx')
        response_desc = html.fromstring(r.text)
        item['SubDescription'] =''.join(response_desc.xpath('//*[@id="ctl00"]/section[7]/div/div[2]/p/text()'))
        immag = []
        images = response_desc.xpath('//*[@class="carousel-inner"]/div/div/@style')
        for img in images:
            image = img.replace('background-image: url(','').replace(');','').strip()
            image = 'http://www.silverstonebuildingomaha.com/'+image
            immag.append(image)
        item['SubImage'] = '|'.join(immag)
        item['SubWebsite'] = ''
        item['AmenityType'] = ''
        yield item

        # process plans:
        #----------------
        r = requests.get('http://www.silverstonebuildingomaha.com/floorplans/default.aspx')
        response_pln = html.fromstring(r.text)
        plan_url = response_pln.xpath('//*[@class="thumbnail"]/@href')
        for pu in plan_url:
            purl = 'http://www.silverstonebuildingomaha.com/floorplans/' + pu
            yield scrapy.Request(url=str(purl), callback=self.plans_details, meta={'sbdn': self.builderNumber})

    def plans_details(self, response):

        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//h2/text()').get()
        except Exception as e:
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = response.meta['sbdn']
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
            BaseSqft = re.findall(r'Starting at (.*?) ft',response.text)[0]
        except Exception as e:
            print(e)

        try:
            bath = response.xpath('//strong[contains(text(),"Bathrooms:")]/../following-sibling::td/text()').get()
            tmp = re.findall(r"(\d+)", bath)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            HalfBaths = 0

        try:
            Bedrooms = response.xpath('//strong[contains(text(),"Bedrooms:")]/../following-sibling::td/text()').get()
        except Exception as e:
            print(e)

        try:
            Garage = response.xpath('//strong[contains(text(),"Garages:")]/../following-sibling::td/text()').get()
        except Exception as e:
            print(e)

        BasePrice = 0.00

        try:
            Description = response.xpath('//*[@style="line-height:2;"]/../p/text()').get()
            if 'AVAILABLE' in Description:
                Description = ''
        except Exception as e:
            Description = ''

        try:
            immag = []
            images = response.xpath('//div[@class="col-sm-6"][2]//a/@href').getall()
            for img in images:
                image = 'http://www.silverstonebuildingomaha.com' + img
                immag.append(image)
            ElevationImage = '|'.join(immag)
        except Exception as e:
            print(e)

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

        try:

            unique = str(PlanName) + str(SubdivisionNumber)  # < -------- Changes here
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
        except Exception as e:
            print(e)

        home_url = response.xpath('//*[contains(text(),"Available Homes With This Floor Plan")]/@href').get().replace('../','')

        if 'PLAN=217' in home_url:
            hurl = 'http://www.silverstonebuildingomaha.com/' + home_url
            yield scrapy.FormRequest(url=str(hurl), callback=self.HomesDetails, meta={'PN': item['unique_number']})

    def HomesDetails(self, response):

        links = response.xpath('//h3/a/@href').extract()

        if 'PLAN=217' in response.url:
            del links[1:4]

        for lk in links:
            homelink = 'http://www.silverstonebuildingomaha.com/homesforsale/' + lk
            r = requests.get(homelink)
            response_home = html.fromstring(r.text)

            try:
                PlanNumber = response.meta['PN']
            except Exception as e:
                print(e)

            try:
                SpecDescription = response_home.xpath('//*[@style="line-height:2;"]/../p/text()')[0]
            except Exception as e:
                print(e)

            try:
                SpecStreet1 = response_home.xpath('//h2/text()')[0]
            except Exception as e:
                print(e)

            try:
                citystate = response_home.xpath('//h4/text()')[0]
                SpecCity = citystate.split(',')[0].strip()
            except Exception as e:
                print(e)

            try:
                state = citystate.split(',')[1].strip()
                SpecState = state.split(' ')[0].strip()
            except Exception as e:
                print(e)

            try:
                SpecZIP = state.split(' ')[1].strip()
            except Exception as e:
                print(e)

            try:
                unique = SpecStreet1+SpecCity+SpecState+SpecZIP
                SpecNumber = int(hashlib.md5(bytes(unique,"utf8")).hexdigest(), 16) % (10 ** 30)
            except Exception as e:
                print(e)

            try:
                SpecCountry = "USA"
            except Exception as e:
                print(e)

            try:
                price = response_home.xpath('//h4/text()')[1]
                SpecPrice = price.replace('$','').replace(',','').replace('.00','').strip()
            except Exception as e:
                print(e)

            try:
                sqft = response_home.xpath('//h4/text()')[2]
                SpecSqft = sqft.replace('ft','').strip()
            except Exception as e:
                print(e)

            try:
                bath = response_home.xpath('//strong[contains(text(),"Bathrooms:")]/../following-sibling::td/text()')[0]
                tmp = re.findall(r"(\d+)", bath)
                SpecBaths = tmp[0]
                if len(tmp) > 1:
                    SpecHalfBaths = 1
                else:
                    SpecHalfBaths = 0

            except Exception as e:
                SpecBaths = 0
                SpecHalfBaths = 0

            try:
                SpecBedrooms = response_home.xpath('//strong[contains(text(),"Bedrooms:")]/../following-sibling::td/text()')[0]
            except Exception as e:
                print(e)

            try:
                MasterBedLocation = 'Down'
            except Exception as e:
                print(e)

            try:
                SpecGarage = response_home.xpath('//strong[contains(text(),"Garages:")]/../following-sibling::td/text()')[0]
            except Exception as e:
                print(e)

            try:
                immag = []
                images = response_home.xpath('//div[@class="col-sm-6"][2]//a/@href')
                for img in images:
                    image = 'http://www.silverstonebuildingomaha.com' + img
                    immag.append(image)
                SpecElevationImage = '|'.join(immag)
            except Exception as e:
                print(e)

            try:
                SpecWebsite = homelink
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
# execute("scrapy crawl silverstonebuildingomaha".split())