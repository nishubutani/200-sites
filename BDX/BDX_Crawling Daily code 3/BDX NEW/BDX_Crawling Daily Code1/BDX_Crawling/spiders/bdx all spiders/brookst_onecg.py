
# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'brookst_onecg'
    allowed_domains = ['https://quotes.toscrape.com/']
    # start_urls = ['https://www.brookstonecg.com/']

    builderNumber = "63676"

    # ------------------- Creating Communities ---------------------- #


    def start_requests(self):
        link = 'https://www.brookstonecg.com'

        self.headers = {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'accept-language': "en-US,en;q=0.9",
            'cookie': "dm_timezone_offset=-330; dm_last_visit=1619690523291; dm_total_visits=1; _gid=GA1.2.1084072090.1619690524; dm_last_page_view=1619692683377; dm_this_page_view=1619692686439; _sp_id.67b3=6110abac5684784d.1619690524.1.1619692686.1619690524; _sp_ses.67b3=1619694486458; _ga=GA1.1.363675064.1619690524; _ga_E9H555DN8F=GS1.1.1619690523.1.1.1619693454.0",
            'sec-ch-ua': "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        }

        yield scrapy.FormRequest(url=link,callback=self.parse,dont_filter=True,headers=self.headers)

    def parse(self, response):

        images = ''
        image = response.xpath('//img/@src').extract()[5:15]
        for i in image:
            images = images + i + '|'
        images = images.strip('|')
        print(images)

        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionName'] = "No Sub Division"
        item2['SubdivisionNumber'] = self.builderNumber
        item2['BuilderNumber'] = self.builderNumber
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        item2['Street1'] = ' 1645 GA Hwy 138'
        item2['City'] = 'Monroe'
        item2['State'] = 'GA'
        item2['ZIP'] = '30655'
        item2['AreaCode'] = '678'
        item2['Prefix'] = '251'
        item2['Suffix'] = '8029'
        item2['Extension'] = ""
        item2['Email'] = 'info@brookstonecg.com'
        item2['SubDescription'] = 'Brookstone Construction Group is a family owned and operated company with over 20 years of custom homes and commercial construction experience. We value what it truly means to feel like family, and we will do our best to build not just a house, but a home.'
        item2['SubImage'] = images
        item2['SubWebsite'] = response.url
        item2['AmenityType'] = ''
        yield item2

        link = 'https://www.brookstonecg.com/home-ideas'
        yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True,headers=self.headers)

    def parse2(self,response):

        links = response.xpath('//li[@class="listItem"]/a/@href').extract()
        for link in links:
            link = 'https://www.brookstonecg.com' + link
            print(link)
            yield scrapy.FormRequest(url=link,callback=self.parse3,dont_filter=True,headers=self.headers)
            # yield scrapy.FormRequest(url='https://www.brookstonecg.com/home-plan/51778hz',callback=self.parse3,dont_filter=True,headers=self.headers)


    def parse3(self,response):


        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//p[@class="rteBlock"]/text()').get()
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
            sqft = response.xpath("//span[contains(text(),'SQUARE FEET')]/../../../div[2]/p/text()").extract_first('')
            # sqft = sqft.split("|")[0]
            sqft = sqft.replace(',', '').replace(".","").strip()
            BaseSqft = re.findall(r"(\d+)", sqft)[0]

        except Exception as e:
            print(e)
            BaseSqft = ''

        try:
            bath = response.xpath("//span[contains(text(),'BATHROOMS')]/../../../div/p/text()").extract_first()
            if '-' in bath:
                bath = bath.split("-")[1]
            tmp = re.findall(r"(\d+)", bath)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            print(e)

        try:
            Bedrooms = response.xpath("//span[contains(text(),'BEDROOMS')]/../../../div/p/text()").extract_first()
            if '-' in Bedrooms:
                Bedrooms = Bedrooms.split("-")[1]
            # Bedrooms = Bedrooms.split("|")[1].split("|")[0]
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)

        try:
            Garage = 0
        except Exception as e:
            Garage = 0
            print(e)


        # Description = 'Brookstone Construction Group is a family owned and operated company with over 20 years of custom homes and commercial construction experience. We value what it truly means to feel like family, and we will do our best to build not just a house, but a home.'
        Description = ''

        try:

            # images1 = response.xpath('//li[@class="dmCoverImgContainer"]/img/@src').extract()
            #
            # images2 = response.xpath('//div[@class="u_1929991324 imageWidget align-center"]/a/img/@src').extract_first('')
            images = []
            imagedata = response.xpath("//img/@src").extract()
            for id in imagedata:
                id = id
                images.append(id)
            ElevationImage = images
            print(ElevationImage)
        except Exception as e:
            print(e)

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

            # ----------------------- Don't change anything here --------------
        unique = str(PlanNumber) + str(SubdivisionNumber) + str(Baths) + str(Bedrooms) #< -------- Changes here
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
        item['ElevationImage'] = "|".join(ElevationImage)
        item['PlanWebsite'] = PlanWebsite
        yield item

        link = 'https://www.brookstonecg.com/available-homes'
        yield scrapy.FormRequest(url=link,callback=self.home_link,dont_filter=True,headers=self.headers)

    def home_link(self,response):
        links = response.xpath('//li[@class="listItem"]/a/@href').extract()
        for link in links:
            link = 'https://www.brookstonecg.com' + link
            yield scrapy.FormRequest(url=link,callback=self.home,dont_filter=True,headers=self.headers)

    def home(self,response):
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

        try:
            try:
                SpecStreet1 = response.xpath('//div[@class="dmNewParagraph u_1704736164"]/text()').extract_first('')
                SpecStreet1 = SpecStreet1.split(",")[0].strip()
            except Exception as e:
                print(e)

            try:
                add = response.xpath('//div[@class="dmNewParagraph u_1704736164"]/text()').extract_first('')
                print(add)
            except Exception as e:
                print(e)

            try:
                SpecC = add.split(",")[1].strip().split(",")[0]
                SpecCity = SpecC
            except Exception as e:
                print(e)

            try:
                SpecState = add.split(",")[2]
                SpecState = SpecState.strip()
                SpecState = SpecState.split(" ")[0]
            except Exception as e:
                print(e)

            try:
                SpecZIP = add.split(",")[1].strip()
                SpecZIP = SpecZIP.strip()
                SpecZIP = SpecZIP.split(" ")[1]
            except Exception as e:
                SpecZIP = '00000'




            try:
                PlanNumber = self.builderNumber
            except Exception as e:
                print(e)

            try:
                SpecCountry = "USA"
            except Exception as e:
                print(e)

            try:
                price = response.xpath("//span[contains(text(),'PRICE')]/../../../div/p/span/span/text()").extract_first('')
                price = price.replace(",","")
                price = re.findall(r"(\d+)", price)[0]
            except Exception as e:
                print(e)
                price = ''


            try:
                SpecBedrooms = response.xpath("//span[contains(text(),'BEDROOMS')]/../../../div/p/span/span/text()").extract_first('')
                if '-' in SpecBedrooms:
                    SpecBedrooms = SpecBedrooms.split("-")[1]
                    print(SpecBedrooms)
                SpecBedrooms = re.findall(r"(\d+)", SpecBedrooms)[0]
            except Exception as e:
                print(str(e))

            try:
                SpecBaths = response.xpath("//span[contains(text(),'BATHROOMS')]/../../../div/p/span/span/text()").extract_first('')
                if '-' in SpecBaths:
                    SpecBaths = SpecBaths.split("-")[1]
                tmp = re.findall(r"(\d+)", SpecBaths)
                SpecBaths = tmp[0]
                if len(tmp) > 1:
                    halfbath = 1
                else:
                    halfbath = 0
            except Exception as e:
                print(str(e))

            try:
                SpecGarage = 0
            except Exception as e:
                print(str(e))

            try:
                SpecSqft = response.xpath("//span[contains(text(),'SQUARE FEET')]/../../../div[2]/p/span/span/text()").extract_first('')
                SpecSqft = SpecSqft.replace(",","")
                # SpecSqft = SpecSqft.split("•")[-1].replace(",", "")
                SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
            except Exception as e:
                print(str(e))

            try:
                MasterBedLocation = "Down"
            except Exception as e:
                print(e)

            try:
                SpecDescription = 'Brookstone Construction Group is a family owned and operated company with over 20 years of custom homes and commercial construction experience. We value what it truly means to feel like family, and we will do our best to build not just a house, but a home.'
            except Exception as e:
                print(e)

            try:
                specElevation = []
                image = response.xpath(
                    '//img/@src').extract()
                for i in image:
                    specElevation.append(i)
                ElevationImage = "|".join(specElevation)
            except Exception as e:
                print(e)

            try:
                SpecWebsite = response.url
            except Exception as e:
                print(e)

            unique = SpecStreet1 + SpecCity + SpecState + SpecZIP + SpecSqft
            print(unique)
            SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)


            f = open("html/%s.html" % SpecNumber, "wb")
            f.write(response.body)
            f.close()

            # ----------------------- Don't change anything here --------------------- #
            item = BdxCrawlingItem_Spec()
            item['SpecNumber'] = SpecNumber
            item['PlanNumber'] = unique_number
            item['SpecStreet1'] = SpecStreet1
            item['SpecCity'] = SpecCity
            item['SpecState'] = SpecState
            item['SpecZIP'] = SpecZIP
            item['SpecCountry'] = SpecCountry
            item['SpecPrice'] = price
            item['SpecSqft'] = SpecSqft
            item['SpecBaths'] = SpecBaths
            item['SpecHalfBaths'] = halfbath
            item['SpecBedrooms'] = SpecBedrooms
            item['MasterBedLocation'] = MasterBedLocation
            item['SpecGarage'] = SpecGarage
            item['SpecDescription'] = SpecDescription
            item['SpecElevationImage'] = ElevationImage
            item['SpecWebsite'] = SpecWebsite
            yield item

        except Exception as e:
            print(e)



    # --------------------------------------------------------------------- #

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl brookst_onecg'.split())