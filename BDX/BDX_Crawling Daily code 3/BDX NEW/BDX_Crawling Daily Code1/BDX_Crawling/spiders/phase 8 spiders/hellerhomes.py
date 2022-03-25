# -*- coding: utf-8 -*-
import hashlib
import json
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header


class DannysullivanconstructionComSpider(scrapy.Spider):
    name = 'hellerhomes'
    allowed_domains = []
    start_urls = ['https://hellersite.com/communities/']
    builderNumber = 28368

    def parse(self, response):
        # glinks = response.xpath(
        #     '//div[@class="so-widget-sow-button so-widget-sow-button-wire-2a6ce404a150"]/div/a/@href').extract()
        # for glink in glinks:
        #     glin = glink.split('https://www.google.com/maps/place/')[1]
        #     glink = glin.split('/@')[0]
        #     glink = glink.replace("+", " ")
        #     subdivisonName = response.xpath('//div[@class="sow-headline-container "]/h5/text()').extract_first(
        #         default="")
        #     subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
        #     f = open("html/%s.html" % subdivisonNumber, "wb")
        #     f.write(response.body)
        #     f.close()
        #     street1 = glink.split(',')[0]
        #     city = glink.split(',')[-2]
        #     state = glink.split(',')[-1].strip().split(' ')[0]
        #     try:
        #         zipcode = glink.split(',')[-1].strip().split(' ')[-1]
        #     except:
        #         zipcode = ''
        #     item2 = BdxCrawlingItem_subdivision()
        #     item2['sub_Status'] = "Active"
        #     item2['SubdivisionName'] = subdivisonName
        #     item2['SubdivisionNumber'] = subdivisonNumber
        #     item2['BuilderNumber'] = self.builderNumber
        #     item2['BuildOnYourLot'] = 0
        #     item2['OutOfCommunity'] = 1
        #     item2['Street1'] = street1
        #     item2['City'] = city
        #     item2['State'] = state
        #     item2['ZIP'] = zipcode
        #     item2['AreaCode'] = ""
        #     item2['Prefix'] = ""
        #     item2['Suffix'] = ""
        #     item2['Extension'] = ""
        #     item2['Email'] = ""
        #     item2[
        #         'SubDescription'] = "Not looking to build in a subdivision? No problem! Heller Homes builds in both subdivisions and rural properties in Allen County and the surrounding counties."
        #     item2['SubImage'] = ""
        #     item2['SubWebsite'] = response.url
        #     yield item2
        for i in range(1, 9):
            if i == 1:
                subdivisonName = 'Lone Oak'
                subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % subdivisonNumber, "wb")
                f.write(response.body)
                f.close()
                item2 = BdxCrawlingItem_subdivision()
                item2['sub_Status'] = "Active"
                item2['SubdivisionName'] = subdivisonName
                item2['SubdivisionNumber'] = subdivisonNumber
                item2['BuilderNumber'] = self.builderNumber
                item2['BuildOnYourLot'] = 0
                item2['OutOfCommunity'] = 1
                item2['Street1'] = '10085-9249 Bass Rd'
                item2['City'] = 'Fort Wayne'
                item2['State'] = 'IN'
                item2['ZIP'] = '46818'
                item2['AreaCode'] = ''
                item2['Prefix'] = ''
                item2['Suffix'] = ''
                item2['Extension'] = ""
                item2['Email'] = ""
                item2[
                    'SubDescription'] = 'Heller Homes builds in both subdivisions and rural properties in Allen County and the surrounding counties.'
                item2[
                    'SubImage'] = "https://i2.wp.com/hellersite.com/wp-content/uploads/2019/06/IMG_4431.jpg?fit=1024%2C773&ssl=1"
                item2['SubWebsite'] = response.url
                yield item2

            elif i == 2:
                subdivisonName = 'Palmira Lakes'
                subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % subdivisonNumber, "wb")
                f.write(response.body)
                f.close()
                item2 = BdxCrawlingItem_subdivision()
                item2['sub_Status'] = "Active"
                item2['SubdivisionName'] = subdivisonName
                item2['SubdivisionNumber'] = subdivisonNumber
                item2['BuilderNumber'] = self.builderNumber
                item2['BuildOnYourLot'] = 0
                item2['OutOfCommunity'] = 1
                item2['Street1'] = 'Palmira Blvd'
                item2['City'] = 'Aboite Township'
                item2['State'] = 'IN'
                item2['ZIP'] = '46818'
                item2['AreaCode'] = ''
                item2['Prefix'] = ''
                item2['Suffix'] = ''
                item2['Extension'] = ""
                item2['Email'] = ""
                item2[
                    'SubDescription'] = 'Heller Homes builds in both subdivisions and rural properties in Allen County and the surrounding counties.'
                item2[
                    'SubImage'] = "https://i2.wp.com/hellersite.com/wp-content/uploads/2020/01/Palmira-Lakes-Sign.jpg?fit=314%2C233&ssl=1"
                item2['SubWebsite'] = response.url
                yield item2
            elif i == 3:
                subdivisonName = 'Prairie Meadows'
                subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % subdivisonNumber, "wb")
                f.write(response.body)
                f.close()
                item2 = BdxCrawlingItem_subdivision()
                item2['sub_Status'] = "Active"
                item2['SubdivisionName'] = subdivisonName
                item2['SubdivisionNumber'] = subdivisonNumber
                item2['BuilderNumber'] = self.builderNumber
                item2['BuildOnYourLot'] = 0
                item2['OutOfCommunity'] = 1
                item2['Street1'] = 'Prairie Meadows Dr'
                item2['City'] = 'Roanoke'
                item2['State'] = 'IN'
                item2['ZIP'] = '46783'
                item2['AreaCode'] = ''
                item2['Prefix'] = ''
                item2['Suffix'] = ''
                item2['Extension'] = ""
                item2['Email'] = ""
                item2[
                    'SubDescription'] = 'Heller Homes builds in both subdivisions and rural properties in Allen County and the surrounding counties.'
                item2[
                    'SubImage'] = "https://i0.wp.com/hellersite.com/wp-content/uploads/2017/11/prarie-meadows.jpg?fit=267%2C200&ssl=1"
                item2['SubWebsite'] = response.url
                yield item2
            elif i == 4:
                subdivisonName = 'NW - Rolling Oaks'
                subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % subdivisonNumber, "wb")
                f.write(response.body)
                f.close()
                item2 = BdxCrawlingItem_subdivision()
                item2['sub_Status'] = "Active"
                item2['SubdivisionName'] = subdivisonName
                item2['SubdivisionNumber'] = subdivisonNumber
                item2['BuilderNumber'] = self.builderNumber
                item2['BuildOnYourLot'] = 0
                item2['OutOfCommunity'] = 1
                item2['Street1'] = 'Kell Rd & W Shoaff Rd'
                item2['City'] = 'Perry Township'
                item2['State'] = 'IN'
                item2['ZIP'] = '46748'
                item2['AreaCode'] = ''
                item2['Prefix'] = ''
                item2['Suffix'] = ''
                item2['Extension'] = ""
                item2['Email'] = ""
                item2[
                    'SubDescription'] = 'Heller Homes builds in both subdivisions and rural properties in Allen County and the surrounding counties.'
                item2[
                    'SubImage'] = "https://i2.wp.com/hellersite.com/wp-content/uploads/2018/05/AVAILABLE-LOGO.jpg?fit=319%2C233&ssl=1"
                item2['SubWebsite'] = response.url
                yield item2
            elif i == 5:
                subdivisonName = 'NW - Edenbridge'
                subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % subdivisonNumber, "wb")
                f.write(response.body)
                f.close()
                item2 = BdxCrawlingItem_subdivision()
                item2['sub_Status'] = "Active"
                item2['SubdivisionName'] = subdivisonName
                item2['SubdivisionNumber'] = subdivisonNumber
                item2['BuilderNumber'] = self.builderNumber
                item2['BuildOnYourLot'] = 0
                item2['OutOfCommunity'] = 1
                item2['Street1'] = 'Edenbridge Boulevard'
                item2['City'] = 'Fort Wayne'
                item2['State'] = 'IN'
                item2['ZIP'] = '46845'
                item2['AreaCode'] = ''
                item2['Prefix'] = ''
                item2['Suffix'] = ''
                item2['Extension'] = ""
                item2['Email'] = ""
                item2[
                    'SubDescription'] = 'Heller Homes builds in both subdivisions and rural properties in Allen County and the surrounding counties.'
                item2[
                    'SubImage'] = "https://i1.wp.com/hellersite.com/wp-content/uploads/2017/11/Edenbridge.jpg?fit=265%2C200&ssl=1"
                item2['SubWebsite'] = response.url
                yield item2
            elif i == 6:
                subdivisonName = 'NE - Valencia'
                subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % subdivisonNumber, "wb")
                f.write(response.body)
                f.close()
                item2 = BdxCrawlingItem_subdivision()
                item2['sub_Status'] = "Active"
                item2['SubdivisionName'] = subdivisonName
                item2['SubdivisionNumber'] = subdivisonNumber
                item2['BuilderNumber'] = self.builderNumber
                item2['BuildOnYourLot'] = 0
                item2['OutOfCommunity'] = 1
                item2['Street1'] = 'Valencia Pl'
                item2['City'] = 'Fort Wayne'
                item2['State'] = 'IN'
                item2['ZIP'] = '46835'
                item2['AreaCode'] = ''
                item2['Prefix'] = ''
                item2['Suffix'] = ''
                item2['Extension'] = ""
                item2['Email'] = ""
                item2[
                    'SubDescription'] = 'Heller Homes builds in both subdivisions and rural properties in Allen County and the surrounding counties.'
                item2[
                    'SubImage'] = "https://i1.wp.com/hellersite.com/wp-content/uploads/2017/11/valencia.jpg?fit=300%2C200&ssl=1"
                item2['SubWebsite'] = response.url
                yield item2
            elif i == 7:
                subdivisonName = 'New Haven - Greenwood Lakes'
                subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % subdivisonNumber, "wb")
                f.write(response.body)
                f.close()
                item2 = BdxCrawlingItem_subdivision()
                item2['sub_Status'] = "Active"
                item2['SubdivisionName'] = subdivisonName
                item2['SubdivisionNumber'] = subdivisonNumber
                item2['BuilderNumber'] = self.builderNumber
                item2['BuildOnYourLot'] = 0
                item2['OutOfCommunity'] = 1
                item2['Street1'] = 'Chesterhills Ct'
                item2['City'] = 'New Haven'
                item2['State'] = 'IN'
                item2['ZIP'] = '46774'
                item2['AreaCode'] = ''
                item2['Prefix'] = ''
                item2['Suffix'] = ''
                item2['Extension'] = ""
                item2['Email'] = ""
                item2[
                    'SubDescription'] = 'Heller Homes builds in both subdivisions and rural properties in Allen County and the surrounding counties.'
                item2[
                    'SubImage'] = "https://i0.wp.com/hellersite.com/wp-content/uploads/2017/11/greenwood-lakes.jpg?fit=302%2C200&ssl=1"
                item2['SubWebsite'] = response.url
                yield item2
        floorplan = 'https://hellersite.com/floor-plans/'
        yield scrapy.FormRequest(url=floorplan, callback=self.floorlinks, dont_filter=True,
                                 meta={'sbdn': subdivisonNumber})

    def floorlinks(self, response):
        SubdivisionNumber = response.meta['sbdn']
        headers = {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            # cookie: _ga=GA1.2.310656239.1599652376; _gid=GA1.2.2085600970.1601709266; _gat=1
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
        # links = response.xpath('//*[@class="sow-image-container"]/a/@href').extract()
        links = response.xpath('//span[contains(text(),"$")]/../@href').extract()
        print(len(links))
        for link in links:
            link = link
            a = 'https://hellersite.com/leslie-2/'
            yield scrapy.FormRequest(url=a, callback=self.planData,headers=headers, dont_filter=True,
                                     meta={'sbdn': SubdivisionNumber})

    def planData(self, response):
        try:
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
            item['Street1'] = '347 West Berry Street Suite 400'
            item['City'] = 'Fort Wayne'
            item['State'] = 'IN'
            item['ZIP'] = '46802'
            item['AreaCode'] = '260'
            item['Prefix'] = '637'
            item['Suffix'] = '9113'
            item['Extension'] = ""
            item['Email'] = ''
            item[
                'SubDescription'] = 'Wanting to get in contact with us? Fill out the form here and we will get back to you soon!'
            item[
                'SubImage'] = 'https://i0.wp.com/hellersite.com/wp-content/uploads/2017/11/greenwood-lakes.jpg?fit=302%2C200&ssl=1'
            item['SubWebsite'] = response.url
            yield item
            print(response.url)


            try:
                Type = 'SingleFamily'
            except Exception as e:
                Type = 'SingleFamily'
                print(e)

            try:
                PlanName = response.xpath('//*[@class="siteorigin-widget-tinymce textwidget"]/ul/li[1]/h2/text()').get()
                if PlanName == None:
                    PlanName = response.xpath('//*[@class="siteorigin-widget-tinymce textwidget"]/ul/li[1]/h1/text()').get()
                PlanName = re.sub('<[^<]+?>', '', str(PlanName))
                print(PlanName)
            except Exception as e:
                PlanName = ''
                print(e)

            try:
                PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % PlanNumber, "wb")
                f.write(response.body)
                f.close()
            except Exception as e:
                print(e)

            try:
                SubdivisionNumber = response.meta['sbdn']
            except Exception as e:
                print(e)

            try:
                PlanNotAvailable = 0
            except Exception as e:
                print(e)

            try:
                BasePrice = response.xpath('//div[@class="siteorigin-widget-tinymce textwidget"]//li[2]/h2/text()').get()
                BasePrice = BasePrice.replace(',','')
                BasePrice = re.findall(r"(\d+)", BasePrice)[0]
                print(BasePrice)
            except Exception as e:
                BasePrice = 0
                print(e)

            try:
                PlanTypeName = 'Single Family'
            except Exception as e:
                print(e)

            try:
                plansquare = response.xpath('//*[contains(text(),"Square Feet")]/text()').getall()
                print(len(plansquare))
                if len(plansquare) == 2:
                    plansquare = plansquare[1]
                if plansquare == []:
                    plansquare = response.xpath('//*[contains(text(),"Square Feet")]/text()[2]').getall()
                plansquare = re.sub('<[^<]+?>', '', str(plansquare))
                BaseSqft = plansquare.split(' ')[0].strip().replace(',', '')
                BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
                print(BaseSqft)
            except Exception as e:
                BaseSqft = 0.00
                print("BaseSqft: ", e)
            try:
                planbeds = response.xpath('//*[contains(text(),"Bed")]/text()').getall()
                print(len(planbeds))
                if len(planbeds) == 3:
                    planbeds = planbeds[1]
                # planbeds = re.sub('<[^<]+?>', '', str(planbeds))
                if len(planbeds) == 2:
                    planbeds = planbeds[1]
                planbeds = "".join(planbeds)
                planbeds = re.findall(r"(\d+)", planbeds)[0]
                print(planbeds)
                if PlanName == 'Allyson':
                    planbeds = 4

            except Exception as e:
                planbeds =0.00
                print("planbeds: ", e)

            try:
                planbath1 = response.xpath('//*[contains(@class,"panel-widget-style panel-widget-style-")]').get()
                bath = re.findall('<li style="text-align: center;">(.*?)Bed, (.*?) Bath',planbath1,re.DOTALL)
                bath = [item for t in bath for item in t][1]
                tmp = re.findall(r"(\d+)", bath)
                planbath = tmp[0]
                print(planbath)
                if len(tmp) > 1:
                    planHalfBaths = 1
                    print(planHalfBaths)
                else:
                    planHalfBaths = 0
                    print(planHalfBaths)
                if PlanName == 'Leslie 2':
                    planbath = 2
                    planHalfBaths =1

            except Exception as e:
                try:
                    planbath = response.xpath("//*[contains(text(),'Bath')]//text()").getall()[1]
                except Exception as e:
                    planbath = 0.00

            try:
                cargarage = response.xpath('//div[@class="siteorigin-widget-tinymce textwidget"]//*[contains(text(),"Garage")]/text()').getall()
                if len(cargarage) == 1:
                    cargarage = 1
                else:
                    cargarage = 0

            except Exception as e:
                print("cargarage: ", e)
            try:
                Description = 'Wanting to get in contact with us? Fill out the form here and we will get back to you soon!'
            except Exception as e:
                Description = ' '
                print('Description:', e)
            try:
                PlanImage = []
                PlanImages = response.xpath("//*[contains(@src,'wp-content/uploads')]/@src").extract()[1:-1]
                for PlanImag in PlanImages:
                    PlanImage.append(PlanImag)
                PlanImage = '|'.join(PlanImage)
                print(PlanImage)
            except Exception as e:
                PlanImage =''
                print("SpecElevationImage: ", e)
            try:
                PlanWebsite = response.url
            except Exception as e:
                print(e)
            try:
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
                item['Baths'] = planbath
                # print(item['Baths'])
                item['HalfBaths'] = planHalfBaths
                # print(item['HalfBaths'])
                item['Bedrooms'] = planbeds
                item['Garage'] = cargarage
                item['Description'] = Description
                item['ElevationImage'] = PlanImage
                item['PlanWebsite'] = PlanWebsite
                print(item)
                yield item
            except Exception as e:
                print(e)
        except Exception as e:
            print('error in extraction',e,response.url)


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl hellerhomes".split())
