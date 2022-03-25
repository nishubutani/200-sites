# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'castlepointhomes'
    allowed_domains = ['castlepointehomes.com']
    start_urls = ['http://www.castlepointehomes.com/']
    builderNumber = 24158


    def parse(self, response):


        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = '17450 Meredith Dr'
        item2['City'] = 'Clive'
        item2['State'] = 'IA'
        item2['ZIP'] = '50325'
        item2['AreaCode'] = '515'
        item2['Prefix'] = "988"
        item2['Suffix'] = "4201"
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "Castle Pointe Homes, a leading Des Moines custom home builder, is family-owned and operated. Led by Mike Miller, who brings with him over 20 years of construction experience, Castle Pointe Homes provides you with the personal service and attention to detail you should expect from a home builder."
        item2['SubImage'] = "http://www.castlepointehomes.com/documents/albums/ProfessionalHousePhotos005_4C2EF7B2601EF.jpg|http://www.castlepointehomes.com/documents/albums/KitchenLoft_22E1ED0B70188.jpg|http://www.castlepointehomes.com/documents/albums/4101NW163rdCirExterior_EA86D0620038B.jpg|http://www.castlepointehomes.com/documents/albums/5_9239445FCE6EE.jpg|http://www.castlepointehomes.com/documents/albums/Deck_9A104ABC973DA.jpg|http://www.castlepointehomes.com/documents/albums/16009PlumDrive014_6287576926D67.jpg"
        item2['SubWebsite'] = ''
        # item2['AmenityType'] = ''
        yield item2

        # -------------------------------------------------------------------- #


        # ------------------------------------ Extract_Plans ----------------------------#
        plan_urls = 'http://www.castlepointehomes.com/en/floor_plans/featured/'
        yield scrapy.Request(url=plan_urls, callback=self.plans_details,
                                 meta={'sbdn': self.builderNumber})

        # ---------------------------------------------------------------------------------#
    def plans_details(self, response):

        divs = response.xpath('//table[@border="0"]/tbody/tr')

        # ------------------------------------- Extracting Plans ------------------------- #
        for div in divs:
            try:
                Type = 'SingleFamily'
            except Exception as e:
                Type = 'SingleFamily'
                print(e)

            try:
                PlanName = div.xpath('.//td/h2//text()').extract()[0].strip()
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
                PlanTypeName = 'Single Family'
            except Exception as e:
                print(e)

            try:
                BasePrice = 0.00
            except Exception as e:
                print(e)

            try:
                BaseSqft = div.xpath('.//p/text()[3]').extract_first(default='0')
                BaseSqft = BaseSqft.split(':')[-1].strip()
                BaseSqft = BaseSqft.replace(',','')

            except Exception as e:
                print(e)

            try:
                Baths = div.xpath('.//p/text()[2]').extract_first(default='0')
                Baths = re.findall(r"(\d+)", Baths)[0]
                print(Baths)
                if len(Baths) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0

            except Exception as e:
                Baths = 0
                print(e)

            try:
                Bedrooms =  div.xpath('.//p/text()[1]').extract_first(default='0')
                Bedrooms = re.findall(r"(\d+)",Bedrooms)[0]
            except Exception as e:
                print(e)
                Bedrooms = 0


            try:
                Garage = 0.00
            except Exception as e:
                print(e)

            try:
                Description = ''
            except Exception as e:
                print(e)

            try:
                ElevationImage = div.xpath('.//td/a/img/@src').extract_first(default='')
            except Exception as e:
                print(e)
                ElevationImage = ""

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






if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl castlepointhomes'.split())