
# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class vtshomeshomesSpider(scrapy.Spider):
    name = 'firettibuilders'
    allowed_domains = []
    start_urls = ['https://firettibuilders.com/gallery/']

    builderNumber = "24906"

    def parse(self, response):
        print('--------------------')

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        imagess = []
        images = response.xpath('//div[@class="pp-photo-gallery-content"]/a/@href').extract()
        for imag in images:
            print(imag)
            imagess.append(imag)
        imagess = "|".join(imagess)
        print(imagess)


        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = '51152'
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '4705 Southport Supply Rd'
        item['City'] = 'Southport'
        item['State'] = 'NC'
        item['ZIP'] = '28461'
        item['AreaCode'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Prefix'] = ""
        item['Email'] = ''
        item['SubDescription'] = "Firetti Builders, Inc. stresses the highest levels of quality, workmanship, and service in each home we build. Since 1977, our designs, expertise, and experience have combined to create the very best. At Firetti Builders, Inc., we are committed to building distinctive, energy-efficient homes that highlight innovative floor plans and unique features. We take pride in our fine-quality craftsmanship, while offering exceptional value"
        item['SubImage'] = imagess
        item['SubWebsite'] = 'https://firettibuilders.com/'
        item['AmenityType'] = ''
        yield item

        link = 'https://firettibuilders.com/featured-plans/'
        yield scrapy.Request(url=link, callback=self.parse2)

    def parse2(self, response):

        divs = response.xpath('//div[@class="fl-row-content-wrap"]//h2')
        for div in divs:

            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                PlanName = div.xpath('.//span/text()').extract_first(
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
                Baths = div.xpath(".//../../../../..//*[contains(text(),'Bath')]/../text()").extract_first(
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
                Bedrooms = div.xpath(".//../../../../..//*[contains(text(),'Bed')]/../text()").extract_first(
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
                BaseSqft = div.xpath(".//../../../../..//*[contains(text(),'Square')]/../text()").extract_first(
                    default='0').strip().replace(",", "")
                if '-' in BaseSqft:
                    BaseSqft = BaseSqft.split("-")[1]
                BaseSqft = BaseSqft.split(" ")[0]
                print(BaseSqft)

            except Exception as e:
                print(e)

            try:
                Description = "".join(div.xpath('.//../../../..//div[@class="pp-sub-heading"]/p/text()').extract())
                # Description = ''
                print(Description)
            except Exception as e:
                Description = ''

            try:
                images = []

                image2 = div.xpath('.//../../../../../../..//div[@class="pp-album-gallery"]/a/@href').extract()
                if image2 != []:
                    for im in image2:
                        images.append(im)

                ElevationImage = "|".join(images)
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
    execute("scrapy crawl firettibuilders".split())