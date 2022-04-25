# -*- coding: utf-8 -*-
import hashlib
import re

import requests
import scrapy
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class BigelowhomesSpider(scrapy.Spider):
    name = 'bigelowhomes'
    allowed_domains = ['www.bigelowhomes.net']
    start_urls = ['http://www.bigelowhomes.net/']
    builderNumber = '57258'

    def parse(self, response):
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
        item['Street1'] = '4057 28TH ST. NW SUITE 100'
        item['City'] = 'ROCHESTER'
        item['State'] = 'MN'
        item['ZIP'] = '55901'
        item['AreaCode'] = '507'
        item['Prefix'] = '529'
        item['Suffix'] = '1161'
        item['Extension'] = ""
        item['Email'] = 'bigelow@bigelowhomes.net'
        item['SubDescription'] = "What makes building a home with Bigelow Homes different and unique? We deliver homes with innovative and affordable design, built around the way you live, and personalized to your specific needs. Our team provides a home building experience with unmatched integrity, and personalized service. The Bigelow Homes team is dedicated to helping you design, build, and move into the home of your dreams with the peace of mind of our long-standing reputation for quality and financial stability. So if you're ready for a home building experience like no other, then get ready to experience Bigelow Homes."
        image = ['http://www.bigelowhomes.net/images/banner1.jpg','http://www.bigelowhomes.net/images/banner2.jpg','http://www.bigelowhomes.net/images/banner3.jpg','http://www.bigelowhomes.net/images/banner4.jpg']
        item['SubImage'] = '|'.join(image)
        item['SubWebsite'] = response.url
        item['AmenityType'] = ""
        yield item

        url = "http://www.bigelowhomes.net/tour.php"

        payload = "sort=plotPrice&sortDir=ASC&searchPlotPrice_min=%240&searchPlotPrice_max=No+Limit&searchStyles=&searchSubdivisions=&searchStatus=4&searchCity=City+name.&searchLot=Lot+No.&searchAddress=Address&searchBedrooms=&searchBathrooms=&searchGarage=&searchSQFT=&task=06a943c59f33a34bb5924aaf72cd2995"
        headers = {
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,gu;q=0.7',
            'Connection': 'keep-alive',
            'Content-Length': '288',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': '__utmz=137462563.1648980640.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); fpestid=hSGc2mTVJQ9mhlmNfZOa2UDdib0J-orgb0peDpjUMwfCYdTNq7TFcZRe67TyLmzei4TsKg; __utma=137462563.2059437150.1648980640.1650302542.1650464162.3; __utmc=137462563; PHPSESSID=l5fca394um7s871u5rco8l6ai3; __utmb=137462563.4.10.1650464162; PHPSESSID=2lms5ht20fjam6q1i0uvvtmbr3',
            'Host': 'www.bigelowhomes.net',
            'Origin': 'http://www.bigelowhomes.net',
            'Referer': 'http://www.bigelowhomes.net/tour.php',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response1 = HtmlResponse(url=response.url, body=response.content)
        divs = response1.xpath('//div[@class="resultItem"]')

        for div in divs:

            Type = 'SingleFamily'

            try:
                plan_link = div.xpath('./@onclick').extract_first('')
                plan_link = re.findall(r"(\d+)", plan_link)[0]
                plan_link = 'http://www.bigelowhomes.net/tour.php?modelID=' + plan_link
            except Exception as e:
                print(e)
                plan_link = ''

            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,gu;q=0.7',
                'Connection': 'keep-alive',
                'Cookie': '__utmz=137462563.1648980640.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); fpestid=hSGc2mTVJQ9mhlmNfZOa2UDdib0J-orgb0peDpjUMwfCYdTNq7TFcZRe67TyLmzei4TsKg; __utma=137462563.2059437150.1648980640.1650468302.1650706633.5; __utmc=137462563; PHPSESSID=ni7u8gn15qm8078iq85lol4085; __utmt=1; __utmb=137462563.12.10.1650706633',
                'Host': 'www.bigelowhomes.net',
                'Referer': 'http://www.bigelowhomes.net/tour.php',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
            }

            response22 = requests.request("POST", plan_link, headers=headers, data=payload)
            response2 = HtmlResponse(url=response22.url, body=response22.content)
            # open_in_browser(response2)

            try:
                PlanName = response2.xpath("//strong[contains(text(),'Address')]/../text()").get().strip()
            except Exception as e:
                print(e)

            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
            SubdivisionNumber = self.builderNumber
            PlanNotAvailable = 0
            PlanTypeName = 'Single Family'

            try:
                BasePrice = div.xpath(".//span[contains(text(),'PRICE')]/../text()").get().replace(",","")
                if BasePrice == "N/A" :
                    BasePrice = '0'
                else:
                    BasePrice = re.findall(r"(\d+)", BasePrice)[0]
            except Exception as e:
                print(e)
                BasePrice = '0'

            try:
                BaseSqft = div.xpath(".//span[contains(text(),'SQFT')]/../text()").get().replace(",","")
                BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
            except Exception as e:
                print(e)
                BaseSqft = "0"

            try:

                tmp = div.xpath('.//span[contains(text(),"BA")]/../text()').get().strip()
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                print(e)

            try:
                Bedrooms = div.xpath('.//span[contains(text(),"BR")]/../text()').get().strip()
            except Exception as e:
                print(e)

            try:
                Garage = div.xpath('.//span[contains(text(),"GAR")]/../text()').get().strip()
            except Exception as e:
                print(e)

                # ----------------------- Don't change anything here ---------------- #
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
            item['Description'] = ''
            item['ElevationImage'] = ''
            item['PlanWebsite'] = response.url
            yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl bigelowhomes".split())

