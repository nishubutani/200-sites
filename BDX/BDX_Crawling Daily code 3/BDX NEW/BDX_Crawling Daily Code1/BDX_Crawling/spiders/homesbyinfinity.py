
# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'homesbyinfinity'
    allowed_domains = ['http://www.homesbyinfinity.com/']
    start_urls = ['http://www.homesbyinfinity.com/']

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
        item['Street1'] = '5208 Highway 90 West'
        item['City'] = 'Mobile'
        item['State'] = 'AL'
        item['ZIP'] = '36619'
        item['AreaCode'] = '251'
        item['Prefix'] ='665'
        item['Suffix'] = '0021'
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = 'With Infinity Homes, you’ll have the opportunity to choose from a wide range of floor plans designed with the easy Southern lifestyle in mind. Want to add a special touch of your own? No problem! Our professional draftsman are ready to accommodate your requests with adjustments that make your home uniquely yours. Our goal is always your satisfaction. That’s why all Infinity Homes are built with the finest materials and craftsmanship.'
        item['SubImage'] = 'http://www.homesbyinfinity.com/Portals/infinityhomes/Gallery/Album/110/DSC00037.JPG|http://www.homesbyinfinity.com/Portals/infinityhomes/Gallery/Album/110/DSC00070.JPG|http://www.homesbyinfinity.com/Portals/infinityhomes/Gallery/Album/110/DSC00093.JPG'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'http://www.homesbyinfinity.com/Floor-Plans'
        yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)

    def parse2(self, response):
        links = response.xpath('//td[@class="album-item"]/div/a/@href').extract()
        for link in links:
            yield scrapy.FormRequest(url=link, callback=self.parse3, dont_filter=True)
            # yield scrapy.FormRequest(url='https://buildimmaculate.com/the-magnolia/', callback=self.parse3, dont_filter=True)

    def parse3(self, response):
        divs = response.xpath('//td[@align="center"]/div[@class="gallerybox4"]')[1:]
        for div in divs:

            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                PlanName = div.xpath('.//following-sibling::span[@class="Normal"]/b/text()').get()
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
                Description = "".join(div.xpath('.//following-sibling::span[@class="Normal"]/following-sibling::div/text()').extract())
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
                Bedrooms = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*bedroom", Description.lower())[0]
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

                images1 = response.xpath('//div[@class="img-inner dark"]/img/@data-src').extract()

                images2 = response.xpath('.//a/@href').extract_first('')
                if ',' in images2:
                    images2 = images2.split(",")[0]
                    print(images2)

                images3 = response.xpath('//div[@class="img-inner image-cover dark"]/img/@data-srcset').extract_first('')
                if ',' in images3:
                    images3 = images3.split(",")[0]
                    if ' ' in images3:
                        images3 = images3.split(" ")[0]
                    print(images3)
                else:
                    images3 = images3


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
    execute('scrapy crawl homesbyinfinity'.split())