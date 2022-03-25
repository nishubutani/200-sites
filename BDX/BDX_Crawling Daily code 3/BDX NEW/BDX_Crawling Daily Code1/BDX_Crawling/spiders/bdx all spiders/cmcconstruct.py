
# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'cmcconstruct'
    allowed_domains = ['https://www.cmcconstruct.com/']
    start_urls = ['https://www.cmcconstruct.com/']

    builderNumber = "53136"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()


        # images = ''
        # image = response.xpath('//div[@class="widget animated fadeInUpShort"]//img[@class="lazy loaded"]').extract()
        # for i in image:
        #     images = images + i + '|'
        # images = images.strip('|')

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = '33908'
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '1181 Vickery Ln Suite 102'
        item['City'] = 'Cordova'
        item['State'] = 'TN'
        item['ZIP'] = '38016'
        item['AreaCode'] = '901'
        item['Prefix'] ='461'
        item['Suffix'] = '9508'
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = 'CMCC, LLC is owned by Phil Chamberlain and Jon McCreery who joined forces to form their successful partnership over 35 years ago.  Hard work, integrity, and a commitment to excellence have been the guiding principles that have earned Chamberlain & McCreery the reputation as a leader in the general contracting industry.  Phil and Jon have also been very involved with building industry trade organizations and their communities through volunteering their time to serve as leaders of governmental, civic, and industry related organizations.'
        item['SubImage'] = 'https://www.cmcconstruct.com/wp-content/uploads/bb-plugin/cache/10233-evergreen-manor-snapsold-screen-192270-11-panorama.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        links = ['https://www.cmcconstruct.com/new-homes/burton-place/','https://www.cmcconstruct.com/new-homes/neville/']

        for link in links:
            yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)
            # yield scrapy.FormRequest(url='https://www.cmcconstruct.com/new-homes/burton-place/',callback=self.parse2,dont_filter=True)

    def parse2(self, response):
        links = response.xpath('//h3[@class="entry-title"]/a/@href').extract()
        for link in links:
            yield scrapy.FormRequest(url=link, callback=self.parse3, dont_filter=True)


    def parse3(self, response):


        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//h1[@class="entry-title"]/text()').get()
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
            Description = ""
        except Exception as e:
            print(e)
            Description = ''


        try:
            try:
                sqft = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*s.f.", Description.lower())[0]
            except Exception as e:
                print(e)
                sqft = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*square foot", Description.lower())[0]

            sqft = sqft.replace("three", "3").replace("four", "4").replace("two", "2")
            sqft = sqft.replace(',', '').strip()
            if '.' in sqft:
                sqft = sqft.split(".")[0]
            BaseSqft = re.findall(r"(\d+)", sqft)[0]

        except Exception as e:
            print(e)
            BaseSqft = ''

        try:

            bath = response.xpath('//div[@title="Bathrooms"]/../div[2]/text()').extract_first('')
            tmp = re.findall(r"(\d+)", bath)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            print(e)
            Baths,HalfBaths = 0,0

        try:
            Bedrooms = response.xpath('//div[@title="Bedrooms"]/../div[2]/text()').get()
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)

        try:

            Garage = response.xpath('//div[@title="Parking Spaces"]/../div[2]/text()').get()
            Garage = Garage.replace("three", "3").replace("four", "4").replace("two", "2")
            Garage = re.findall(r"(\d+)", Garage)[0]

        except Exception as e:
            print(e)
            Garage = 0



        try:

            images1 = response.xpath('//div[@class="img-inner dark"]/img/@data-src').extract()

            images2 = response.xpath('//div[@class="epl-featured-image it-featured-image"]/a/img/@src').extract_first('')
            if ',' in images2:
                images2 = images2.split(",")[0]
                print(images2)


            images = []
            for id in images1:
                id = id
                images.append(id)
            ElevationImage = images

            if images2 != '':
                ElevationImage.append(images2)


        except Exception as e:
            print(e)

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

            # ----------------------- Don't change anything here --------------
        unique = str(PlanNumber) + str(SubdivisionNumber)   # < -------- Changes here
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
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = Description
        item['ElevationImage'] = "|".join(ElevationImage)
        item['PlanWebsite'] = PlanWebsite
        yield item

    # --------------------------------------------------------------------- #


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl cmcconstruct'.split())