
# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'trademarkhomesllc'
    allowed_domains = ['http://trademarkhomesllc.com//']
    start_urls = ['http://trademarkhomesllc.com/']

    builderNumber = "50820"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()


        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = self.builderNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '189 Fort Wayne Ave'
        item['City'] = 'Richmond'
        item['State'] = 'IN'
        item['ZIP'] = '47374'
        item['AreaCode'] = ''
        item['Prefix'] =''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = 'We are your premiere Eastern Indiana and Western Ohio home builder for over 25 years. We are here to show you how we can create a custom home to fit your lifestyle. Building your dream home with quality craftsmanship and superb attention to detail is why we are the choice builder in the area.'
        item['SubImage'] = "https://isteam.wsimg.com/ip/45a6e1e8-74aa-4af4-9673-f6c7bbc4730e/75278318_2545661665555081_4281401122104541184_.jpg|https://img1.wsimg.com/isteam/ip/45a6e1e8-74aa-4af4-9673-f6c7bbc4730e/81472367_2663687203752526_5775726115326787584_.jpg/:/rs=w:600,cg:true,m|https://img1.wsimg.com/isteam/ip/45a6e1e8-74aa-4af4-9673-f6c7bbc4730e/75278318_2545661665555081_4281401122104541184_.jpg/:/rs=w:600,cg:true,m"
        item['SubWebsite'] = 'https://trademarkhomesllc.com/'
        item['AmenityType'] = ''
        yield item

        link = 'https://trademarkhomesllc.com/homes-for-sale'
        yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)

    def parse2(self,response):
        divs = response.xpath('//div[@class="widget widget-content widget-content-content-7"]')
        print(len(divs))
        for div in divs:
            try:
                PlanName = div.xpath('.//h2/span/text()').extract_first()
                print(PlanName)
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
                Bedroo = div.xpath('.//*[contains(text(),"Bedroom")]/text()').extract_first().strip()
                print(Bedroo)
                Bedroom = Bedroo.split(',')[0]
                Bedrooms = re.findall(r"(\d+)", Bedroom)[0]
                # Bedrooms = Bedroom.split(' Bed')[0].strip()

            except Exception as e:
                Bedrooms = 0
                print("Bedrooms: ", e)

            try:
                Bathroo = div.xpath('.//*[contains(text(),"Bath")]/text()').extract_first().strip()
                # Baths = Bathroo.split(',')[1]
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
                Garage = div.xpath('.//*[contains(text(),"Car Garage")]/text()').extract_first().strip().replace(',', '')
                Garage = re.findall(r"(\d+)", Garage)[0]
            except Exception as e:
                print(e)
                Garage =0.0
            try:
                BaseSqft = div.xpath('.//*[contains(text(),"sq ft")]/text()').extract_first().strip().replace(',', '')
                BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
            except Exception as e:
                print("BaseSQFT: ", e)

            try:
                ElevationImages = []
                ElevationImage11 = div.xpath('.//source/@data-srcsetlazy').extract()
                # ElevationImage2 = div.xpath('.//source/@data-srcsetlazy').extract_first('')
                if ElevationImage11 != []:
                    for ElevationImage1 in ElevationImage11:
                        ElevationImage1 = ElevationImage1.split(",")[0].split("//")[1]
                        ElevationImage1 = ElevationImage1.split("/:")[0]
                        ElevationImage1 = "https://" + ElevationImage1

                        ElevationImages.append(ElevationImage1)
                # if ElevationImage2 != '':
                #     ElevationImage2 = ElevationImage2.split(",")[0].split("//")[1]
                #     ElevationImages.append(ElevationImage2)

                ElevationImage = "".join(ElevationImages)

            except Exception as e:
                print(str(e))

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
            item['Description'] = ''
            item['ElevationImage'] = ElevationImage
            item['PlanWebsite'] = PlanWebsite
            yield item


    # --------------------------------------------------------------------- #


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl trademarkhomesllc'.split())