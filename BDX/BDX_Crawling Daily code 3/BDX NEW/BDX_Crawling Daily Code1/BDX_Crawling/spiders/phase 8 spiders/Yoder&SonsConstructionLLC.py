# -- coding: utf-8 --
import json
import scrapy
import requests
from scrapy.http import HtmlResponse
import hashlib
import re
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

bedroom_map = {"three bedroom": 3, "two bedroom": 2, "four bedroom": 4}
bathroom_map = {"Both bathroom": [2, 0], "two and a half baths": [2, 1],
                "three and a half baths": [3, 1], "two full baths": [2, 0],
                "two baths": [2, 0], "one bathroom": [1, 0], "two bath": [2, 0]}

class YoderAndSonsConstructionSpider(scrapy.Spider):
    name = 'Yoder_And_Sons_Construction'
    allowed_domains = []
    start_urls = ['https://yoderandsonsconstruction.com/services/custom-homes/']
    builderNumber = "22630"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        # f = open("html/%s.html" % self.builderNumber, "wb")
        # f.write(response.body)
        # f.close()

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = "10222 Woodyard Road"
        item['City'] = "Greenwood"
        item['State'] = "DE"
        item['ZIP'] = "19950"
        item['AreaCode'] = "302"
        item['Prefix'] = "349"
        item['Suffix'] = "0444"
        item['Extension'] = ""
        item['Email'] = ""
        item['SubDescription'] = ""
        try:
            req = requests.get('https://yoderandsonsconstruction.com/image-galleries/', verify=False)
            response_images = HtmlResponse(url=req.url,body=req.content)
            images = response_images.xpath('//article[@itemtype="http://schema.org/BlogPosting"]//img/parent::a/@href').extract()
            images = '|'.join(['https://yoderandsonsconstruction.com'+ image for image in images])
        except Exception as e:
            images = ""
            print(e)
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        yield item

        # ------------------------------------------------ HOMES --------------------------------------------------- #

        plans = requests.get('https://yoderandsonsconstruction.com/services/custom-homes/')
        response_plans = HtmlResponse(url=plans.url,body=plans.content)
        plans_links = ['https://yoderandsonsconstruction.com'+ plan for plan in response_plans.xpath('*//p[@class="readmore"]/a/@href').extract()]

        for plan in plans_links:
            res_s = requests.get(plan)
            response_s = HtmlResponse(url=res_s.url,body=res_s.content)
            PlanName = response_s.xpath('//h2[@itemprop="name"]/text()').extract_first().strip()
            PlanWebsite = response_s.url
            Description = response_s.xpath('*//div[@itemprop="articleBody"]/div[1]/text()').extract_first()
            plan_image = response_s.xpath('*//div[@class="img-fulltext-left"]/img/@src').extract_first()
            Plan_Image = "https://yoderandsonsconstruction.com" + str(plan_image) if plan_image else ""
            plan_image2 = response_s.xpath('*//div[@class="rt-image"]/img/@src').extract_first()
            Plan_Image2 = "https://yoderandsonsconstruction.com" + plan_image2 if plan_image2 else ""
            ElevationImage = ""
            if Plan_Image and Plan_Image2:
                ElevationImage = str(Plan_Image) + "|" + str(Plan_Image)
            elif Plan_Image:
                ElevationImage = Plan_Image
            elif Plan_Image2:
                ElevationImage = Plan_Image2

            plan_details = response_s.xpath('*//div[@itemprop="articleBody"]//ul[1]/li/text()').extract()
            if not plan_details:
                plan_details = response_s.xpath('*//div[@itemprop="articleBody"]//ul[1]/li/strong/text()').extract()
            # ------------------------------------------- Extract Homedetails ------------------------------ #

            try:
                PlanNumber = int(hashlib.md5(bytes(str(plan), "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % PlanNumber, "wb")
                f.write(response_s.body)
                f.close()
            except Exception as e:
                PlanNumber = ""
                print(e)

            try:
                BaseSqft, Garage = 0, 0
                for plan_d in plan_details:
                    if "living space" in plan_d or "Living space" in plan_d:
                        BaseSqft = re.findall('\d+', plan_d)
                        BaseSqft = "".join(BaseSqft) if BaseSqft else 0
                    elif "Garage" in plan_d:
                        Garage = 1.0
            except Exception as e:
                BaseSqft, Garage = 0, 0
                print(e)

            try:
                Bedrooms, Baths, HalfBaths = 0, 0, 0
                for bed in bedroom_map:
                    if bed in Description:
                        Bedrooms = bedroom_map[bed]
                for bath in bathroom_map:
                    if bath in Description:
                        Baths, HalfBaths = bathroom_map[bath]
            except:
                Bedrooms, Baths, HalfBaths = 0, 0, 0


            Type = 'SingleFamily'
            PlanNotAvailable = 0
            PlanTypeName = 'Single Family'
            BasePrice = 0

        # ----------------------- Don't change anything here --------------
            try:
                unique = str(PlanName)+str(self.builderNumber)   # < -------- Changes here
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here

                item = BdxCrawlingItem_Plan()
                item['Type'] = Type
                item['PlanNumber'] = PlanNumber
                item['unique_number'] = unique_number  # < -------- Changes here
                item['SubdivisionNumber'] = self.builderNumber
                item['PlanName'] = PlanName
                item['PlanNotAvailable'] = PlanNotAvailable
                item['PlanTypeName'] = PlanTypeName
                item['BasePrice'] = BasePrice
                item['BaseSqft'] = BaseSqft
                item['Baths'] = Baths
                item['HalfBaths'] = HalfBaths
                item['Bedrooms'] = Bedrooms
                item['Garage'] = Garage
                item['Description'] = Description[:1500]
                item['ElevationImage'] = ElevationImage
                item['PlanWebsite'] = PlanWebsite
                yield item
            except Exception as e:
                print(e)

# from scrapy.cmdline import execute
# execute("scrapy crawl Yoder_And_Sons_Construction".split())