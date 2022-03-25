# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'rivertoriver_loghomes_spider'
    allowed_domains = ['rivertoriverloghomes.com']
    start_urls = ['https://rivertoriverloghomes.com/']
    builderNumber = 466897446200317839859943872247


    def parse(self, response):

        images = ''
        image = response.xpath('//*[contains(@src,"wp-content/uploads")]/@src').extract()
        for i in image:
            images = images  + i + '|'
        images = images.strip('|')


        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = '2163 S Centurion Place'
        item2['City'] = 'Boise'
        item2['State'] = 'ID'
        item2['ZIP'] = '83709'
        item2['AreaCode'] = '208'
        item2['Prefix'] = "881"
        item2['Suffix'] = "8564"
        item2['Extension'] = ""
        item2['Email'] = "scott@rivertoriverloghomes.com"
        item2['SubDescription'] = "River to River Log Homes is your Independent Representative for Log Homes of America & Summit Log Homes. With over 13 years of experience, River to River Log Homes takes pride in their craftsmanship."
        item2['SubImage'] = images
        item2['SubWebsite'] = ''
        item2['AmenityType'] = ''
        yield item2

        # -------------------------------------------------------------------- #


        # ------------------------------------ Extract_Plans ----------------------------#
        plan_urls = response.xpath('//a[contains(text(),"Catalog")]/@href').extract()[0]
        yield scrapy.Request(url=plan_urls, callback=self.plans_details,
                                 meta={'sbdn': self.builderNumber})

        # ---------------------------------------------------------------------------------#
    def plans_details(self, response):
        # ------------------------------------- Extracting Plans ------------------------- #
        plan_ul = response.xpath('//*[@class="row expanded small-up-1 medium-up-3 large-up-4"]/div')
        print(plan_ul)
        for div in plan_ul:
            try:
                Type = 'SingleFamily'
            except Exception as e:
                Type = 'SingleFamily'
                print(e)

            try:
                PlanName = div.xpath('.//*[@class="card-divider"]/h3/text()').extract()[0].strip()
            except Exception as e:
                PlanName = ''
                print(e)

            try:
                PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % PlanNumber, "wb")
                f.write(response.body)
                f.close()
            except Exception as e:
                print(e)

            try:
                SubdivisionNumber = response.meta['sbdn']
            except Exception as e:
                print(e)


            try:
                PlanNotAvailable = 0
            except Exception as e:
                print(e)

            try:
                PlanTypeName = response.xpath('//div[@class="homeType"]/p/text()').extract_first(default='Single Family').strip()
            except Exception as e:
                print(e)

            try:
                BasePrice = 0.00
            except Exception as e:
                print(e)

            try:
                BaseSqft = div.xpath('.//*[@class="entry-content card-section house-info"]/h3/text()').extract_first(default='0')
                BaseSqft = BaseSqft.split(':')[-1].strip()
                BaseSqft = BaseSqft.replace(',','')

            except Exception as e:
                print(e)

            try:
                Baths = 0
                HalfBaths = 0
            except Exception as e:
                Baths = 0
                print(e)

            try:
                Bedrooms = div.xpath('.//*[@class="entry-content card-section house-info"]/h4[contains(text(),"Bedrooms:")]/text()').extract_first()
                Bedrooms = Bedrooms.split(":")[-1].strip()
                if Bedrooms == '':
                    Bedrooms = 0

            except Exception as e:
                Bedrooms = 0
                print(e)

            try:
                Garage = 0.00

            except Exception as e:
                print(e)

            try:
                Description = 'All plans can be customized to your needs for your log home, log hybrid home or timber frame. Plans can also be custome drawn to your specifications. All plans are arranged below from the smallest to the largest. Click on any photo to view floor plans.'
            except Exception as e:
                print(e)

            try:
                ElevationImage = div.xpath('.//*[@class="image-card"]/img/@src').extract_first(default='')
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
            item['Description'] = Description
            item['ElevationImage'] = ElevationImage
            item['PlanWebsite'] = PlanWebsite
            yield item
        # --------------------------------------------------------------------- #




if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl rivertoriver_loghomes_spider'.split())