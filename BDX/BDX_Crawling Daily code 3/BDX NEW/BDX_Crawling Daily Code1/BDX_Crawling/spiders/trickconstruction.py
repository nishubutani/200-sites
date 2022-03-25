# -*- coding: utf-8 -*-
import json
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'trickconstruction'
    allowed_domains = ['harlowbuilders.net']
    start_urls = ['https://www.trickconstruction.com/']
    builderNumber = 19900


    def parse(self, response):

        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = '1305 TWIN OAKS ROAD EAST'
        item2['City'] = 'NORTHPORT'
        item2['State'] = 'AL'
        item2['ZIP'] = '35473'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "Trick Construction encourages and supports an affirmative advertising and marketing program in which there are no barriers to obtaining housing because of race, color, religion, sex, handicap, familial status, or national origin. All residential real estate information on this website is subject to the Federal Fair Housing Act Title VIII of the Civil Rights Act of 1968, as amended, which makes it illegal to advertise any preference, limitation, or discrimination because of race, color, religion, sex, handicap, familial states, or national origin, or intention to make any such preference, limitation or discrimination.Your state or local jurisdiction may impose additional requirements. We are committed to the letter and spirit of the United States policy for the achievement of equal housing opportunity"
        item2['SubImage'] = "https://images.squarespace-cdn.com/content/v1/5caf31a7755be20933430199/1555877738378-6N2GN5CJOZN5RDJSE5P8/002+No+Name.JPG?format=1500w|https://images.squarespace-cdn.com/content/v1/5caf31a7755be20933430199/1555877750537-9LHZNWBHWZVKIWAXIA39/007+%282%29No+Name.JPG?format=1500w|https://images.squarespace-cdn.com/content/v1/5caf31a7755be20933430199/1555877760218-CCY3Y2KWHV7JW8D2J4ZF/008TNR+294.JPG?format=1500w|https://images.squarespace-cdn.com/content/v1/5caf31a7755be20933430199/1555877762775-JANBFOCDYPL0HDVOYTTL/15+MGMimosa+Gard.jpg?format=1500w|https://images.squarespace-cdn.com/content/v1/5caf31a7755be20933430199/1555877778619-MUPF2RSXYB3TZHUO1XUG/44ROY+front.JPG?format=1500w|https://images.squarespace-cdn.com/content/v1/5caf31a7755be20933430199/1555877780909-CLTJIPZ3AXWBOOEK5OUK/50+Easton+Place+elev.jpg?format=1500w"
        item2['SubWebsite'] = 'https://www.trickconstruction.com/'
        item2['AmenityType'] = ''
        yield item2

        link = 'https://giffordandgifford.com/custom-homes/'
        yield scrapy.FormRequest(url=link, callback=self.plan, dont_filter=True)


    def plan(self, response):

        links = response.xpath("//a[contains(@href,'custom-homes/')]/h4/../@href").extract()
        for link in links:
            link = 'https://giffordandgifford.com/' + str(link)
            print(link)
            yield scrapy.FormRequest(url=link,callback=self.plan_details,dont_filter=True)

    def plan_details(self,response):

        try:
            Type = 'SingleFamily'
        except Exception as e:
            Type = 'SingleFamily'
            print(e)

        try:
            PlanName = response.xpath("//h1/text()").extract_first('').strip()
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
            SubdivisionNumber = self.builderNumber
        except Exception as e:
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
            BasePrice = 0.00
        except Exception as e:
            print(e)

        try:

            BaseSqft = response.xpath("//*[contains(text(),'Sq Ft')]/preceding-sibling::strong[1]/text()").extract_first(default='0')
            if '_' in BaseSqft:
                BaseSqft = BaseSqft.split("-")[1]
            BaseSqft = BaseSqft.replace(',', '')
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]

        except Exception as e:
            print(e)

        try:
            Baths = response.xpath("//*[contains(text(),'Bath')]/preceding-sibling::strong[1]/text()").extract_first(
                default='0')
            Baths = re.findall(r"(\d+)", Baths)[0]

            if len(Baths) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0

        except Exception as e:
            Baths = 0
            print(e)

        try:
            Bedrooms = response.xpath("//*[contains(text(),'Bed')]/preceding-sibling::strong[1]/text()").extract_first(default='0')
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)
            Bedrooms = 0

        try:
            Garage = response.xpath("//*[contains(text(),'Garage')]/preceding-sibling::strong[1]/text()").extract_first('')
            # Garage = response.xpath(".//*[contains(text(),'Garages')]/../text()").extract_first(default='0')
            Garage = re.findall(r"(\d+)", Garage)[0]

        except Exception as e:
            print(e)
            Garage = "0"

        try:
            Description = ""
        except Exception as e:
            print(e)
            Description = ""

        try:
            ElevationImage = response.xpath('//div[@class="h-image__frame-container"]/img/@src').extract()
            ElevationImage = "|".join(ElevationImage)
        except Exception as e:
            print(e)
            ElevationImage = ""

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

            # ----------------------- Don't change anything here --------------
        unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
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


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl trickconstruction'.split())





