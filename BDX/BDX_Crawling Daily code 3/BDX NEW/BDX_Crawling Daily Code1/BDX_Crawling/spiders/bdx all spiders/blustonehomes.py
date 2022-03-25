
# -*- coding: utf-8 -*-
import hashlib
import re
import time

import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class blustonehomes(scrapy.Spider):
    name = 'blustonehomes'
    allowed_domains = ['https://www.blustonehomes.com']
    start_urls = ['https://www.blustonehomes.com']

    builderNumber = "63655"

    def parse(self, response):

        images = ''
        image = response.xpath('//div[@class="cycle-slideshow"]/img/@src').extract()
        for i in image:
            images = images + i + '|'
        images = images.strip('|')

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '600 4TH STREET SUITE 815'
        item['City'] = 'SIOUX'
        item['State'] = 'IA'
        item['ZIP'] = '51101'
        item['AreaCode'] = '712'
        item['Prefix'] = '301'
        item['Suffix'] = '5172'
        item['Extension'] = ""
        item['Email'] = 'INFO@BLUSTONEHOMES.COM'
        item['SubDescription'] = 'BluStone Homes is backed by over 45 years of experience in the home building industry in the Midwest. BluStone Homes craftsmen have built site-built and custom system-built homes to exacting standards with the highest quality materials for both single family and multi-family housing.We work very hard to ensure your experience with our company exceeds your expectations for customer service, quality construction and outstanding amenities as we bring your dreams to life. We look forward to developing your dream home for you and your family.'
        item['SubImage'] = 'https://www.blustonehomes.com/img/home_slider_whispering_creek.jpg|https://www.blustonehomes.com/img/julia_circle_kitchen.jpg|'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'https://www.blustonehomes.com/gallery.php'
        yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)

    def parse2(self,response):


        #--------- here iam using div method -----------#


        divs = response.xpath('//div[@class="pi-row"]')
        for div in divs:

            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                PlanName = div.xpath('.//h2/text()').get().replace("\n","").replace("\t","").strip()
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
                BasePrice = response.xpath("//font[contains(text(),'$')]/text()").extract_first('0')
                BasePrice = BasePrice.replace(',', '').replace(".", "").strip()
                BasePrice = re.findall(r"(\d+)", BasePrice)[0]
            except Exception as e:
                print(e)
                BasePrice = 0

            try:
                sqft = div.xpath('.//div[@class="pi-responsive-table-2xs"]//span[contains(text(),"Sqft:")]/../following-sibling::td/text()').extract_first('')
                # sqft = sqft.split("|")[2]
                sqft = sqft.replace(',', '').replace(".", "").strip()
                BaseSqft = re.findall(r"(\d+)", sqft)[0]


            except Exception as e:
                print(e)
                BaseSqft = ''

            try:
                bath = div.xpath('.//div[@class="pi-responsive-table-2xs"]//span[contains(text(),"Bath:")]/../following-sibling::td/text()').extract_first()
                if '/' in bath:
                    bath =bath.split("/")[1]
                    print(bath)

                tmp = re.findall(r"(\d+)", bath)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                print(e)

            try:
                Bedrooms = div.xpath('.//div[@class="pi-responsive-table-2xs"]//span[contains(text(),"Beds:")]/../following-sibling::td/text()').extract_first()
                if '/' in Bedrooms:
                    Bedrooms = Bedrooms.split("/")[1]
                # Bedrooms = Bedrooms.split("|")[1].split("|")[0]
                Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            except Exception as e:
                print(e)

            try:
                Garage = div.xpath('.//div[@class="pi-responsive-table-2xs"]//span[contains(text(),"Garage:")]/../following-sibling::td/text()').extract_first()
                Garage = Garage.replace(',', '').replace(".", "").replace("Triple","3").replace("Double","2").strip()
                Garage = re.findall(r"(\d+)", Garage)[0]

            except Exception as e:
                Garage = 0
                print(e)


            # Description = 'Brookstone Construction Group is a family owned and operated company with over 20 years of custom homes and commercial construction experience. We value what it truly means to feel like family, and we will do our best to build not just a house, but a home.'
            Description = ''

            try:
                ElevationImage = div.xpath('.//div[@class="pi-img-w pi-img-round-corners pi-img-shadow-light pi-margin-bottom-25"]//a/@href').extract_first('')
                if ElevationImage != '':
                    ElevationImage = "https://www.blustonehomes.com/" + str(ElevationImage)
                print(ElevationImage)

            except Exception as e:
                print(e)
                ElevationImage = ''


            try:
                PlanWebsite = response.url
            except Exception as e:
                print(e)

                # ----------------------- Don't change anything here --------------
            unique = str(PlanNumber) + str(SubdivisionNumber) + str(Baths) + str(Bedrooms)  # < -------- Changes here
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
            item['Description'] = Description
            item['ElevationImage'] = ElevationImage
            item['PlanWebsite'] = PlanWebsite
            yield item


#--- use bdxstaticdata_3 - tabkle for this bdx


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl blustonehomes'.split())


    