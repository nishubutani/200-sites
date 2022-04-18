# -*- coding: utf-8 -*-
import hashlib
import re

import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class createHomesSpider(scrapy.Spider):
    name = 'Homecreatehome'
    allowed_domains = []
    start_urls = ['https://www.homecretehomes.com/']

    builderNumber = "16319"

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
        item['Street1'] = '3174 SW Savona Blvd'
        item['City'] = 'Port St Lucie'
        item['State'] = 'FL'
        item['ZIP'] = '34953'
        item['AreaCode'] = '772'
        item['Prefix'] = '248'
        item['Suffix'] = '4663'
        item['Extension'] = ""
        item['Email'] = 'info@homecretehomes.com'
        item['SubDescription'] = 'Homecrete Homes is your local Port St. Lucie home builder with a reputation of excellence – Homecrete has TWICE been awarded TCBA’s Builder of the Year Award. We believe in building YOUR home, not ours – providing you with the customization and modifications you need to make your new home just the way you imagine it.'
        item['SubImage'] = 'https://www.homecretehomes.com/wp-content/uploads/2020/04/3174sw-savona-model-pano-800px.jpg|https://www.homecretehomes.com/wp-content/uploads/2020/06/1.png|https://www.homecretehomes.com/wp-content/uploads/2020/06/1.png|https://www.homecretehomes.com/wp-content/uploads/2020/06/1.png|https://www.homecretehomes.com/wp-content/uploads/2020/06/1.png'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        plan_links = ['https://www.homecretehomes.com/new-home-builder-port-st-lucie',
                    'https://homecretehomes.com/custom-homes/']
        for plan_link in plan_links:
            yield scrapy.Request(url=plan_link, callback=self.parse3,dont_filter=True)

    def parse3(self, response):

        links = response.xpath('//div[@class="elementor-button-wrapper"]/a/span/span[contains(text(),"Detail")]/../../@href').extract()
        for link in links:
            yield scrapy.FormRequest(url=link, callback=self.parse4, dont_filter=True)

    def parse4(self, response):

        try:
            PlanName = response.xpath('//h1/text()|//h2/text()').extract_first('')
        except Exception as e:
            print("PlanName: ", e)

        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = self.builderNumber
            print(SubdivisionNumber)
        except Exception as e:
            print(str(e))

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
            print(str(e))

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

        try:
            Bedroo = response.xpath('//*[contains(text(),"Bed")]/text()').extract_first('').replace("\n", "").strip()
            if 'or' in Bedroo:
                Bedroo = Bedroo.split("or")[0]
            Bedrooms = re.findall(r"(\d+)", Bedroo)[0]
        except Exception as e:
            Bedrooms = 0
            print("Bedrooms: ", e)

        try:
            Bathroo = response.xpath('//*[contains(text(),"Bath")]/text()').extract_first('').strip().replace("\n",
                                                                                                                 "").strip()
            tmp = re.findall(r"(\d+)", Bathroo)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0

        except Exception as e:
            Baths = 0
            print("Baths: ", e)

        try:
            # desc = "".join(response.xpath('//div[@class="centered_content"]/div/div/text()').extract()).replace("\n","").strip()
            desc = ''
            # print(desc)
        except Exception as e:
            print(e)
            desc = ''

        try:
            Garage = response.xpath('//*[contains(text(),"Garage")]/text()').extract_first('').strip().replace(',', '')
            Garage = re.findall(r"(\d+)", Garage)[0]
            Garage = 0
        except Exception as e:
            print("Garage: ", e)
            Garage = 0

        try:
            BaseSqft = response.xpath('//*[contains(text(),"Sq")]/text()').extract_first('').strip().replace(',','')
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
        except Exception as e:
            print("BaseSQFT: ", e)

        try:
            ElevationImages = []
            ElevationImage2 = response.xpath('//div[@class="jet-engine-gallery-grid__item"]/a/@href').extract()
            if ElevationImage2 != []:
                for image in ElevationImage2:
                    # image = 'https://homesbydeesign.com/' + image
                    ElevationImages.append(image)
                # ElevationImages.append(ElevationImage1)

            ElevationImage = "|".join(ElevationImages)

        except Exception as e:
            print(str(e))
            ElevationImage = ""

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
        item['Description'] = desc
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item

    #
    #
    #     url='https://www.homecretehomes.com/custom-home-builder/'
    #     yield scrapy.Request(url=url, callback=self.home_details,dont_filter=True)
    #
    # def home_details(self, response):
    #
    #     unique = str("Plan Unknown") + str(self.builderNumber)  # < -------- Changes here
    #     unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
    #                 10 ** 30)  # < -------- Changes here
    #     item = BdxCrawlingItem_Plan()
    #     item['unique_number'] = unique_number
    #     item['Type'] = "SingleFamily"
    #     item['PlanNumber'] = "Plan Unknown"
    #     item['SubdivisionNumber'] = self.builderNumber
    #     item['PlanName'] = "Plan Unknown"
    #     item['PlanNotAvailable'] = 1
    #     item['PlanTypeName'] = 'Single Family'
    #     item['BasePrice'] = 0
    #     item['BaseSqft'] = 0
    #     item['Baths'] = 0
    #     item['HalfBaths'] = 0
    #     item['Bedrooms'] = 0
    #     item['Garage'] = 0
    #     item['Description'] = ""
    #     item['ElevationImage'] = ""
    #     item['PlanWebsite'] = ""
    #     yield item
    #
    #     home = re.findall('<h3><span style="color: #215411;">(.*?)jpg" ></a>', response.text, re.DOTALL)
    #     for k in home:
    #
    #         try:
    #             SpecStreet1 =  re.findall('(.*?)</span>',k)[0].strip()
    #
    #             SpecCity="Port St Lucie"
    #             SpecState = "FL"
    #             SpecZIP= '34953'
    #
    #             web= re.findall('href="(.*?)"',k,re.DOTALL)
    #             webiste=web[1]
    #
    #
    #             ig=re.findall('data-options="thumbnail: (.*?)"',k,re.DOTALL)
    #             image=ig[1].replace("\'","").replace('\\','')
    #
    #             unique = SpecStreet1 + SpecCity + SpecState + SpecZIP + webiste
    #             SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
    #
    #             f = open("html/%s.html" % SpecNumber, "wb")
    #             f.write(response.body)
    #             f.close()
    #
    #         except Exception as e:
    #             print(e)
    #
    #         try:
    #             SpecBedrooms = re.findall('<li><strong>(.*?)Bedroom',k)[0].strip()
    #             print(SpecBedrooms)
    #         except Exception as e:
    #             print(str(e))
    #
    #         try:
    #             SpecBaths = re.findall('Bedroom plus office,(.*?)full baths',k)[0].strip()
    #             if '.' in SpecBaths:
    #                 print(response.url)
    #
    #         except Exception as e:
    #             print(str(e))
    #
    #
    #         try:
    #             SpecGarage = re.findall('baths,(.*?)car',k)[0].strip()
    #
    #         except Exception as e:
    #             print(str(e))
    #
    #
    #         Sft= ''.join(re.findall('conditioned space(.*?)total square feet',k,re.DOTALL))
    #         SpecSqft = ''.join(re.findall('(\d+)',Sft,re.DOTALL))
    #         print(SpecSqft)
    #
    #         try:
    #             MasterBedLocation = "Down"
    #         except Exception as e:
    #             print(e)
    #
    #         try:
    #             SpecDescription = "At Homecrete Homes our philosophy is simple — Your Home, Built Better! To achieve this we offer the latest technology at affordable prices in the construction of Green – High Performance Energy – Sustainable homes. The environmentally friendly and sustainable homes we build focus on efficient use of energy, water and building materials. As a green builder we offer a variety of features and materials to help to improve your improve your living environment and your quality fo life."
    #         except Exception as e:
    #             print(e)
    #
    #
    #         # ----------------------- Don't change anything here --------------------- #
    #         item = BdxCrawlingItem_Spec()
    #         item['SpecNumber'] = SpecNumber
    #         item['PlanNumber'] = unique_number
    #         item['SpecStreet1'] = SpecStreet1
    #         item['SpecCity'] = SpecCity
    #         item['SpecState'] = SpecState
    #         item['SpecZIP'] = SpecZIP
    #         item['SpecCountry'] = "USA"
    #         item['SpecPrice'] = 0.00
    #         item['SpecSqft'] = SpecSqft
    #         item['SpecBaths'] = SpecBaths
    #         item['SpecHalfBaths'] = 0
    #         item['SpecBedrooms'] = SpecBedrooms
    #         item['MasterBedLocation'] = MasterBedLocation
    #         item['SpecGarage'] = SpecGarage
    #         item['SpecDescription'] = SpecDescription
    #         item['SpecElevationImage'] = image
    #         item['SpecWebsite'] = webiste
    #         yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl Homecreatehome".split())