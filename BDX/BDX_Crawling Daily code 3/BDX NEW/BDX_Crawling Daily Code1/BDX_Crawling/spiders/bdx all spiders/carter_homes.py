# -*- coding: utf-8 -*-
import hashlib
import re

import requests
import scrapy
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class carterhomesSpider(scrapy.Spider):
    name = 'carter_homes'
    allowed_domains = ['www.carterhomesofutah.com/']
    start_urls = ['http://carterhomesofutah.com/gallery/']
    builderNumber = 24010

    def parse(self, response):

        images = ''
        image = response.xpath('//div[@class="envira-gallery-item-inner"]/a/@href').extract()
        for i in image:
            images = images + i + '|'
        images = images.strip('|')
        print(images)


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
        item['Street1'] = 'PO Box 48038'
        item['City'] = 'Salt'
        item['State'] = 'UT'
        item['ZIP'] = '84037'
        item['AreaCode'] = '801'
        item['Prefix'] = '668'
        item['Suffix'] = '8494'
        item['Extension'] = ""
        item['Email'] = ''
        item[
            'SubDescription'] = 'Carter Homes of Utah builds a wide spectrum of Northern Utahs housing needs from starter homes, move-ups, custom homes, town homes and apartments. We serve the Counties of Northern Utah; Davis, Weber, Morgan, and Box Elder. Give us a call today for more information about your new home!'
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        url = 'http://carterhomesofutah.com/home-designs/'
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.plandetail,
                                 meta={'sbdn': self.builderNumber})

    def parse_planlink(self, response):

        try:
            links = response.xpath('//a[@class="home-design-title"]/@href').extract()
            plandetains = {}
            for link in links:
                yield scrapy.Request(url=self.start_urls[0] + str(link), callback=self.plans_details,
                                     meta={'sbdn': self.builderNumber, 'PlanDetails': plandetains}, dont_filter=True)
        except Exception as e:
            print(e)

    def plandetail(self, response):
        divs = response.xpath('//section[@class="homes_for_sale_wrap"]/div/div/div')
        for div in divs:

            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                SubdivisionNumber = response.meta['sbdn']
            except Exception as e:
                print(e)

            try:
                PlanName = div.xpath('.//a/h2/text()').extract_first(default='').strip()
                print(PlanName)
            except Exception as e:
                print(e)

            try:
                PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
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

            try:

                Baths = str(div.xpath(
                    './/div[@class="home-design-content"]//li[6]').extract_first(
                    default='0').strip()).replace(",", "")
                Baths = re.sub('<[^<]+?>', '', str(Baths))
                tmp = re.findall(r"(\d+)", Baths)
                Baths = re.findall(r'(\d+)', Baths)[0]
                print(Baths)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                print(e)

            try:
                Bedrooms = str(div.xpath(
                    './/div[@class="home-design-content"]//li[5]').extract_first(
                    default='0').strip()).replace(",", "")
                Bedrooms = re.sub('<[^<]+?>', '', str(Bedrooms))
                Bedrooms = re.findall(r'(\d+)', Bedrooms)[0]
                print(Bedrooms)
            except Exception as e:
                print(e)

            try:

                Garage = 0.0
                print(Garage)

                BaseSqft = str(div.xpath(
                    './/div[@class="home-design-content"]//li[2]').extract_first(
                    default='0').strip()).replace(",", "")

                BaseSqft = re.sub('<[^<]+?>', '', str(BaseSqft))
                # BaseSqft =BaseSqft.split(' squar')[-2]
                # BaseSqft = BaseSqft.split(" ")[-1]
                BaseSqft = re.findall(r'(\d+)', BaseSqft)[0]
                print(BaseSqft)
            except Exception as e:
                print(e)

            # try:
            #     Description = div.xpath('.//div[@class="home-design-content"]//li[4]/text()').extract_first(
            #         default='').strip()
            #     print(Description)
            # except Exception as e:
            #     print(e)



            url = div.xpath('.//article/a/@href').extract_first()
            print(url)

            # '//div[@class="row"]//img/@src'



            response1 = requests.request("GET", url)
            response1 = HtmlResponse(url=url, body=response1.content)
            image = response1.xpath('//div[@class="row"]//img/@src').extract()
            print(image)


            Elevationimage = []
            for i in image:
                if 'logo.png' not in i:
                    Elevationimage.append(i)

            print(Elevationimage)
            Elevationimage =  "|".join(Elevationimage)
            print(Elevationimage)


            desc = response1.xpath('//div[@class="homedesign_desc"]/p/text()').extract_first('')
            print(desc)

            if desc == '':
                Description = 'Call us at 801-668-8494 to request pricing'
            else:
                Description = desc


            #
            # try:
            #     PlanWebsite = response.url
            # except Exception as e:
            #     print(e)

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
            print(item['Baths'])
            item['HalfBaths'] = HalfBaths
            print(item['HalfBaths'])
            item['Bedrooms'] = Bedrooms
            item['Garage'] = Garage
            item['Description'] = Description
            item['ElevationImage'] = Elevationimage
            item['PlanWebsite'] = url
            yield item



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl carter_homes'.split())