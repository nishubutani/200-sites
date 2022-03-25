# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header


class DannysullivanconstructionComSpider(scrapy.Spider):
    name = 'bluestoneCustomhome'
    allowed_domains = []
    start_urls = ['http://bluestonecustombuilders.com/']
    builderNumber = 52297

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
        item['Street1'] = 'P.O. Box 451042'
        item['City'] = 'Omaha'
        item['State'] = 'NE'
        item['ZIP'] = '68145'
        item['AreaCode'] = '402'
        item['Prefix'] = '871'
        item['Suffix'] = '4411'
        item['Extension'] = ""
        item['Email'] = 'info@bluestonecustombuilders.com'
        item[
            'SubDescription'] = 'As a “Cost Plus” builder, we build custom homes in Omaha in the $400,000 – $1,000,000 price range, partnering with you throughout the entire home building process to ensure your dream home needs are met. Contact us today at (402) 871-4411 or to view model homes in Omaha and new construction homes in Omaha to find what you like best, and let’s build your dream home together! BlueStone Custom Builders is the premier custom home builder in Omaha, Nebraska; click here to see what people are saying about us.'
        item[
            'SubImage'] = 'http://bluestonecustombuilders.com/wp-content/uploads/2014/11/270667_23-e1528913475890.jpg|http://bluestonecustombuilders.com/wp-content/uploads/2014/11/270667_26-e1528912833625.jpg|http://bluestonecustombuilders.com/wp-content/uploads/2014/11/264618_02-e1528914723664.jpg|http://bluestonecustombuilders.com/wp-content/uploads/2014/11/interior-02.jpg|http://bluestonecustombuilders.com/wp-content/uploads/2014/11/kitchen-02-e1528914124609.jpg'
        item['SubWebsite'] = response.url
        yield item

        flinks = ['http://bluestonecustombuilders.com/2-story-floor-plans/',
                  'http://bluestonecustombuilders.com/1-5-story-floor-plans/',
                  'http://bluestonecustombuilders.com/ranch-floor-plan/',
                  'http://bluestonecustombuilders.com/townhome-floor-plans/']
        for flink in flinks:
            # a = 'http://bluestonecustombuilders.com/ranch-floor-plan/'
            yield scrapy.FormRequest(url=flink, callback=self.fDetail, dont_filter=True)

    def fDetail(self, response):
        try:
            PlanNames = response.xpath('//td[@align="center"]//span//text()').getall()
            BaseSqfts = response.xpath('//td[@align="center"]/p/text()[2]').extract()
            Bedroos = response.xpath('//*[contains(text(),"Bedrooms")]/text()[1]').extract()
            Bathroos = response.xpath('//*[contains(text(),"Bedrooms")]/text()[2]').extract()
            Garages = response.xpath('//*[contains(text(),"Bedrooms")]/text()[3]').extract()
            ElevationImages = response.xpath('//td[@align="center"]/a/img/@src').extract()
            for planName,baseSqft,bedroo,bathroo,garage,ElevationImage in zip(PlanNames,BaseSqfts,Bedroos,Bathroos,Garages,ElevationImages):
                PlanName = planName.strip()
                BaseSqf = baseSqft.strip().replace(',','')
                BaseSqft = re.findall(r"(\d+)",BaseSqf)[0]
                Be = bedroo.strip()
                Bed = re.findall(r"(\d+)",Be)[0]
                Bath = bathroo.strip()
                tmp = re.findall(r"(\d+)", Bath)
                Baths = tmp[0]
                if len(tmp) > 1:
                    planHalfBaths = 1
                else:
                    planHalfBaths = 0
                Garag = garage.strip()
                Garage = re.findall(r"(\d+)",Garag)[0]
                hs = str(PlanName)+str(Bed)+str(BaseSqft)+str(Baths)
                PlanNumber = int(hashlib.md5(bytes(hs,"utf8")).hexdigest(), 16) % (10 ** 30)
                ElevationImage = ElevationImage
                print(PlanName,BaseSqft,Bed,Baths,Garage,ElevationImage)

                unique = str(PlanNumber) + str(self.builderNumber)  # < -------- Changes here
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
                item = BdxCrawlingItem_Plan()
                item['Type'] = 'SingleFamily'
                item['PlanNumber'] = PlanNumber
                item['unique_number'] = unique_number  # < -------- Changes here
                item['SubdivisionNumber'] = self.builderNumber
                item['PlanName'] = PlanName
                item['PlanNotAvailable'] = '0'
                item['PlanTypeName'] = 'Single Family'
                item['BasePrice'] = '0'
                item['BaseSqft'] = BaseSqft
                item['Baths'] = Baths
                item['HalfBaths'] = planHalfBaths
                item['Bedrooms'] = Bed
                item['Garage'] = Garage
                item['Description'] = 'Click on each of the elevations below to view floor plans on Houzz.'
                item['ElevationImage'] = ElevationImage
                item['PlanWebsite'] = response.url
                yield item
        except Exception as e:
            print("Problem-------> ",e)

if __name__ == '__main__':
    execute("scrapy crawl bluestoneCustomhome".split())