# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'aa_newhomes'
    allowed_domains = ['http://aa-newhomes.com/']
    # start_urls = ['http://aa-newhomes.com/']
    start_urls = ['http://aa-newhomes.com/find-your-new-home/lohr-woods/']

    builderNumber = "62064"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        #------- creating community -----------------------------#

        subdivisonName = 'Lohr Woods'
        street1 = 'St James Blvd'


        # ------------------------------------------#
        # ab = []
        try:
            aminity = response.text
            aminity = aminity.title()
        except Exception as e:
            print(e)
        amenity_list = ["Pool", "Playground", "GolfCourse", "Tennis", "Soccer", "Volleyball", "Basketball",
                        "Baseball", "Views", "Lake", "Pond", "Marina", "Beach", "WaterfrontLots", "Park",
                        "Trails", "Greenbelt", "Clubhouse", "CommunityCenter"]
        a = list()
        for i in amenity_list:
            # print(i)
            if i in aminity:
                # print(i)
                a.append(i)
        ab = '|'.join(a)

        subdivisonNumber = int(hashlib.md5(bytes(subdivisonName + response.url, "utf8")).hexdigest(), 16) % (10 ** 30)

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = subdivisonNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = subdivisonName
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = street1
        item['City'] = 'Ann Arbor'
        item['State'] = 'MI'
        item['ZIP'] = '48108'
        item['AreaCode'] = '734'
        item['Prefix'] = '996'
        item['Suffix'] = '9456'
        item['Extension'] = ""
        item['Email'] = 'louis@lkforest.com'
        item['SubDescription'] = 'Situated in the heart of Pittsfield Township Lohr Woods is an up and coming neighborhood with a lot to offer. Prices from 400,000’s we have a wide range of custom plans available. Abundance of wooded lots and wild life views'
        item['SubImage'] = 'http://aa-newhomes.com/wp-content/uploads/2014/01/dsc_0057.jpg|http://aa-newhomes.com/wp-content/uploads/2014/02/Oaktree-view-back-36.jpg|http://aa-newhomes.com/wp-content/uploads/2014/01/Lohr-Woods-logo-alpha.png'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ab
        yield item

        # link = 'http://aa-newhomes.com/'
        # yield scrapy.FormRequest(url=link,callback=self.community,dont_filter=True)


        # def community(self,response):
        #
        #
        #     images = ''
        #     image = response.xpath('//@src').extract()
        #     for i in image:
        #         images = images + i + '|'
        #     images = images.strip('|')
        #
        #     item = BdxCrawlingItem_subdivision()
        #     item['sub_Status'] = "Active"
        #     item['SubdivisionNumber'] = ''
        #     item['BuilderNumber'] = self.builderNumber
        #     item['SubdivisionName'] = "No Sub Division"
        #     item['BuildOnYourLot'] = 0
        #     item['OutOfCommunity'] = 0
        #     item['Street1'] = '725 W. Ellsworth Road'
        #     item['City'] = 'Ann Arbor'
        #     item['State'] = 'MI'
        #     item['ZIP'] = '48108'
        #     item['AreaCode'] = '734'
        #     item['Prefix'] ='996'
        #     item['Suffix'] = '9456'
        #     item['Extension'] = ""
        #     item['Email'] = 'louis@lkforest.com'
        #     item['SubDescription'] = 'JOHNSON BUILDING GROUP/HIGHPOINTE BUILDERS is a well-established building company in Ann Arbor, and the exclusive builder in the Lohr Woods neighborhood. Located in Pittsfield Township, off Lohr road, near Ellsworth, Lohr Woods offers 50 oversized homes sites, most of which back up to open space. Home sites are base...'
        #     item['SubImage'] = images
        #     item['SubWebsite'] = response.url
        #     item['AmenityType'] = ''
        #     yield item


        links = response.xpath('//ul[@class="sub-menu"]/li/a/@href').extract()
        for link in links:
            yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True,meta={'subdivisonNumber':subdivisonNumber})


    def parse2(self,response):

        subdivisonNumber = response.meta['subdivisonNumber']
        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//h1/text()').get()
        except Exception as e:
            PlanName = ''
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName  + response.url, "utf8")).hexdigest(), 16) % (
                        10 ** 30)
        except Exception as e:
            PlanNumber = ''
            print(e)

        try:
            SubdivisionNumber = subdivisonNumber
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
            sqft = response.xpath('//span[@class="ruler-icon"]/text()').get()
            sqft = sqft.replace(',', '').strip()
            BaseSqft = re.findall(r"(\d+)", sqft)[0]

        except Exception as e:
            print(e)

        try:
            bath = response.xpath('//span[@class="bath-icon"]/text()').get()
            tmp = re.findall(r"(\d+)", bath)[0]
            Baths = tmp[0]
            if len(str(tmp)) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            print(e)

        try:
            Bedrooms = response.xpath('//span[@class="bed-icon"]/text()').get()
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)

        try:
            Garage = response.xpath('//span[@class="garage-icon"]/text()').get()
            Garage = re.findall(r"(\d+)", Garage)[0]
            if not Garage:
                Garage = 0
        except Exception as e:
            Garage = 0
            print(e)

        try:
            Description = ''.join(
                response.xpath('//div[@class="description"]/p/text()').getall())
            if not Description:
                Description = ''
        except Exception as e:
            print(e)

        try:
            images = []
            imagedata = response.xpath('//div[@class="tiled-gallery-item tiled-gallery-item-large"]/a/@href').getall()
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
        item['Description'] = Description
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item


        # --------------------------------------------------------------------- #


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl aa_newhomes'.split())