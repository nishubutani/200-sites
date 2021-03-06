# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class createHomesSpide1r(scrapy.Spider):
    name = 'ncmodulars'
    allowed_domains = []
    start_urls = ['http://www.ncmodulars.com']
    builderNumber = "52975"

    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

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
        item['Street1'] = '3300 Jefferson Davis Hwy'
        item['City'] = 'Sanford'
        item['State'] = 'NC'
        item['ZIP'] = '27332'
        item['AreaCode'] = '772'
        item['Prefix'] = '248'
        item['Suffix'] = '4663'
        item['Extension'] = ""
        item['Email'] = 'info@homecretehomes.com'
        item['SubDescription'] = 'Homes by Vanderbuilt is a licensed general contractor in North Carolina, South Carolina and Virginia.  We have been in the modular housing business since 1984 and are privileged to have served thousands of satisfied homeowners.  We look forward to welcoming you into the Homes by Vanderbuilt family.'
        item['SubImage'] = 'https://ncmodulars.com/Content/HomeImages/large/83_render_prim.jpg|https://ncmodulars.com/Content/HomeImages/large/2159_render_prim.jpg|https://ncmodulars.com/Content/HomeImages/large/4174_render_prim_1588263232.jpg|https://ncmodulars.com/Content/HomeImages/large/4179_render_prim_1592862085.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item


        link = 'https://ncmodulars.com/Plans/Default'
        yield scrapy.Request(url=link, callback=self.parse3,dont_filter=True)

    def parse3(self, response):

        links = response.xpath('//p[@class="searchResultsplanName"]/a/@href').extract()
        for link in links:
            link = 'https://ncmodulars.com/' + link
            yield scrapy.FormRequest(url=link, callback=self.parse4, dont_filter=True)

    def parse4(self, response):

        try:
            PlanName = response.xpath('//h5[@class="card-title"]/span/text()').extract_first('')
        except Exception as e:
            print("PlanName: ", e)

        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = self.builderNumber
            print(SubdivisionNumber)
        except Exception as e:
            print(str(e))

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
            print(str(e))

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

        try:
            Bedroo = response.xpath('//*[contains(text(),"Bed")]/following-sibling::span/text()').extract_first('').replace("\n", "").strip()
            Bedrooms = re.findall(r"(\d+)", Bedroo)[0]
        except Exception as e:
            Bedrooms = 0
            print("Bedrooms: ", e)

        try:
            Bathroo = response.xpath('//*[contains(text(),"Bath")]/following-sibling::span/text()').extract_first('').strip().replace("\n","").strip()
            tmp = re.findall(r"(\d+)", Bathroo)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0

        except Exception as e:
            Baths = 0
            print("Baths: ", e)

        try:
            # desc = "".join(response.xpath('//div[@class="centered_content"]/div/div/text()').extract()).replace("\n","").strip()
            desc = ''
            # print(desc)
        except Exception as e:
            print(e)
            desc = ''

        try:
            # Garage = response.xpath('//*[contains(text(),"Garag")]/text()').extract_first('').strip().replace(',', '')
            # Garage = re.findall(r"(\d+)", Garage)[0]
            Garage = 0
        except Exception as e:
            print("Garage: ", e)
            Garage = 0

        try:
            BaseSqft = response.xpath('//*[contains(text(),"Finished")]/following-sibling::span/text()').extract_first('').strip().replace(',','')
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
        except Exception as e:
            print("BaseSQFT: ", e)

        try:
            ElevationImages = []
            ElevationImage2 = response.xpath("//img[contains(@src,'.jpg')]/@src").extract()[:2]
            if ElevationImage2 != []:
                for image in ElevationImage2:
                    image = 'https://ncmodulars.com/' + image
                    ElevationImages.append(image)
                # ElevationImages.append(ElevationImage1)

            ElevationImage = "|".join(ElevationImages)

        except Exception as e:
            print(str(e))
            ElevationImage = ""

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
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = desc
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl ncmodulars".split())