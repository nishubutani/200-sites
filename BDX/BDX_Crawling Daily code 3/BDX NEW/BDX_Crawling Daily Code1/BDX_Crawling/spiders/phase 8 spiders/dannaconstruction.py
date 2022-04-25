import hashlib
import re
import time
from selenium.webdriver.chrome.options import Options
import scrapy
from scrapy.http import HtmlResponse

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class DannaconstructionSpider(scrapy.Spider):
    name = 'dannaconstruction'
    allowed_domains = ['www.dannaconstruction.com']
    start_urls = ['http://https://www.dannaconstruction.com/']
    builderNumber = '52920'

    def start_requests(self):
        url = 'https://www.dannaconstruction.com/communities'
        yield scrapy.FormRequest(url=url)

    def parse(self, response):

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
            item['Street1'] = '51246 Woodside Drive'
            item['City'] = 'Washington'
            item['State'] = 'MI'
            item['ZIP'] = '48042'
            item['AreaCode'] = '586'
            item['Prefix'] = '685'
            item['Suffix'] = '1335'
            item['Extension'] = ""
            item['Email'] = 'DannaConstruction@gmail.com'
            des = response.xpath('//*[@class="p2inlineContent"]//*[@class="font_8"]/text()').getall()
            desc=[]
            for i in des:
                if len(i)>20:
                    desc.append(i)
            item['SubDescription'] = ''.join(desc)
            image = response.xpath('//*[@class="p2inlineContent"]//*[@itemprop="image"]/@src').getall()
            item[
                'SubImage'] = '|'.join(image)
            item['SubWebsite'] = response.url
            yield item

            unique = str("Plan Unknown") + str(self.builderNumber)  # < -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
            item = BdxCrawlingItem_Plan()
            item['unique_number'] = unique_number
            item['Type'] = "SingleFamily"
            item['PlanNumber'] = "Plan Unknown"
            item['SubdivisionNumber'] = self.builderNumber
            item['PlanName'] = "Plan Unknown"
            item['PlanNotAvailable'] = 1
            item['PlanTypeName'] = 'Single Family'
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

            homelink = 'https://www.dannaconstruction.com/ready-to-move-in-homes'

            yield scrapy.FormRequest(url=homelink,callback=self.home,meta={'PN':unique_number})

    def home(self,response):

        item = BdxCrawlingItem_Spec()
        try:
            options = Options()
            options.headless = True
            from selenium import webdriver

            driver = webdriver.Chrome(chrome_options=options, executable_path="chromedriver.exe")
            driver.maximize_window()
            time.sleep(15)

            driver.get(response.url)

            res = driver.page_source
            response = HtmlResponse(url=driver.current_url, body=bytes(res.encode('utf-8')))
            print(response)

            detail = response.xpath('//*[@style="width: 285px; pointer-events: none;"]')
            images = response.xpath('//*[@style="object-position:50% 50%;width:275px;height:190px;object-fit:cover"]')
            # # adds = response.xpath('//*[@id="content"]')
            # adds = ['60017 Stonecrest Dr. Washington Twp., mi ','60872 Stonecrest Dr. Washington Twp MI 48094']

            # for detail,image,add in zip(details,images,adds):
                # sold = detail.xpath('.//*[@style="object-position:50% 50%;width:409px;height:305px;object-fit:cover"]/@src').get()
                # if sold != "https://static.wixstatic.com/media/cee51c_44306aa03b16423a9a63e7d3e715fc19.png/v1/fill/w_409,h_305,al_c,lg_1,q_85/cee51c_44306aa03b16423a9a63e7d3e715fc19.webp":


            address = '60872 Stonecrest Dr. Washington Twp MI 48094'
            SpecStreet1 = address.split('.')[0]
            # SpecState = re.findall(r'([A-Z]{2})',address)[0]
            SpecState ="MI"
            SpecCity = address.split('.')[1].split(SpecState)[0].strip()
            SpecZIP = re.findall(r'(\d+)',address)[1]


            try:

                unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
            except Exception as e:
                SpecNumber = ''

            item['SpecNumber'] = SpecNumber
            item['SpecStreet1'] = SpecStreet1
            item['SpecCity'] = SpecCity
            item['SpecState'] = SpecState
            item['SpecZIP'] = SpecZIP


            unique = str("Plan Unknown") + str(self.builderNumber)  # < -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
                    10 ** 30)
            PlanNumber = unique_number

            item['PlanNumber'] = PlanNumber



            SpecBedrooms = detail.xpath(
                '//*[contains(text(),"Bedrooms")]/text()').extract()[-1]
            SpecBedrooms = re.findall(r"(\d+)", SpecBedrooms)
            SpecBedrooms = SpecBedrooms[0]



            SpecBath = detail.xpath(
                '//*[contains(text(),"Bathrooms")]/text()').extract()[-1].strip().replace('.','')
            SpecBaths = re.findall(r"(\d+)", SpecBath)[-1]

            tmp = SpecBaths
            if len(tmp) > 1:
                SpecBaths = SpecBaths[0]
                SpecHalfBaths = 1
            else:
                SpecBaths = SpecBaths
                SpecHalfBaths = 0
            # print(SpecBaths)




            SpecGarage = detail.xpath('//*[contains(text(),"Garages")]/text()').extract()[-1].strip().replace('.','')
            SpecGarage = re.findall(r"(\d+)", SpecGarage)[-1]
            if len(SpecGarage)>1:
                SpecGarage = SpecGarage[0]+'.'+SpecGarage[1]




            SpecSqft = detail.xpath('//*[contains(text(),"sq,ft")]/text()').extract()[-1].strip().replace(',','')
            SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]






            descr = "D'Anna Construction Company understands the amount of pressure and stress of building a new home could be. That is why we believe that building a relationship with our clients is one of the most important aspects in building a new home. We offer high quality materials and work with the best craftsmanship in the business! We at D'Anna Construction understand that time is precious and don't take it for granted. Here are our custom 'Ready to Move in Homes'  available for you."



            ElevationImage = images.xpath('./@src').extract()[-1]





            SpecWebsite = response.url



        # ----------------------- Don't change anything here --------------------- #


            item['SpecCountry'] = "USA"
            item['SpecPrice'] = 0
            item['SpecSqft'] = SpecSqft
            item['SpecBaths'] = SpecBaths
            item['SpecHalfBaths'] = SpecHalfBaths
            item['SpecBedrooms'] = SpecBedrooms
            item['MasterBedLocation'] = "Down"
            item['SpecGarage'] = SpecGarage
            item['SpecDescription'] = descr
            item['SpecElevationImage'] = ElevationImage
            item['SpecWebsite'] = SpecWebsite
            yield item

        except Exception as e:
            print(e)


from scrapy.cmdline import execute
# execute("scrapy crawl dannaconstruction".split())

