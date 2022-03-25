# -*- coding: utf-8 -*-
import hashlib
import re
import requests
import scrapy
from decimal import Decimal
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class cBiCustomHomesSpider(scrapy.Spider):
    name = 'cBi_Custom_Home'
    allowed_domains = ['http://www.cbicustomhomes.com/']
    start_urls = ['http://www.cbicustomhomes.com/']

    builderNumber = "24248"


    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #
        image1 = '|'.join(response.xpath('//table//div/img/@src').extract())
        image1 = self.start_urls[0] + image1.strip('|')
        image2 = []
        try:
            gallary_link = self.start_urls[0] + response.xpath('//*[contains(text(),"Gallery")]/@href').extract_first()
            res = requests.get(url=gallary_link)
            response1 = HtmlResponse(url=res.url, body=res.content)
            image_path = response1.xpath('//td//a/img/@src').extract()
            for image in image_path:
                image2.append(f"{self.start_urls[0]}{image}")
            image3 = '|'.join(image2)
        except Exception as e:
            print(e)
        images = image1+'|'+image3
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = "34 Washington Circle"
        item['City'] = "Lake Forest"
        item['State'] = "IL"
        item['ZIP'] = "60045"
        item['AreaCode'] = "847"
        item['Prefix'] = "652"
        item['Suffix'] = "1277"
        item['Extension'] = ""
        item['Email'] = "info@cbicustomhomes.com"
        item['SubDescription'] = ""
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        yield item

        try:
            link = self.start_urls[0] + response.xpath('//*[contains(text(),"Available Homes")]/@href').extract_first()
            PlanDetails = {}
            yield scrapy.Request(url=link,callback=self.plans_details,meta={'sbdn':self.builderNumber,'PlanDetails':PlanDetails},dont_filter=True)
        except Exception as e:
            print(e)

    # def parse_home(self,response):
    #     PN = response.meta['PlanDetails']
    #     sbdn = response.meta['sbdn']
    #     home_links = response.xpath('//td/a/@href').extract()
    #     for home_link in home_links:
    #         home_link = self.start_urls[0] + home_link
    #         yield scrapy.Request(url=str(home_link), callback=self.home_list, dont_filter=True, meta={"PN": PN,"sbdn": sbdn})

    def plans_details(self, response):
        try:
            plandetails = response.meta['PlanDetails']
            unique = str("Plan Unknown") + str(self.builderNumber)  # < -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
            plandetails["Plan Unknown"] = unique_number
            item = BdxCrawlingItem_Plan()
            item['unique_number'] = unique_number
            item['Type'] = "SingleFamily"
            item['PlanNumber'] = "Plan Unknown"
            item['SubdivisionNumber'] = self.builderNumber
            item['PlanName'] = "Plan Unknown"
            item['PlanNotAvailable'] = 1
            item['PlanTypeName'] = 'Single Family'
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

            home_links = response.xpath('//td/a/@href').extract()
            for home_link in home_links:
                home_link = self.start_urls[0] + home_link
                yield scrapy.Request(url=str(home_link), callback=self.home_list, dont_filter=True,meta={"PN": plandetails, "sbdn": response.meta['sbdn']})
        except Exception as e:
            print("process_home", e, response.url)

    def home_list(self,response):
        if response.xpath('//img[contains(@src,"availabletop.gif")]'):
            SpecStreet1 = response.xpath('//h3[contains(text(),"Available Home:")]/following-sibling::text()').extract_first().strip()
            csz = response.xpath('//h3[contains(text(),"Available Home:")]/following-sibling::br/following-sibling::text()').extract_first()
            SpecCity = csz.split(',')[0].strip()
            SpecState = csz.split(',')[1].split()[0].strip()
            SpecZIP = csz.split(',')[1].split()[1].strip()

            unique = SpecStreet1 + SpecCity + SpecState + SpecZIP + str(response.url)
            SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            PN = response.meta['PN']
            PlanNumber = PN['Plan Unknown']

            try:
                SpecCountry = "USA"
            except Exception as e:
                print(e)

            try:
                SpecPrice1 = response.xpath('//h3[contains(text(),"Price:")]/following-sibling::text()').extract_first(default='0').strip().replace(',','')
                if 'million' in SpecPrice1:
                    SpecPrice_list = re.findall(r"[0-9]*\.?[0-9]*", SpecPrice1)
                    for spec in SpecPrice_list:
                        if spec != '':
                            SpecPrice = str(Decimal(spec)*1000000)
                else:
                    SpecPrice = re.findall(r"(\d+)", SpecPrice1)[1]
            except Exception as e:
                print(e)

            try:
                SpecSqft = response.xpath('//h3[contains(text(),"Overall Square Footage:")]/following-sibling::text()').extract_first(default='0')
                SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
            except Exception as e:
                print(e)
            try:
                home_specification = response.xpath('//h3[contains(text(),"Home Specifications:")]/following-sibling::text()').extract()
                for home_spec in home_specification:
                    if "Bath" in home_spec:
                        if 'Full Baths' in home_spec and 'Half Baths' in home_spec:
                            SpecBaths = re.findall(r'(.*?)Full Baths',home_spec)[0].strip()
                            SpecHalfBaths = re.findall(r',(.*?)Half Baths',home_spec)[0].strip()
                            if '.' in SpecHalfBaths:
                                SpecHalfBaths = re.findall(r"(\d+)", SpecHalfBaths)[0]
                        else:
                            SpecBaths = home_spec.strip()
                            tmp = re.findall(r"(\d+)", SpecBaths)
                            SpecBaths = tmp[0]
                            if len(tmp) > 1:
                                SpecHalfBaths = 1
                            else:
                                SpecHalfBaths = 0
                    elif "Bedroom" in home_spec:
                        SpecBedrooms = re.findall(r"(\d+)", home_spec)[0]
            except Exception as e:
                print(e)

            try:
                MasterBedLocation = "Down"
            except Exception as e:
                print(e)

            try:
                SpecDescription = "As an award winning design and build firm, cBi Custom Homes has been recognized for its architectural integrity and historically pure designs and construction. For over 15 years, cBi has consistently provided each client with exceptional home value, exceeding client expectations."
            except Exception as e:
                print(e)

            try:
                ElevationImage = re.findall(r'SRC="availabletop.gif"(.*?)SRC="(.*?)"',response.text,re.DOTALL)[0][1]
                SpecElevationImage = 'http://www.cbicustomhomes.com/' + ElevationImage
            except Exception as e:
                print(e)

            try:
                SpecWebsite = response.url
            except Exception as e:
                print(e)

            try:
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = PlanNumber
                item['SpecStreet1'] = SpecStreet1
                item['SpecCity'] = SpecCity
                item['SpecState'] = SpecState
                item['SpecZIP'] = SpecZIP
                item['SpecCountry'] = SpecCountry
                item['SpecPrice'] = SpecPrice
                item['SpecSqft'] = SpecSqft
                item['SpecBaths'] = SpecBaths
                item['SpecHalfBaths'] = SpecHalfBaths
                item['SpecBedrooms'] = SpecBedrooms
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = 0
                item['SpecDescription'] = SpecDescription
                item['SpecElevationImage'] = SpecElevationImage
                item['SpecWebsite'] = SpecWebsite
                yield item
            except Exception as e:
                print(e)


from scrapy.cmdline import execute
# execute("scrapy crawl cBi_Custom_Home".split())