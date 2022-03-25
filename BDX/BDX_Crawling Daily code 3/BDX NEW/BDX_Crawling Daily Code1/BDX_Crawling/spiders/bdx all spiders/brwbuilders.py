# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class brwbuilders(scrapy.Spider):
    name = 'brwbuilders'
    allowed_domains = ['https://brwbuilders.com/']
    start_urls = ['https://brwbuilders.com/']
    builderNumber = "63679"

    def parse(self, response):


        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        # images = ''
        # image = response.xpath('//div[@class="gallery-reel-item-src"]/img/@data-src').extract()
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
        item['Street1'] = '130 South Geronimo Street'
        item['City'] = 'Destin'
        item['State'] = 'FL'
        item['ZIP'] = '32550'
        item['AreaCode'] = '850'
        item['Prefix'] ='837'
        item['Suffix'] = '4413'
        item['Extension'] = ""
        item['Email'] = 'athomason@brwbuilders.com'
        item['SubDescription'] = 'BRW Builders of Destin, Inc. wants to help you realize your own personal American Dream by building you the home you’ve always wanted. Our construction company in Destin, FL, has been building custom homes for over three decades. From single homes to site developments, we have a reputation for both quality and craftsmanship. Our attention to detail and superior workmanship ensure every project we complete will be a source of pride and enjoyment for its owner.'
        item['SubImage'] = 'http://brwbuilders.com/wp-content/uploads/billboard-our-work.jpg|https://brwbuilders.com/wp-content/uploads/1Lot39Retreat.jpg|https://brwbuilders.com/wp-content/uploads/14Lot31CeruleanLanding.2.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'https://brwbuilders.com/gallery/'
        yield scrapy.FormRequest(url=link,callback=self.parse3,dont_filter=True)

    def parse3(self, response):

        divs = response.xpath('//p')
        for div in divs:

            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                PlanName = div.xpath('.//text()[2]').get().strip()
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
                sqft = div.xpath(".//text()[5]").extract_first('')
                sqft = sqft.split("square foot")[0]
                sqft = sqft.replace(",", "")
                BaseSqft = re.findall(r"(\d+)", sqft)[0]

            except Exception as e:
                print(e)
                BaseSqft = ''

            try:

                bath = div.xpath(".//text()[5]").extract_first('')
                if 'bathroom' in bath:
                    bath = bath.split("bathroom")[0].strip().replace("full","4")

                else:
                    bath = bath.split("baths")[0].strip().replace("full","4")
                # bath = bath.split()[-1]
                if PlanName == "Lot 1, Blk 3, Blue Mountain Beach":
                    bath = bath.split()[-1].replace("full", "4")
                elif PlanName == 'Lot 122, Avalon Beach Estates':
                    bath = bath.split()[-1].replace("full", "4")
                elif PlanName == 'Lot 19, Blk F, Kelly Plantation':
                    bath = bath.split()[-1].replace("full", "4")
                elif PlanName == 'Lot 2, Blk 6, Dalton Drive':
                    bath = bath.split(",")[-1].replace("full", "4")
                else:
                    bath = bath.split("and")[-1].replace("full","4")
                # else:
                #     bath = bath.split()[-1].replace("full", "4")
                # bath = bath.split("/")[1].split("/")[0].strip()
                tmp = re.findall(r"(\d+)", bath)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                    tempd = div.xpath(".//text()[5]").extract_first('')
                    if 'half baths' in  tempd:
                        HalfBaths = 2
                else:
                    HalfBaths = 0
                    tempd = div.xpath(".//text()[5]").extract_first('')
                    if 'half baths' in tempd:
                        HalfBaths = 2
            except Exception as e:
                print(e)
                bath,HalfBaths='',''

            try:
                Bedrooms = div.xpath(".//text()[5]").extract_first('')
                Bedrooms = Bedrooms.split("bedroom")[0].strip()
                Bedrooms = Bedrooms.split()[-1].replace("four","4")
                Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            except Exception as e:
                print(e)

            try:
                price = response.xpath('//span[contains(text(),"$")]/text()').extract_first('')
                price = price.replace(",", "")
                price = re.findall(r"(\d+)", price)[0]

            except Exception as e:
                print(e)
                price = '0'

            try:
                BasePrice = price
            except Exception as e:
                print(e)

            try:
                Garage = div.xpath(".//text()[5]").extract_first('')
                Garage = Garage.split("car garage")[0]
                Garage = Garage.split()[-1]
                print(Garage)
                Garage = re.findall(r"(\d+)", Garage)[0]
            except Exception as e:
                print(e)
                Garage = 0

            try:

                desc = div.xpath(".//text()[5]").extract_first('')
                Description = desc
            except Exception as e:
                print(e)

            try:
                # img1 = response.xpath('.//following-sibling::div/dl/dt/a/@href').extract_first('')
                images = []
                imagediv = div.xpath('.//following-sibling::div')
                for i in imagediv[0:1]:
                    imagedata = i.xpath('.//dl/dt/a/@href').extract()
                    for id in imagedata:
                        id = id
                        images.append(id)
                    # if img1  != '':
                    #     images.append(img1)
                    ElevationImage = "|".join(images)
                    ElevationImage = ElevationImage
            except Exception as e:
                print(e)
                ''

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
            item['Description'] = Description
            item['ElevationImage'] = ElevationImage
            item['PlanWebsite'] = PlanWebsite
            yield item
        # --------------------------------------------------------------------- #


        # --------------------------------------------------------------------- #

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl brwbuilders'.split())
