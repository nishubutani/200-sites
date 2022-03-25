
# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class allanbuilders(scrapy.Spider):
    name = 'allanbuilders'
    allowed_domains = ['https://allanbuilders.com/']
    start_urls = ['https://allanbuilders.com/']
    builderNumber = "62666"

    def parse(self, response):


        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        # images = ''
        # image = response.xpath('//div[@class="gallery-reel-item-src"]/img/@data-src').extract()
        # for i in image:
        #     images = images + i + '|'
        # images = images.strip('|')

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = 'N118 W18531 Bunsen Drive'
        item['City'] = 'Germantown'
        item['State'] = 'WI'
        item['ZIP'] = '53022'
        item['AreaCode'] = '866'
        item['Prefix'] ='569'
        item['Suffix'] = '2500'
        item['Extension'] = ""
        item['Email'] = 'sales@vci-wi.com'
        item['SubDescription'] = 'Allan Builders has developed a solid reputation for custom and semi-custom home building and believe that building a new home is just as much about building a relationship as it is about the physical construction of the home.'
        item['SubImage'] = 'https://allanbuilders.com/wp-content/uploads/2020/11/Seville_II_SP_1.jpg|https://allanbuilders.com/wp-content/uploads/2020/11/Seville_II_SP_3.jpg|https://allanbuilders.com/wp-content/uploads/2020/08/Braxton_1.jpg|https://allanbuilders.com/wp-content/uploads/2020/08/Braxton_3.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        # link = 'https://allanbuilders.com/open_models/'
        # link = 'https://allanbuilders.com/home_designs/'

        links = ['https://allanbuilders.com/home_designs/','https://allanbuilders.com/open_models/']
        for link in links:
            yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)

    def parse2(self,response):

        links = response.xpath('//div[@class="wpb_wrapper"]/div/figure/a/@href').extract()
        for link in links:
            # yield scrapy.FormRequest(url='https://allanbuilders.com/annsley-standard-plan/',callback=self.parse3,dont_filter=True)
            yield scrapy.FormRequest(url=link,callback=self.parse3,dont_filter=True)


    def parse3(self, response):

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
            sqft = response.xpath("//li[contains(text(),'Sq. Ft')]/text()").extract_first('')
            if sqft == '':
                sqft = response.xpath("//span[contains(text(),'Sq. Ft')]/text()").extract_first('')
                if sqft == '':
                    sqft = response.xpath("//h2[contains(text(),'Sq. Ft')]/text()").extract_first('')
            sqft = sqft.replace(",", "")
            BaseSqft = re.findall(r"(\d+)", sqft)[0]

        except Exception as e:
            print(e)
            BaseSqft = ''

        try:

            bath = response.xpath("//li[contains(text(),'baths')]/text()").extract_first('')
            if bath == '':
                bath = response.xpath("//span[contains(text(),'baths')]/text()").extract_first('')
            # bath = bath.split("/")[1].split("/")[0].strip()
            tmp = re.findall(r"(\d+)", bath)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            print(e)

        try:
            Bedrooms = response.xpath("//li[contains(text(),'bedro')]/text()").extract_first('')
            if Bedrooms == '':
                Bedrooms = response.xpath("//span[contains(text(),'bedro')]/text()").extract_first('')
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)

        try:
            price = response.xpath('//span[contains(text(),"$")]/text()').extract_first('')
            price = price.replace(",", "")
            price = re.findall(r"(\d+)", price)[0]

        except Exception as e:
            print(e)
            price = '0'

        try:
            BasePrice = price
        except Exception as e:
            print(e)

        try:
            Garage = response.xpath("//li[contains(text(),'car')]/text()").extract_first('')
            if Garage == '':
                Garage = response.xpath("//span[contains(text(),'car')]/text()").extract_first('')
            print(Garage)
            Garage = re.findall(r"(\d+)", Garage)[0]
        except Exception as e:
            print(e)
            Garage = 0

        try:

            desc = "'Allan Builders has developed a solid reputation for custom and semi-custom home building and believe that building a new home is just as much about building a relationship as it is about the physical construction of the home.'"
            Description = desc
        except Exception as e:
            print(e)

        try:
            img1 = response.xpath('//div[@class="vc_single_image-wrapper   vc_box_border_grey"]/img/@src').extract_first('')
            images = []
            imagedata = response.xpath('//figure[@class="wpb_wrapper vc_figure"]//img/@src').getall()
            for id in imagedata:
                id = id
                images.append(id)
            if img1  != '':
                images.append(img1)
            ElevationImage = "|".join(images)
            ElevationImage = ElevationImage
        except Exception as e:
            print(e)
            ''

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

            # ----------------------- Don't change anything here --------------
        unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
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
        item['Description'] = Description
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item
    # --------------------------------------------------------------------- #

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl allanbuilders'.split())
