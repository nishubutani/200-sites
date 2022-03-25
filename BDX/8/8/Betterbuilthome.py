import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class BetterbuilthomeSpider(scrapy.Spider):
    name = 'Betterbuilthome'
    allowed_domains = []
    start_urls = ['http://betterbuilthomesmi.com/']
    builderNumber = 52915

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
        item['Street1'] = '5529 Jada'
        item['City'] = 'Highland'
        item['State'] = 'MI'
        item['ZIP'] = '48356'
        item['AreaCode'] = '248'
        item['Prefix'] ='894'
        item['Suffix'] = '6428'
        item['Extension'] = ""
        item['Email'] ='info@betterbuilthomesmi.com'
        item['SubDescription'] ='Our goal is simple; to get you into a home that is well built, reliable and affordable.A home you will love and want to show off to your friends and family. There is a big difference between a house and your home. Allow us to show you that difference. At Better Built Homes, we do just what our name implies, and we do it with honesty, integrity and an old-fashioned sense of pride in what we do. With 20 years’ experience in the homebuilding industry, you can count on owner Chuck Burt to build the house of your dreams.'
        item['SubImage']= ''
        item['SubWebsite'] = response.url
        yield item


        link = 'http://betterbuilthomesmi.com/homes/'
        yield scrapy.FormRequest(url=link,callback=self.home_link,dont_filter=True)

    def home_link(self,response):
        links = response.xpath('//*[@class="inner clear"]/div/a[1]/@href').extract()
        print(links)
        for i in links:
            print(i)
            # i1 = 'http://betterbuilthomesmi.com/homes/white-eagle/towering-oaks/'
            yield scrapy.FormRequest(url=i,callback=self.home_detail)

    def home_detail(self,response):
        print(response.url)
        try:
            PlanName = response.xpath('//*[@id="title-banner"]/div/h1/text()').extract_first()
            print(PlanName)
        except Exception as e:
            print("PlanName ",e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % PlanNumber, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
            print(e)

        try:
            BasePrice = response.xpath('//*[contains(text(),"Priced")]/text()').extract_first()
            if BasePrice == None or BasePrice == '':
                BasePrice = response.xpath('//*[contains(text(),"Starting at")]/text()').extract_first().replace(',','')
            BasePrice =BasePrice.replace(',','')
            BasePrice = re.findall(r"(\d+)", BasePrice)[0]
            print(BasePrice)
        except Exception as e:
            BasePrice = 0
        try:
            BaseSqft = response.xpath('//*[contains(text(),"BASIC LAYOUT")]/../text()[2]').extract_first()
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
            print(BaseSqft)
        except Exception as e:
            BaseSqft = 0
        try:
            Bedrooms = response.xpath('//*[contains(text(),"BASIC LAYOUT")]/../text()[4]').extract_first()
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            print(Bedrooms)
        except Exception as e:
            Bedrooms = 0
        try:
            Baths = response.xpath('//*[contains(text(),"BASIC LAYOUT")]/../text()[5]').extract_first()
            tmp = re.findall(r"(\d+)", Baths)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
                print(HalfBaths)
            else:
                HalfBaths = 0
                print(HalfBaths)
        except Exception as e:
            Baths = 0
            HalfBaths = 0

        try:
            Garage = response.xpath('//*[contains(text(),"LIVING")]/../text()[2]').extract_first()
            Garage = re.findall(r"(\d+)", Garage)[0]
            print(Garage)
        except Exception as e:
            Garage = 0



        try:
            ElevationImage = re.findall(r' style="background-image: url(\(.*?)\)',response.text)
            print(ElevationImage)
            if ElevationImage == '':
                ElevationImage = re.findall(r'style="position: fixed; width: 100%; background-image: url(\(.*?)\)',response.text)
            ElevationImage = '|'.join(ElevationImage).replace("'","").replace("(","")
            print(ElevationImage)
        except ElevationImage as e:
            ElevationImage = ""


        SubdivisionNumber = self.builderNumber #if subdivision is not available
        unique = str(PlanNumber)+str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = PlanName
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = BasePrice
        item['BaseSqft'] = BaseSqft
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = "Our goal is simple; to get you into a home that is well built, reliable and affordable.A home you will love and want to show off to your friends and family. There is a big difference between a house and your home. Allow us to show you that difference. At Better Built Homes, we do just what our name implies, and we do it with honesty, integrity and an old-fashioned sense of pride in what we do. With 20 years’ experience in the homebuilding industry, you can count on owner Chuck Burt to build the house of your dreams."
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = response.url
        yield item


# execute("scrapy crawl Betterbuilthome".split())