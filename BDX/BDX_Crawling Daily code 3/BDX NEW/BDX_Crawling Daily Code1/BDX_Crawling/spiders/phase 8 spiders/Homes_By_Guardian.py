# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class HomesByGuardianSpider(scrapy.Spider):
    name = 'Homes_By_Guardian'
    allowed_domains = ['www.homesbyguardian.com']
    start_urls = []

    builderNumber = "51052"
    def start_requests(self):
        url = 'https://www.homesbyguardian.com/communities'
        header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Upgrade-Insecure-Requests": "1",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Mobile Safari/537.36",
            "Connection": "keep-alive"}
        yield scrapy.FormRequest(url=url, callback=self.communityDetails,headers=header)

       ####  Fake community
    def communityDetails(self, response):
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
        item['Street1'] = '1103 Old Town Ln, Suite 200, Office #20'
        item['City'] = 'Cheyenne'
        item['State'] = 'WY'
        item['ZIP'] = '82009'
        item['AreaCode'] = '307'
        item['Prefix'] = '201'
        item['Suffix'] = '3876'
        item['Extension'] = ""
        item['Email'] = 'contact@guardiancompanies.com'
        item['SubDescription'] = ''.join(response.xpath('//div[@class="fl-module fl-module-rich-text fl-node-5eb07f8828eb5"]//div[@class="fl-rich-text"]/p/text()').extract())
        images = response.xpath('//div[@class="fl-module-content fl-node-content"]//div[@class="fl-photo fl-photo-align-center"]//img/@src').extract()
        item['SubImage'] = "|".join(images)
        item['SubWebsite'] = response.url
        yield item

        #     # ------------------- If Plan Found found ------------------------- #
        #
        # SubdivisionNumber = SubdivisionNumber #if subdivision is there
        Sub_links = response.xpath('//div[@class="fl-module-content fl-node-content"]//div[@class="fl-photo fl-photo-align-center"]//a/@href').extract()

        for Sub_links in Sub_links:
            url =Sub_links
            header = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Upgrade-Insecure-Requests": "1",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Mobile Safari/537.36",
                "Connection": "keep-alive"}
            yield scrapy.FormRequest(url=url, callback=self.plan_url, headers=header)

    def plan_url(self, response):
        plan_links = response.xpath('//div[@class="fl-button-wrap fl-button-width-auto fl-button-left"]/a[@class="fl-button"]/../a/@href').extract()
        for plan_links in plan_links:
            url1 = plan_links
            header = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Upgrade-Insecure-Requests": "1",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Mobile Safari/537.36",
                "Connection": "keep-alive"}
            yield scrapy.FormRequest(url=url1, callback=self.plan_details, headers=header)

    def plan_details(self, response):
        PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
        f = open("html/%s.html" % PlanNumber, "wb")
        f.write(response.body)
        f.close()

        try:
            planname=response.xpath('//*/h3/text()').extract_first()
            planname=planname.replace("Floor Plan","").strip()
        except Exception as e:
            print(e)

        try:
            Bedrooms1 = response.xpath('//table[@style="width: 100%; border-collapse: collapse; border-style: none;"]//tr/td//*[contains(text(),"Bedrooms:")]/../following-sibling::td/text()').extract_first().strip()
            tmp = re.findall(r"(\d+)", Bedrooms1)
            max_all = max(tmp)
            print("The maximum bedroom : " + str(max_all))
            Bedrooms1 = ''.join(max_all)
        except Exception as e:
            Bedrooms1 = 0
            print(e)

        try:
            bathrooms1 = response.xpath('//table[@style="width: 100%; border-collapse: collapse; border-style: none;"]//tr/td//*[contains(text(),"Baths:")]/../following-sibling::td/text()').extract_first().strip()
            if "." and "-" in str(bathrooms1):
                bathrooms11 = bathrooms1.split('-')
                max_all1 = max(bathrooms11)
                print("The maximum of bathroom : " + str(max_all1))
                bathrooms = max_all1
            else:
                bathrooms1 = re.findall(r"(\d+)", bathrooms1)
                max_all1 = max(bathrooms1)
                print("The maximum of bathroom : " + str(max_all1))
                bathrooms = ''.join(max_all1)

            tmp = max_all1
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            bathrooms = 0
            HalfBaths = 0

        try:
            Garage = response.xpath('//table[@style="width: 100%; border-collapse: collapse; border-style: none;"]//tr/td//*[contains(text(),"Garage:")]/../following-sibling::td/text()').extract_first().strip()
            if "." and "-" in str(Garage):
                Garage = Garage.split('-')
                max_Garage = max(Garage)
                print("The maximum of Garage: " + str(max_Garage))
                Garage = max_Garage
            else:
                tmp = re.findall(r"(\d+)", Garage)
                Garage = tmp[0]
        except Exception as e:
            Garage = 0


        try:
            feet = response.xpath('//table[@style="width: 100%; border-collapse: collapse; border-style: none;"]//tr/td//*[contains(text(),"Square Footage:")]/../following-sibling::td/text()').extract_first().strip()
            feet = ''.join(feet).replace(",", "").strip()
            feet = re.findall(r"(\d+)", feet)
            max_all2 = max(feet)
            print(str(max_all2))
            feet = max_all2
        except Exception as e:
            feet = 0
            print(e)

        try:
            Price = str(response.xpath('//table[@style="width: 100%; border-collapse: collapse; border-style: none;"]//tr/td//*[contains(text(),"Price Range:")]/../following-sibling::td/text()').extract_first(default='0').strip()).replace(",", "")
            Price = re.findall(r"(\d+)", Price)[0]
        except Exception as e:
            Price=0

        PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
        SubdivisionNumber = self.builderNumber  # if subdivision is there
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)


        try:
            Decs2 = response.xpath('//div/h3/..//p/text()').extract_first()
            Description= Decs2.strip(',')
        except Exception as e:
            Description = ''

        webContent=response.text
        try:
            bunch=""
            if "<script type=\"text/javascript" in str(webContent):
                bunch = webContent.split("<script type=\"text/javascript", 1)[1]
                bunch = bunch.split("id=\'fl-builder-layout-", 1)[0]
                bunch=re.sub('[\t]|\n|\s\s+|\r', ' ', str(bunch))
        except Exception as e:
            print("bunch Not found")

        try:
            imgurl = re.findall("<script src='https://www.homesbyguardian.com/wp-content/uploads/bb-plugin/cache/(.*?)'", bunch)
            imgurl=''.join(imgurl)
            if imgurl!='':
                imgurl="https://www.homesbyguardian.com/wp-content/uploads/bb-plugin/cache/" + imgurl
            print(imgurl)
        except Exception as e:
            imgurl=""


        if imgurl!="":
            header = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Upgrade-Insecure-Requests": "1",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Mobile Safari/537.36",
                "Connection": "keep-alive"}
            yield scrapy.FormRequest(url=imgurl, callback=self.plan_images, headers=header,meta={'PlanNumber': PlanNumber,
                                       'unique_number': unique_number, 'SubdivisionNumber': SubdivisionNumber, 'planname': planname,'feet':feet,'bathrooms':bathrooms,'HalfBaths':HalfBaths,'Bedrooms1':Bedrooms1,'Price':Price,'Garage':Garage,'link':response.url,'Description':Description})

    def plan_images(self, response):

        try:
            images = re.findall(',x3largeURL:"(.*?)"', response.text, re.DOTALL)
            ElevationImage = "|".join(images)
        except Exception as e:
            ElevationImage = ''

        item = BdxCrawlingItem_Plan()
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = response.meta['PlanNumber']
        item['unique_number'] = response.meta['unique_number']
        item['SubdivisionNumber'] = response.meta['SubdivisionNumber']
        item['PlanName'] = response.meta['planname']
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = response.meta['Price']
        item['BaseSqft'] = response.meta['feet']
        item['Baths'] = response.meta['bathrooms']
        item['HalfBaths'] = response.meta['HalfBaths']
        item['Bedrooms'] = response.meta['Bedrooms1']
        item['Garage'] = response.meta['Garage']
        item['Description']=response.meta['Description']
        item['ElevationImage']=ElevationImage
        item['PlanWebsite'] = response.meta['link']

        yield item


# from scrapy.cmdline import execute
# execute("scrapy crawl Homes_By_Guardian".split())

