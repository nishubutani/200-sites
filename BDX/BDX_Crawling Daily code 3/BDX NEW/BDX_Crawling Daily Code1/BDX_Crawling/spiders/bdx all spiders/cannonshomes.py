

# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class camlin_customhomes(scrapy.Spider):
    name = 'cannonshomes'
    allowed_domains = ['https://www.cannonshomes.com/']
    start_urls = ['https://www.cannonshomes.com/']

    builderNumber = "63728"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

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
        item['Street1'] = '17245B E Illinois Hwy 142'
        item['City'] = 'Opdyke'
        item['State'] = 'IL'
        item['ZIP'] = '62872'
        item['AreaCode'] = '618'
        item['Prefix'] ='242'
        item['Suffix'] = '4080'
        item['Extension'] = ""
        item['Email'] = 'office@cannonshomes.com'
        item['SubDescription'] = 'At Cannon Homes Inc., we know that your time and money are important. When it comes to an investment as big as a house, you can’t afford to waste any resources. That’s why working with our team of experts is the best decision you could make as a potential home owner. For one, we are an exclusive Champion Homes modular homes dealer. This means we are experts in Champion Homes pricing, building standards, and warranty procedures. So, if you want a custom-built home from one of the leading manufacturers, Cannon Homes Inc. can do the job. We’re also proud of our competitive pricing — because we’re an exclusive dealer, we’re able to build modular homes at excellent prices. If you’re looking for a modular home in Southern Illinois, our modular homes are a cut above the rest. Visit us today in Opdyke or contact us to learn more about our modular homes!'
        item['SubImage'] = 'https://www.camlincustomhomes.com/content/img/817_home-design-show.jpg|https://www.camlincustomhomes.com/content/img/280_banner-lowcountry.jpg|https://www.camlincustomhomes.com/content/img/1533_banner-.jpg|https://www.camlincustomhomes.com/content/img/1564_Redfish-Cove.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        # link = 'https://www.cannonshomes.com/our-homes'
        links = ['https://www.chbmodels.com/1036IL','https://www.chbmodels.com/1036IL?page=2','https://www.chbmodels.com/1036IL?page=3',
                 'https://www.chbmodels.com/1036IL?page=4','https://www.chbmodels.com/1036IL?page=5']
        for link in links:
            yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)

    def parse2(self,response):
        # open_in_browser(response)
        links = response.xpath('//div[@class="grid grid--gutter"]/div/div/div/a/@href').extract()
        for link in links:
            print(link)
            yield scrapy.FormRequest(url=link,callback=self.plan,dont_filter=True)


    def plan(self,response):
        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//h2/text()').get()
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

            sqft = response.xpath('//div[@class="u-space"]/p/@data-configurator-details').extract_first('')
            # print(sqft)
            sqft = sqft.split(",")[0]

            sqft = sqft.replace(',', '').strip()

            BaseSqft = re.findall(r"(\d+)", sqft)[0]

        except Exception as e:
            print(e)
            BaseSqft = ''

        try:

            bath = response.xpath('//div[@class="u-space"]/p/@data-configurator-details').extract_first('')
            bath = bath.split(",")[2]
            # print(bath)
            tmp = re.findall(r"(\d+)", bath)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            print(e)

        try:

            Bedrooms = response.xpath('//div[@class="u-space"]/p/@data-configurator-details').extract_first('')
            Bedrooms = Bedrooms.split(",")[1]
            # Bedrooms = Bedrooms.split("–")[2]

            # Bedrooms = Bedrooms.split("|")[1].split("|")[0]
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)

        try:
            # Garage = response.xpath('//div[@itemprop="description"]/p/text()[3]').extract_first('')
            # Garage = re.findall(r"(\d*[three]*[four]*[two]*)[-]*[ ]*car garage", response.text.lower())[0]
            Garage = Garage = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*car garage", response.text.lower())[0]
            Garage = Garage.replace("three", "3").replace("four", "4").replace("two", "2")
            Garage = re.findall(r"(\d+)", Garage)[0]
        except Exception as e:
            print(e)
            Garage = 0

        try:
            Description = 'At Cannon Homes Inc., we know that your time and money are important. When it comes to an investment as big as a house, you can’t afford to waste any resources. That’s why working with our team of experts is the best decision you could make as a potential home owner. For one, we are an exclusive Champion Homes modular homes dealer. This means we are experts in Champion Homes pricing, building standards, and warranty procedures. So, if you want a custom-built home from one of the leading manufacturers, Cannon Homes Inc. can do the job. We’re also proud of our competitive pricing — because we’re an exclusive dealer, we’re able to build modular homes at excellent prices. If you’re looking for a modular home in Southern Illinois, our modular homes are a cut above the rest. Visit us today in Opdyke or contact us to learn more about our modular homes!'
        except Exception as e:
            print(e)
            Description = ''

            # try:
            #     price = response.xpath('//li[@class="listing-price"]/text()').extract_first()
            #     print(price)
            #     if '.' in price:
            #         price = price.split(".")[0]
            #     price = re.findall(r"(\d+)", price)[0]
            # except Exception as e:
            #     print(e)

        price = 0

        try:

            images1 = response.xpath('//img/@src').extract()
            print(images1)


            images = []
            for id in images1:
                id =  id
                if ',' in id:
                    print(id)
                    id = id.split("http")[2]
                    id = 'http' + id
                    print(id)
                images.append(id)
            ElevationImage = images

            print(ElevationImage)
        except Exception as e:
            print(e)

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

            # ----------------------- Don't change anything here --------------
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
    execute('scrapy crawl cannonshomes'.split())