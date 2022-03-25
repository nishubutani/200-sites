#
# # -*- coding: utf-8 -*-\0import hashlib
# import hashlib
# import re
# import time
#
# from scrapy.http import HtmlResponse
# from selenium import webdriver
#
# import scrapy
# from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
#
#
# class buydestinyhomes(scrapy.Spider):
#     name = 'buydestinyhomes'
#     allowed_domains = ['https://buydestinyhomes.com/']
#     start_urls = ['https://buydestinyhomes.com/']
#
#     builderNumber = "63703"
#
#     def parse(self, response):
#         EXE_PATH = r"D:\chromedriver.exe"
#         options = webdriver.ChromeOptions()
#         options.add_argument("--headless")
#         # options.add_argument("user-data-dir=C:\\Users\\xbyte\\AppData\\Local\\Google\\Chrome\\User Data")
#         driver = webdriver.Chrome(executable_path=EXE_PATH, options=options)
#
#         images = ''
#         image = response.xpath('//div[@class="cycle-slideshow"]/img/@src').extract()
#         for i in image:
#             images = images + i + '|'
#         images = images.strip('|')
#
#         item = BdxCrawlingItem_subdivision()
#         item['sub_Status'] = "Active"
#         item['SubdivisionNumber'] = ''
#         item['BuilderNumber'] = self.builderNumber
#         item['SubdivisionName'] = "No Sub Division"
#         item['BuildOnYourLot'] = 0
#         item['OutOfCommunity'] = 0
#         item['Street1'] = '750 SE ALICE’S RD'
#         item['City'] = 'WAUKEE'
#         item['State'] = 'IA'
#         item['ZIP'] = '50263'
#         item['AreaCode'] = '515'
#         item['Prefix'] = '216'
#         item['Suffix'] = '1015'
#         item['Extension'] = ""
#         item['Email'] = 'info@RolwesCo.com'
#         item['SubDescription'] = 'Dedicated to delivering extraordinary building experiences; Destiny Homes offers home and lot packages throughout Iowa. When you choose Destiny Homes, you are choosing a company that will create your dream home with strength and superiority while also exceeding your expectations'
#         item['SubImage'] = 'https://buydestinyhomes.com/wp-content/uploads/2020/07/bw-denali-1920x1080.jpg|https://buydestinyhomes.com/wp-content/uploads/2020/07/dhouse-1-300x214.jpg|https://buydestinyhomes.com/wp-content/uploads/2020/07/dhouse-3-3-300x214.jpg'
#         item['SubWebsite'] = response.url
#         item['AmenityType'] = ''
#         yield item
#
#         url = "https://buydestinyhomes.com/find-your-home/home-plans/"
#         driver.get(url)
#         time.sleep(5)
#         key = True
#         while key:
#             try:
#                 s = lambda x: driver.execute_script('return document.body.parentNode.scroll' + x)
#                 driver.set_window_size(s('Width'), s('Height'))
#                 # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#                 time.sleep(3)
#                 driver.find_element_by_xpath('//button[@class="wpgb-button wpgb-load-more"]').click()
#                 # driver.execute_script("arguments[0].click();", button1)
#                 # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#                 time.sleep(5)
#             except Exception as e:
#                 key = False
#
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(5)
#
#         response = HtmlResponse(url=driver.current_url, body=driver.page_source, encoding="utf-8")
#         links = response.xpath('//div[@class="wpgb-card-wrapper"]//a[@class="wpgb-card-layer-link"]/@href').extract()
#         print(len(links))
#         for link in links:
#             yield scrapy.Request(url=link, dont_filter=True, callback=self.parse3)
#         # # link = 'https://buydestinyhomes.com/find-your-home/move-in-ready-homes/'
#         # yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)
#
#     # def parse2(self, response):
#     #     links = response.xpath('//div[@class="class="]/a/@href').extract()
#     #     for link in links:
#     #         print(link)
#     #         yield scrapy.FormRequest(url=link, callback=self.parse3, dont_filter=True)
#     #         # yield scrapy.FormRequest(url='https://www.brookstonecg.com/home-plan/51778hz',callback=self.parse3,dont_filter=True,headers=self.headers)
#
#     def parse3(self, response):
#
#         try:
#             Type = 'SingleFamily'
#         except Exception as e:
#             print(e)
#
#         try:
#             PlanName = response.xpath('//h1[@class="hpc-title entry-title"]/text()').get()
#         except Exception as e:
#             PlanName = ''
#             print(e)
#
#         try:
#             PlanNumber = int(hashlib.md5(bytes(PlanName + response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
#         except Exception as e:
#             PlanNumber = ''
#             print(e)
#
#         try:
#             SubdivisionNumber = self.builderNumber
#             print(SubdivisionNumber)
#         except Exception as e:
#             SubdivisionNumber = ''
#             print(e)
#
#         try:
#             PlanNotAvailable = 0
#         except Exception as e:
#             print(e)
#
#         try:
#             PlanTypeName = 'Single Family'
#         except Exception as e:
#             print(e)
#
#         try:
#             BasePrice = 0
#         except Exception as e:
#             print(e)
#
#         try:
#             sqft = response.xpath('//div[@class="hpc-label"][contains(text(),"SQ FT")]/text()').extract_first('')
#             # sqft = sqft.split("|")[0]
#             sqft = sqft.replace(',', '').replace(".", "").strip()
#             BaseSqft = re.findall(r"(\d+)", sqft)[0]
#
#         except Exception as e:
#             print(e)
#             BaseSqft = ''
#
#         try:
#             bath = response.xpath("//div[@class='hpc-label'][contains(text(),'Baths')]/text()").extract_first()
#             if '-' in bath:
#                 bath = bath.split("-")[1]
#             tmp = re.findall(r"(\d+)", bath)
#             Baths = tmp[0]
#             if len(tmp) > 1:
#                 HalfBaths = 1
#             else:
#                 HalfBaths = 0
#         except Exception as e:
#             print(e)
#
#         try:
#             Bedrooms = response.xpath("//div[@class='hpc-label'][contains(text(),'Bedrooms')]/text()").extract_first()
#             if '-' in Bedrooms:
#                 Bedrooms = Bedrooms.split("-")[1]
#             # Bedrooms = Bedrooms.split("|")[1].split("|")[0]
#             Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
#         except Exception as e:
#             print(e)
#
#         try:
#             Garage = response.xpath("//div[@class='hpc-label'][contains(text(),'Car')]/text()").extract_first()
#             if '-' in Garage:
#                 Garage = Garage.split("-")[1]
#             # Bedrooms = Bedrooms.split("|")[1].split("|")[0]
#             Garage = re.findall(r"(\d+)", Garage)[0]
#         except Exception as e:
#             Garage = 0
#             print(e)
#
#         try:
#             Description = response.xpath('//div[@class="hpc-description"]/p/text()').extract_first('')
#             print(Description)
#         except Exception as e:
#             print(e)
#             Description=''
#
#         try:
#
#             # images1 = response.xpath('//li[@class="dmCoverImgContainer"]/img/@src').extract()
#             #
#             # images2 = response.xpath('//div[@class="u_1929991324 imageWidget align-center"]/a/img/@src').extract_first('')
#             images = []
#             imagedata = response.xpath('//div[@class="kb-gallery-image-contain kadence-blocks-gallery-intrinsic kb-gallery-image-ratio-land32"]/img/@src').extract()
#             for id in imagedata:
#                 id = id
#                 images.append(id)
#             ElevationImage = images
#             print(ElevationImage)
#         except Exception as e:
#             print(e)
#
#         try:
#             PlanWebsite = response.url
#         except Exception as e:
#             print(e)
#
#             # ----------------------- Don't change anything here --------------
#         unique = str(PlanNumber) + str(SubdivisionNumber) + str(Baths) + str(Bedrooms)  # < -------- Changes here
#         unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
#         item = BdxCrawlingItem_Plan()
#         item['Type'] = Type
#         item['PlanNumber'] = PlanNumber
#         item['unique_number'] = unique_number  # < -------- Changes here
#         item['SubdivisionNumber'] = SubdivisionNumber
#         item['PlanName'] = PlanName
#         item['PlanNotAvailable'] = PlanNotAvailable
#         item['PlanTypeName'] = PlanTypeName
#         item['BasePrice'] = BasePrice
#         item['BaseSqft'] = BaseSqft
#         item['Baths'] = Baths
#         item['HalfBaths'] = HalfBaths
#         item['Bedrooms'] = Bedrooms
#         item['Garage'] = Garage
#         item['Description'] = Description
#         item['ElevationImage'] = "|".join(ElevationImage)
#         item['PlanWebsite'] = PlanWebsite
#         yield item
#
#         links = response.xpath('//div[@class="listing-thumb"]/a/@href').extract()
#         templink = ['https://buydestinyhomes.com/move-in-ready-homes/1500-ne-cedarwood-drive/','https://buydestinyhomes.com/move-in-ready-homes/612-ne-pearl-street']
#         #----- fake plan #
#
#
#         links = links + templink
#         for link in links:
#             print(link)
#             yield scrapy.FormRequest(url=link,callback=self.parse4,dont_filter=True,meta={'unique_number':unique_number})
#             # yield scrapy.FormRequest(url='https://buydestinyhomes.com/move-in-ready-homes/114-destiny-drive/',callback=self.parse4,dont_filter=True,meta={'unique_number':unique_number})
#
#
#     def parse4(self,response):
#
#         item = BdxCrawlingItem_Plan()
#         unique = str("Plan Unknown") + str(self.builderNumber)
#         unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
#         item['unique_number'] = unique_number
#         item['Type'] = "SingleFamily"
#         item['PlanNumber'] = "Plan Unknown"
#         item['SubdivisionNumber'] = self.builderNumber
#         item['PlanName'] = "Plan Unknown"
#         item['PlanNotAvailable'] = 1
#         item['PlanTypeName'] = "Single Family"
#         item['BasePrice'] = 0
#         item['BaseSqft'] = 0
#         item['Baths'] = 0
#         item['HalfBaths'] = 0
#         item['Bedrooms'] = 0
#         item['Garage'] = 0
#         item['Description'] = ""
#         item['ElevationImage'] = ""
#         item['PlanWebsite'] = ""
#         yield item
#
#         if response.url == 'https://buydestinyhomes.com/move-in-ready-homes/1500-ne-cedarwood-drive/' or response.url == 'https://buydestinyhomes.com/move-in-ready-homes/612-ne-pearl-street/':
#             unique_number = unique_number
#         else:
#             unique_number = response.meta['unique_number']
#
#         address = response.xpath('//h1[@class="entry-title"]/text()').get(default='')
#         try:
#             # Home_Name = response.xpath('//div[@class="green-title"]//span//text()').get()
#             SpecStreet1 = address.split(',')[0]
#             SpecCity = address.split(',')[1].strip().split(",")[0].strip()
#             try:
#                 SpecState = address.split(',')[2].strip().split(" ")[0].strip().replace("Polk","IA")
#             except Exception as e:
#                 print(e)
#                 SpecState = 'IA'
#             SpecZIP = address.split(',')[2].strip().split(" ")[1].strip()
#             unique = SpecStreet1 + SpecCity + SpecState + SpecZIP + response.url
#             SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
#
#             f = open("html/%s.html" % SpecNumber, "wb")
#             f.write(response.body)
#             f.close()
#
#         except Exception as e:
#             print(e)
#
#         try:
#             SpecCountry = "USA"
#         except Exception as e:
#             print(e)
#
#         try:
#             SpecPrice = response.xpath('//div[@class="property-detail-price"]/text()').get()
#             SpecPrice = SpecPrice.replace(",", "")
#             SpecPrice = re.findall(r"(\d+)", SpecPrice)[0]
#         except Exception as e:
#             print(e)
#             SpecPrice = 0
#
#         try:
#             SpecSqft = response.xpath("//span[contains(text(),'Sq')]/../text()").extract_first('')
#             SpecSqft = SpecSqft.replace(",", "")
#             SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
#         except Exception as e:
#             print(e)
#             SpecSqft = 0
#
#         try:
#             SpecBaths = response.xpath("//span[contains(text(),'Bath')]/../text()").get(default='')
#             tmp = re.findall(r'(\d+)', SpecBaths)
#             print(SpecBaths)
#             SpecBaths = SpecBaths[0]
#             if len(tmp) > 1:
#                 SpecHalfBaths = 1
#             else:
#                 SpecHalfBaths = 0
#         except Exception as e:
#             print(e)
#
#         try:
#             SpecBedrooms = response.xpath("//span[contains(text(),'Bedrooms')]/../text()").get(default='').strip()
#             SpecBedrooms = ''.join(re.findall(r'(\d+)', SpecBedrooms))
#         except Exception as e:
#             print(e)
#             SpecBedrooms = ''
#
#         SpecGarage = 0
#
#         try:
#             MasterBedLocation = "Down"
#         except Exception as e:
#             print(e)
#
#         try:
#             SpecDescription = response.xpath('//div[@class="hpc-description"]/text()').extract_first('')
#             print(SpecDescription)
#         except Exception as e:
#             print(e)
#
#         try:
#             SpecWebsite = response.url
#         except Exception as e:
#             print(e)
#
#
#
#         try:
#             images = []
#             imagedata = response.xpath(
#                 '//li/img/@src').extract()
#             for id in imagedata:
#                 id =  id
#                 images.append(id)
#             ElevationImage = images
#             print(ElevationImage)
#             SpecElevationImage = images
#         except Exception as e:
#             print(e)
#
#         # ----------------------- Don't change anything here ---------------- #
#         item = BdxCrawlingItem_Spec()
#         item['SpecNumber'] = SpecNumber
#         item['PlanNumber'] = unique_number
#         item['SpecStreet1'] = SpecStreet1
#         item['SpecCity'] = SpecCity
#         item['SpecState'] = SpecState
#         item['SpecZIP'] = SpecZIP
#         item['SpecCountry'] = SpecCountry
#         item['SpecPrice'] = SpecPrice
#         item['SpecSqft'] = SpecSqft
#         item['SpecBaths'] = SpecBaths
#         item['SpecHalfBaths'] = SpecHalfBaths
#         item['SpecBedrooms'] = SpecBedrooms
#         item['MasterBedLocation'] = MasterBedLocation
#         item['SpecGarage'] = SpecGarage
#         item['SpecDescription'] = SpecDescription
#         item['SpecElevationImage'] = "|".join(SpecElevationImage)
#         item['SpecWebsite'] = SpecWebsite
#         yield item
#
#     # --------------------------------------------------------------------- #
#
#
# if __name__ == '__main__':
#     from scrapy.cmdline import execute
#     execute('scrapy crawl buydestinyhomes'.split())
#

