
# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class vtshomeshomesSpider(scrapy.Spider):
    name = 'yourgeminihomes'
    allowed_domains = []
    start_urls = ['http://www.yourgeminihomes.com/']

    builderNumber = "25992"

    def parse(self, response):
        print('--------------------')

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        # imagess = []
        # images = response.xpath('//a[@class="x-div portfolio-item-link"]/div/div/@data-bg').extract()
        # for imag in images:
        #     print(imag)
        #     imagess.append(imag)
        # imagess = "|".join(imagess)
        # print(imagess)


        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = '26148'
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '1685 Pleasant Hill Rd'
        item['City'] = 'Bowling Green'
        item['State'] = 'KY'
        item['ZIP'] = '42103'
        item['AreaCode'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Prefix'] = ""
        item['Email'] = ''
        item['SubDescription'] = "Gemini Homes is a custom home builder located in Bowling Green, KY. We specialize in building quality homes that fulfill your exact specifications. In addition to custom home design, we also offer:"
        item['SubImage'] = 'http://www.yourgeminihomes.com/imagerotation/image3.jpg|http://www.yourgeminihomes.com/imagerotation/image4.jpg|http://www.yourgeminihomes.com/imagerotation/image5.jpg|http://www.yourgeminihomes.com/imagerotation/image1.jpg'
        item['SubWebsite'] = 'http://www.yourgeminihomes.com/'
        item['AmenityType'] = ''
        yield item

        link = 'http://www.yourgeminihomes.com/2_Story_House_Plans_Bowling_Green_KY.php'
        yield scrapy.Request(url=link, callback=self.parse2)

    def parse2(self, response):

        divs = response.xpath('//div[@align="left"]/table/tbody')
        for div in divs:

            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                PlanName = div.xpath('.//tr/td/h2/text()').extract_first(
                    default='').strip()
                print(PlanName)
            except Exception as e:
                print(e)

            try:
                PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
                print(PlanName)
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
                Baths = div.xpath(".//tr/td//li[contains(text(),'Bath')]/text()").extract_first(
                    default='0').strip().replace(",", "")
                if '-' in Baths:
                    Baths = Baths.split("-")[1].strip()
                Baths = Baths.split(" ")[0]
                Baths = re.findall(r"(\d+)", Baths)
                Bath = Baths[0]
                print(Baths)
                if len(Baths) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                print(e)

            try:
                Bedrooms = div.xpath(".//tr/td//li[contains(text(),'Bed')]/text()").extract_first(
                    default='0').strip().replace(",", "")
                if '-' in Bedrooms:
                    Bedrooms = Bedrooms.split("-")[1].strip()
                Bedrooms = Bedrooms.split(" ")[0]
                print(Bedrooms)
            except Exception as e:
                print(e)

            try:
                Garage = 0.0
            except Exception as e:
                print(e)
                Garage = 0.0

            try:
                BaseSqft = div.xpath(".//tr/td//li[contains(text(),'sq.')]/text()").extract_first(
                    default='0').strip().replace(",", "")
                if '-' in BaseSqft:
                    BaseSqft = BaseSqft.split("-")[1]
                BaseSqft = BaseSqft.split(" ")[0]
                print(BaseSqft)

            except Exception as e:
                print(e)

            try:
                Description = "".join(div.xpath('.//tr//div[@align="left"]/p/text()').extract())
                # Description = ''
                print(Description)
            except Exception as e:
                Description = ''

            try:
                # images = []
                #
                # image2 = div.xpath('.//../../../../../../..//div[@class="pp-album-gallery"]/a/@href').extract()
                # if image2 != []:
                #     for im in image2:
                #         images.append(im)
                #
                # ElevationImage = "|".join(images)

                ElevationImage = ''
                print(ElevationImage)
            except Exception as e:
                print(e)
                ElevationImage = ''

            try:
                PlanWebsite = response.url
            except Exception as e:
                print(e)

                # SubdivisionNumber = SubdivisionNumber #if subdivision is there
            SubdivisionNumber = self.builderNumber  # if subdivision is not available
            unique = str(PlanName) + str(SubdivisionNumber)
            print(unique)
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

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
            item['Baths'] = Bath
            item['HalfBaths'] = HalfBaths
            item['Bedrooms'] = Bedrooms
            item['Garage'] = Garage
            item['Description'] = Description
            item['ElevationImage'] = ElevationImage
            item['PlanWebsite'] = PlanWebsite
            yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl yourgeminihomes".split())