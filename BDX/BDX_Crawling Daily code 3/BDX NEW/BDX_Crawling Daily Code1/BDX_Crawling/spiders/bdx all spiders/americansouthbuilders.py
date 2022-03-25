


# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'americansouthbuilders'
    allowed_domains = ['https://blvdhomes.com/']
    start_urls = ['https://blvdhomes.com/']

    builderNumber = "62714"

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
        item['Street1'] = '161 Maple'
        item['City'] = 'Eunice'
        item['State'] = 'LA'
        item['ZIP'] = '70535'
        item['AreaCode'] = '337'
        item['Prefix'] ='546'
        item['Suffix'] = '6322'
        item['Extension'] = ""
        item['Email'] = 'americansouthbuildersllc@yahoo.com'
        item['SubDescription'] = 'American South Builders, LLC was established in March 2004 by the Shane Frey Family.  The Frey family has been established in business in Louisiana since 1988.  American South Builders is a residential design, building contractor and a member of the Better Business Bureau and Acadian Home Builders Association. '
        item['SubImage'] = 'http://www.americansouthbuilders.com/images/header.gif'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'http://www.americansouthbuilders.com/houses-floor-plans/'
        yield scrapy.FormRequest(url=link, callback=self.parse3, dont_filter=True)


    def parse3(self, response):

        divs = response.xpath('//div[@class="floorplanblock"]')
        for div in divs:

            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                PlanName = div.xpath('.//p/text()[3]').get('').strip()
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


            BasePrice = 0

            try:
                sqft = div.xpath(".//p/text()[3]").extract_first('')
                sqft = sqft.replace(',', '').replace(".","").strip()
                BaseSqft = re.findall(r"(\d+)", sqft)[0]

            except Exception as e:
                print(e)
                BaseSqft = ''

            try:
                bath = div.xpath(".//p/text()[1]").extract_first('')
                bath = bath.split("/")[1]
                if '-' in bath:
                    bath = bath.split("-")[1]
                tmp = re.findall(r"(\d+)", bath)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                print(e)

            try:
                Bedrooms = div.xpath(".//p/text()[1]").extract_first('')
                Bedrooms = Bedrooms.split("/")[0]
                if '-' in Bedrooms:
                    Bedrooms = Bedrooms.split("-")[1]
                # Bedrooms = Bedrooms.split("|")[1].split("|")[0]
                Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            except Exception as e:
                print(e)
                Bedrooms = ''

            Garage = 0



            try:
                # Description = 'American South Builders, LLC was established in March 2004 by the Shane Frey Family.  The Frey family has been established in business in Louisiana since 1988.  American South Builders is a residential design, building contractor and a member of the Better Business Bureau and Acadian Home Builders Association. '
                Description = ''
            except Exception as e:
                print(e)


            try:

                # images1 = response.xpath('//li[@class="dmCoverImgContainer"]/img/@src').extract()
                #
                # images2 = response.xpath('//div[@class="u_1929991324 imageWidget align-center"]/a/img/@src').extract_first('')
                images = []
                # imagedata = div.xpath('.//p/a/img/@src').extract()
                imagedata = div.xpath('.//p/a/@href').extract()
                for id in imagedata:
                    id = 'http://www.americansouthbuilders.com/houses-floor-plans/' + id
                    images.append(id)
                ElevationImage = images
                print(ElevationImage)
            except Exception as e:
                print(e)

            try:
                PlanWebsite = response.url
            except Exception as e:
                print(e)

            try:
                PlanNumber = int(hashlib.md5(bytes(PlanName + response.url , "utf8")).hexdigest(), 16) % (
                        10 ** 30)
            except Exception as e:
                PlanNumber = ''
                print(e)

                # ----------------------- Don't change anything here --------------
            unique = str(PlanNumber) + str(SubdivisionNumber) + str(Baths) + str(Bedrooms) #< -------- Changes here
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
            item['ElevationImage'] = "|".join(ElevationImage)
            item['PlanWebsite'] = PlanWebsite
            yield item



    # --------------------------------------------------------------------- #


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl americansouthbuilders'.split())