# -*- coding: utf-8 -*-\0import hashlib
import hashlib
import re
import time

import requests
from scrapy.http import HtmlResponse
from selenium import webdriver

import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class buydestinyhomes(scrapy.Spider):
    name = 'buydestinyhomes'
    allowed_domains = ['https://buydestinyhomes.com/']
    # start_urls = ['https://buydestinyhomes.com/']
    start_urls = ['https://buydestinyhomes.com/find-your-home/communities/']

    builderNumber = "63703"

    def parse(self, response):


        links = response.xpath('//a[@class="development-image"]/@href').extract()
        for link in links:
            print(link)
            # link ='https://buydestinyhomes.com/community/destiny-place/'
            # link ='https://buydestinyhomes.com/community/beaverbrooke/'
            # link ='https://buydestinyhomes.com/community/parkside/'
            yield scrapy.FormRequest(url=link,callback=self.community,dont_filter=True)

    def community(self,response):
        subdivisonName = response.xpath('//h1/text()').extract_first(default="")
        subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)

        city_state = response.xpath("//h4/text()").extract_first('')

        try:
            city = city_state.split(",")[0]
            print(city)
        except Exception as e:
            print(e)
            city = ''

        try:
            state = city_state.split(",")[1].replace("Iowa","IA").strip()
            print(state)
        except Exception as e:
            print(e)
            state = ''

        try:
            zip_code = response.xpath('//a[@class="listing-title"]/text()[2]').extract_first().strip()
            zip_code = zip_code.split()[-1]
            print(zip_code)
        except Exception as e:
            print(e)
            zip_code = ''


        f = open("html/%s.html" % subdivisonNumber, "wb")
        f.write(response.body)
        f.close()

        if zip_code != '':

            try:
                aminity = ''.join(response.xpath('//span/text()').getall())
                aminity = aminity.title()
            except Exception as e:
                print(e)
            a = []
            amenity_list = ["Pool", "Playground", "GolfCourse", "Tennis", "Soccer", "Volleyball", "Basketball",
                            "Baseball", "Views", "Lake", "Pond", "Marina", "Beach", "WaterfrontLots", "Park",
                            "Trails", "Greenbelt", "Clubhouse", "CommunityCenter"]
            for i in amenity_list:
                # print(i)
                if i in aminity:
                    # print(i)
                    a.append(i)
            ab = '|'.join(a)

            item2 = BdxCrawlingItem_subdivision()
            item2['sub_Status'] = "Active"
            item2['SubdivisionName'] = subdivisonName
            item2['SubdivisionNumber'] = subdivisonNumber
            item2['BuilderNumber'] = self.builderNumber
            item2['BuildOnYourLot'] = 0
            item2['OutOfCommunity'] = 1
            item2['AreaCode'] = ''
            item2['Prefix'] = ''
            item2['Suffix'] = ''
            item2['Extension'] = ""
            item2['Email'] = ""
            item2['SubDescription'] ="".join(response.xpath('//div[@class="community-description"]//p/text()').extract())
            item2['SubImage'] = response.xpath('//a[@id="first-in-tour"]/img/@src').extract_first('')
            item2['SubWebsite'] = response.url
            item2['AmenityType'] = ab

            item2['Street1'] = ''
            item2['City'] = city
            item2['State'] = state
            item2['ZIP'] = zip_code
            yield item2

            ## createing fake community -------------------------------------------#

            # images = ''
            # image = response.xpath('//div[@class="cycle-slideshow"]/img/@src').extract()
            # for i in image:
            #     images = images + i + '|'
            # images = images.strip('|')
            #
            # item = BdxCrawlingItem_subdivision()
            # item['sub_Status'] = "Active"
            # item['SubdivisionNumber'] = ''
            # item['BuilderNumber'] = self.builderNumber
            # item['SubdivisionName'] = "No Sub Division"
            # item['BuildOnYourLot'] = 0
            # item['OutOfCommunity'] = 0
            # item['Street1'] = '750 SE ALICE’S RD'
            # item['City'] = 'WAUKEE'
            # item['State'] = 'IA'
            # item['ZIP'] = '50263'
            # item['AreaCode'] = '515'
            # item['Prefix'] = '216'
            # item['Suffix'] = '1015'
            # item['Extension'] = ""
            # item['Email'] = 'info@RolwesCo.com'
            # item['SubDescription'] = 'Dedicated to delivering extraordinary building experiences; Destiny Homes offers home and lot packages throughout Iowa. When you choose Destiny Homes, you are choosing a company that will create your dream home with strength and superiority while also exceeding your expectations'
            # item['SubImage'] = 'https://buydestinyhomes.com/wp-content/uploads/2020/07/bw-denali-1920x1080.jpg|https://buydestinyhomes.com/wp-content/uploads/2020/07/dhouse-1-300x214.jpg|https://buydestinyhomes.com/wp-content/uploads/2020/07/dhouse-3-3-300x214.jpg'
            # item['SubWebsite'] = response.url
            # item['AmenityType'] = ''
            # yield item


            spec_links = response.xpath('//div[@class="featured-listing-wrap"]/div[@class="listing-thumb"]/a[contains(@href,"homes-for-sale")]/@href').extract()
            links = response.xpath('//div[@class="featured-listing-wrap"]/div[@class="class="]/a[contains(@href,"/home-plans")]/@href').extract()
            for link in links:
                print(link)
                yield scrapy.FormRequest(url=link,callback=self.parse3,dont_filter=True,meta={'subdivisonNumber':subdivisonNumber,'spec_links':spec_links})


                # EXE_PATH = r"D:\chromedriver.exe"
                # options = webdriver.ChromeOptions()
                # # options.add_argument("--headless")
                # # options.add_argument("user-data-dir=C:\\Users\\xbyte\\AppData\\Local\\Google\\Chrome\\User Data")
                # driver = webdriver.Chrome(executable_path=EXE_PATH, options=options)
                #
                # url = "https://buydestinyhomes.com/find-your-home/home-plans/"
                # driver.get(url)
                # time.sleep(5)
                # key = True
                # while key:
                #     try:
                #         s = lambda x: driver.execute_script('return document.body.parentNode.scroll' + x)
                #         driver.set_window_size(s('Width'), s('Height'))
                #         # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                #         time.sleep(3)
                #         driver.find_element_by_xpath('//button[@class="wpgb-button wpgb-load-more"]').click()
                #         # driver.execute_script("arguments[0].click();", button1)
                #         # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                #         time.sleep(5)
                #     except Exception as e:
                #         key = False
                #
                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # time.sleep(5)
                #
                # response = HtmlResponse(url=driver.current_url, body=driver.page_source, encoding="utf-8")
                # links = response.xpath('//div[@class="wpgb-card-wrapper"]//a[@class="wpgb-card-layer-link"]/@href').extract()
                # print(len(links))
                # for link in links:
                #     yield scrapy.Request(url=link, dont_filter=True, callback=self.parse3)
                # # # link = 'https://buydestinyhomes.com/find-your-home/move-in-ready-homes/'
                # # yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)

                # def parse2(self, response):
                #     links = response.xpath('//div[@class="class="]/a/@href').extract()
                #     for link in links:
                #         print(link)
                #         yield scrapy.FormRequest(url=link, callback=self.parse3, dont_filter=True)
                #         # yield scrapy.FormRequest(url='https://www.brookstonecg.com/home-plan/51778hz',callback=self.parse3,dont_filter=True,headers=self.headers)

    def parse3(self, response):

        subdivisonNumber  = response.meta['subdivisonNumber']
        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//h1[@class="hpc-title entry-title"]/text()').get()
        except Exception as e:
            PlanName = ''
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName + response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            PlanNumber = ''
            print(e)

        # try:
        #     SubdivisionNumber = self.builderNumber
        #     print(SubdivisionNumber)
        # except Exception as e:
        #     SubdivisionNumber = ''
        #     print(e)

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
            sqft = response.xpath('//div[@class="hpc-label"][contains(text(),"SQ FT")]/text()').extract_first('')
            # sqft = sqft.split("|")[0]
            sqft = sqft.replace(',', '').replace(".", "").strip()
            BaseSqft = re.findall(r"(\d+)", sqft)[0]

        except Exception as e:
            print(e)
            BaseSqft = ''

        try:
            bath = response.xpath("//div[@class='hpc-label'][contains(text(),'Baths')]/text()").extract_first()
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
            Bedrooms = response.xpath("//div[@class='hpc-label'][contains(text(),'Bedrooms')]/text()").extract_first()
            if '-' in Bedrooms:
                Bedrooms = Bedrooms.split("-")[1]
            # Bedrooms = Bedrooms.split("|")[1].split("|")[0]
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)

        try:
            Garage = response.xpath("//div[@class='hpc-label'][contains(text(),'Car')]/text()").extract_first()
            if '-' in Garage:
                Garage = Garage.split("-")[1]
            # Bedrooms = Bedrooms.split("|")[1].split("|")[0]
            Garage = re.findall(r"(\d+)", Garage)[0]
        except Exception as e:
            Garage = 0
            print(e)

        try:
            Description = response.xpath('//div[@class="hpc-description"]/p/text()').extract_first('')
            print(Description)
        except Exception as e:
            print(e)
            Description=''

        try:

            # images1 = response.xpath('//li[@class="dmCoverImgContainer"]/img/@src').extract()
            #
            # images2 = response.xpath('//div[@class="u_1929991324 imageWidget align-center"]/a/img/@src').extract_first('')
            images = []
            imagedata = response.xpath('//div[@class="kb-gallery-image-contain kadence-blocks-gallery-intrinsic kb-gallery-image-ratio-land32"]/img/@src').extract()
            for id in imagedata:
                id = id
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
        unique = str(PlanNumber) + str(subdivisonNumber) + str(Baths) + str(Bedrooms)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['Type'] = Type
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number  # < -------- Changes here
        item['SubdivisionNumber'] = subdivisonNumber
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

        # links = response.xpath('//div[@class="listing-thumb"]/a/@href').extract()
        # templink = ['https://buydestinyhomes.com/move-in-ready-homes/1500-ne-cedarwood-drive/','https://buydestinyhomes.com/move-in-ready-homes/612-ne-pearl-street']
        # #----- fake plan #
        #
        #
        # links = links + templink
        # for link in links:
        #     print(link)
        #     yield scrapy.FormRequest(url=link,callback=self.parse4,dont_filter=True,meta={'unique_number':unique_number})
        #     # yield scrapy.FormRequest(url='https://buydestinyhomes.com/move-in-ready-homes/114-destiny-drive/',callback=self.parse4,dont_filter=True,meta={'unique_number':unique_number})


        # def parse4(self,response):

        item = BdxCrawlingItem_Plan()
        unique = str("Plan Unknown") + str(subdivisonNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item['unique_number'] = unique_number
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = "Plan Unknown"
        item['SubdivisionNumber'] = subdivisonNumber
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

        spec_links = response.meta['spec_links']
        for spec in spec_links:
            print(spec)
            yield scrapy.FormRequest(url=spec,callback=self.spec,dont_filter=True,meta={'subdivisonNumber':subdivisonNumber,'unique_number':unique_number})

    def spec(self,response):
        unique_number = response.meta['unique_number']

        # if response.url == 'https://buydestinyhomes.com/move-in-ready-homes/1500-ne-cedarwood-drive/' or response.url == 'https://buydestinyhomes.com/move-in-ready-homes/612-ne-pearl-street/':
        #     unique_number = unique_number
        # else:
        #     unique_number = response.meta['unique_number']

        address = response.xpath('//h1[@class="entry-title"]/text()').get(default='')
        try:
            # Home_Name = response.xpath('//div[@class="green-title"]//span//text()').get()
            SpecStreet1 = address.split(',')[0]
            SpecCity = address.split(',')[1].strip().split(",")[0].strip()
            try:
                SpecState = address.split(',')[2].strip().split(" ")[0].strip().replace("Polk","IA")
            except Exception as e:
                print(e)
                SpecState = 'IA'
            SpecZIP = address.split(',')[2].strip().split(" ")[1].strip()
            unique = SpecStreet1 + SpecCity + SpecState + SpecZIP + response.url
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
            SpecPrice = response.xpath('//div[@class="property-detail-price"]/text()').get()
            SpecPrice = SpecPrice.replace(",", "")
            SpecPrice = re.findall(r"(\d+)", SpecPrice)[0]
        except Exception as e:
            print(e)
            SpecPrice = 0

        try:
            SpecSqft = response.xpath("//span[contains(text(),'Sq')]/../text()").extract_first('')
            SpecSqft = SpecSqft.replace(",", "")
            SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
        except Exception as e:
            print(e)
            SpecSqft = 0

        try:
            SpecBaths = response.xpath("//span[contains(text(),'Bath')]/../text()").get(default='')
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
            SpecBedrooms = response.xpath("//span[contains(text(),'Bedrooms')]/../text()").get(default='').strip()
            SpecBedrooms = ''.join(re.findall(r'(\d+)', SpecBedrooms))
        except Exception as e:
            print(e)
            SpecBedrooms = ''

        SpecGarage = 0

        try:
            MasterBedLocation = "Down"
        except Exception as e:
            print(e)

        try:
            SpecDescription = response.xpath('//div[@class="hpc-description"]/text()').extract_first('')
            print(SpecDescription)
        except Exception as e:
            print(e)

        try:
            SpecWebsite = response.url
        except Exception as e:
            print(e)



        try:
            images = []
            imagedata = response.xpath(
                '//li/img/@src').extract()
            for id in imagedata:
                id =  id
                images.append(id)
            ElevationImage = images
            print(ElevationImage)
            SpecElevationImage = images
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
        item['SpecElevationImage'] = "|".join(SpecElevationImage)
        item['SpecWebsite'] = SpecWebsite
        yield item

    # --------------------------------------------------------------------- #


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl buydestinyhomes'.split())

