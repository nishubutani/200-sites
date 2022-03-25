# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header

class DannysullivanconstructionComSpider(scrapy.Spider):
    name = 'henessyhomes'
    allowed_domains = []
    start_urls = ['http://www.hennesseyhomesinc.com/']
    builderNumber = 40385

    def parse(self, response):
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
        item['Street1'] = 'W7101 Firelane 2'
        item['City'] = 'Menasha'
        item['State'] = 'WI'
        item['ZIP'] = '54952'
        item['AreaCode'] = '920'
        item['Prefix'] = '470'
        item['Suffix'] = '9691'
        item['Extension'] = ""
        item['Email'] = 'build@hennesseyhomesinc.com'
        item[
            'SubDescription'] = "Hennessey Homes Inc. is a leading Fox Cities home builder with a proven record of excellence in designing and managing quality construction projects in the Fox Valley - Appleton, WI area for over 25 years. No matter the size of your new home construction project, the experienced professionals at Hennessey Homes Inc. will plan, design, construct, and maintain your new home project. You'll Be Glad You Chose Us! Effective planning is crucial to the successful completion of any project. Before starting the project, our team of experts will first assess your needs and goals. Then we provide you with an cost estimate and time-line for completion. From beginning to end you will be involved every step of the way. Cost-Effective Services Eliminate all the items on your to-do list by calling the experts at Hennessey Homes Inc. You'll be glad you did! We have many years of experience and work hard to make sure the job is done right while saving you time, money, and aggravation. We'll be there whenever you need us."
        item[
            'SubImage'] = 'http://www.hennesseyhomesinc.com/image/53817730.jpg'
        item['SubWebsite'] = response.url
        yield item

        planlinks = ['http://www.hennesseyhomesinc.com/single-story-plans.html','http://www.hennesseyhomesinc.com/2-story-plans.html']
        for link in planlinks:
            yield scrapy.FormRequest(url=link,callback=self.plandetail,dont_filter=True)

    def plandetail(self,response):
        print(response.url)
        divs = response.xpath('//div[@align="left"]')
        for div in divs:
            try:
                Type = 'SingleFamily'
            except Exception as e:
                Type = 'SingleFamily'
                print(e)

            try:
                PlanName = div.xpath('.//p/font/text()').get()
                PlanName = re.sub('<[^<]+?>', '', str(PlanName))
                print(PlanName)
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
                SubdivisionNumber = response.meta['sbdn']
            except Exception as e:
                print(e)

            try:
                PlanNotAvailable = 0
            except Exception as e:
                print(e)

            try:
                BasePrice = 0.00
            except Exception as e:
                print(e)

            try:
                PlanTypeName = 'Single Family'
            except Exception as e:
                print(e)

            try:
                plansquare = div.xpath('.//*[contains(text(),"Sq. Ft.")]/text()').get()
                # print(plansquare)
                plansquare = re.sub('<[^<]+?>', '', str(plansquare))
                BaseSqft = re.findall(r"(\d+)",plansquare)[0]
                print(BaseSqft)
            except Exception as e:
                print("BaseSqft: ", e)
            try:
                planbeds = div.xpath('.//*[contains(text(),"bedroom")]/text()').get()
                # planbeds = re.sub('<[^<]+?>', '', str(planbeds))
                if '-' in planbeds:
                    planbeds = planbeds.split('-')[-1]
                planbeds = re.findall(r"(\d+)", planbeds)[0]
                print(planbeds)

            except Exception as e:
                print("planbeds: ", e)
            try:
                planbath = div.xpath('.//*[contains(text(),"bath")]/text()').get()
                planbath = re.sub('<[^<]+?>', '', str(planbath))
                # planbath = planbath.split(',')[1]
                tmp = re.findall(r"(\d+)", planbath)
                planbath = tmp[0]
                print(planbath)
                if len(tmp) > 1:
                    planHalfBaths = 1
                    print(planHalfBaths)
                else:
                    planHalfBaths = 0
                    print(planHalfBaths)
                # print(planbath)
            except Exception as e:
                print("planbath: ", e)
            try:
                cargarage = div.xpath('.//*[contains(text(),"car garage")]/text()').get()
                cargarage = re.sub('<[^<]+?>', '', str(cargarage))
                cargarage = re.findall(r"(\d+)",cargarage)[0]
                print(cargarage)
            except Exception as e:
                cargarage = 0
                print("cargarage: ", e)
            try:
                Description = ' '
                # print(Description)
            except Exception as e:
                Description = ' '
                print('Description:', e)
            try:
                PlanImage = 'http://www.hennesseyhomesinc.com/image/53817730.jpg'
                # PlanImages = response.xpath('//li//img/@src').extract()
                # for PlanImag in PlanImages:
                #     PlanImage.append(PlanImag)
                # PlanImage = '|'.join(PlanImage)
                # print(PlanImage)
            except Exception as e:
                print("SpecElevationImage: ", e)
            try:
                PlanWebsite = response.url
            except Exception as e:
                print(e)
            try:
                unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
                        10 ** 30)  # < -------- Changes here
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
                item['Baths'] = planbath
                item['HalfBaths'] = planHalfBaths
                item['Bedrooms'] = planbeds
                item['Garage'] = cargarage
                item['Description'] = Description
                item['ElevationImage'] = PlanImage
                item['PlanWebsite'] = PlanWebsite
                print(item)
                yield item
            except Exception as e:
                print(e)

        homelink = 'http://www.hennesseyhomesinc.com/homes-for-sale.html'
        yield scrapy.FormRequest(url=homelink,callback=self.HomeDetail,dont_filter=True)

    def HomeDetail(self,response):
        try:
            SpecStreet1 = response.xpath('//span[@itemprop="streetAddress"]//text()').extract_first()
            SpecStreet1=SpecStreet1.replace(",","")
            SpecCity =response.xpath('//span[@itemprop="addressLocality"]//text()').extract_first()
            SpecState = response.xpath('//span[@itemprop="addressRegion"]//text()').extract_first()
            SpecZIP =response.xpath('//span[@itemprop="postalCode"]//text()').extract_first()
            unique = str(SpecStreet1) + str(SpecCity) + str(SpecState) + str(SpecZIP)
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
            SpecPrice = str(response.xpath('normalize-space(//span[@itemprop="price"]//text())').extract_first(default='0').strip()).replace(",", "")
            SpecPrice = re.findall(r"(\d+)", SpecPrice)[0]
        except Exception as e:
            print(e)

        try:
            SpecSqft = str(response.xpath('normalize-space(//ul[@class="property-meta list-horizontal list-style-disc list-spaced"]//li[@data-label="property-meta-sqft"]//span/text())').extract_first(
                default='0').strip()).replace(",", "")
            SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
        except Exception as e:
            SpecSqft = 0

        try:
            SpecBaths = str(response.xpath(
                'normalize-space(//ul[@class="property-meta list-horizontal list-style-disc list-spaced"]//li[@data-label="property-meta-bath"]//span/text())').extract_first(
                default='0').strip()).replace(",", "")
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
            SpecBedrooms = str(response.xpath(
                'normalize-space(//ul[@class="property-meta list-horizontal list-style-disc list-spaced"]//li[@data-label="property-meta-beds"]//span/text())').extract_first(
                default='0').strip()).replace(",", "")
            SpecBedrooms = re.findall(r"(\d+)", SpecBedrooms)[0]
        except Exception as e:
            SpecBedrooms = 0

        try:
            MasterBedLocation = "Down"
        except Exception as e:
            print(e)

        try:
            SpecGarage = response.xpath('//div[@class="load-more-features load-more-trigger"]/div[@class="row"]/div[@class="col-sm-6"]/ul[@class="list-default"]/li[contains(text(),"Number of Garage Spaces:")]').get()
            SpecGarage = re.findall(r"(\d+)", SpecGarage)[0]
        except Exception as e:
            SpecGarage = 0

        try:
            SpecDescription = response.xpath('//*[@id="ldp-detail-romance"]//text()').extract()
            SpecDescription = str(''.join(SpecDescription)).strip()
            SpecDescription = SpecDescription.replace("\n", "").replace("  ", "")
        except Exception as e:
            print(e)

        try:
            ElevationImage = response.xpath('//*[@class="fsgallery-main owl-carousel ldp-photos "]//div[@class=""]//img//@data-src').extract()
            ElevationImage = "|".join(ElevationImage)
            SpecElevationImage = ElevationImage
        except Exception as e:
            print(e)
        if ElevationImage=="":
            try:
                ElevationImage = response.xpath('//*[@class="modal-body"]/div[@id="ldpPhotoGallery"]/div[@class="photo-item"]//img//@data-src').extract()
                ElevationImage = "|".join(ElevationImage)
                SpecElevationImage = ElevationImage
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
if __name__ == '__main__':
    execute("scrapy crawl henessyhomes".split())