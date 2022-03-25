# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
import requests
from scrapy.http import HtmlResponse

class CastillohousingSpider(scrapy.Spider):
    name = 'castillohousing'
    allowed_domains = []
    start_urls = ['http://castillohousing.com/']

    builderNumber = "926400450873021078194379372516"

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
        item['Street1'] = "3300 Henderson Blvd #202"
        item['City'] = "Tampa"
        item['State'] = "FL"
        item['ZIP'] = "33609"
        item['AreaCode'] = "813"
        item['Prefix'] = "876"
        item['Suffix'] = "8433"
        item['Extension'] = ""
        item['Email'] = "acastillo@castillohousing.com"
        item['SubDescription'] = "We build in all cities and municipalities located within Hillsborough, Pinellas, and Pasco counties. If you are interested in building a new home designed with energy efficiency and sustainability in mind or would like to remodel your existing home, please contact us today. As always, there is no obligation and our initial consultation are free."
        item['SubImage'] = "https://castillohousing.com/wp-content/uploads/2019/06/Cameron-1.jpg|https://castillohousing.com/wp-content/uploads/2018/11/Ext-Back-View-Patio-Stairs.jpg"
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        res_pp = "https://castillohousing.com/floor-plans/"
        yield scrapy.FormRequest(url=res_pp,dont_filter=True,callback=self.parse2)

    def parse2(self,response):

        links = response.xpath('//h3[@class="et_pb_module_header"]/a/@href').extract()
        for link in links:
            link = 'https://castillohousing.com' + link
            print(link)
            yield scrapy.FormRequest(url=link,callback=self.parse3,dont_filter=True)

    def parse3(self,response):

        plan_page_links = response.xpath('//div[@class="wpl_prp_bot"]/a/@href').extract()
        for link in plan_page_links:
            yield scrapy.FormRequest(url=link,callback=self.parse4,dont_filter=True)

    def parse4(self,response):
        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//h1[@class="title_text"]/text()').get()
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
            sqft = response.xpath("//*[contains(text(),'Living Area : ')]/span/text()").get()
            if '-' in sqft:
                sqft = sqft.split("-")[1]
            sqft = sqft.replace(',', '').strip()
            BaseSqft = re.findall(r"(\d+)", sqft)[0]

        except Exception as e:
            print(e)
            BaseSqft = '0'

        try:
            bath = response.xpath("//*[contains(text(),'Bath : ')]/span/text()").get()
            if '-' in bath:
                bath = bath.split("-")[1]
            tmp = re.findall(r"(\d+)", bath)
            Baths = tmp[0]
            if len(str(tmp)) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            print(e)


        try:
            Bedrooms = response.xpath("//*[contains(text(),'Bedroom : ')]/span/text()").get()
            if '-' in Bedrooms:
                Bedrooms = Bedrooms.split("-")[1]
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)

        try:
            Garage = response.xpath("//h3[contains(text(),'GARAGE')]/../p/span/text()").get()
            if '-' in Garage:
                Garage = Garage.split("-")[1]
            Garage = re.findall(r"(\d+)", Garage)[0]
            if not Garage:
                Garage = 0
        except Exception as e:
            Garage = 0
            # print(e)

        try:
            desc = response.xpath('//div[@class="fl-module-content fl-node-content"]/p/text()').extract_first('')
            print(desc)
        except Exception as e:
            # print(e)
            desc = ''

        try:
            images = []
            imagedata = response.xpath('//div[@class="lSSlideOuter "]//li//img/@src').getall()
            for id in imagedata:
                id = id
                images.append(id)
            ElevationImage = "|".join(images)
        except Exception as e:
            print(e)

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
        item['Description'] = desc
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item





if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl castillohousing'.split())

