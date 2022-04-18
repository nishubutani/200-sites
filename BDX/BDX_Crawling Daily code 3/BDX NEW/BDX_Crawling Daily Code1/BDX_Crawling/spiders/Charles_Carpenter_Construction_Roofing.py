# -*- coding: utf-8 -*-
import hashlib
import json
import re
import requests
import scrapy
from decimal import Decimal
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class CharlesCarpenterConstructionRoofingSpider(scrapy.Spider):
    name = 'charles_carpenter_construction_roofing'
    allowed_domains = ['http://charlescarpenterhomes.com/']
    start_urls = ['http://charlescarpenterhomes.com/']

    builderNumber = "24380"


    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #
        image = response.xpath('//img[@data-image-id="54ecdad5e4b0feaa477efd11"]/@data-src').extract_first()
        images = image.strip('|')
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = "693 Caribbean Road"
        item['City'] = "Satellite Beach"
        item['State'] = "FL"
        item['ZIP'] = "32937"
        item['AreaCode'] = ""
        item['Prefix'] = ""
        item['Suffix'] = ""
        item['Extension'] = ""
        item['Email'] = ""
        about_url = "http://charlescarpenterhomes.com" + response.xpath('//*[contains(text(),"About Us")]/@href').extract_first()
        res_a = requests.get(url=about_url)
        response_a = HtmlResponse(url=res_a.url, body=res_a.content)
        item['SubDescription'] = ' '.join(response_a.xpath('//*[@class="sqs-block-content"]/p/text()').extract()).strip()
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        try:
            link = "http://charlescarpenterhomes.com" + response.xpath('//*[contains(text(),"Models")]/@href').extract_first()
            PlanDetails = {}
            yield scrapy.Request(url=link,callback=self.plans_details,meta={'sbdn':self.builderNumber,'PlanDetails':PlanDetails},dont_filter=True)
        except Exception as e:
            print(e)

    def plans_details(self, response):
        plandetails = response.meta['PlanDetails']
        all_details = response.xpath('//*[@class="project gallery-project"]//*[@class="project-description"]')
        for detail in all_details:
            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                SubdivisionNumber = response.meta['sbdn']
            except Exception as e:
                print(e)

            try:
                PlanName = detail.xpath('./../h2/text()').extract_first()
            except Exception as e:
                print(e)

            try:
                plan_link = detail.xpath('./../../@data-url').extract_first()
                PlanWebsite = f"{response.url}#{plan_link}"
            except Exception as e:
                print(e)

            try:
                PlanNumber = int(hashlib.md5(bytes(PlanWebsite, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % PlanNumber, "wb")
                f.write(response.body)
                f.close()
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
                BasePrice = '0'
            except Exception as e:
                print(e)


            plan_description = ' '.join(detail.xpath('.//text()').extract())
            try:
                Baths = re.findall(r'Full Baths\s?~\s?(.*?)\s',plan_description)[0].strip()
                Baths = re.findall(r"(\d+)", Baths)[0]
            except Exception as e:
                print(e)
                Baths = '0'

            try:
                HalfBaths = re.findall(r'Half Baths\s?~\s?(.*?)\s',plan_description)[0].strip()
                HalfBaths = re.findall(r"(\d+)", HalfBaths)[0]
            except Exception as e:
                print(e)
                HalfBaths = 0

            try:
                Bedrooms = re.findall(r'Bedrooms\s?~\s?(.*?)\s',plan_description)[0].strip()
            except Exception as e:
                print(e)
                Bedrooms = '0'

            try:
                Garage = re.findall(r'Garage Type\s?~\s?(.*?)Car',plan_description)[0].strip()
            except Exception as e:
                print(e)
                Garage = 0

            try:
                if re.findall(r'TOTAL\s?~\s?(.*?)sq.ft',plan_description) != []:
                    BaseSqft = re.findall(r'TOTAL\s?~\s?(.*?)sq.ft',plan_description)[0].replace(',','').strip()
                elif re.findall(r'Total\s?~\s?(.*?)sq.ft',plan_description) != []:
                    BaseSqft = re.findall(r'Total\s?~\s?(.*?)sq.ft', plan_description)[0].replace(',', '').strip()
                else:
                    BaseSqft = '0'
            except Exception as e:
                print(e)
                BaseSqft = '0'

            try:
                Description = detail.xpath('./p/text()').extract_first().strip()
                if "Number of Stories " in Description:
                    Description = detail.xpath('./p/span[@style="font-size:11px"]/text()').extract_first().strip()
            except Exception as e:
                print(e)

            try:
                ElevationImage1 = detail.xpath('./../../*[@class="image-list"]//img/@src').extract_first().strip()
                try:floorplanImage = detail.xpath('./../../*[@class="image-list"]//img[contains(@alt,"FP-")]/@data-src').extract_first().strip()
                except:floorplanImage = ''
                if floorplanImage != '':
                    ElevationImage = ElevationImage1 + '|' + floorplanImage
                else:
                    ElevationImage = ElevationImage1
            except Exception as e:
                print(e)

            SubdivisionNumber = SubdivisionNumber  # if subdivision is there
            # SubdivisionNumber = self.builderNumber #if subdivision is not available
            unique = str(PlanNumber) + str(SubdivisionNumber)
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            plandetails[PlanName] = unique_number
            item = BdxCrawlingItem_Plan()
            item['Type'] = Type
            item['PlanNumber'] = PlanNumber
            item['unique_number'] = unique_number
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
    execute("scrapy crawl charles_carpenter_construction_roofing".split())