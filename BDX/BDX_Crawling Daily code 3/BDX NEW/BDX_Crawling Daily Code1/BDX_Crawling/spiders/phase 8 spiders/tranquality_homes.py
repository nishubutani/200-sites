# -*- coding: utf-8 -*-
import scrapy
import hashlib
import re
import scrapy
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class TranqualityHomesSpider(scrapy.Spider):
    name = 'tranquality_homes'
    allowed_domains = ['www.tranquilitycustomhomes.com']
    start_urls = ['http://www.tranquilitycustomhomes.com/']
    builderNumber = '19814'

    def parse(self, response):
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
        item['Street1'] = "19533 Rambling Creek Drive"
        item['City'] = "Edmond"
        item['State'] = "OK"
        item['ZIP'] = "73012"
        item['AreaCode'] = "405"
        item['Prefix'] = "252"
        item['Suffix'] = '1152'
        item['Extension'] = ""
        item['Email'] = "sales@tranquilitycustomhomes.com"
        item[
            'SubDescription'] = "Tranquility Custom Homes builds in the Oklahoma City Metro Area in these communities or on your own land.  We can also purchase lots in other communities...just ask us if there is a specific area you are interested in building in!"
        item[
            'SubImage'] = ''
        item['SubWebsite'] = response.url
        yield item

        try:
            plan_link = "http://www.tranquilitycustomhomes.com/plans"
            print(plan_link)


            yield scrapy.Request(url=plan_link, callback=self.parse_planlink,
                                     dont_filter=True)
        except Exception as e:
            print(e)

    def parse_planlink(self,response):

        planlinks = response.xpath('//strong//@href').extract()
        for planlink in planlinks:
            if "/" not in planlink:
                planlink = "/" + str(planlink)

            yield scrapy.Request(url= "http://www.tranquilitycustomhomes.com" + str(planlink), callback=self.plandetail,
                                 dont_filter=True)

    def plandetail(self,response):
        item = BdxCrawlingItem_Plan()


        PlanName = response.xpath('//h1[@class="entry-title"]/text()').get()
        if not PlanName:
            PlanName = ''

        if PlanName =="":
           item['PlanName'] = "The Griffith"
           item['Bedrooms'] = '3'
           item['Baths'] = '2'
           item['HalfBaths'] = '0'
           item['ElevationImage'] = "https://my.matterport.com/api/v1/player/models/P7Tt5nCcHPn/thumb?width=400&dpr=1.25&disable=upscale"
           item['BaseSqft'] = '1908'
           item['Garage'] = '0'


        else :
            try:
                item['PlanName'] = PlanName
            except Exception as e:
                item['PlanName'] = ''
            try:
                bedroom = response.xpath('//span[contains(text(),"Bedrooms")]/text()').get()
                item['Bedrooms'] = re.findall(r'(\d+)',bedroom)[0]
            except Exception as e:
                item['Bedrooms'] = 0

            try:
                bathroom = response.xpath('//span[contains(text(), "Full Bathrooms")]/text()').get()
                item['Baths'] = re.findall(r'(\d+)',bathroom)[0]
            except Exception as e:
                item['Baths'] = 0

            try:
                Half_bathrooms = response.xpath('//span[contains(text(),"Half Bathrooms")]/text()').get()
                item['HalfBaths'] = re.findall(r'(\d+)',Half_bathrooms)[0]
            except Exception as e:
                item['HalfBaths'] = 0

            try:
                garage = response.xpath('//span[contains(text(),"Garage")]/text()').get()
                item['Garage'] = re.findall(r'(\d+)',garage)[0]
            except Exception as e:
                item['Garage'] = 0

            try:
                feet = response.xpath('//span[contains(text(),"Square Feet")]/text()').get()
                item['BaseSqft'] = re.findall(r'(\d+)',feet)[0]
            except Exception as e:
                item['BaseSqft'] = '0'

            try:
                # elevation = response.xpath('//a/img[@class="lazy-image"]/@src').getall()
                url_add = "http://www.tranquilitycustomhomes.com"
                ElevationImage = '|'.join(response.urljoin(url_add + i) for i in response.xpath(
                                                                                '//a/img[@class="lazy-image"]/@src').extract())

                item['ElevationImage'] = ElevationImage
            except Exception as e:
                item['ElevationImage'] = ''

        try:
             item['Description'] = response.xpath('//div[@class="feat"]/span[1]/text()').get()
             if not item['Description']:
                 item['Description'] = response.xpath('//p/span[1]/text()').get()
                 if not item['Description']:
                     item['Description'] = "n/a"

        except Exception as e:
            item['Description'] = "n/a"


        PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
        f = open("html/%s.html" % PlanNumber, "wb")
        f.write(response.body)
        f.close()


        unique = str(PlanNumber) + str(self.builderNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)


        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = self.builderNumber

        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0

        item['PlanWebsite'] = response.url
        yield item

from scrapy.cmdline import execute
# execute("scrapy crawl tranquality_homes".split())







