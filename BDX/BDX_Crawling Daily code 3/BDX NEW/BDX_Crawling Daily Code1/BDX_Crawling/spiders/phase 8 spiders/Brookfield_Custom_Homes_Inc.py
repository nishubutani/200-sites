# -*- coding: utf-8 -*-
import scrapy
import hashlib
import re
import scrapy
from lxml import html
from scrapy.utils.response import open_in_browser
import requests

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class BrookfieldCustomHomesIncSpider(scrapy.Spider):
    name = 'Brookfield_Custom_Homes_Inc'
    allowed_domains = []
    start_urls = ['https://brookfieldcustomhomes.com/communities/']
    builderNumber = 22980

    def parse(self, response):
        community_links = response.xpath('//*[@class="card"]/a/@href').extract()
        for links in community_links:
            print("Communities------------->", links)
            yield scrapy.FormRequest(url=links, callback=self.property_details)

    def property_details(self, response):
        # ------------------- Creating Communities --------------------- #
        try:
            subdivisonName = response.xpath('//*[@class="margin-b-sm"]/text()').extract_first()
            subdivisonNumber = int(hashlib.md5(bytes(str(subdivisonName) + str(self.builderNumber), "utf8")).hexdigest(), 16) % (10 ** 30)
            # print(subdivisonNumber)
        except Exception as e:
            print(e)

        f = open("html/%s.html" % subdivisonNumber, "wb")
        f.write(response.body)
        f.close()
        try:
            ElevationImage = '|'.join(re.findall(r'url(.*?);"></div>',response.text)).replace('(','').replace(')','')
        except Exception as e:
            print(str(e))
        a=response.xpath('//*[@class="margin-b-sm margin-t-sm"]/text()').extract_first()
        Street1=a.split(',')[0].strip()
        City=a.split(',')[1].strip()
        State=a.split(',')[-1].strip()
        State = State.split(' ')[0]
        z=a.split(',')[-1].strip()
        Zip = re.findall(r"(\d+)",z)
        Zip = Zip[0]

        SubDescription = ''.join(response.xpath('//*[@class="margin-b-md"]//text()').extract()).strip()

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionName'] = subdivisonName
        item['SubdivisionNumber'] = subdivisonNumber
        item['BuilderNumber'] = self.builderNumber
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 1
        item['Street1'] = Street1
        item['City'] = City.strip()
        item['State'] = 'OK'
        item['ZIP'] = Zip
        item['AreaCode'] = '405'
        item['Prefix'] = '310'
        item['Suffix'] = '6656'
        item['Extension'] = ""
        item['Email'] = "Sales@brookfieldcustomhomes.com"
        item['SubDescription'] = SubDescription
        item['SubImage'] = ElevationImage
        item['SubWebsite'] = response.url
        yield item

        url = 'https://brookfieldcustomhomes.com/plans/'
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.Plans_url,
                                     meta={'sbdn': subdivisonNumber})

    def Plans_url(self,response):
        sbdn = response.meta['sbdn']
        urls = response.xpath('//*[@class="card"]/a/@href').extract()
        for url in urls:
            print("PLANS--------------------->",url)
            yield scrapy.FormRequest(url=url,dont_filter=True,callback=self.Plans_details,meta={'sbdn':sbdn})

    def Plans_details(self,response):
        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)
        try:
            PlanName = response.xpath('//*[@class="margin-b-md"]/text()').extract_first().strip()
        except Exception as e:
            print(e)
        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = response.meta['sbdn']
            # print(SubdivisionNumber)
        except Exception as e:
            print(str(e))

        try:
            PlanNotAvailable = 0
        except Exception as e:
            print(e)

        PlanTypeName = 'Single Family'

        try:
            BasePrice = response.xpath('//*[@class="margin-b-sm"]/h4[1]/text()').extract_first().replace(',','')
            BasePrice = re.findall(r"(\d+)", BasePrice)
            BasePrice =BasePrice[0]
        except Exception as e:
            print(str(e))

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

        Baths = response.xpath('//*[@class="col-md-7 col-sm-12 col-xs-12 no-gutters margin-t-sm margin-b-sm"]/div[2]/h5/text()').extract_first()
        Bath = re.findall(r"(\d+)", Baths)
        Baths = Bath[0]
        tmp = Bath
        if len(tmp) > 1:
            HalfBaths = 1
        else:
            HalfBaths = 0

        Bedrooms = response.xpath('//*[@class="col-md-7 col-sm-12 col-xs-12 no-gutters margin-t-sm margin-b-sm"]/div[1]/h5/text()').extract_first()
        Bedrooms = re.findall(r"(\d+)", Bedrooms)
        Bedrooms = Bedrooms[0]

        Garage = response.xpath('//*[@class="col-md-7 col-sm-12 col-xs-12 no-gutters margin-t-sm margin-b-sm"]/div[3]/h5/text()').extract_first()
        Garage = re.findall(r"(\d+)", Garage)
        Garage = Garage[0]

        try:
            BaseSqft = response.xpath('//*[@class="col-md-7 col-sm-12 col-xs-12 no-gutters margin-t-sm margin-b-sm"]/div[4]/h5/text()').extract_first().replace(',','')
            BaseSqft = re.findall(r"(\d+)", BaseSqft)
            BaseSqft = BaseSqft[0]
        except Exception as e:
            BaseSqft = 0
            print(e)


        try:
            Description = 0
        except:
            Description = ''

        try:
            ElevationImage = ''.join(re.findall(r'url(.*?);"></div>',response.text)).replace('(','').replace(')','')
        except Exception as e:
            print(str(e))

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

        url = 'https://brookfieldcustomhomes.com/homes/'
        yield scrapy.FormRequest(url=url,dont_filter=True,callback=self.Home_Url,meta={'PN': unique_number})

    def Home_Url(self,response):
        PN = response.meta['PN']
        urls = response.xpath('//*[@class="card"]/a/@href').extract()
        for url in urls:
            print('HOMES------------->',url)
            yield scrapy.Request(url=url, callback=self.home_details, meta={'PN': PN})

    def home_details(self,response):
        try:
            address = response.xpath('//*[@class="margin-b-sm margin-t-none"]/text()').extract_first()
            add = address.split(',')
            SpecStreet1 = add[0]
            SpecCity = add[1].strip()

            state = add[-1].strip()
            SpecState = state.split(' ')[0]
            zip = add[-1]
            SpecZIP = ''.join(re.findall(r"(\d+)", zip))
            # print(SpecZIP)

            unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
            # print(unique)
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
            SpecPrice = response.xpath('//h4[@class="margin-b-sm"]/text()').extract_first().replace('Price: ', '').strip()
            SpecPrice = SpecPrice.replace('$', '')
            SpecPrice = re.sub(',', '', SpecPrice)
            SpecPrice = SpecPrice.strip()
            # print(SpecPrice)
        except Exception as e:
            print(str(e))

        try:
            SpecBedrooms = response.xpath('//*[@class="col-md-7 col-sm-12 col-xs-12 no-gutters margin-t-sm margin-b-sm"]/div[1]/h5/text()').extract_first()
            SpecBedrooms = re.findall(r"(\d+)", SpecBedrooms)
            SpecBedrooms = SpecBedrooms[0]
        except Exception as e:
            print(str(e))

        try:
            SpecBath = response.xpath('//*[@class="col-md-7 col-sm-12 col-xs-12 no-gutters margin-t-sm margin-b-sm"]/div[2]/h5/text()').extract_first()
            SpecBaths = re.findall(r"(\d+)", SpecBath)
            SpecBaths = SpecBaths[0]
            tmp = SpecBath
            if len(tmp) > 1:
                SpecHalfBaths = 1
            else:
                SpecHalfBaths = 0
            # print(SpecBaths)
        except Exception as e:
            print(str(e))

        try:
            SpecGarage = response.xpath('//*[@class="col-md-7 col-sm-12 col-xs-12 no-gutters margin-t-sm margin-b-sm"]/div[3]/h5/text()').extract_first()
            SpecGarage = re.findall(r"(\d+)", SpecGarage)
            SpecGarage = SpecGarage[0]
        except Exception as e:
            print(str(e))

        try:

            SpecSqft = response.xpath('//*[@class="col-md-7 col-sm-12 col-xs-12 no-gutters margin-t-sm margin-b-sm"]/div[4]/h5/text()').extract_first().replace(',','')
            SpecSqft = re.findall(r"(\d+)", SpecSqft)
            SpecSqft = SpecSqft[0]
        except Exception as e:
            print(str(e))

        try:
            MasterBedLocation = "Down"
        except Exception as e:
            print(e)

        try:
            SpecDescription = 0

        except Exception as e:
            print(e)

        try:
            ElevationImage ='|'.join(re.findall(r'url(.*?);"></div>',response.text)).replace('(','').replace(')','')

        except Exception as e:
            print(str(e))

        try:
            SpecWebsite = response.url
        except Exception as e:
            print(e)

        # ----------------------- Don't change anything here --------------------- #
        item = BdxCrawlingItem_Spec()
        item['SpecNumber'] = SpecNumber
        item['PlanNumber'] = PlanNumber
        item['SpecStreet1'] = SpecStreet1
        item['SpecCity'] = SpecCity
        item['SpecState'] = 'OK'
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
        item['SpecElevationImage'] = ElevationImage
        item['SpecWebsite'] = SpecWebsite
        yield item

# from scrapy.cmdline import execute
# execute("scrapy crawl Brookfield_Custom_Homes_Inc --nolog".split())

