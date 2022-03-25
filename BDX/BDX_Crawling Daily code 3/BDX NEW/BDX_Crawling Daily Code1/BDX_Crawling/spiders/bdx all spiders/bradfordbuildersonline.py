# bradfordbuildersonline
# 63665



# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'bradfordbuildersonline'
    allowed_domains = ['https://www.bradfordbuildersonline.com/']
    start_urls = ['https://www.bradfordbuildersonline.com/2015/01/07/village-at-sycamore/']

    builderNumber = "63665"

    def parse(self, response):


        #---------------creating community ---------------#

        subdivisonName = response.xpath('//h2/text()').extract_first('').strip()

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = int(hashlib.md5(bytes(subdivisonName+response.url,"utf8")).hexdigest(), 16) % (10 ** 30)
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = subdivisonName
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 1
        item['Street1'] = '2624 Thorngrove Court'
        item['City'] = 'Fayetteville'
        item['State'] = 'NC'
        item['ZIP'] = '28303'
        item['AreaCode'] = '910'
        item['Prefix'] = '308'
        item['Suffix'] = '9500'
        item['Extension'] = ""
        item['Email'] = 'douglarsen36@gmail.com'
        item['SubDescription'] = 'Apex Builders was founded by Doug and Amy Larsen.  We are North Dakotans and though our company is fairly new (celebrating our fifth year) we have been active in real estate for the past 15 years.  Prior to building houses we spent our time working on investment properties ranging from single family homes to commercial apartment buildings to the Wingate by Wyndham located in Bismarck.  We have developed many house plans in the past three years.  Typically our houses are in the $270,000 to $450,000 price range.  We believe we deliver a superior product at very reasonable price point with top-of-the-industry customer service.'
        item['SubImage'] = 'https://www.bradfordbuildersonline.com/wp-content/uploads/2015/01/header_sycamore-585x360.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

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
        item['Street1'] = '2919 Breezewood Ave #200'
        item['City'] = 'Fayetteville'
        item['State'] = 'NC'
        item['ZIP'] = '28303'
        item['AreaCode'] = '910'
        item['Prefix'] = '308'
        item['Suffix'] = '9500'
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = ''
        item['SubImage'] = 'https://www.bradfordbuildersonline.com/wp-content/uploads/2015/01/100_0307.jpg|https://www.bradfordbuildersonline.com/wp-content/uploads/2015/01/100_0439.jpg|https://www.bradfordbuildersonline.com/wp-content/uploads/2015/01/100_0608.jpg|https://www.bradfordbuildersonline.com/wp-content/uploads/2015/01/100_0617.jpg|https://www.bradfordbuildersonline.com/wp-content/uploads/2015/01/100_0618.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'https://www.bradfordbuildersonline.com/category/featured_homes/'
        yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)

    def parse2(self,response):

        links = response.xpath('//a[@rel="bookmark"]/../p/following-sibling::a/@href').extract()
        for link in links:
            # yield scrapy.FormRequest(url='https://www.bradfordbuildersonline.com/2015/01/06/247-blueridge/',callback=self.parse3,dont_filter=True)
            yield scrapy.FormRequest(url=link,callback=self.parse3,dont_filter=True)


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

        status = response.xpath('//h2/text()').extract_first('')
        if 'SOLD' not in status:
            status = response.xpath("//*[contains(text(),'Address:')]/following-sibling::text()").extract_first('')
            if 'SOLD' not in status:


                address = response.xpath("//strong[contains(text(),' Address:')]/../text()[4]").get(default='')

                try:
                    if 'Hope Mills' in address:
                        SpecCity = " ".join(address.split(',')[0].strip().split()[-2:])
                        SpecStreet1 = address.split(SpecCity)[0].strip()
                        SpecState = address.split(',')[1].strip().split(" ")[0].strip()
                        SpecZIP = address.split(',')[1].strip().split(" ")[1].strip()
                    elif '.' in address:
                        # 'Hope Mills'
                    # Home_Name = response.xpath('//div[@class="green-title"]//span//text()').get()
                        SpecStreet1 = address.split('.')[0].strip()
                        SpecCity = address.split('.')[1].strip().split(",")[0].strip()
                        SpecState = address.split(',')[1].strip().split(" ")[0].strip()
                        SpecZIP = address.split(',')[1].strip().split(" ")[1].strip()
                    else:
                        SpecCity = address.split(',')[0].strip().split()[-1].strip()
                        SpecStreet1 = address.split(SpecCity)[0].strip()
                        SpecState = address.split(',')[1].strip().split(" ")[0].strip()
                        SpecZIP = address.split(',')[1].strip().split(" ")[1].strip()

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
                    SpecPrice = response.xpath("//strong[contains(text(),'Price:')]/following-sibling::text()").get()
                    SpecPrice = SpecPrice.replace(",","")
                    SpecPrice = re.findall(r"(\d+)", SpecPrice)[0]
                except Exception as e:
                    print(e)
                    SpecPrice = 0

                try:
                    SpecSqft = response.xpath("//strong[contains(text(),'Square feet')]/following-sibling::text()").extract_first('')
                    SpecSqft = SpecSqft.replace(",","")
                    SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
                except Exception as e:
                    print(e)
                    SpecSqft = ''

                try:
                    SpecBaths = response.xpath("//strong[contains(text(),'Number of bathrooms')]/following-sibling::text()").extract_first('').replace("\n","")
                    tmp = re.findall(r'(\d+)', SpecBaths)
                    print(SpecBaths)
                    SpecBaths = tmp[0]
                    if len(tmp) > 1:
                        SpecHalfBaths = 1
                    else:
                        SpecHalfBaths = 0
                except Exception as e:
                    print(e)
                    SpecBaths,SpecHalfBaths = '',''

                try:
                    SpecGarage = response.xpath("//strong[contains(text(),'Garage Size:')]/following-sibling::text()").get(default='').strip().replace("double","2").replace("triple","3").replace("Double","2")
                    SpecGarage = re.findall(r'(\d+)', SpecGarage)[0]
                except Exception as e:
                    print(e)
                    SpecGarage = 0

                try:
                    SpecBedrooms = response.xpath(
                        "//strong[contains(text(),'Number of bedrooms')]/following-sibling::text()").get(default='').strip()
                    SpecBedrooms = re.findall(r'(\d+)', SpecBedrooms)
                except Exception as e:
                    print(e)
                    SpecBedrooms = ''


                # SpecGarage = 0

                # try:
                #     # Garage = response.xpath('//div[@itemprop="description"]/p/text()[3]').extract_first('')
                #     # Garage = re.findall(r"(\d*[three]*[four]*[two]*)[-]*[ ]*car garage", response.text.lower())[0]
                #     Garage = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*car garage", response.text.lower())[0]
                #     Garage = Garage.replace("three", "3").replace("four", "4").replace("two", "2").replace("double","2").replace("triple")
                #     SpecGarage = re.findall(r"(\d+)", Garage)[0]
                # except Exception as e:
                #     print(e)
                #     SpecGarage = 0

                try:
                    MasterBedLocation = "Down"
                except Exception as e:
                    print(e)

                try:
                    SpecDescription = response.xpath("//strong[contains(text(),'Full Description:')]/following-sibling::text()").extract_first('')
                    SpecDescription = SpecDescription.encode('ascii', 'ignore').decode('utf8').replace("\n", "")
                    print(SpecDescription)
                except Exception as e:
                    print(e)
                    SpecDescription = ''

                try:
                    SpecWebsite = response.url
                except Exception as e:
                    print(e)

                try:
                    SpecElevationImage = response.xpath('//div[@align="right"]/img/@src').extract_first('')
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

    # --------------------------------------------------------------------- #

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl bradfordbuildersonline'.split())
