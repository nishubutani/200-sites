
# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'build4g'
    allowed_domains = ['https://build4g.com/']
    start_urls = ['https://build4g.com/']

    builderNumber = "63682"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()


        # images = ''
        # image = response.xpath('//div[@class="widget animated fadeInUpShort"]//img[@class="lazy loaded"]').extract()
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
        item['Street1'] = '488 PINEVILLE RD'
        item['City'] = 'STATESVILLE'
        item['State'] = 'NC'
        item['ZIP'] = '28677'
        item['AreaCode'] = '833'
        item['Prefix'] ='284'
        item['Suffix'] = '5344'
        item['Extension'] = ""
        item['Email'] = 'sam@build4g.com'
        item['SubDescription'] = 'Great homes don’t just happen. They require careful planning, attention to detail, and quality workmanship. It can be said: “A house well planned, is a house half built.” We have discovered that by focusing on the initial planning stage, building your home will be simpler and less stressful. We design with your budget in mind, allowing you to build your dream home at a price you can afford.'
        item['SubImage'] = 'https://build4g.com/wp-content/uploads/2019/02/customhome.jpg|https://build4g.com/wp-content/uploads/2020/02/widget_modern-720x480.jpg|https://build4g.com/wp-content/uploads/2019/02/widget_videos.jpg|https://build4g.com/wp-content/uploads/2019/02/why4g.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item


        link = 'https://build4g.com/portfolio/'
        yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)


    def parse2(self,response):
        links = response.xpath('//div[@class="animatedParent animateOnce"]/a/@href').extract()
        for link in links:
            yield scrapy.FormRequest(url=link,callback=self.parse3,dont_filter=True)


    def parse3(self,response):
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
            sqft = response.xpath("//h4[contains(text(),'Square Ft*')]/../h3/text()").extract_first('')
            # sqft = sqft.split("|")[0]
            sqft = sqft.replace(',', '').strip()
            if '.' in sqft:
                sqft = sqft.split(".")[0]
            BaseSqft = re.findall(r"(\d+)", sqft)[0]

        except Exception as e:
            print(e)
            BaseSqft = ''

        try:
            bath = response.xpath("//h4[contains(text(),'Bathrooms')]/../h3/text()").extract_first()
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
            Bedrooms = response.xpath("//h4[contains(text(),'Bedrooms')]/../h3/text()").extract_first()
            if '-' in Bedrooms:
                Bedrooms = Bedrooms.split("-")[1]
            # Bedrooms = Bedrooms.split("|")[1].split("|")[0]
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)

        try:
            # Garage = response.xpath('//div[@itemprop="description"]/p/text()[3]').extract_first('')
            # Garage = re.findall(r"(\d*[three]*[four]*[two]*)[-]*[ ]*car garage", response.text.lower())[0]
            Garage =  Garage = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*car garage", response.text.lower())[0]
            Garage = Garage.replace("three","3").replace("four","4").replace("two","2")
            Garage = re.findall(r"(\d+)", Garage)[0]
        except Exception as e:
            print(e)
            Garage = 0


        try:
            Description = "".join(response.xpath('//div[@class="animated fadeInLeftShort"]/p/text()').extract())
            # Description = Description.encode('ascii','ignore').decode('utf8')
            # Description = 'Brookstone Construction Group is a family owned and operated company with over 20 years of custom homes and commercial construction experience. We value what it truly means to feel like family, and we will do our best to build not just a house, but a home.'
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

            images1 = response.xpath('//div[@class="swiper-slide"]/img/@data-src').extract()

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
    execute('scrapy crawl build4g'.split())