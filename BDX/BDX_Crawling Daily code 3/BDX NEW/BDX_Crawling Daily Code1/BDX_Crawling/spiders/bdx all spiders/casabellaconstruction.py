# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
import requests
from scrapy.http import HtmlResponse
class casabellaconstructionSpider(scrapy.Spider):
    name = 'casabellaconstruction'
    allowed_domains = ['casabellaconstruction.com']
    start_urls = ['https://casabellaconstruction.com/']

    builderNumber = "529443120563621281917374561655"

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
        item['Street1'] = "10502 N Ambassador Dr Ste 230"
        item['City'] = "Kansas City"
        item['State'] = "MO"
        item['ZIP'] = "64153"
        item['AreaCode'] = "816"
        item['Prefix'] = "436"
        item['Suffix'] = "9969"
        item['Extension'] = ""
        item['Email'] = "amberjury@yahoo.com"
        item['SubDescription'] = "Casa Bella Construction has earned a reputation as one of the Kansas City metro area’s premier custom home builders. They are consistent winners of the Home Builder’s Associations’ American Dream Grand Award, Pick of the Parade, and Distinctive Design and Plan contests. They have also won many Kansas City Home and Gardens and Kansas City at Home publications’ Model of the Year Awards."
        item['SubImage'] = ""
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item


        url = 'https://casabellaconstruction.com/home-plans/'
        yield scrapy.Request(url=url, callback=self.plan_links)

    def plan_links(self,response):
        links = response.xpath('//a[@class="fill"]/@href').extract()
        for link in links:
            print(link)
            yield scrapy.FormRequest(url=link,callback=self.plans_detail,dont_filter=True)
            
        # ------------------------------------------- Extract Homedetails ------------------------------ #

    def plans_detail(self, response):


        PlanName = response.xpath('//h1/text()').extract_first()
        BaseSqft = 0

        try:
            basefeet = ''.join(response.xpath('./div/div/div/div/p/text()').extract())
        except Exception as e:
            basefeet=''

        try:
            Baths_temp = response.xpath('//p[@class="lead"]/text()[2]').extract_first('')
            print(Baths_temp)
            if '–' in Baths_temp:
                Baths_temp = Baths_temp.split("–")[-1]
                print(Baths_temp)
            if '.' in Baths_temp:
                Baths_temp = Baths_temp.split(".")[0]
                HalfBaths = 1
                print(Baths_temp)

        except Exception as e:
            print(e)


        try:
            Bedrooms = response.xpath('//p[@class="lead"]/text()[2]').extract_first('')
            if '–' in Bedrooms:
                Bedrooms = Bedrooms.split("-")[-1]
        except Exception as e:
            Bedrooms = 0

        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        # try:
        #     SubdivisionNumber = response.meta['sbdn']
        # except Exception as e:
        #     print(e)

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
            # print(BasePrice)
            # BasePrice = re.findall(r"(\d+)", BasePrice)[0]
        except Exception as e:
            print(e)

        try:
            Garage = 0
        except Exception as e:
            print(e)

        try:
            Description = ''
        except Exception as e:
            print(str(e))

        try:
            ElevationImage = response.xpath('./div/div/div/div//img/@src').extract()

            if ElevationImage != []:
                ElevationImage = "|".join(ElevationImage)
            else:
                ElevationImage = ''


            while ElevationImage.startswith('|'):
                ElevationImage = ElevationImage[1:]
            while ElevationImage.endswith('|'):
                ElevationImage = ElevationImage[:-1]

        except Exception as e:
            print(e)

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

        if Baths == '':
            Baths = 0

        # ----------------------- Don't change anything here --------------

        unique = str(PlanNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['Type'] = Type
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number  # < -------- Changes here
        item['PlanName'] = PlanName

        item['SubdivisionNumber'] = self.builderNumber

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

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl casabellaconstruction".split())