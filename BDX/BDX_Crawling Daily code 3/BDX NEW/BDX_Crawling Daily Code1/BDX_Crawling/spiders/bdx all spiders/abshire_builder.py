# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'abshire_builder'
    allowed_domains = ['https://abshirebuildinggroup.com/']
    start_urls = ['https://abshirebuildinggroup.com/galleries/home-galleries/victoria-mackenzie/']

    builderNumber = "62088"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()



        images = ''
        image = response.xpath('//div[@class="envira-gallery-item-inner"]/a/@href').extract()
        for i in image:
            images = images + i + '|'
        images = images.strip('|')

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '105 WINDING BROOK'
        item['City'] = 'LUMBERTON'
        item['State'] = 'TX'
        item['ZIP'] = '77657'
        item['AreaCode'] = '409'
        item['Prefix'] ='781'
        item['Suffix'] = '7000'
        item['Extension'] = ""
        item['Email'] = 'bethkirkrealtor@gmail.com'
        item['SubDescription'] = 'We hope you"re pleased with your Abshire Custom Home.   Working hard to help you realize your dream home is what keeps us going.  Nothing would please us more than to hear from you and tell us how we did.  Please take a moment to leave us a review on Google... thank you very much for trusting us with your home!'
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item


        links = ['https://abshirebuildinggroup.com/designs/','https://abshirebuildinggroup.com/designs/page/2/']
        for link in links:
            yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)


    def parse2(self,response):
        links = response.xpath('//div[@class="listing-widget-thumb"]/a/@href').extract()
        for link in links:
            yield scrapy.FormRequest(url=link,callback=self.parse3,dont_filter=True)


    def parse3(self,response):

        temp = response.xpath('//span[@class="listing-status for-sale"]/text()').extract_first()
        temp1 = response.xpath('//span[@class="listing-status sold"]/text()').extract_first()
        print(temp)
        print(temp1)


        if 'sold' not in response.text or "built and sold in" in response.text:

            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                PlanName = response.xpath('//h1/text()').get()
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
                sqft = response.xpath("//span[contains(text(),'Sq Ft:')]/../text()").extract_first('')
                # sqft = sqft.split("|")[0]
                sqft = sqft.replace(',', '').strip()
                if '.' in sqft:
                    sqft = sqft.split(".")[0]
                BaseSqft = re.findall(r"(\d+)", sqft)[0]

            except Exception as e:
                print(e)
                BaseSqft = ''

            try:
                bath = response.xpath("//span[contains(text(),'Baths:')]/../text()").extract_first()
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
                Bedrooms = response.xpath("//span[contains(text(),'Beds:')]/../text()").extract_first()
                if '-' in Bedrooms:
                    Bedrooms = Bedrooms.split("-")[1]
                # Bedrooms = Bedrooms.split("|")[1].split("|")[0]
                Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            except Exception as e:
                print(e)

            try:
                # Garage = response.xpath('//div[@itemprop="description"]/p/text()[3]').extract_first('')
                Garage = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*car garage", response.text.lower())[0]
                Garage = Garage.replace("three","3").replace("four","4").replace("two","2")
                Garage = re.findall(r"(\d+)", Garage)[0]
            except Exception as e:
                print(e)
                Garage = 0


            try:
                Description = "".join(response.xpath('//div[@id="listing-description"]/p/text()').extract())
                Description = Description.encode('ascii','ignore').decode('utf8')
                # Description = 'Brookstone Construction Group is a family owned and operated company with over 20 years of custom homes and commercial construction experience. We value what it truly means to feel like family, and we will do our best to build not just a house, but a home.'
            except Exception as e:
                print(e)
                Description = ''

            try:
                price = response.xpath('//li[@class="listing-price"]/text()').extract_first()
                print(price)
                # price = price.replace(".","")
                if '.' in price:
                    price = price.split(".")[0]

                price = price.replace(",","")
                price = re.findall(r"(\d+)", price)[0]
            except Exception as e:
                print(e)
                price = 0
            try:

                images1 = response.xpath('//div[@class="envira-lazy"]/img/@src').extract()
                if images1 == []:
                    images1 = response.xpath('//div[@class="envira-gallery-item-inner"]/a/@href').extract()
                    if images1 == []:
                        images1 = response.xpath('//img[@class="aligncenter wp-image-2005 size-full"]/@src').extract()
                        if images1 == []:
                            images1 = response.xpath('//div[@id="listing-gallery"]/figure/a/img/@src').extract()
                #
                images2 = response.xpath('//div[@itemprop="image"]/img/@src').extract_first('')
                images = []
                for id in images1:
                    id = id
                    images.append(id)
                ElevationImage = images

                if images2 != '':
                    ElevationImage.append(images2)

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
            item['BasePrice'] = price
            item['BaseSqft'] = BaseSqft
            item['Baths'] = Baths
            item['HalfBaths'] = HalfBaths
            item['Bedrooms'] = Bedrooms
            item['Garage'] = Garage
            item['Description'] = Description
            item['ElevationImage'] = "|".join(ElevationImage)
            item['PlanWebsite'] = PlanWebsite
            yield item



        # --------------------------------------------------------------------- #


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl abshire_builder'.split())