
# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'arvolabuilders'
    allowed_domains = ['http://arvolabuilders.com/']
    start_urls = ['http://arvolabuilders.com/']

    builderNumber = "62788"

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
        item['Street1'] = '532 Walnut Street'
        item['City'] = 'Monticello'
        item['State'] = 'MN'
        item['ZIP'] = '55362'
        item['AreaCode'] = '615'
        item['Prefix'] ='799'
        item['Suffix'] = '5391'
        item['Extension'] = ""
        item['Email'] = 'chad@arvolabuilders.com'
        item['SubDescription'] = 'Arvola Builders was founded in 2002 by Chad and Katie Arvola.  We have built a reputation of building quality homes by using quality materials, providing excellent workmanship and focusing on attention to detail.   We offer a variety of plans to choose from with our Town, Country and Cottage Series homes.  Whether you are looking for your first home,  a move-up home or a cottage style home, we have the options to build a quality home for you'
        item['SubImage'] = 'https://storage.googleapis.com/production-hostgator-v1-0-5/685/260685/0O8VI62n/d687c5f861e64165a7da3b3867a3b156'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'http://arvolabuilders.com/town-series'


        #---------------------------------------------------------------------------------------------------------------#

        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        PlanName = 'The Albion II'

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
            PlanWebsite = 'http://arvolabuilders.com/town-series'
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
        item['BaseSqft'] = '1412'
        item['Baths'] = '2'
        item['HalfBaths'] = '0'
        item['Bedrooms'] = '3'
        item['Garage'] = '0'
        item['Description'] = 'Arvola Builders was founded in 2002 by Chad and Katie Arvola.  We have built a reputation of building quality homes by using quality materials, providing excellent workmanship and focusing on attention to detail.   We offer a variety of plans to choose from with our Town, Country and Cottage Series homes.  Whether you are looking for your first home,  a move-up home or a cottage style home, we have the options to build a quality home for you'
        item['ElevationImage'] ='https://storage.googleapis.com/production-hostgator-v1-0-5/685/260685/0O8VI62n/d687c5f861e64165a7da3b3867a3b156'
        item['PlanWebsite'] = PlanWebsite
        yield item

        # --------------------------------------------------------------------- #

        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        PlanName = 'The Henshaw'

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
            PlanWebsite = 'http://arvolabuilders.com/town-series'
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
        item['BaseSqft'] = '1288'
        item['Baths'] = '2'
        item['HalfBaths'] = '0'
        item['Bedrooms'] = '2'
        item['Garage'] = '0'
        item[
            'Description'] = 'Arvola Builders was founded in 2002 by Chad and Katie Arvola.  We have built a reputation of building quality homes by using quality materials, providing excellent workmanship and focusing on attention to detail.   We offer a variety of plans to choose from with our Town, Country and Cottage Series homes.  Whether you are looking for your first home,  a move-up home or a cottage style home, we have the options to build a quality home for you'
        item[
            'ElevationImage'] = 'https://storage.googleapis.com/production-hostgator-v1-0-5/685/260685/0O8VI62n/d687c5f861e64165a7da3b3867a3b156'
        item['PlanWebsite'] = PlanWebsite
        yield item

        #=======================================================================#

        # --------------------------------------------------------------------- #

        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        PlanName = 'The Somers'

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
            PlanWebsite = 'http://arvolabuilders.com/town-series'
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
        item['BaseSqft'] = '1928'
        item['Baths'] = '2'
        item['HalfBaths'] = '1'
        item['Bedrooms'] = '3'
        item['Garage'] = '0'
        item[
            'Description'] = 'Arvola Builders was founded in 2002 by Chad and Katie Arvola.  We have built a reputation of building quality homes by using quality materials, providing excellent workmanship and focusing on attention to detail.   We offer a variety of plans to choose from with our Town, Country and Cottage Series homes.  Whether you are looking for your first home,  a move-up home or a cottage style home, we have the options to build a quality home for you'
        item[
            'ElevationImage'] = 'https://storage.googleapis.com/production-hostgator-v1-0-5/685/260685/0O8VI62n/d687c5f861e64165a7da3b3867a3b156'
        item['PlanWebsite'] = PlanWebsite
        yield item

        #--------------------------------------------------------------------------------#

        # --------------------------------------------------------------------- #

        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        PlanName = 'The Bertrum'

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
            PlanWebsite = 'http://arvolabuilders.com/town-series'
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
        item['BaseSqft'] = '1574'
        item['Baths'] = '2'
        item['HalfBaths'] = '0'
        item['Bedrooms'] = '3'
        item['Garage'] = '0'
        item[
            'Description'] = 'Arvola Builders was founded in 2002 by Chad and Katie Arvola.  We have built a reputation of building quality homes by using quality materials, providing excellent workmanship and focusing on attention to detail.   We offer a variety of plans to choose from with our Town, Country and Cottage Series homes.  Whether you are looking for your first home,  a move-up home or a cottage style home, we have the options to build a quality home for you'
        item[
            'ElevationImage'] = 'https://storage.googleapis.com/production-hostgator-v1-0-5/685/260685/0O8VI62n/d687c5f861e64165a7da3b3867a3b156'
        item['PlanWebsite'] = PlanWebsite
        yield item

        # --------------------------------------------------------------------------------#

        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        PlanName = 'The Augusta'

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
            PlanWebsite = 'http://arvolabuilders.com/town-series'
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
        item['BaseSqft'] = '1636'
        item['Baths'] = '2'
        item['HalfBaths'] = '0'
        item['Bedrooms'] = '3'
        item['Garage'] = '0'
        item[
            'Description'] = 'Arvola Builders was founded in 2002 by Chad and Katie Arvola.  We have built a reputation of building quality homes by using quality materials, providing excellent workmanship and focusing on attention to detail.   We offer a variety of plans to choose from with our Town, Country and Cottage Series homes.  Whether you are looking for your first home,  a move-up home or a cottage style home, we have the options to build a quality home for you'
        item[
            'ElevationImage'] = 'https://storage.googleapis.com/production-hostgator-v1-0-5/685/260685/0O8VI62n/d687c5f861e64165a7da3b3867a3b156'
        item['PlanWebsite'] = PlanWebsite
        yield item

        # --------------------------------------------------------------------------------#

        # --------------------------------------------------------------------------------#

        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        PlanName = 'The Millstone'

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
            PlanWebsite = 'http://arvolabuilders.com/town-series'
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
        item['BaseSqft'] = '1538'
        item['Baths'] = '2'
        item['HalfBaths'] = '1'
        item['Bedrooms'] = '3'
        item['Garage'] = '0'
        item['Description'] = 'Arvola Builders was founded in 2002 by Chad and Katie Arvola.  We have built a reputation of building quality homes by using quality materials, providing excellent workmanship and focusing on attention to detail.   We offer a variety of plans to choose from with our Town, Country and Cottage Series homes.  Whether you are looking for your first home,  a move-up home or a cottage style home, we have the options to build a quality home for you'
        item[
            'ElevationImage'] = 'https://storage.googleapis.com/production-hostgator-v1-0-5/685/260685/0O8VI62n/d687c5f861e64165a7da3b3867a3b156'
        item['PlanWebsite'] = PlanWebsite
        yield item

        # --------------------------------------------------------------------------------#

        # --------------------------------------------------------------------- #

        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        PlanName = 'The Somers'

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
            PlanWebsite = 'http://arvolabuilders.com/town-series'
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
        item['BaseSqft'] = '1928'
        item['Baths'] = '2'
        item['HalfBaths'] = '1'
        item['Bedrooms'] = '3'
        item['Garage'] = '0'
        item['Description'] = 'Arvola Builders was founded in 2002 by Chad and Katie Arvola.  We have built a reputation of building quality homes by using quality materials, providing excellent workmanship and focusing on attention to detail.   We offer a variety of plans to choose from with our Town, Country and Cottage Series homes.  Whether you are looking for your first home,  a move-up home or a cottage style home, we have the options to build a quality home for you'
        item['ElevationImage'] = 'https://storage.googleapis.com/production-hostgator-v1-0-5/685/260685/0O8VI62n/d687c5f861e64165a7da3b3867a3b156'
        item['PlanWebsite'] = PlanWebsite
        yield item

        # --------------------------------------------------------------------------------#

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl arvolabuilders'.split())