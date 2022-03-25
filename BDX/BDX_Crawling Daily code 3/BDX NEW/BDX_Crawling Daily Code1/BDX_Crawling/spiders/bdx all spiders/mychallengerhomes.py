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
from scrapy.http import HtmlResponse
from w3lib.html import remove_tags
from w3lib.http import basic_auth_header

from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class MyChallengerHomesSpider(scrapy.Spider):
    name = 'mychallengerhomes'
    allowed_domains = []
    start_urls = []

    builderNumber = '895235487532251015528466758228'

    def start_requests(self):
        links = ['https://challengerhomes.com/locations/colorado/northern-colorado/','https://challengerhomes.com/locations/colorado/colorado-springs/']
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # -------------------- fetch all the Communities ----- #
        try:
            link = response.xpath('//*[@data-list="communities"]//a[@class="CommunitiesMapList__list-link"]/@href').extract()
            for li in link:
                yield scrapy.Request(url=li, callback=self.communities, meta={'BN': self.builderNumber})
                # yield scrapy.Request(url="https://challengerhomes.com/communities/colorado/colorado-springs/the-townes-at-woodmen-heights/", callback=self.communities, meta={'BN': self.builderNumber})
        except Exception as e:
            print(e)

    def communities(self, response):

        sold_out = ''.join(response.xpath('//*[@class="CommunityHeader__status"]/span/text()').extract()).strip()

        if 'SOLD OUT' not in sold_out:

            f = open("html/%s.html" % self.builderNumber, "wb")
            f.write(response.body)
            f.close()



            url = response.url
            try:
                SubDescription = ''.join(response.xpath('//*[@class="CommunityHeader__status"]/span/text()').extract()).strip()
                if not SubDescription:
                    SubDescription = ''
            except Exception as e:
                SubDescription = ''
                print(e)

            try:
                if 'Coming Soon' in SubDescription:
                    sub_Status = 'ComingSoon'
                else:
                    sub_Status = 'Active'
            except Exception as e:
                sub_Status = ''
                print(e)

            try:
                sname = response.xpath('//*[@class="heading heading--h1"]/text()').extract_first()
                SubdivisionName = sname
            except Exception as e:
                SubdivisionName = ''
                print(e)

            try:
                SubdivisionNumber = int(hashlib.md5(bytes(SubdivisionName+url, "utf8")).hexdigest(), 16) % (10 ** 30)
            except Exception as e:
                SubdivisionNumber= ''
                print(e)

            try:
                # addinfo = ''.join(response.xpath('//*[contains(text(),"Single Family Home")]//following-sibling::text()').extract()).strip()
                addinfo = response.xpath('//*[@class="CommunityHeader__subtitle"]/a//text()').extract()[1].replace('  ',' ')
                address = addinfo.split(',')[0].strip()
                city = addinfo.split(',')[1].strip()
                state = addinfo.split(',')[-1].strip().split(' ')[0]
                zip = addinfo.split(',')[-1].strip().split(' ')[1]
            except Exception as e:
                address = city = state = zip = ''
                print(e)

            try:
                Email = response.xpath('//*[@class="CommunityContact__sales-rep__email CommunityContact__sales-rep__email--top"]/text()').extract_first().strip()
            except Exception as e:
                Email = ''
                print(e)

            try:
                phone = response.xpath('//*[contains(text(),"Call ")]/text()[1]').extract()[0].replace('Call','').replace('(','').replace(')','').replace('-',' ').strip()
                AreaCode = phone.split(' ')[0]
                Prefix = phone.split(' ')[1]
                Suffix = phone.split(' ')[-1]
                Extension = ""
            except Exception as e:
                AreaCode = Prefix = Suffix = Extension = ""
                print(e)

            try:
                image = response.xpath('//*[@class="CommunityHero CommunityPage"]//div[@class="CommunityHero__image image-fit js-community-hero-image is-active"]/img/@data-src').extract()
                SubImage = '|'.join(image)
            except Exception as e:
                SubImage = ""
                print(e)

            try:
                SubWebsite = response.url
            except Exception as e:
                SubWebsite = ''
                print(e)

            a = []
            # aminity = ''.join(response.xpath('//*[@class="ll-features-content__half right col-md-1of2"]/ul[1]/li/text()').extract())
            try:
                aminity = ''.join(response.xpath('//*[@class="_grid  _grid--align-stretch"]//div[@class="Content _grid__col _grid__col--medium-11"]//text()').extract())
            except Exception as e:
                aminity = ''
                print(e)

            amenity_list = ["Pool", "Playground", "GolfCourse", "Tennis", "Soccer", "Volleyball", "Basketball",
                            "Baseball", "Views", "Lake", "Pond", "Marina", "Beach", "WaterfrontLots", "Park",
                            "Trails", "Greenbelt", "Clubhouse", "CommunityCenter"]
            for i in amenity_list:
                if i in aminity:
                    a.append(i)
            aminity_new = '|'.join(a)

            # ----------------------- Don't change anything here --------------
            item2 = BdxCrawlingItem_subdivision()
            item2['sub_Status'] = sub_Status
            item2['SubdivisionNumber'] = SubdivisionNumber
            item2['BuilderNumber'] = self.builderNumber
            item2['SubdivisionName'] = SubdivisionName
            item2['BuildOnYourLot'] = 0
            item2['OutOfCommunity'] = 1
            item2['Street1'] = address
            item2['City'] = city
            item2['State'] = state
            item2['ZIP'] = zip
            item2['AreaCode'] = AreaCode
            item2['Prefix'] = Prefix
            item2['Suffix'] = Suffix
            item2['Extension'] = Extension
            item2['Email'] = Email
            item2['SubDescription'] = SubDescription
            item2['SubImage'] = SubImage
            item2['SubWebsite'] = SubWebsite
            item2['AmenityType'] = aminity_new
            yield item2

            # process plans:
            # ----------------
            plan_url = response.xpath('//*[@class="CommunityFloorplansHomes__list _grid _grid--pad-large js-sort-floorplans-list"]//a[@class="preview__link"]/@href').extract()
            # plan_url = response.xpath('//div[@class="CommunitiesArchive__section js-communities-archives-section is-active"]//div[@class="CommunitiesMapList__list-items"]//a/@href').extract()
            for pu in plan_url:
                yield scrapy.Request(url=pu, callback=self.plan_details, meta={'SubdivisionNumber': item2['SubdivisionNumber']})

    def plan_details(self, response):

        a = response.meta['SubdivisionNumber']
        try:
            Type = 'SingleFamily'
        except Exception as e:
            Type = ''
            print(e)

        try:
            PlanName = response.xpath('//h1[@class="heading heading--h1"]/text()').extract_first().strip()
        except Exception as e:
            PlanName = ''
            print(e)

        try:
            PlanNotAvailable = 0
        except Exception as e:
            PlanNotAvailable = ''
            print(e)

        try:
            PlanTypeName = 'Single Family'
        except Exception as e:
            PlanTypeName = ''
            print(e)

        try:
            BasePrice = response.xpath('//*[@class="CommunityHeader__main _grid__col _grid__col--medium-10"]//span/strong/text()').extract_first().replace('$','').replace(',','').strip()
            BasePrice = BasePrice
        except Exception as e:
            BasePrice = 0

        try:
            BaseSqft = ''.join(response.xpath('//*[@class="specs__spec specs__spec--sqft"]//div//text()').extract()).split('-')[0]
            BaseSqft = ''.join(re.findall(r'\d', BaseSqft))
        except Exception as e:
            BaseSqft = 0

        try:
            Baths = response.xpath('//*[@class="specs__spec specs__spec--bath"]//div//text()').extract()[-1]
            if '-' in Baths:
                Baths = Baths.split('-')[-1].replace('Baths ','').strip()
            # Baths = ''.join(re.findall(r'\d', Baths))
            tmp = re.findall(r"(\d+)", Baths)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            Baths = 0
            HalfBaths = 0
            print(e)

        try:
            Bedrooms = ''.join(response.xpath('//*[@class="specs__spec specs__spec--bed"]//div//text()').extract())
            if '-' in Bedrooms:
                Bedrooms = Bedrooms.split('-')[-1].replace('Beds ','').strip()
            Bedrooms = ''.join(re.findall(r'\d', Bedrooms))
        except Exception as e:
            Bedrooms = 0

        try:
            Garage = ''.join(response.xpath('//*[@class="specs__spec specs__spec--car"]//div//text()').extract())
            if '-' in Garage:
                Garage = Garage.split('-')[-1].replace('Garage ','').strip()
            Garage = ''.join(re.findall(r'\d', Garage))

        except Exception as e:
            Garage = ''
            print(e)

        try:
            Description = ''.join(response.xpath('//*[@class="Content _grid__col _grid__col--medium-11"]//p/text()').extract())[0:1999]
        except Exception as e:
            Description = ''
            print(str(e))

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            PlanNumber = ''
            print(e)

        try:
            ima1 = '|'.join(response.xpath('//*[@class="CommunityHero PlanPage"]//div[@class="CommunityHero__image image-fit js-community-hero-image is-active"]/img/@data-src').extract())
            ima2 = '|'.join(response.xpath('//*[@class="_grid _grid--align-center _grid--pad-large"]//img[@class="lazy loaded"]/@data-src').extract())
            ima3 = '|'.join(response.xpath('//*[@class="Gallery js-gallery module pad-v-lg"]//img/@data-src').extract())
            if ima2 == '':
                ima2 = ''.join(response.xpath('//*[@id="secondfloor"]/img/@src').extract())
            ElevationImage = ima1 + '|' + ima2 + '|' + ima3.strip('|')
        except Exception as e:
            ElevationImage = ''
            print(e)

        try:
            PlanWebsite = response.url
        except Exception as e:
            PlanWebsite = ''
            print(e)
        try:
            plans_uni = int(hashlib.md5(bytes(response.url + a, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        except Exception as e:
            print(e)

        # ----------------------- Don't change anything here --------------
        unique = str(PlanNumber) + str(a)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
                10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['Type'] = Type
        item['PlanNumber'] = plans_uni
        # item['unique_number'] = unique_number  # < -------- Changes here
        item['unique_number'] = PlanNumber  # < -------- Changes here
        item['SubdivisionNumber'] = a
        # item['SubdivisionNumber'] = self.builderNumber
        item['PlanName'] = PlanName
        item['PlanNotAvailable'] = PlanNotAvailable
        item['PlanTypeName'] = PlanTypeName
        item['BasePrice'] = BasePrice
        item['BaseSqft'] = BaseSqft
        item['Baths'] = int(Baths)
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = int(Bedrooms)
        item['Garage'] = Garage
        item['Description'] = Description.replace('   ', ' ').replace('\xa0', '')
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item

        spec_lnk = "https://challengerhomes.com/communities/colorado/northern-colorado/sorrento/"
        spec_res = requests.request("GET", spec_lnk)
        res2 = HtmlResponse(url=spec_lnk, body=spec_res.content)
        spec_link=res2.xpath('//div[@class="CommunityFloorplansHomes__list _grid _grid--pad-large js-sort-homes-list"]//a/@href').getall()
        for splink in spec_link:
            spec_finallnk=splink
            yield scrapy.Request(url=spec_finallnk,callback=self.spec_details,dont_filter=True)

    def spec_details(self,response):
        try:
            num1 ="".join(response.xpath('//div[@class="CommunityHeader__plan"]/a/text()').getall()).strip()
        except:
            num1 = "Plan Unknown"
        # pln111 = "".join(num1).strip().lower()
        plan_number11 = int(hashlib.md5(bytes(num1, "utf8")).hexdigest(), 16) % (10 ** 30)

        try:
            city_st_z="".join(response.xpath('//div[@class="CommunityHeader__main _grid__col _grid__col--medium-11"]//div[@class="CommunityHeader__subtitle"]/text()').getall()).split(" ")
            print(city_st_z)
        except Exception as e:
            print(e)
            city_st_z=""

        try:
            city=city_st_z[0].replace(",","")
            print(city)
        except Exception as e:
            print(e)
            city=""

        try:
            state=city_st_z[1]
            print(state)
        except Exception as e:
            print(e)
            state="0"

        try:
            zipcode=city_st_z[2]
            print(zipcode)
        except Exception as e:
            print(e)
            zipcode=""
        imglst=[]
        try:
            # img="|".join(response.xpath('//div[@class="CommunityHero PlanPage"]//div[@class="CommunityHero__image image-fit js-community-hero-image is-active"]//img//@src').getall())
            # img=response.xpath('//div[@class="CommunityHero PlanPage"]//div[@class="CommunityHero__image image-fit js-community-hero-image is-active"]//img/@data-srcset').getall()
            img=response.xpath('//div[@class="Gallery__chunk _grid _grid--pad js-gallery-chunk"]/div/div/img/@srcset').getall()
            for ii in img:
                img1="".join(ii).replace("\n","").replace("  ","").split(",")[-1]
                imglst.append(img1)
            images="|".join(imglst)
        except Exception as e:
            print(e)
            img=""

        item = BdxCrawlingItem_Spec()
        item['PlanNumber'] = plan_number11
        item['SpecStreet1'] = response.xpath('//div[@class="CommunityHeader__main _grid__col _grid__col--medium-11"]//h1/text()').getall()[0]
        item['SpecCity'] = city
        item['SpecState'] = state
        item['SpecZIP'] = zipcode
        item['SpecNumber'] = int(hashlib.md5(bytes(item['SpecStreet1'], "utf8")).hexdigest(), 16) % (10 ** 30)
        item['SpecCountry'] = 'USA'
        item['SpecPrice'] = 0
        item['SpecSqft'] ="".join(response.xpath('//div[@class="specs__spec specs__spec--sqft"]/div/text()').get()).replace(" Sq. Ft. ","")
        item['SpecBaths'] ="".join(response.xpath('//div[@class="specs__spec specs__spec--bath"]/div/text()').get()).replace(" Baths ","")
        item['SpecHalfBaths'] = 0
        item['SpecBedrooms'] ="".join(response.xpath('//div[@class="specs__spec specs__spec--bed"]/div/text()').get()).replace(" Beds ","")
        item['MasterBedLocation'] = 'Down'
        item['SpecGarage'] ="".join(response.xpath('//div[@class="specs__spec specs__spec--car"]/div/text()').get()).replace(" Car Garage ","")
        item['SpecDescription'] = ''
        item['SpecElevationImage'] =images
        item['SpecWebsite'] = response.url
        yield item

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl mychallengerhomes".split())