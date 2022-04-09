# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from scrapy.http import HtmlResponse

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from lxml import html

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'homesbydeesign'
    allowed_domains = ['https://homesbydeesign.com/']
    start_urls = ['https://homesbydeesign.com/']

    builderNumber = "33174"

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
        item['Street1'] = '731 Mortar Street'
        item['City'] = 'Mascoutah'
        item['State'] = 'IL'
        item['ZIP'] = '62258'
        item['AreaCode'] = ''
        item['Prefix'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = 'HBD Homes is a true new custom home builder in the Metro East-St. Louis area. We have several developments located in and around Belleville, Caseyville, Columbia, Freeburg, O’Fallon, Mascoutah, Millstadt, Swansea, Shiloh, Smithton Illinois and throughout St. Clair County IL. We build new custom homes that range in price from $160,000.00 to $2.5 million. This is a large range to cover in our industry where price traditionally determines quality. This is where our company is so different. The quality of service, materials, and craftsmanship are of the highest in our region, and are found at all price points.'
        item['SubImage'] = "https://homesbydeesign.com/images/plans/the_kensington/kensington.jpg|https://homesbydeesign.com/images/plans/the_clifford/clifford01_1stfl_plan.jpg|https://homesbydeesign.com/images/gallery/the_clifford/clifford_08_82_thumb1000.jpg|https://homesbydeesign.com/images/plans/the_alyssa/alyssa01_1stfl_plan.jpg|https://homesbydeesign.com/images/plans/the_espresso/espresso.jpg"
        item['SubWebsite'] = 'https://www.davelargenthomes.com/'
        item['AmenityType'] = ''
        yield item


        link = 'https://homesbydeesign.com/plans.php'
        yield scrapy.FormRequest(url=link, callback=self.parse3, dont_filter=True)

    def parse3(self, response):

        links = response.xpath('//div[@class="row"]/h5/a/@href').extract()
        for link in links:
            link = 'https://homesbydeesign.com/' + link
            yield scrapy.FormRequest(url=link,callback=self.parse4,dont_filter=True)

    def parse4(self,response):

        try:
            PlanName = response.xpath('//h1/text()').extract_first('')
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
            Bedroo = response.xpath('//*[contains(text(),"Bed")]/../text()').extract_first('').replace("\n","").strip()
            Bedrooms = re.findall(r"(\d+)", Bedroo)[0]
        except Exception as e:
            Bedrooms = 0
            print("Bedrooms: ", e)

        try:
            Bathroo = response.xpath('//*[contains(text(),"Bath")]/../text()').extract_first('').strip().replace("\n","").strip()
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
            desc = "".join(response.xpath('//div[@class="centered_content"]/div/div/text()').extract()).replace("\n","").strip()
            print(desc)
        except Exception as e:
            print(e)
            desc = ''

        try:
            Garage = response.xpath('//*[contains(text(),"Garag")]/text()').extract_first('').strip().replace(',', '')
            Garage = re.findall(r"(\d+)", Garage)[0]
        except Exception as e:
            print("Garage: ", e)
            Garage = 0

        try:
            BaseSqft = response.xpath('//*[contains(text(),"Square")]/../text()').extract_first('').strip().replace(',', '')
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
        except Exception as e:
            print("BaseSQFT: ", e)


        try:
            ElevationImages = []
            ElevationImage2 = response.xpath('//a[@class="lightbox_item"]/@href').extract()
            if ElevationImage2 != []:
                for image in ElevationImage2:
                    image = 'https://homesbydeesign.com/' + image
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

    # ---------------------------------------------------------------------


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl homesbydeesign'.split())



