
# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'buildimmaculate'
    allowed_domains = ['https://buildimmaculate.com/']
    start_urls = ['https://buildimmaculate.com/']

    builderNumber = "63685"

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
        item['Street1'] = '2 NORTH MAIN STREET'
        item['City'] = 'PROVIDENCE'
        item['State'] = 'UT'
        item['ZIP'] = '84332'
        item['AreaCode'] = '435'
        item['Prefix'] ='787'
        item['Suffix'] = '8700'
        item['Extension'] = ""
        item['Email'] = 'sales@buildimmaculate.com'
        item['SubDescription'] = 'Immaculate construction has been building quality homes for over 20 years.  All of our construction managers have 25 plus years of experience in the industry.  We have an eye for quality and style that is unmatched.  Our goal is to give you the best quality home at a competitive price.  Interested in knowing more of  what  makes us different?  Come see us  today to experience the  Immaculate difference!'
        item['SubImage'] = 'https://buildimmaculate.com/wp-content/uploads/2019/10/exterior-1200x800.jpg|https://buildimmaculate.com/wp-content/uploads/2020/10/lantern-hills-1.jpg|https://buildimmaculate.com/wp-content/uploads/2019/10/23-2-1214x800.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'https://buildimmaculate.com/floor-plans/'
        yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)

    def parse2(self, response):
        links = response.xpath('//div[@class="col-inner"]/a/@href').extract()
        for link in links:
            yield scrapy.FormRequest(url=link, callback=self.parse3, dont_filter=True)
            # yield scrapy.FormRequest(url='https://buildimmaculate.com/the-magnolia/', callback=self.parse3, dont_filter=True)

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
            BasePrice = 0
        except Exception as e:
            print(e)

        try:

            sqft = response.xpath('//div[@class="col-inner"]/p/text()[1]').extract_first('')
            # sqft = sqft.split("|")[0]
            sqft = sqft.replace(',', '').strip()
            if '.' in sqft:
                sqft = sqft.split(".")[0]
            BaseSqft = re.findall(r"(\d+)", sqft)[0]

        except Exception as e:
            print(e)
            BaseSqft = ''

        try:
            if PlanName == "The Alpine":
                bath = response.xpath('//div[@class="col-inner"]/p/text()[6]').extract_first()
            else:
                bath = response.xpath('//div[@class="col-inner"]/p/text()[4]').extract_first()
            if 'or' in bath:
                bath = bath.split("or")[1]
            tmp = re.findall(r"(\d+)", bath)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            print(e)

        try:
            if PlanName == "The Alpine":
                Bedrooms = response.xpath('//div[@class="col-inner"]/p/text()[5]').extract_first()
            else:
                Bedrooms = response.xpath('//div[@class="col-inner"]/p/text()[3]').extract_first()
            if 'or' in Bedrooms:
                Bedrooms = Bedrooms.split("or")[1]
            # Bedrooms = Bedrooms.split("|")[1].split("|")[0]
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)

        try:

            Garage = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*car garage", response.text.lower())[0]
            Garage = Garage.replace("three", "3").replace("four", "4").replace("two", "2")
            Garage = re.findall(r"(\d+)", Garage)[0]

            # if Garage1 == '':

            try:
                Garage1 = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*car garage", response.text.lower())[1]
                Garage1 = Garage1.replace("three", "3").replace("four", "4").replace("two", "2")
                Garage1 = re.findall(r"(\d+)", Garage1)[0]
            except Exception as e:
                print(e)
                Garage1 = '0'


            if Garage1 > Garage:
                Garage = Garage1

        except Exception as e:
            print(e)
            Garage = 0

        try:
            # Description = "".join(response.xpath('//div[@class="animated fadeInLeftShort"]/p/text()').extract())
            # Description = Description.encode('ascii','ignore').decode('utf8')
            # Description = 'long with Immaculate Construction, a licensed general contractor, work together to market, build and sell homes in Logan and the surrounding area, as well as St. George, Utah.'
            Description = ''
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

            images1 = response.xpath('//div[@class="img-inner dark"]/img/@data-src').extract()

            images2 = response.xpath('//div[@class="entry-image relative"]/a/img/@data-src').extract_first('')
            if ',' in images2:
                images2 = images2.split(",")[0]
                print(images2)

            images3 = response.xpath('//div[@class="img-inner image-cover dark"]/img/@data-srcset').extract_first('')
            if ',' in images3:
                images3 = images3.split(",")[0]
                if ' ' in images3:
                    images3 = images3.split(" ")[0]
                print(images3)
            else:
                images3 = images3




            images = []
            for id in images1:
                id = id
                images.append(id)
            ElevationImage = images

            if images2 != '':
                ElevationImage.append(images2)

            if images3 != '':
                ElevationImage.append(images3)

            print(ElevationImage)
        except Exception as e:
            print(e)

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

            # ----------------------- Don't change anything here --------------
        unique = str(PlanNumber) + str(SubdivisionNumber)   # < -------- Changes here
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
    execute('scrapy crawl buildimmaculate'.split())