
# ------------- creating fake community --------------------------------------------#


# -*- coding: utf-8 -*-
import hashlib
import re
import time

import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class bmiconstruction(scrapy.Spider):
    name = 'bmiconstruction'
    allowed_domains = ['https://bmiconstruction.net/']
    start_urls = ['https://bmiconstruction.net/']

    builderNumber = "63657"


    def parse(self,response):

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '13406 Seymour Meyers'
        item['City'] = 'Covington'
        item['State'] = 'LA'
        item['ZIP'] = '70433'
        item['AreaCode'] = '985'
        item['Prefix'] = '792'
        item['Suffix'] = '9294'
        item['Extension'] = ""
        item['Email'] = 'brian@bmiconstruction.net'
        item['SubDescription'] = 'BMI Construction is a locally owned, trusted and licensed contractor offering reliable, personalized service and impeccable craftsmanship. Our mission is to set the standard for quality and service with your satisfaction as our top priority. BMI Construction is owned and operated by Brian Intravia. Brian grew up in the Covington area and learned the construction industry at a young age from his father, who is a longtime builder/developer in St. Tammany Parish. After graduating from St. Paul’s High School, he attended Louisiana State University where he received a BS in Civil Engineering. BMI Construction has been building homes in St. Tammany for 18 years. Brian uses his experience and a hands on approach to ensure each client’s new home is everything they expect and more. Brian currently lives in the Madisonville area with his wife and two children'
        item['SubImage'] = 'https://c3filedepot.jerichodev.com/bmiconstruction/files/banners/133_Natchez_Court_Banner.jpg|https://c3filedepot.jerichodev.com/bmiconstruction/files/banners/67502_Antioch_Banner.jpg|https://c3filedepot.jerichodev.com/bmiconstruction/files/banners/67614_Antioch_Banner.jpg|https://c3filedepot.jerichodev.com/bmiconstruction/files/banners/459_BEDICO_PARKWAY_Banner.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        links = response.xpath("//a[contains(text(),'Floor Plans')]/../ul/li/a/@href").extract()
        if links != []:
            links = links + ['/homes-for-sale']
        for link in links:
            link = 'https://bmiconstruction.net' + link
            print(link)
            yield scrapy.FormRequest(url=link,callback=self.plan,dont_filter=True)
        #
        # yield scrapy.FormRequest(url='https://bmiconstruction.net/homes-for-sale',callback=self.plan,dont_filter=True)


    def plan(self,response):
        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)


        divs = response.xpath('//div[@class="alternatable-property-info"]/div')
        for div in divs:


            try:
                price = div.xpath('.//div/div[2]/h3/text()').extract_first('')
                price = price.replace(",","")
                price = re.findall(r"(\d+)", price)[0]
            except Exception as e:
                price = 0

            try:
                PlanName = div.xpath('.//h4/text()').get()
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
                BasePrice = 0
            except Exception as e:
                print(e)

            try:

                sqft = div.xpath(".//span[contains(text(),'SQ. FT')]/../span/text()").extract_first('')
                # sqft = sqft.split("|")[0]
                sqft = sqft.replace(',', '').strip()
                if '.' in sqft:
                    sqft = sqft.split(".")[0]
                BaseSqft = re.findall(r"(\d+)", sqft)[0]

            except Exception as e:
                print(e)
                BaseSqft = ''

            try:
                bath = div.xpath(".//span[contains(text(),'BATHS')]/../span/text()").extract_first()
                if 'or' in bath:
                    bath = bath.split("or")[1]
                tmp = re.findall(r"(\d+)", bath)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                print(e)

            try:

                Bedrooms = div.xpath(".//span[contains(text(),'BEDS')]/../span/text()").extract_first('')
                if 'or' in Bedrooms:
                    Bedrooms = Bedrooms.split("or")[1]
                # Bedrooms = Bedrooms.split("|")[1].split("|")[0]
                Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            except Exception as e:
                print(e)

            try:
                Garage = div.xpath(".//span[contains(text(),'GARAGE')]/../span/text()").extract_first('')

                Garage = re.findall(r"(\d+)", Garage)[0]
            except Exception as e:
                print(e)
                Garage = 0

            try:
                # Description = 'BMI Construction is owned and operated by Brian Intravia. Brian grew up in the Covington area and learned the construction industry at a young age from his father, who is a longtime builder/developer in St. Tammany Parish. After graduating from St. Paul’s High School, he attended Louisiana State University where he received a BS in Civil Engineering. BMI Construction has been building homes in St. Tammany for 18 years. Brian uses his experience and a hands on approach to ensure each client’s new home is everything they expect and more.'
                Description = ''
            except Exception as e:
                print(e)
                Description = ''


            try:

                images1 = div.xpath('.//a[1]/@href').extract()
                images = []
                for id in images1:
                    images.append(id)
                ElevationImage = images

            except Exception as e:
                print(e)

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
            item['BasePrice'] = price
            item['BaseSqft'] = BaseSqft
            item['Baths'] = Baths
            item['HalfBaths'] = HalfBaths
            item['Bedrooms'] = Bedrooms
            item['Garage'] = Garage
            item['Description'] = Description
            item['ElevationImage'] = "|".join(ElevationImage)
            item['PlanWebsite'] = PlanWebsite
            yield item




if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl bmiconstruction'.split())