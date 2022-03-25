

# -*- coding: utf-8 -*-
import hashlib
import re
import time

import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class blueribbonhb(scrapy.Spider):
    name = 'blueribbonhb'
    allowed_domains = ['http://www.blueribbonhb.com/']
    start_urls = ['http://www.blueribbonhb.com/']

    builderNumber = "63654"

    def parse(self, response):

        images = ''
        image = response.xpath('//div[@class="cycle-slideshow"]/img/@src').extract()
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
        item['Street1'] = '45 S. RIVERVIEW ST'
        item['City'] = 'LABELLE'
        item['State'] = 'FL'
        item['ZIP'] = '33935'
        item['AreaCode'] = '863'
        item['Prefix'] = '674'
        item['Suffix'] = '7128'
        item['Extension'] = ""
        item['Email'] = 'info@blueribbonhb.com'
        item['SubDescription'] = 'Hendry County is home to the growing cities of LaBelle and Clewiston - and soon, to you.  With agriculture as its economic backbone, Hendry County maintains the charm of country living while still being close enough to both the beach and cities like Fort Myers and West Palm Beach to allow for a fun day or afternoon outing.'
        item['SubImage'] = 'http://www.blueribbonhb.com/uploads/1/0/9/6/109686093/split-floorplan-hummigbird-1-car_orig.jpg|http://www.blueribbonhb.com/uploads/1/0/9/6/109686093/kingfisher-iii-elevation_orig.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'http://www.blueribbonhb.com/models.html'
        yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)

    def parse2(self,response):
        links = response.xpath('//div[@class="wsite-image wsite-image-border-none "]/a/@href').extract()
        print(links)
        for link in links:
            link = 'http://www.blueribbonhb.com' + link
            yield scrapy.FormRequest(url=link,callback=self.parse3,dont_filter=True)
            # yield scrapy.FormRequest(url='http://www.blueribbonhb.com/kingfisher.html',callback=self.parse3,dont_filter=True)

    def parse3(self,response):
        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//h2//text()[1]').get()
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
            BasePrice = response.xpath("//font[contains(text(),'$')]/text()").extract_first('0')
            BasePrice =BasePrice.replace(',', '').replace(".", "").strip()
            BasePrice = re.findall(r"(\d+)", BasePrice)[0]
        except Exception as e:
            print(e)
            BasePrice = 0

        try:
            sqft = response.xpath("//font[contains(text(),'Bedr')]/text()").extract_first('')
            sqft = sqft.split("|")[2]
            sqft = sqft.replace(',', '').replace(".", "").strip()
            BaseSqft = re.findall(r"(\d+)", sqft)[0]

            if len(BaseSqft) < 3:
                sqft = response.xpath("//h2[contains(text(),'Living')]/text()").extract_first('')
                sqft = sqft.replace(',', '').replace(".", "").strip()
                BaseSqft = re.findall(r"(\d+)", sqft)[0]

                if len(BaseSqft) < 3:
                    sqft = response.xpath("//font[contains(text(),'Living')]/text()").extract_first('')
                    sqft = sqft.replace(',', '').replace(".", "").strip()
                    BaseSqft = re.findall(r"(\d+)", sqft)[0]



        except Exception as e:
            print(e)
            BaseSqft = ''

        try:
            bath = response.xpath("//font[contains(text(),'Bedr')]/text()").extract_first()
            if '|' in bath:
                bath = bath.split("|")[1]
                bath = bath.split("|")[0]
            tmp = re.findall(r"(\d+)", bath)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            print(e)

        try:
            Bedrooms = response.xpath("//font[contains(text(),'Bedr')]/text()").extract_first()
            if '|' in Bedrooms:
                Bedrooms = Bedrooms.split("|")[0]
            # Bedrooms = Bedrooms.split("|")[1].split("|")[0]
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)

        try:
            Garage = response.xpath("//font[contains(text(),'Bedr')]/text()").extract_first()
            # Garage = Garage.split("|")[2]
            Garage = Garage.split("Car")[0]
            if '|' in Garage:
                Garage = Garage.split()[-1]
            Garage = Garage.replace(',', '').replace(".", "").strip()
            Garage = re.findall(r"(\d+)", Garage)[0]

        except Exception as e:
            Garage = 0

            if Garage == 0:
                try:
                    Garage = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*car garage", response.text.lower())[0]
                    Garage = Garage.replace("three", "3").replace("four", "4").replace("two", "2")
                    Garage = re.findall(r"(\d+)", Garage)[0]
                except Exception as e:
                    print(e)
                    Garage = 0


        try:
            Description = response.xpath('//div[@class="paragraph"]//text()[1]').extract_first('').strip()
            if Description == '':
                Description = response.xpath('//div[@class="paragraph"]/text()').extract_first('')
                if Description == '':
                    Description = response.xpath('//div[@class="paragraph"]/text()[2]').extract_first('')
            Description = Description.encode('ascii', 'ignore').decode('utf8').replace("\n", "")
            print(Description)
        except Exception as e:
            print(e)
            Description = ''

            # Description = 'Brookstone Construction Group is a family owned and operated company with over 20 years of custom homes and commercial construction experience. We value what it truly means to feel like family, and we will do our best to build not just a house, but a home.'

        try:

            images = set()
            xpathimage = response.xpath("//img[contains(@src,'orig.jpg')]/@src").extract()
            if xpathimage!= []:
                for image1 in xpathimage:
                    image1 = 'http://www.blueribbonhb.com' + image1
                    images.add(image1)

            image = re.findall('{"url":"(.*?)","width"', response.text)
            for img in image:
                # print(img)
                img_url = 'http://www.blueribbonhb.com/uploads/' + img
                # print(img_url)
                img_url = img_url.replace(".jpg","_orig.jpg")
                print(img_url)

                images.add(img_url)

            ElevationImage = images
            print(ElevationImage)
        except Exception as e:
            print(e)

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

            # ----------------------- Don't change anything here --------------
        unique = str(PlanNumber) + str(SubdivisionNumber) + str(Baths) + str(Bedrooms)  # < -------- Changes here
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
        item['ElevationImage'] = "|".join(ElevationImage)
        item['PlanWebsite'] = PlanWebsite
        yield item




if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl blueribbonhb'.split())



