# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class EmbuildersSpider(scrapy.Spider):
    name = 'embuilders'
    allowed_domains = ['embuilders.com']
    start_urls = ['http://embuilders.com/']

    builderNumber = "554459091097825076611924151749"

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
        item['Street1'] = "Augusta Cir"
        item['City'] = "Gillette"
        item['State'] = "WY"
        item['ZIP'] = "82718"
        item['AreaCode'] = "307"
        item['Prefix'] = "696"
        item['Suffix'] = "5769"
        item['Extension'] = ""
        item['Email'] = "info@embuilders.com"
        item['SubDescription'] = "Nothing says resort-style living like a finely manicured golf-course, club house and amenities that make for a lifestyle balanced between activity and tranquility. Set amid the “Big Sky” beauty of Gillette, Wyoming, you can bask in the serenity of your spacious backyard or enjoy the company of a close knit community—including golfing with your friends and family, taking in a swim with your kids at the pool or enjoy an evening of drinks and dinner with neighbors at the club. Accessible to Interstate 90, the community is just minutes from the heart of Gillette and is adjacent to the City of Gillette’s Field of Dreams—a new multi-sport complex for all ages and interests."
        item['SubImage'] = "http://embuilders.com/wp-content/uploads/2013/08/plot.png|http://embuilders.com/wp-content/uploads/2013/06/contact1.png|http://embuilders.com/wp-content/uploads/2013/06/oil.png"
        item['SubWebsite'] = 'http://embuilders.com/our-community/'
        item['AmenityType'] = ''
        yield item
        

        item = BdxCrawlingItem_Plan()
        unique = str("Plan Unknown") + str(self.builderNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item['unique_number'] = unique_number
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = "Plan Unknown"
        item['SubdivisionNumber'] = self.builderNumber
        item['PlanName'] = "Plan Unknown"
        item['PlanNotAvailable'] = 1
        item['PlanTypeName'] = "Single Family"
        item['BasePrice'] = 0
        item['BaseSqft'] = 0
        item['Baths'] = 0
        item['HalfBaths'] = 0
        item['Bedrooms'] = 0
        item['Garage'] = 0
        item['Description'] = ""
        item['ElevationImage'] = ""
        item['PlanWebsite'] = ""
        yield item

        url = "http://embuilders.com/our-homes"

        headers = {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'accept-encoding': "gzip, deflate",
            'accept-language': "en-US,en;q=0.9",
            'cache-control': "max-age=0",
            'connection': "keep-alive",
            'host': "embuilders.com",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.request("GET", url, headers=headers)

        print(response.text)

        response = HtmlResponse(url=url, body=response.content)



        var = response.xpath('//a[@id="learnmoreclick"]')
        for i in var:
            url = i.xpath('./@href').extract_first()
            print(url)
            # PlanName = i.xpath('./span/text()').extract_first()
            # print(PlanName)

            yield scrapy.FormRequest(url,callback=self.getPlans,method='GET')

    def getPlans(self,response):
        Type = 'SingleFamily'

        PlanNotAvailable = 0
        PlanTypeName = "Single Family"

        try:
            PlanName = response.url.split("http://embuilders.com/")[1]
            print(PlanName)
            PlanName = PlanName.replace("-", " ").replace("/","")
        except Exception as e:
            print(e)
            PlanName = ''


        try:
            PlanNumber = int(hashlib.md5(bytes(response.url,"utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        BasePrice = '0'
        BaseSqft = response.xpath('//span[contains(text(),"SqFt")]/text()').extract_first()
        if BaseSqft:
            BaseSqft = BaseSqft.split(':')[1].replace(',','').strip()

        Baths = response.xpath('//span[contains(text(),"Baths Full")]/text()').extract_first()
        if Baths:
            Baths = Baths.split(':')[1].strip()

        HalfBaths = 0

        Bedrooms = response.xpath('//span[contains(text(),"Bedrooms")]/text()').extract_first()
        if Bedrooms:
            Bedrooms = Bedrooms.split(':')[1].strip()

        Garage = response.xpath('//span[contains(text(),"Garage")]/text()').extract_first()
        if Garage:
            Garage = Garage.split(':')[1].strip()

        Description = response.xpath('//*[contains(text(),"OVERVIEW")]/parent::h6/following-sibling::p/text()').extract_first(default='')

        ElevationImage = response.xpath('//div[@class="flex-container post_gallery"]//li/img/@src').extract()

        abc = response.xpath('//div[@class="boxes clearfix"]//div/a/img/@src').extract()

        ElevationImage.extend(abc)

        if ElevationImage !=[]:
            ElevationImage = '|'.join(ElevationImage)

        PlanWebsite = response.url
        item = BdxCrawlingItem_Plan()
        item['Type'] = Type
        item['PlanNumber'] = PlanNumber
        item['SubdivisionNumber'] = self.builderNumber
        item['PlanName'] = PlanName

        unique = str(item['PlanName']) + str(self.builderNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

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
        item['unique_number'] = unique_number
        yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl embuilders".split())

