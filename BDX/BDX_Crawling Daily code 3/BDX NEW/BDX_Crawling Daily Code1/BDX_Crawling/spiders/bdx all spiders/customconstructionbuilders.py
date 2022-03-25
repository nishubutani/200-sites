

# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class vtshomeshomesSpider(scrapy.Spider):
    name = 'customconstructionbuilders'
    allowed_domains = []
    start_urls = ['https://www.customconstructionbuilders.com/the-gallery/']

    builderNumber = "53085"

    def parse(self, response):
        print('--------------------')

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        imagess = []
        images = response.xpath('//div[@class="grid-gallery__items-container"]/div//picture/source[1]/@data-srcset').extract()
        for imag in images:
            print(imag)
            imag = imag.split(",")[-1].strip()
            print(imag)
            imag = imag.split(" ")[0]
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
        item['Street1'] = '2809 Birchwood Pass'
        item['City'] = 'Cross Plains'
        item['State'] = 'WI'
        item['ZIP'] = '53528'
        item['AreaCode'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Prefix'] = ""
        item['Email'] = ''
        item['SubDescription'] = "To succeed for more than 30 years as a company, it helps to have a clear vision of what you stand for. Back in 1989 our founder, Jamie Zajicek, gave us just that when he created Custom Construction Builders, Inc. We know that your home is all about you and your families lifestyle, and we honor that by making sure your new home meets your every expectation. We are especially pleased by the number of our homeowners who have come back to us to build their second or third Custom Construction Builders home, an honor that they are confident in us. We bring you the new generation of Custom Home Building, with high-quality construction and craftsmanship."
        item['SubImage'] = imagess
        item['SubWebsite'] = 'https://www.customconstructionbuilders.com/'
        item['AmenityType'] = ''
        yield item

        link = 'https://www.customconstructionbuilders.com/featured-homes/'
        yield scrapy.FormRequest(url=link,callback=self.parse,dont_filter=True)

    def plan(self, response):
        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        divs = response.xpath('//div[@class="alternatable-property-info"]/div')
        for div in divs:

            try:
                price = div.xpath('.//div/div[2]/h3/text()').extract_first('')
                price = price.replace(",", "")
                price = re.findall(r"(\d+)", price)[0]
            except Exception as e:
                price = 0

            try:
                PlanName = div.xpath('.//h4/text()').get()
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

                sqft = div.xpath(".//span[contains(text(),'SQ. FT')]/../span/text()").extract_first('')
                # sqft = sqft.split("|")[0]
                sqft = sqft.replace(',', '').strip()
                if '.' in sqft:
                    sqft = sqft.split(".")[0]
                BaseSqft = re.findall(r"(\d+)", sqft)[0]

            except Exception as e:
                print(e)
                BaseSqft = ''

            try:
                bath = div.xpath(".//span[contains(text(),'BATHS')]/../span/text()").extract_first()
                if 'or' in bath:
                    bath = bath.split("or")[1]
                tmp = re.findall(r"(\d+)", bath)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                print(e)

            try:

                Bedrooms = div.xpath(".//span[contains(text(),'BEDS')]/../span/text()").extract_first('')
                if 'or' in Bedrooms:
                    Bedrooms = Bedrooms.split("or")[1]
                # Bedrooms = Bedrooms.split("|")[1].split("|")[0]
                Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            except Exception as e:
                print(e)

            try:
                Garage = div.xpath(".//span[contains(text(),'GARAGE')]/../span/text()").extract_first('')

                Garage = re.findall(r"(\d+)", Garage)[0]
            except Exception as e:
                print(e)
                Garage = 0

            try:
                # Description = 'BMI Construction is owned and operated by Brian Intravia. Brian grew up in the Covington area and learned the construction industry at a young age from his father, who is a longtime builder/developer in St. Tammany Parish. After graduating from St. Paul’s High School, he attended Louisiana State University where he received a BS in Civil Engineering. BMI Construction has been building homes in St. Tammany for 18 years. Brian uses his experience and a hands on approach to ensure each client’s new home is everything they expect and more.'
                Description = ''
            except Exception as e:
                print(e)
                Description = ''

            try:

                images1 = div.xpath('.//a[1]/@href').extract()
                images = []
                for id in images1:
                    images.append(id)
                ElevationImage = images

            except Exception as e:
                print(e)

            try:
                PlanWebsite = response.url
            except Exception as e:
                print(e)

                # ----------------------- Don't change anything here --------------
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
            item['BasePrice'] = price
            item['BaseSqft'] = BaseSqft
            item['Baths'] = Baths
            item['HalfBaths'] = HalfBaths
            item['Bedrooms'] = Bedrooms
            item['Garage'] = Garage
            item['Description'] = Description
            item['ElevationImage'] = "|".join(ElevationImage)
            item['PlanWebsite'] = PlanWebsite
            yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl customconstructionbuilders".split())