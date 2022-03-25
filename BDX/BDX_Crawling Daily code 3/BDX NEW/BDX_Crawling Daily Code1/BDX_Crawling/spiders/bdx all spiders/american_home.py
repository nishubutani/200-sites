# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'american_home'
    allowed_domains = ['https://www.americanhomecorp.com/']
    start_urls = ['https://www.americanhomecorp.com']

    builderNumber = "62710"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()



        images = ''
        image = response.xpath('//div[@class="soliloquy-viewport"]/ul/li/img/@src').extract()
        for i in image:
            images = images + i + '|'
        images = images.strip('|')

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '5368 Deepwoods Court'
        item['City'] = 'Sanford'
        item['State'] = 'FL'
        item['ZIP'] = '32771'
        item['AreaCode'] = '407'
        item['Prefix'] ='302'
        item['Suffix'] = '6603'
        item['Extension'] = ""
        item['Email'] = 'info@americanhomecorp.com'
        item['SubDescription'] = 'American Home Corp is renowned for magnificent custom built homes and remodeling projects as well as spacious additions to homes in the Central Florida/Orlando area. We build luxurious custom homes in Seminole and Lake County with prominence in the Lake Mary, Sanford, Longwood, Altamonte Springs, Mt. Dora, Eustis, Sorrento, Clermont, and Groveland areas.'
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'https://www.americanhomecorp.com/'
        yield scrapy.FormRequest(url=link, callback=self.parse2, dont_filter=True)

    def parse2(self, response):
        links = response.xpath('//ul[@class="sub-menu"]/li/a[contains(@href,"custom-homes")]/@href').extract()
        print(links)
        for link in links:
            yield scrapy.FormRequest(url=link, callback=self.parse3, dont_filter=True)

    def parse3(self, response):

        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//h1/text()').get()
        except Exception as e:
            PlanName = ''
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName + response.url, "utf8")).hexdigest(), 16) % (
                    10 ** 30)
        except Exception as e:
            PlanNumber = ''
            print(e)

        try:
            SubdivisionNumber = self.builderNumber
            print(SubdivisionNumber)
        except Exception as e:
            SubdivisionNumber = ''
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
            BasePrice = 0
        except Exception as e:
            print(e)

        try:
            sqft = response.xpath("//*[contains(text(),'Total Sq Ft:')]/../text()").get()
            sqft = sqft.replace(',', '').strip()
            BaseSqft = re.findall(r"(\d+)", sqft)[0]

        except Exception as e:
            print(e)
            BaseSqft = '0'

        try:
            bath = response.xpath("//*[contains(text(),'Baths:')]/../text()").get()
            tmp = re.findall(r"(\d+)", bath)
            Baths = tmp[0]
            if len(str(tmp)) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            print(e)


        try:
            Bedrooms = response.xpath("//*[contains(text(),'Beds:')]/../text()").get()
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)

        try:
            Garage = response.xpath("//*[contains(text(),'Garages:')]/../text()").get()
            Garage = re.findall(r"(\d+)", Garage)[0]
            if not Garage:
                Garage = 0
        except Exception as e:
            Garage = 0
            print(e)

        # try:
        #     Description = ''.join(
        #         response.xpath('//div[@class="description"]/p/text()').getall())
        #     if not Description:
        #         Description = ''
        # except Exception as e:
        #     print(e)

        try:
            images = []
            imagedata = response.xpath("//img[contains(@src,'uplo')]/@src").getall()
            for id in imagedata:
                id = id
                images.append(id)
            ElevationImage = "|".join(images)
        except Exception as e:
            print(e)

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
        item[
            'Description'] = 'Boise Idaho’s leading custom home builder, designs homes that fits our client’s needs from growing families to empty nesters or any custom or semi- custom home design. Our homes are well designed and built to last. They are beautiful, uniquely yours as well as energy efficient. You can feel the quality inside your new home and when viewing it from the street.'
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item

    # --------------------------------------------------------------------- #


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl american_home'.split())