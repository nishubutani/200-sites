# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class AndersonhomesllcSpider(scrapy.Spider):
    name = 'dmihomes'
    allowed_domains = []
    start_urls = ['https://dmihomes.com/areas-we-build/south-gulf-cove/']

    builderNumber = "30494"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        # f = open("html/%s.html" % self.builderNumber, "wb")
        # f.write(response.body)
        # f.close()
        subdivisonNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = subdivisonNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = "17568 Rockefeller Circle"
        item['City'] = "Ft. Myers"
        item['State'] = "FL"
        item['ZIP'] = "33967"
        item['AreaCode'] = "360"
        item['Prefix'] = "452"
        item['Suffix'] = "1232"
        item['Extension'] = ""
        item['AmenityType'] = ""
        item['Email'] = ""
        item['SubDescription'] = "Since 1977, DMI Home Builders has been making dreams a reality in Southwest Florida. As a family-owned and operated business, we build more than just houses, we build memories. From Sarasota to Naples and beyond, our team works hard to bring you the comfortable, yet luxurious, lifestyle of Southwest Florida. With a variety of unique home designs and thousands of open lots to choose from, our team can help you find the perfect place to call home at an affordable price. With three generations of experience, you can trust DMI to handle your home building journey from start to finish."
        item['SubImage'] = response.xpath('//div[@class="entry-content"]//img/@src').extract_first(default="").strip()
        item['SubWebsite'] = "https://dmihomes.com/"
        yield item

        link = response.xpath('//nav[@class="et-menu-nav"]/ul/li[3]/a/@href').get()
        s=requests.Session()
        res = s.get(link)
        res_data=HtmlResponse(url=link,body=res.content)
        divs = res_data.xpath('//span[text()="Download Floor Plan"]/../../../../../..')
        for div in divs:
            Type ='SingleFamily'
            SubdivisionNumber=subdivisonNumber
            PlanNotAvailable =0
            PlanTypeName ='Single Family'
            BasePrice = 0.00

            try:
                PlanName = div.xpath('./div/div[2]/div/h4/text()').get()
            except Exception as e:
                print('error in ',e)
            try:
                BaseSqft = int(str(div.xpath('./div/div[2]/div/div/text()').get(default='0')).split()[0].strip())
            except Exception as e:
                print('error in ',e)
            try:
                Bedrooms = int(str(div.xpath('./div/div[2]/div/div[2]/text()').get()).split()[0].strip())
            except Exception as e:
                print('error in ',e)
            try:
                Baths = int(str(div.xpath('./div/div[2]/div/div[3]/text()').get()).split()[0].strip())
            except Exception as e:
                print('error in ',e)
            try:
                HalfBaths = 0
            except Exception as e:
                print('error in ',e)
            try:
                Garage = 0
            except Exception as e:
                print('error in ',e)
            try:
                Description = ""
            except Exception as e:
                print('error in ',e)
            try:
                ElevationImage = div.xpath('./div/div[2]/div[2]//a/@href').get()
            except Exception as e:
                print('error in ',e)
            try:
                PlanWebsite = res.url
            except Exception as e:
                print('error in ',e)
            try:
                PlanNumber = int(hashlib.md5(bytes(str(PlanName), "utf8")).hexdigest(), 16) % (10 ** 30)# unique key
            except Exception as e:
                print('error in ',e)
            # unique_number =PlanNumber #FOREIGN key
            unique = str(PlanNumber) + str(SubdivisionNumber)
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            item = BdxCrawlingItem_Plan()
            item['Type'] = Type
            item['PlanNumber'] = PlanNumber
            item['unique_number'] = unique_number
            item['SubdivisionNumber'] = subdivisonNumber
            item['PlanName'] = PlanName
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
    execute("scrapy crawl dmihomes".split())