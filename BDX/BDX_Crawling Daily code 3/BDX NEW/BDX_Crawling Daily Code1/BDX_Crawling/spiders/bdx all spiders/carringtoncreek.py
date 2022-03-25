

# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'carringtoncreek'
    allowed_domains = ['https://www.carringtoncreek.com/']
    start_urls = ['https://www.carringtoncreek.com/']

    builderNumber = "33908"

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
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = 'PO Box 10176'
        item['City'] = 'Fort Smith'
        item['State'] = 'AR'
        item['ZIP'] = '72719'
        item['AreaCode'] = '479'
        item['Prefix'] ='459'
        item['Suffix'] = '6200'
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = 'Founded in 2003, Carrington Creek Homes is a full-service design and build firm, overseeing custom home projects from concept to completion throughout Northwest Arkansas and the River Valley. Our philosophy for home building is centered around experiencing excellence. We believe building a home is one of the most important decisions our clients will ever make – therefore, we strive to tailor each project specific to our client’s vision. Throughout our process, we take pride in providing what matters most: first class design options, quality craftsmanship, and a lasting partnership with a builder you can trust.'
        item['SubImage'] = 'https://images.squarespace-cdn.com/content/v1/5a12f85abff200f859bd1eaa/1516903415400-3QJMLHAASFLKBMLS5KL3/CCHsquarespace-18.jpg?format=2500w|https://images.squarespace-cdn.com/content/v1/5a12f85abff200f859bd1eaa/1517514640380-VH1Q5M4RMCH7GSYV3KWT/CCHsquarespace-22.jpg?format=2500w|https://images.squarespace-cdn.com/content/v1/5a12f85abff200f859bd1eaa/1523397978548-9OSDEHG5UK9P0S625ZBM/CCHInsta-403.jpg?format=750w|https://images.squarespace-cdn.com/content/v1/5a12f85abff200f859bd1eaa/1636041014990-LEWTYBC0L90TRAOM0MT0/image-asset.jpeg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'https://www.carringtoncreek.com/homes'
        yield scrapy.FormRequest(url=link,callback=self.parse3,dont_filter=True)


    def parse3(self, response):
        divs = response.xpath('//div[@class="col sqs-col-4 span-4"]')
        for div in divs:

            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                PlanName = div.xpath('.//h3/text()').get()
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
                Description = "".join(div.xpath('.//text()').extract())
                Description = Description.replace("\n","").strip()
            except Exception as e:
                print(e)
                Description = ''


            try:
                try:
                    sqft = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*sq. ft", Description.lower())[0]
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

                bath = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*bath", Description.lower())[0]
                tmp = re.findall(r"(\d+)", bath)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                print(e)

            try:
                Bedrooms = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*bed", Description.lower())[0]
                Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            except Exception as e:
                print(e)

            try:

                Garage = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*car garage", Description.lower())[0]
                Garage = Garage.replace("three", "3").replace("four", "4").replace("two", "2")
                Garage = re.findall(r"(\d+)", Garage)[0]

            except Exception as e:
                print(e)
                Garage = 0



            try:

                images1 = div.xpath('.//img/@data-src').extract()

                images2 = response.xpath('.//a/@href').extract_first('')
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
            item['BasePrice'] = '0'
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
    execute('scrapy crawl carringtoncreek'.split())