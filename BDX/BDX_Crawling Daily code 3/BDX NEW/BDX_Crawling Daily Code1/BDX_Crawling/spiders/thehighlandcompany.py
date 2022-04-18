import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class HillCountrySpider(scrapy.Spider):
    name = 'thehighlandcompany'
    allowed_domains = []
    start_urls = ['https://www.thehighlandcompany.com/']
    builderNumber = 51658

    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = self.builderNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '982 N. Winstead Avenue'
        item['City'] = 'Rocky Mount'
        item['State'] = 'NC'
        item['ZIP'] = '27804'
        item['AreaCode'] = ''
        item['Prefix'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = 'Since 1985, The Highland Company of Rocky Mount has been one of Eastern North Carolinas premier builders! Whether you are a first time home buyer, or looking to build for the first time, The Highland Company is committed and ready to go to work for you!'
        item['SubImage'] = 'https://www.thehighlandcompany.com/uploads/2/3/1/0/23106720/home-1_orig.jpg|https://www.thehighlandcompany.com/uploads/2/3/1/0/23106720/9652197_orig.jpg|https://www.thehighlandcompany.com/uploads/2/3/1/0/23106720/2800126_orig.jpg|https://www.thehighlandcompany.com/uploads/2/3/1/0/23106720/3797907_orig.jpg|https://www.thehighlandcompany.com/uploads/2/3/1/0/23106720/424972_orig.jpg|https://www.thehighlandcompany.com/uploads/2/3/1/0/23106720/5324209_orig.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        links = response.xpath('//li[@class="wsite-menu-subitem-wrap "]/a[contains(@href,"the")]/@href').extract()
        for link in links:
            link = 'https://www.thehighlandcompany.com' + link
            yield scrapy.FormRequest(url=link, callback=self.parse3, dont_filter=True)

    def parse3(self, response):

        try:
            PlanName = response.xpath('//h2/text()').extract_first()
            print(PlanName)
        except Exception as e:
            print("PlanName: ", e)
        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = self.builderNumber
            print(SubdivisionNumber)
        except Exception as e:
            print(str(e))

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
            print(str(e))

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)
        try:
            Bedroo = response.xpath("//*[contains(text(),'bedroom')]/text()").extract_first().strip()
            Bedroom = Bedroo.split('bedrooms')[0]
            if 'or' in Bedroom:
                Bedrooms = re.findall(r"(\d+)", Bedroom)[1]
            else:
                Bedrooms = re.findall(r"(\d+)", Bedroom)[0]

            # Bedrooms = Bedroom.split(' Bed')[0].strip()

        except Exception as e:
            Bedrooms = 0
            print("Bedrooms: ", e)

        try:
            Bathroo = response.xpath("//*[contains(text(),'bedroom')]/text()").extract_first().strip()
            Bathroo = Bathroo.split("bedroom")[1].replace(" 1/2",".5")
            tmp = re.findall(r"(\d+)", Bathroo)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0

        except Exception as e:
            Baths = 0
            print("Baths: ", e)

        try:
            Garage = Garage = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*car garage", response.text.lower())[0]
            Garage = Garage.replace("three", "3").replace("four", "4").replace("two", "2")
            Garage = re.findall(r"(\d+)", Garage)[0]
        except Exception as e:
            print(e)
            try:
                Garage = Garage = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*gar garage", response.text.lower())[0]
                Garage = Garage.replace("three", "3").replace("four", "4").replace("two", "2")
                Garage = re.findall(r"(\d+)", Garage)[0]
            except:
                Garage = 0

        try:
            BaseSqft = response.xpath(
                '//div[@class="text z-t-20 z-text-white"]/text()[7]').extract_first().strip().replace(',', '')
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
        except Exception as e:
            print("BaseSQFT: ", e)
            BaseSqft = ''

        try:
            ElevationImages = []
            ElevationImage1 = response.xpath('//div[@class="wsite-image wsite-image-border-thin "]/a/@href').extract_first('')
            ElevationImage22 = response.xpath('//div[@class="wsite-image wsite-image-border-none "]/a/img/@src').extract()
            if ElevationImage1 != '':
                ElevationImage1 = 'https://www.thehighlandcompany.com' + ElevationImage1
                ElevationImages.append(ElevationImage1)
            if ElevationImage22 != []:
                for ElevationImage2 in ElevationImage22:
                    ElevationImage2 = 'https://www.thehighlandcompany.com' + ElevationImage2
                    ElevationImages.append(ElevationImage2)


            ElevationImage = "|".join(ElevationImages)

        except Exception as e:
            print(str(e))

            ElevationImage = ''

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
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item


if __name__ == '__main__':
    execute("scrapy crawl thehighlandcompany".split())