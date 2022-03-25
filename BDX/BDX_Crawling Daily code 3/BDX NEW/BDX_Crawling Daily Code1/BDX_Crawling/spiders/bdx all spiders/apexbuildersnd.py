
# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'apexbuildersnd'
    allowed_domains = ['https://www.apexbuildersnd.com/']
    start_urls = ['https://www.apexbuildersnd.com/']

    builderNumber = "62738"

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
        item['Street1'] = 'PO Box 652'
        item['City'] = 'Mandan'
        item['State'] = 'ND'
        item['ZIP'] = '58554'
        item['AreaCode'] = '701'
        item['Prefix'] ='400'
        item['Suffix'] = '3625'
        item['Extension'] = ""
        item['Email'] = 'douglarsen36@gmail.com'
        item['SubDescription'] = 'We are continuously improving our designs & product line and will always remain flexible to handle you as an individual—tailoring our service and product to your needs. We strive to simplify the process so the experience of building a home won’t require a divorce lawyer.  Instead of being filled with stress and angst, it is filled with smiles and enjoyment.'
        item['SubImage'] = 'https://www.apexbuildersnd.com/wp-content/uploads/2016/04/DSCN0552-e1492705833429.jpg|https://www.apexbuildersnd.com/wp-content/uploads/2016/04/DSCN0519-300x225.jpg|https://www.apexbuildersnd.com/wp-content/uploads/2015/03/IMG_4729-300x200.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'https://www.apexbuildersnd.com/homes-for-sale/'
        yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)

    def parse2(self,response):
        links = response.xpath('//div[@class="entry"]//h2/a/@href').extract()
        print(links)
        for link in links:
            link = link
            yield scrapy.FormRequest(url=link,callback=self.parse3,dont_filter=True)
            # yield scrapy.FormRequest(url='https://www.apexbuildersnd.com/for-sale-344-e-lasalle-drive-bismarck-nd/',callback=self.parse3,dont_filter=True)


    def parse3(self, response):

        item = BdxCrawlingItem_Plan()
        unique = str("Plan Unknown") + str(self.builderNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item['unique_number'] = unique_number
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = "Plan Unknown"
        item['SubdivisionNumber'] = self.builderNumber
        item['PlanName'] = "Plan Unknown"
        item['PlanNotAvailable'] = 1
        item['PlanTypeName'] = "Single Family"
        item['BasePrice'] = 0
        item['BaseSqft'] = 0
        item['Baths'] = 0
        item['HalfBaths'] = 0
        item['Bedrooms'] = 0
        item['Garage'] = 0
        item['Description'] = ""
        item['ElevationImage'] = ""
        item['PlanWebsite'] = ""
        yield item


        address = response.xpath('//h1/text()').get(default='').split(':')[1]
        try:

            # Home_Name = response.xpath('//div[@class="green-title"]//span//text()').get()
            SpecStreet1 = address.split(',')[0].strip()
            SpecCity = address.split(',')[1].strip().split(" ")[0].strip()
            SpecState = address.split(',')[1].split(" ")[2].strip()
            SpecZIP = '00000'
            unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
            SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

            f = open("html/%s.html" % SpecNumber, "wb")
            f.write(response.body)
            f.close()

        except Exception as e:
            print(e)

        try:
            SpecCountry = "USA"
        except Exception as e:
            print(e)

        try:
            SpecPrice = response.xpath("//li[contains(text(),'$')]/text()").get()
            SpecPrice = SpecPrice.replace(",","")
            SpecPrice = re.findall(r"(\d+)", SpecPrice)[0]
        except Exception as e:
            print(e)
            SpecPrice = 0

        try:
            SpecSqft = response.xpath("//li[contains(text(),'Sq Ft')]/text()").extract_first('')
            SpecSqft = SpecSqft.replace(",","")
            SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
        except Exception as e:
            print(e)
            SpecSqft = 0

        try:
            SpecBaths = response.xpath("//li[contains(text(),' Bath')]/text()").get(default='')
            tmp = re.findall(r'(\d+)', SpecBaths)
            print(SpecBaths)
            SpecBaths = SpecBaths[0]
            if len(tmp) > 1:
                SpecHalfBaths = 1
            else:
                SpecHalfBaths = 0
        except Exception as e:
            print(e)

        try:
            SpecBedrooms = response.xpath("//li[contains(text(),'Bed')]/text()").get(default='').strip()
            SpecBedrooms = re.findall(r'(\d+)', SpecBedrooms)
        except Exception as e:
            print(e)
            SpecBedrooms = ''

        SpecGarage = 0

        try:
            MasterBedLocation = "Down"
        except Exception as e:
            print(e)

        try:
            SpecDescription = response.xpath('//div[@class="entry"]/p[2]/text()').extract_first('')
            print(SpecDescription)
        except Exception as e:
            print(e)

        try:
            SpecWebsite = response.url
        except Exception as e:
            print(e)

        try:
            SpecElevationImage = response.xpath('//div[@class="custom-frame-wrapper alignleft"]/img/@src').extract_first('')
            print(SpecElevationImage)
        except Exception as e:
            print(e)

        # ----------------------- Don't change anything here ---------------- #
        item = BdxCrawlingItem_Spec()
        item['SpecNumber'] = SpecNumber
        item['PlanNumber'] = unique_number
        item['SpecStreet1'] = SpecStreet1
        item['SpecCity'] = SpecCity
        item['SpecState'] = SpecState
        item['SpecZIP'] = SpecZIP
        item['SpecCountry'] = SpecCountry
        item['SpecPrice'] = SpecPrice
        item['SpecSqft'] = SpecSqft
        item['SpecBaths'] = SpecBaths
        item['SpecHalfBaths'] = SpecHalfBaths
        item['SpecBedrooms'] = SpecBedrooms
        item['MasterBedLocation'] = MasterBedLocation
        item['SpecGarage'] = SpecGarage
        item['SpecDescription'] = SpecDescription
        item['SpecElevationImage'] = SpecElevationImage
        item['SpecWebsite'] = SpecWebsite
        yield item



#--- use bdxstaticdata_3 - tabkle for this bdx
    # --------------------------------------------------------------------- #

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl apexbuildersnd'.split())