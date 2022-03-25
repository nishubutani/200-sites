# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from word2number import w2n
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class BrittainAndWhiteSpider(scrapy.Spider):
    name = 'Brittain_and_White'
    allowed_domains = ['www.brittainwhite.com']
    start_urls = []

    builderNumber = "52812"

    def start_requests(self):
        url = 'http://www.brittainwhite.com/townhomes_condos.shtml'
        header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Upgrade-Insecure-Requests": "1",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Referer": "http://www.brittainwhite.com/customhomes.shtml",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Mobile Safari/537.36",
            "Connection": "keep-alive"}
        yield scrapy.FormRequest(url=url, callback=self.communityDetails, headers=header)

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
        item['Street1'] = '5521 Jackson Street'
        item['City'] = 'Alexandria'
        item['State'] = 'LA'
        item['ZIP'] = '71303'
        item['AreaCode'] = '318'
        item['Prefix'] = '442'
        item['Suffix'] = '0221'
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = ''.join(response.xpath('//font[@id="content7"]//text()').extract())
        images = response.xpath('//td[@width="455"]//table[@cellspacing="0"]//tr//td//a//img//@src').extract()
        item['SubImage'] =str('|'.join(["http://www.brittainwhite.com/" + img for img in images]))
        item['SubWebsite'] = response.url
        yield item

        #     # ------------------- If Plan Found found ------------------------- #
        #
        # SubdivisionNumber = SubdivisionNumber #if subdivision is there
        plan_links = response.xpath('//div[@style="position:relative; left:20;"]/a/@href').extract()
        plan_name = response.xpath('//div[@style="position:relative; left:20;"]/a/text()').extract()
        for plan_links,plan_name in zip(plan_links,plan_name):
            url = "http://www.brittainwhite.com/" + plan_links
            # url="http://www.brittainwhite.com/modelc.shtml"
            plan_name=plan_name
            header = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Upgrade-Insecure-Requests": "1",
                # "Referer": "http://www.brittainwhite.com/customhomes.shtml",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Mobile Safari/537.36",
                "Connection": "keep-alive"}
            yield scrapy.FormRequest(url=url, callback=self.plan_details, headers=header,meta={'plan_name':plan_name})


    def plan_details(self, response):
        PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
        f = open("html/%s.html" % PlanNumber, "wb")
        f.write(response.body)
        f.close()

        PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
        SubdivisionNumber = self.builderNumber  # if subdivision is there
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

        try:
            planname = response.meta['plan_name']
        except Exception as e:
            print(e)

        try:
            Decs2 = ''.join(response.xpath('//table[@cellspacing="0"][@cellpadding="0"][@border="0"][@id="content9"]//tr//td//text()').extract())
            Decs2 = re.sub('[\t]|\n|\s\s+|\r', ' ', str(Decs2))
            Description = Decs2.strip()
        except Exception as e:
            Description = ''

        if "model" in str(response.url):
            try:
                Bedrooms1 = response.xpath('//font[@id="content12"]/text()').extract()
                try:
                    Bedrooms2=Bedrooms1[0]
                    Bedrooms2 = re.sub('[\t]|\n|\s\s+|\r', ' ', str(Bedrooms2))
                    Bedrooms = re.findall('(.*?)Bedroom', Bedrooms2)[0].strip()
                    Bathroom = re.findall(',(.*?)Bath', Bedrooms2)[0].strip()
                except Exception as e:
                    Bedrooms=0
                    Bathroom=0

                try:
                     bunch=Bedrooms1[1]
                     bunch = re.sub('[\t]|\n|\s\s+|\r', ' ', str(bunch))
                     a = re.findall(r"(\d+)", bunch)
                except Exception as e:
                    print(e)

                try:
                    bunch2 = Bedrooms1[2]
                    bunch2 = re.sub('[\t]|\n|\s\s+|\r', ' ', str(bunch2))
                    b = re.findall(r"(\d+)", bunch2)
                except Exception as e:
                    print(e)

                max_all = (max(a, b))
                print("The maximum feet : " + str(max_all))
                feet = ''.join(max_all)
            except Exception as e:
                feet = 0
                print(e)

            try:
                images1 = response.xpath('//font[@id="content11"]/../img/@src').extract()
                ElevationImage =str('|'.join(["http://www.brittainwhite.com/" + img for img in images1]))
            except Exception as e:
                ElevationImage = ''

            try:
                Garage =Description.split('Enclosed, attached', 1)[1]
                Garage=Garage.split('-car garage', 1)[0].strip()
                Garage = (w2n.word_to_num(Garage))
            except Exception as e:
                Garage = 0

        else:

            Bedrooms1 = response.xpath('//font[@id="content9"]/text()').extract()
            try:
                Bedrooms2 = Bedrooms1[0]
                Bedrooms2 = re.sub('[\t]|\n|\s\s+|\r', ' ', str(Bedrooms2))
                Bedrooms = re.findall('(.*?)Bedroom', Bedrooms2)[0].strip()
                Bathroom = re.findall('/(.*?)Bath', Bedrooms2)[0].strip()
            except Exception as e:
                Bedrooms = 0
                Bathroom = 0

            try:
                bunch = Bedrooms1[1]
                bunch = re.sub('[\t]|\n|\s\s+|\r', ' ', str(bunch))
                tmp = re.findall(r"(\d+)", bunch)
                feet = ''.join(tmp)
            except Exception as e:
                feet=0


            try:
                images =response.xpath('//td[@width="195"][@align="center"][@valign="top"]/table//tr/td/a/@href').extract()
                ElevationImage1 =str('|'.join(["http://www.brittainwhite.com/" + img for img in images]))
            except Exception as e:
                ElevationImage1 = ''
            try:
                images1 = response.xpath('//*[@style="border: solid 2px #09588b;"]/../img/@src').extract()
                ElevationImage2 =str('|'.join(["http://www.brittainwhite.com/" + img for img in images1]))
            except Exception as e:
                ElevationImage2 = ''

            ElevationImage = ElevationImage1 + "|" + ElevationImage2
            ElevationImage = ElevationImage.strip('|')
            Garage=0
        item = BdxCrawlingItem_Plan()
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = planname
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0
        item['BaseSqft'] =feet
        item['Baths'] = Bathroom
        item['HalfBaths'] =0
        item['Bedrooms'] = Bedrooms
        item['Garage'] =Garage
        item['Description'] =Description
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = response.url

        yield item

# from scrapy.cmdline import execute
# execute("scrapy crawl Brittain_and_White".split())


