# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header

class DannysullivanconstructionComSpider(scrapy.Spider):
    name = 'harpedevelopment'
    allowed_domains = []
    start_urls = ['https://www.harpedevelopment.com/']
    builderNumber = 14327

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
        item['Street1'] = '8501 75th St., Suite H'
        item['City'] = 'Kenosha'
        item['State'] = 'WI'
        item['ZIP'] = '53142'
        item['AreaCode'] = '262'
        item['Prefix'] = '694'
        item['Suffix'] = '1677'
        item['Extension'] = ""
        item['Email'] = 'admin@harpedevelopment.com'
        item[
            'SubDescription'] = 'Harpe Development is a family owned and operated company serving Southeastern Wisconsin’s Kenosha, Racine, Milwaukee and Walworth Counties.  Our goal is to make your building experience an enjoyable and stress free experience from day one.  We pride ourselves on honesty, transparency and accountability; and understand that building or buying a home is one of the biggest decisions and investments of your life. '
        item[
            'SubImage'] = 'https://dev-harpe.pantheonsite.io/wp-content/uploads/2019/01/34771908_10157425819798154_3213600148407975936_o-copy.jpg|https://www.harpedevelopment.com/wp-content/uploads/2019/01/34747657_10157425819933154_3334327839397773312_o.jpg|https://www.harpedevelopment.com/wp-content/uploads/2019/01/34793794_10157425821113154_1866689526684975104_o.jpg'
        item['SubWebsite'] = response.url
        yield item

        plinks = ['https://www.harpedevelopment.com/ranch/', 'https://www.harpedevelopment.com/1-5-story/',
                  'https://www.harpedevelopment.com/2-story/']
        for plink in plinks:
            # a = 'https://www.harpedevelopment.com/ranch/'
            yield scrapy.FormRequest(url=plink, callback=self.finalplink, dont_filter=True)

    def finalplink(self, response):
        # links = response.xpath('//div[@class="fusion-portfolio-content-wrapper"]//h2/a/@href').extract()
        links = response.xpath('//div[@class="fusion-portfolio-content-wrapper"]//div[@class="fusion-image-wrapper"]//a[contains(@href,"")]/@href').extract()
        print(len(links))
        for link in links:
            # b = 'https://www.harpedevelopment.com/portfolio-items/hampton/?portfolioCats=5'
            yield scrapy.FormRequest(url=link, callback=self.plandetail, dont_filter=True)

    def plandetail(self, response):
        print(response.url)
        try:
            PlanName = response.xpath('//*[@class="entry-title"]/text()').extract_first().strip()
            print(PlanName)
        except Exception as e:
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = self.builderNumber
            print(SubdivisionNumber)
        except Exception as e:
            print(str(e))

        try:
            BasePrice = 0.00
        except Exception as e:
            print(e)
        try:
            Bedrooms = response.xpath('//*[contains(text(),"Bedrooms")]/../../span[4]/text()').extract_first()
            if Bedrooms == None or Bedrooms == '':
                Bedrooms = response.xpath('//*[contains(text(),"Bedrooms")]/../span[4]/text()').extract_first()
            if PlanName == 'Harmony':
                Bedrooms = response.xpath('//span[@class="views-label views-label-field-bedrooms"]/text()').extract_first()
            print(Bedrooms)
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0].strip()
        except Exception as e:
            Bedrooms = 0
            print("Bed: ", e)
        try:
            Baths = response.xpath('//*[contains(text(),"Bathrooms")]/../../span[6]/text()').extract_first()
            if Baths == None or Baths == '':
                Baths = response.xpath('//*[contains(text(),"Bathrooms")]/../span[6]/text()').extract_first()
            Baths = Baths.replace('|','')
            if '.5' in Baths:
                Baths = Baths.split('.5')[0].strip()
                HalfBaths = 1
            else:
                Baths = Baths.strip()
                HalfBaths = 0
            if PlanName == 'Hampton':
                Baths = '3'
                HalfBaths = '1'
            # print(Baths,HalfBaths)
        except Exception as e:
            # Baths = 0
            # HalfBaths = 0
            print("Baths: ", e)
        try:
            BaseSqft = response.xpath('//*[contains(text(),"Square Feet")]/../text()').extract_first()
            if BaseSqft == None or BaseSqft == '':
                BaseSqft = response.xpath('//*[contains(text(),"Square Feet")]/text()').extract_first()
            BaseSqft = BaseSqft.replace(',', '').replace(':', '').strip()
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
            print(BaseSqft)
        except Exception as e:
            BaseSqft = 0
            print("BaseSqft", e)

        try:
            Garage = response.xpath('//*[contains(text(),"Garage Size")]/../text()').extract_first()
            if Garage == None or Garage == '':
                Garage = response.xpath('//*[contains(text(),"Garage Size")]/../span[8]/text()').get()
            Garage = re.findall(r"(\d+)", Garage)[0]
            print(Garage)
        except Exception as e:
            Garage = 0
        try:
            ElevationImageLinks = response.xpath('//*[contains(text(),"Gallery")]/../@href').getall()
            if ElevationImageLinks == '' or ElevationImageLinks == None or ElevationImageLinks == []:
                ElevationImage = response.xpath('//*[@class="fusion-image-wrapper"]//img/@src').extract_first()
            for imagelink in ElevationImageLinks:
                # reaponse1=requests.get(imagelink)
                res_1 = requests.get(imagelink)
                response1 = HtmlResponse(url=res_1.url, body=res_1.content)

                images = response1.xpath('//div[@class="fusion-gallery-image"]/a/@href').getall()
                print(len(images))
                ElevationImage = "|".join(images)

            if PlanName == 'Landon':
                ElevationImage = "https://www.harpedevelopment.com/wp-content/uploads/2019/02/landon-200x104.png"
            if PlanName == 'Harmony':
                ElevationImage = "https://www.harpedevelopment.com/wp-content/uploads/2018/12/Screen-Shot-2019-01-08-at-12.23.17-PM-200x67.png"
            if PlanName == 'Heritage':
                ElevationImage = 'https://www.harpedevelopment.com/wp-content/uploads/2019/02/Heritage-200x95.png'
            if PlanName == 'Ashland':
                ElevationImage = 'https://www.harpedevelopment.com/wp-content/uploads/2018/11/Screen-Shot-2019-01-08-at-11.58.58-AM-200x65.png'
            if PlanName == 'Sussex':
                ElevationImage = 'https://www.harpedevelopment.com/wp-content/uploads/2018/12/Screen-Shot-2019-01-08-at-12.34.49-PM-200x74.png'
            if PlanName == 'Weston':
                ElevationImage = 'https://www.harpedevelopment.com/wp-content/uploads/2019/02/Screen-Shot-2019-02-06-at-12.45.13-PM-200x99.png'
            if PlanName == 'kingston':
                ElevationImage = 'https://www.harpedevelopment.com/wp-content/uploads/2018/12/Screen-Shot-2019-01-08-at-12.09.38-PM-200x67.png'
            if PlanName == 'Chesapeak':
                ElevationImage = 'https://www.harpedevelopment.com/wp-content/uploads/2018/12/Screen-Shot-2019-01-08-at-12.05.17-PM-200x74.png'



                print(ElevationImage)
        except Exception as e:
            ElevationImage = response.xpath('//*[@class="fusion-image-wrapper"]/a/@href').get()

        unique = str(PlanName) + str(SubdivisionNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number  # < -------- Changes here
        item['SubdivisionNumber'] = self.builderNumber
        item['PlanName'] = PlanName
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = BasePrice
        item['BaseSqft'] = BaseSqft
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item[
            'Description'] = 'Harpe Development is a family owned and operated company serving Southeastern Wisconsin’s Kenosha, Racine, Milwaukee and Walworth Counties.  Our goal is to make your building experience an enjoyable and stress free experience from day one.  We pride ourselves on honesty, transparency and accountability; and understand that building or buying a home is one of the biggest decisions and investments of your life. '
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = response.url
        yield item


from scrapy.cmdline import execute

if __name__ == '__main__':
    execute("scrapy crawl harpedevelopment".split())