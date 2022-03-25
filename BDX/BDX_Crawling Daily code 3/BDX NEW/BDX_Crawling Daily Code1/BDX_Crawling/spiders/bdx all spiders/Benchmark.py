# -*- coding: utf-8 -*-
import hashlib
import re

import requests
import scrapy
import scrapy.utils
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class Benchmarkbuilder(scrapy.Spider):
    name = 'benchmark'
    allowed_domains = []
    start_urls = ['https://www.benchmarkbuildersiowa.com/our-communities/']
    builderNumber = "62952"
    def __init__(self):
        self.temp_list = []


    def parse(self, response):
        try:
            urls=response.xpath('//*[@class="button button-primary"]/@href').extract()
            for url in urls:
                urlss=url
                yield scrapy.Request(url=urlss,callback=self.parse1)
        except Exception as e:
            print(e)
    def parse1(self, response):
        if '/brook-landing-des-moines/' in response.url:
            SpecStreet1='Brook Landing Des Moines'
            SpecCity='Delaware'
            SpecState='IA'
            SpecZIP='00000'
        elif '/harvest-ridge-ankeny/' in response.url:
            SpecStreet1 = 'Harvest Ridge'
            SpecCity = 'Ankeny'
            SpecState = 'IA'
            SpecZIP = '00000'
        elif '/pine-valley-pleasant-hill/' in response.url:
            SpecStreet1 = 'Pine Valley'
            SpecCity = 'Pleasant Hill'
            SpecState = 'IA'
            SpecZIP = '00000'
        else:
            address = response.xpath('//*[contains(text(),"Google Map")]/@href').get()
            print(address)
            try:
                # Home_Name = response.xpath('//div[@class="green-title"]//span//text()').get()
                SpecStreet1 = address.split('/')[5].split(',')[0].replace('+',' ')
                SpecCity = address.split('/')[5].split(',')[1].replace('+','')
                SpecState = address.split('/')[5].split(',')[2].replace('+',' ').split()[0]
                SpecZIP = address.split('/')[5].split(',')[2].replace('+',' ').split()[1]

            except Exception as e:
                print(e)
        try:
            subdivisonName=response.xpath('//*[@class="page-title"]/text()').extract_first().strip()
            subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % subdivisonNumber, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
            print(e)
        try:
            a = []
            # aminity = ''.join(response.xpath('//*[@class="ll-features-content__half right col-md-1of2"]/ul[1]/li/text()').extract())
            try:
                aminity = ''.join(response.xpath('//*[@class="col-md-11 col-lg-10 col-xl-7"]/p/text()').extract())
            except Exception as e:
                print(e)

            amenity_list = ["Pool", "Playground", "GolfCourse", "Tennis", "Soccer", "Volleyball", "Basketball",
                            "Baseball", "Views", "Lake", "Pond", "Marina", "Beach", "WaterfrontLots", "Park",
                            "Trails", "Greenbelt", "Clubhouse", "CommunityCenter"]
            for i in amenity_list:
                if i in aminity:
                    a.append(i)
            ab = '|'.join(a)
        except Exception as e:
            print(e)
        try:
            subname=response.xpath('//*[@class="page-title"]/text()').extract_first().strip()
            SubdivisionNumber1 = int(hashlib.md5(bytes(subname, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % SubdivisionNumber1, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
            print(e)

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = SubdivisionNumber1
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = subname
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = SpecStreet1
        item['City'] = SpecCity
        item['State'] = "IA"
        item['ZIP'] = SpecZIP
        item['AreaCode'] = "515"
        item['Prefix'] = "963"
        item['Suffix'] = "8335"
        item['Extension'] = ""
        item['Email'] = "@Benchmarkbuildersiowa"
        item['SubDescription'] =aminity
        item['AmenityType'] = ab
        item['SubImage'] = "https://www.benchmarkbuildersiowa.com/wp-content/uploads/2020/02/slide4-1920x700.jpg|https://www.benchmarkbuildersiowa.com/wp-content/uploads/2020/02/slide1-1920x700.jpg|https://www.benchmarkbuildersiowa.com/wp-content/uploads/2020/02/slide2-1920x700.jpg|https://www.benchmarkbuildersiowa.com/wp-content/uploads/2020/02/slide3-1920x700.jpg"
        item['SubWebsite'] = response.url
        yield item
        temp_dict = {
            'subdivisonNumber': subdivisonNumber,
            'zip_code': SpecZIP
        }
        self.temp_list.append(temp_dict)


        # try:
        #     home_link=response.xpath('//*[contains(text(),"Current Listings")]/@href').extract()
        #     if home_link!=[]:
        #         for hlink in  home_link:
        #             hlink=hlink
        #             yield scrapy.Request(url=hlink, callback=self.process_home,dont_filter=True,
        #                     meta={'SubdivisionNumber1': SubdivisionNumber1})
        # except Exception as e:
        #     print(e)

        yield scrapy.Request(url="https://www.benchmarkbuildersiowa.com/floor-plans/",dont_filter=True, callback=self.plan1,meta={'SubdivisionNumber1':SubdivisionNumber1})

    def plan1(self, response):
        try:
            SubdivisionNumber1 = response.meta['SubdivisionNumber1']
            links = response.xpath('//*[@class="unit-body"]/a/@href').extract()
            for link in links:
                link = link
                yield scrapy.Request(url=link, callback=self.Plan,meta={'SubdivisionNumber1':SubdivisionNumber1})
        except Exception as e:
            print(e)

    def Plan(self, response):
        SubdivisionNumber = self.builderNumber
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = self.builderNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = "2785 N Ankeny Blvd Ste 22"
        item['City'] = "Ankeny"
        item['State'] = "IA"
        item['ZIP'] = "50023"
        item['AreaCode'] = "515"
        item['Prefix'] = "963"
        item['Suffix'] = "8335"
        item['Extension'] = ""
        item['Email'] = "@Benchmarkbuildersiowa"
        item['SubDescription'] = """At Benchmark Builders, we bring our experience and quality craftsmanship to deliver high quality yet affordable homes to the Central Iowa market. With our commitment to building energy efficient homes, you will be proud to own a home that will provide you and your family years of memories and enjoyment.Our homes are built with affordability and quality in mind. Each of our builds come with features such as granite countertops, luxury vinyl plank floors, energy-efficient appliances, and spacious layouts.Whether you are a first-time homebuyer or looking to move up, Benchmark Builders offer choice, quality, and value throughout our communities. Choose from a wide selection of new homes located near shopping, dining, recreation, and major employers."""
        item['AmenityType'] = ''
        item['SubImage'] = "https://www.benchmarkbuildersiowa.com/wp-content/uploads/2020/02/slide4-1920x700.jpg|https://www.benchmarkbuildersiowa.com/wp-content/uploads/2020/02/slide1-1920x700.jpg|https://www.benchmarkbuildersiowa.com/wp-content/uploads/2020/02/slide2-1920x700.jpg|https://www.benchmarkbuildersiowa.com/wp-content/uploads/2020/02/slide3-1920x700.jpg"
        item['SubWebsite'] = response.url
        yield item

        try:
            planname = response.xpath('//*[@class="page-title"]/text()').extract_first()
            PlanNumber = int(hashlib.md5(bytes(planname, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % PlanNumber, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
            print(e)

        try:
            BasePrice = "0"  # response.xpath('normalize-space(//span[@class="price"]/text())').extract_first().strip().replace('$', '').replace('+','')
        except Exception as e:
            BasePrice = ""
            print("SpecPrice", e, response.url)

        try:

            BaseSqft1 = response.xpath('//*[contains(text(),"SECOND LEVEL:")]/text()').extract_first().replace(',', '')
            BaseSqft1 = re.findall('(\d+)', BaseSqft1)[0]
            BaseSqft1 = int(BaseSqft1)
        except Exception as e:
            BaseSqft1 = 0
            print(e)
        try:
            BaseSqft2 = response.xpath('//*[contains(text(),"MAIN LEVEL:")]/text()').extract_first().replace(',', '')
            BaseSqft2 = re.findall('(\d+)', BaseSqft2)[0]
            BaseSqft2 = int(BaseSqft2)

        except Exception as  e:
            BaseSqft2 = 0
            print(e)
        try:
            BaseSqft3 = response.xpath('//*[contains(text(),"OPT LOWER LEVEL:")]/text()').extract_first().replace(',',
                                                                                                                  '').replace(
                "'", "")
            BaseSqft3 = re.findall('(\d+)', BaseSqft3)[0]
            BaseSqft3 = int(BaseSqft3)
        except Exception as e:
            BaseSqft3 = 0
            print("SpecSqft", e, response.url)
        try:
            BaseSqft4 = BaseSqft1 + BaseSqft2 + BaseSqft3
            BaseSqft = BaseSqft4
            print(BaseSqft)
        except Exception as e:
            BaseSqft = 0
            print(e)

        try:
            Baths = response.xpath('//*[contains(text(),"BED:")]/text()').get().split('/')[-1]
            tmp = re.findall(r"(\d.\d)", Baths) or re.findall(r"(\d)", Baths)
            Baths = int(float(tmp[0]))
            if len(tmp[0]) > 1:
                planHalfBaths = 1
            else:
                planHalfBaths = 0
        except Exception as e:
            Baths = 0
            planHalfBaths = 0
            print("Baths", e, response.url)

        try:
            Bedrooms = response.xpath('//*[contains(text(),"BED:")]/text()').get().split('/')[0]
            Bedrooms = re.findall(r"(\d)", Bedrooms)[0]
        except Exception as e:
            Bedrooms = 0
            print("SpecBedrooms", e, response.url)

        try:
            Garage = '0.0'  # response.xpath('//div[@class="property-details"]//*[contains(text(),"Gar")]/text()').get()
            # Garage = re.findall(r"(\d)", Garage)[0]
        except Exception as e:
            print(e)
            Garage = 0
            print('SpecGarage', e, response.url)

        try:
            PDescription = """At Benchmark Builders, we bring our experience and quality craftsmanship to deliver high quality yet affordable homes to the Central Iowa market. With our commitment to building energy efficient homes, you will be proud to own a home that will provide you and your family years of memories and enjoyment.Our homes are built with affordability and quality in mind. Each of our builds come with features such as granite countertops, luxury vinyl plank floors, energy-efficient appliances, and spacious layouts.Whether you are a first-time homebuyer or looking to move up, Benchmark Builders offer choice, quality, and value throughout our communities. Choose from a wide selection of new homes located near shopping, dining, recreation, and major employers."""

        except Exception as e:
            print("SpecDescription", e, response.url)
        images=''
        try:
            images1 = response.xpath('//*[@class="floor-meta"]//img/@src').extract_first()
            im1 = response.xpath('//*[@class="section floor-hdr"]/@style').extract_first(default='')
            if im1=='':
                im1=''
            else:
                im2=re.findall('url(.*?).jpg',str(im1))
            try:
                images=images1+'|'+im2
                print('images',images)
            except Exception as e:
                print('error in images')
                print(e)

        except Exception as e:
            print("SpecElevationImage", e, response.url)

        try:
            PlanWebsite = response.url
            print(PlanWebsite)
        except Exception as e:
            print(e)

        try:
            item = BdxCrawlingItem_Plan()
            unique = str(PlanNumber) + str(SubdivisionNumber)
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            item['unique_number'] = unique_number
            item['Type'] = "SingleFamily"
            item['PlanNumber'] = PlanNumber
            item['SubdivisionNumber'] = SubdivisionNumber
            item['PlanName'] = planname
            item['PlanNotAvailable'] = 1
            item['PlanTypeName'] = "Single Family"
            item['BasePrice'] = BasePrice
            item['BaseSqft'] = BaseSqft
            item['Baths'] = Baths
            item['HalfBaths'] = planHalfBaths
            item['Bedrooms'] = Bedrooms
            item['Garage'] = Garage
            item['Description'] = PDescription
            item['ElevationImage'] = images
            item['PlanWebsite'] = PlanWebsite
            yield item

        except Exception as e:
            print("Problem in Unknown Plan creation:", e)

        SubdivisionNumber1=SubdivisionNumber
        yield scrapy.Request(url='https://www.benchmarkbuildersiowa.com/property/', callback=self.process_home,dont_filter=True,meta={'SubdivisionNumber1':SubdivisionNumber1})


    def process_home(self, response):
        SubdivisionNumber1=response.meta['SubdivisionNumber1']
        try:
            links = response.xpath('//*[@class="card-img-container"]/a/@href').extract()
            for link in links:
                link = link
                yield scrapy.Request(url=link, callback=self.homedetails,meta={'SubdivisionNumber1':SubdivisionNumber1},dont_filter=True)
        except Exception as e:
            print(e)

    def homedetails(self, response):
        SubdivisionNumber1=response.meta['SubdivisionNumber1']
        try:

            r=response.url
            print(r)
            a = response.xpath('//*[@class="col"]//@src').extract()
            a = response.xpath('//*[@class="col"]/iframe/@src').extract()

            b = re.findall('q=(.*?)&', str(a))
            c = ''.join(b).split('+')
            SpecStreet1 = c[0].strip()
            SpecCity = c[1].strip()
            SpecState = 'IA'
            SpecZIP = c[2].strip()
            if SpecZIP==None:
                SpecZIP='00000'
            else:
                SpecZIP = SpecZIP
            if  'https://www.benchmarkbuildersiowa.com/property/3120-brook-landing-des-moines/' in response.url:
                SpecStreet1 = '3120 Brook Landing'
                SpecCity = 'Des Moines'
                SpecState = 'IA'
                SpecZIP = '00000'
                unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()

            if "/2826-nw-westwood-ct-ankeny/" in response.url:
                SpecZIP = '50023'
                unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()

            elif "/401-ryan-cir-ne-mitchellville/" in response.url:
                SpecCity = "Ankeny"
                SpecZIP = '50169'
                unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
            elif "/402-ryan-circle-mitchellville/" in response.url:
                SpecZIP = '50169'
                unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
            elif "/180-aspen-drive-norwalk/" in response.url:
                SpecStreet1 = '180 Aspen Drive'
                SpecZIP = '50211'
                unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
            elif "/2704-nw-beechwood-st-ankeny/" in response.url:
                SpecStreet1 = '2704 NW Beechwood St'
                SpecCity = 'Ankeny'
                SpecZIP = '50023'
                unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()

            try:

                unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
            except Exception as e:
                print(e)

            try:
                SpecPrice = response.xpath('//*[@class="text-center py-3 mx-0 h2bg"]/text()').getall()[0].strip().replace('$', '').replace(',', '')
                if "TBD" in SpecPrice:
                    SpecPrice = '0'
            except Exception as e:
                SpecPrice = 0
                print(e)

            try:
                if "/308-ne-62nd-st-ankeny/" in response.url:
                    SpecSqft = '0'
                else:
                    SpecSqft = response.xpath('//*[contains(text(),"sq.ft")]/text()|//*[contains(text(),"Area")]/following-sibling::h6[1]/text()').extract()[0].strip().replace(',', '')
                    SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
            except Exception as e:
                SpecSqft = 0

            try:
                SpecBaths = response.xpath('//*[@class="card-body p-0 m-0"]/h6[contains(text(),"Baths")]/text()').extract_first()
                tmp = re.findall(r"(\d+)", SpecBaths)
                SpecBaths = tmp[0]
                if len(tmp) > 1:
                    SpecHalfBaths = 1
                else:
                    SpecHalfBaths = 0

            except Exception as e:
                SpecBaths = 0
                SpecHalfBaths = 0

            try:
                SpecBedrooms = response.xpath(
                    '//*[@class="card-body p-0 m-0"]/h6[contains(text(),"Bedroom")]/text()').extract_first()
                SpecBedrooms = re.findall(r'(\d+)', SpecBedrooms)[0]
            except Exception as e:
                SpecBedrooms = 0
            try:
                garage = response.xpath('//*[contains(text(),"Garage")]/text()').extract_first()
                garage = re.findall(r'(\d+)', garage)[0]
            except Exception as e:
                garage = 0
                print(e)

            try:
                SpecDescription = ''.join(
                    response.xpath('//*[contains(text(),"About")]/following-sibling::p/text()').extract()).strip()
            except Exception as e:
                SpecDescription = ''

            try:
                ElevationImage = response.xpath('//*[@class=" p-0 m-0 col-md-3"]/a/@href').extract()
                img = []
                for s in ElevationImage:
                    s = re.sub('\n|\t|\s\s+', '', s).strip()
                    if s != "":
                        img.append(s)
                images_new = '|'.join(img)
            except Exception as e:
                img = ''

            for i in self.temp_list:
                print(SpecZIP)

                subdivisionnumber = i['subdivisonNumber']
                zip_code = i['zip_code']
                if SpecZIP == zip_code:


                    unique = str(subdivisionnumber)  # < -------- Changes here
                    unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
                    item = BdxCrawlingItem_Plan()
                    item['unique_number'] = unique_number
                    item['Type'] = "SingleFamily"
                    item['PlanNumber'] = "Plan Unknown"
                    item['SubdivisionNumber'] = subdivisionnumber
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

                    # ----------------------- Don't change anything here ---------------- #
                    item = BdxCrawlingItem_Spec()
                    item['SpecNumber'] = SpecNumber
                    item['PlanNumber'] = unique_number
                    item['SpecStreet1'] = SpecStreet1
                    item['SpecCity'] = SpecCity
                    item['SpecState'] = SpecState
                    item['SpecZIP'] = SpecZIP
                    item['SpecCountry'] = 'USA'
                    item['SpecPrice'] = SpecPrice
                    item['SpecSqft'] = SpecSqft
                    item['SpecBaths'] = SpecBaths
                    item['SpecHalfBaths'] = SpecHalfBaths
                    item['SpecBedrooms'] = SpecBedrooms
                    item['MasterBedLocation'] = "Down"
                    item['SpecGarage'] = garage
                    item['SpecDescription'] = SpecDescription
                    item['SpecElevationImage'] = images_new
                    item['SpecWebsite'] = response.url
                    yield item

                else:
                    pass


        except Exception as e:
            print(e)
            print("commm")
        # --------------------------------------------------------------------- #
if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl benchmark".split())