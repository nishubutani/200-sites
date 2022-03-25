# -*- coding: utf-8 -*-
import scrapy
import hashlib
import re
import scrapy
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec



class WatershollandSpider(scrapy.Spider):
    name = 'watersholland'
    allowed_domains = ['www.watersholland.com']
    start_urls = ['http://www.watersholland.com']
    builderNumber = "52139"

    def parse(self, response):
        community_links = "https://www.watersholland.com/communities"

        yield scrapy.FormRequest(url=community_links,
                                 callback=self.community)

    def community(self,response):
        communitys = response.xpath('//div[@class="summary-title"]/a/@href').extract()
        texts = response.xpath('//div[@class="summary-title"]/a/text()').extract()

        for community,text in zip(communitys,texts):
            if "Sold Out"  not in text:
                if "Register Here" not in text:
                    link = community
                    print(link)




                    yield scrapy.FormRequest(url= "https://www.watersholland.com" + str(link),
                                     callback=self.plan_links)

    def plan_links(self, response):

        item = BdxCrawlingItem_subdivision()

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
        item['Street1'] = "4115 South Creek Drive"
        item['City'] = "Chattanooga"
        item['State'] = "TN"
        item['ZIP'] = "37406"
        item['AreaCode'] = "423"
        item['Prefix'] = "595"
        item['Suffix'] = "8666"
        item['Extension'] = ""
        item['Email'] = ""

        item[
            'SubDescription'] = response.xpath(
            '//div[@class="sqs-block-content"]/p/text()').extract_first(
            default="")
        item['SubImage'] = 'https://images.squarespace-cdn.com/content/v1/5af9d09d70e80243641d2f10/1527720006288-DFWINYZ3M23IYX7LHGSZ/ke17ZwdGBToddI8pDm48kPVQ4y9Qz_4IyiUzkWsm6yh7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0m2EAVJiLKxn6RD_K9rHr9fuvIDG6ANQ__l7kVwUchyM1f5W_FMh-GOI_fcKuJc5rw/_MED5654_5_6_tonemapped.png'
        item['SubWebsite'] = response.url
        yield item

        try:
            plan_links = response.xpath('//div[@class="summary-title"]/a/@href').extract()
            print(plan_links)
            # plan_links = "https://worleybuildersinc.com/communities/"
            for plan_link in plan_links:
                des = response.xpath('//div[@class="sqs-block-content"]/p/text()').get()
                if not des:
                    des = ""
                if "https://www.watersholland.com" not in plan_link:
                    plan_link = "https://www.watersholland.com" + str(plan_link)

                # print(plan_link)


                yield scrapy.Request(url=plan_link, callback=self.parse_planlink, meta={"des":des},dont_filter=True)

        except Exception as e:
            print(e)

    def parse_planlink(self,response):


        SubdivisionNumber = self.builderNumber
        planname = response.xpath('//div[@class="sqs-block-content"]/h2/text()').get()
        bedroom = response.xpath('//div[@class="sqs-block-content"]//ul/li[contains(text(),"Bedrooms")]/text()').get()
        if not bedroom:
            bedroom = response.xpath(
                '//div[@class="sqs-block-content"]//ul/li/p[contains(text(),"Bedrooms")]/text()').get()
        bedroom = re.findall(r'(\d)',bedroom)[0]
        # bedroom = bedroom.split()[0]
        bathroom = response.xpath('//div[@class="sqs-block-content"]//ul/li[contains(text(),"Bathrooms")]/text()').get()
        if not bathroom :
            bathroom = response.xpath('//div[@class="sqs-block-content"]//ul/li[contains(text(),"Baths")]/text()').get()
            if not bathroom :
                bathroom = response.xpath('//div[@class="sqs-block-content"]//ul/li/p[contains(text(),"Baths")]/text()').get()
                if not bathroom:
                    bathroom = response.xpath('//div[@class="sqs-block-content"]//ul/li/p[contains(text(),"Bathrooms")]/text()').get()
                    if not bathroom:
                        bathroom = 0

        bathroom =  re.findall(r"(\d+)", bathroom)
        # bathroom = bathroom.split()[0]
        tmp = bathroom[0]
        #
        if len(bathroom) > 1:
            HalfBaths = 1
        else:
            HalfBaths = 0

        feet = response.xpath('//div[@class="sqs-block-content"]//ul/li[contains(text(),"square feet")]/text()').get()
        if not feet:
            feet = response.xpath(
                '//div[@class="sqs-block-content"]//ul[1]/li/p[contains(text(),"SF")]/text()').get()
            if not feet:
                feet = response.xpath(
                    '//div[@class="sqs-block-content"]//ul[1]/li[contains(text(),"SF")]/text()').get()
                if not feet:
                    feet = response.xpath(
                        '//div[@class="sqs-block-content"]//ul[1]/li/p[contains(text(),"square feet")]/text()').get()
        feet = re.findall(r'(\d+)', feet.replace(',',''))[0]
        # feet = feet.split()[0]

        garage = response.xpath('//div[@class="sqs-block-content"]//ul/li[contains(text(),"Car Garage")]/text()').get()
        if not garage:
            garage = response.xpath(
                '//div[@class="sqs-block-content"]//ul/li/p[contains(text(),"Car Garage")]/text()').get()
        # garage = garage.replace('-','')
            if not garage:
                garage = 0
        try:
            garage = re.findall(r'(\d)', garage)[0]
        except Exception as e :
            garage= 0

        # if "-" in garage:
        #     garage = garage.split("-")[0]
        # elif garage==0:
        #     garage = 0
        # else:
        #     garage = garage.split()[0]

        ElevationImage = response.xpath('//img[@class="thumb-image"]/@data-src').extract()
        print(ElevationImage)


        PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
        f = open("html/%s.html" % PlanNumber, "wb")
        f.write(response.body)
        f.close()
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)


        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = planname
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0
        item['BaseSqft'] = feet
        item['Baths'] = tmp
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = bedroom
        item['Garage'] = garage
        item['Description'] = response.meta['des']
        # ElevationImage = response.xpath('//img[@class="thumb-image loaded"]/@src').extract()
        item['ElevationImage'] = "|".join(ElevationImage)
        item['PlanWebsite'] = response.url

        yield item





from scrapy.cmdline import execute
# execute("scrapy crawl watersholland".split())





