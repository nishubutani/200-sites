import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header
from bs4 import BeautifulSoup

class CramercustomHomesSpider(scrapy.Spider):
    name = 'cramercustomhomes'
    allowed_domains = []
    start_urls = ['http://cramercustomhomes.com/']
    builderNumber = 51983

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
        item['Street1'] = 'PO BOX 1181'
        item['City'] = 'Mahomet'
        item['State'] = 'IL'
        item['ZIP'] = '61853'
        item['AreaCode'] = '217'
        item['Prefix'] = '840'
        item['Suffix'] = '9178'
        item['Extension'] = ""
        item['Email'] = ''
        item[
            'SubDescription'] = 'Put aside the notion that building a home is an “overwhelming” experience.Our goal is to make sure that building your home with Cramer Homes is exciting and memorable. Our design and supply partners make the selection process easy and fun! You may only build one home in a lifetime; our objective as your home builder is to be sure you enjoy the whole process and the finished product!'
        item[
            'SubImage'] = 'http://cramercustomhomes.net/wp-content/uploads/2013/10/Home_Page_Pix_1_1900x1100.jpg|http://cramercustomhomes.net/wp-content/uploads/2013/10/Home_Page_Pix_5_1900x1100.jpg|http://cramercustomhomes.net/wp-content/uploads/2013/10/Home_Page_Pix_2_1900x1100.jpg|http://cramercustomhomes.net/wp-content/uploads/2013/10/Home_page_Pix_4_1900x1100.jpg|http://cramercustomhomes.net/wp-content/uploads/2013/10/Home_Page_Pix_6_1900x1100.jpg|http://cramercustomhomes.net/wp-content/uploads/2013/10/Home_Page_Pix_2_1900x1100.jpg'
        item['SubWebsite'] = response.url
        yield item

        plan_link = 'http://cramercustomhomes.com/build-your-dream-home/home-plans/'
        yield scrapy.FormRequest(url=plan_link, callback=self.planDetail, dont_filter=True,meta={'sbdn':self.builderNumber})

    def planDetail(self, response):
        divs = response.xpath('//div[@class="content-full-width"][2]/div')
        ElevationImages = response.xpath('//div[@class="content-full-width"]/div').getall()
        for div,ElevationImage in zip(divs,ElevationImages):
            try:
                PlanName = div.xpath('.//div/p/text()').extract_first()
                # print(PlanName)
            except Exception as e:
                print("PlanName: ",e)
            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
            except Exception as e:
                print(e)

            try:
                SubdivisionNumber = response.meta['sbdn']
                # print(SubdivisionNumber)
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
                Bedroo = div.xpath(
                    './/*[contains(text(),"Bed")]').extract_first().strip()
                Bedroom = Bedroo.split('|')[1]
                Bedrooms = Bedroom.split(' Bed')[0].strip()

            except Exception as e:
                Bedrooms = 0
                print("Bedrooms: ",e)

            try:
                Bathroo = div.xpath(
                    './/*[contains(text(),"Bath")]').extract_first().strip()
                Bathroom = Bathroo.split('|')[1]
                Baths = Bathroom.split(' Bed,')[1].strip()
                tmp = re.findall(r"(\d+)", Baths)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0

            except Exception as e:
                Baths = 0
                print("Baths: ", e)

            Garage = 0
            try:
                BaseSqft = div.xpath(
                    './/*[contains(text(),"sq ft")]').extract_first().strip().replace(',','')
                if "|" in BaseSqft:
                    BaseSqf = BaseSqft.split('|')[0]
                    BaseSqft = ''.join(re.findall(r"(\d+)", BaseSqf))
                    BaseSqft = BaseSqft.strip()
                print(BaseSqft)
            except Exception as e:
                print("BaseSQFT: ",e)

            try:
                print(PlanName)
                if PlanName == "Carabella":
                    ElevationImages = "http://cramercustomhomes.net/wp-content/uploads/2013/10/Carabella_300x175.jpg"
                elif PlanName == "Lakewood":
                    ElevationImages = "http://cramercustomhomes.net/wp-content/uploads/2013/10/Lakewood_300x175.jpg"
                elif PlanName == "South Hampton":
                    ElevationImages = "http://cramercustomhomes.net/wp-content/uploads/2013/10/SouthHampton_300x175.jpg"
                elif PlanName == "San Marco":
                    ElevationImages = "http://cramercustomhomes.net/wp-content/uploads/2014/05/SanMarco_300x175.jpg"
                else:
                    ElevationImages = []
                    c = re.findall(r'<a href="(.*?)" rel=',ElevationImage)
                    for j in c:
                        ElevationImages.append(j)
                    ElevationImages = "|".join(ElevationImages)
            except Exception as e:
                    print(str(e))

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
            item['Description'] = 'We have access to building sites, in nearly every development in the area! Bring us your custom home plans or choose from one of the many popular plans in our library. Click one of the thumbnails below for a PDF sheet with full details.'
            item['ElevationImage'] = ElevationImages
            item['PlanWebsite'] = PlanWebsite
            yield item

if __name__ == '__main__':
    execute("scrapy crawl cramercustomhomes".split())