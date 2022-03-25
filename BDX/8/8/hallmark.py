# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header

class hallmarkSpider(scrapy.Spider):
    name = 'hallmark'
    allowed_domains = []
    start_urls = ['http://hallmarkbuildersinc.net/']
    builderNumber = 27640

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
        item['Street1'] = '8620 Trinity Road Suite 202'
        item['City'] = 'Cordova'
        item['State'] = 'TN'
        item['ZIP'] = '38018'
        item['AreaCode'] = '901'
        item['Prefix'] ='753'
        item['Suffix'] = '3950'
        item['Extension'] = ""
        item['Email'] =''
        item['SubDescription'] ='Hallmark Builders Inc has been building homes in the Memphis area since 1983, building over 1000 homes from $80,000 to over $2,000,000. The three principals Doug Bayliff, Ronnie Faulkner and Harry Todtman have been working together since 1978. They have earned a solid reputation for building a quality semi-custom home with many amenities at a reasonable price. The company at the present time is concentrating it’s efforts in the Memphis suburbs of Arlington and Lakeland.  Each with it’s own superior school system and small town atmosphere making Arlington and Lakeland two of the most desirable areas to live and raise a family. Both towns are located conveniently located off I-40 and a short distance to Memphis’ biggest mall, stores and restaurants.'
        item['SubImage']= 'http://hallmarkbuildersinc.net/wp-content/uploads/2017/05/sectionheader.jpg|http://hallmarkbuildersinc.net/wp-content/uploads/2017/05/slide1.jpg|http://hallmarkbuildersinc.net/wp-content/uploads/2017/05/DSC_0709.jpg|http://hallmarkbuildersinc.net/wp-content/uploads/2017/04/Floorplans.jpg'
        item['SubWebsite'] = response.url
        yield item

        pl = 'http://hallmarkbuildersinc.net/our-floorplans/'
        yield scrapy.FormRequest(url=pl,callback=self.plinks,dont_filter=True)

    def plinks(self,response):
        links1 = response.xpath('//*[@class="row-hover"]//td/a/@href').extract()
        links2 = ['http://hallmarkbuildersinc.net/project/chateau-iii/']
        links = links1 + links2
        print(len(links))
        for link in links:
            print(link)
            yield scrapy.FormRequest(url=link,callback=self.PlanDetail,dont_filter=True)

    def PlanDetail(self,response):
        print(response.url)
        try:
            PlanName = response.xpath('//div[@class="header-content"]/h1/text()').extract_first().strip()
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
            Bedroom = response.xpath('//*[contains(text(),"BED")]/text()').extract_first()
            Bedrooms = Bedroom.split(' BED')[0]
            print(Bedrooms)
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            print(Bedrooms)
        except Exception as e:
            Bedrooms = 0
            print("Bedrooms: ", e)

        try:
            Bathroom = response.xpath('//*[contains(text(),"BATH")]/text()').extract_first()
            print(Bathroom)
            Bathroom = Bathroom.split(' BATH')[0].split('BED ·')[-1].strip()
            tmp = re.findall(r"(\d+)", Bathroom)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0

        except Exception as e:
            Baths = 0
            print("Baths: ", e)

        try:
            Garage = 0
        except Exception as e:
            Garage = 0
            print("Garage: ", e)

        try:
            BaseSqft = response.xpath('//*[contains(text(),"SQ FT")]/text()').extract_first()
            BaseSqft = BaseSqft.split('BATH ·')[-1].split(' SQ FT')[0].replace(',','')
            # print(BaseSqft)
            BaseSqft = ''.join(re.findall(r"(\d+)", BaseSqft))
            BaseSqft = BaseSqft.strip()
            print(BaseSqft)
        except Exception as e:
            print("BaseSQFT: ", e)

        # try:
        #     ElevationImage = re.findall('<img src="(.*?)"', response.text)
        #     ElevationImage = "|".join(ElevationImage)
        #     print(ElevationImage)
        #
        # except Exception as e:
        #     print(str(e))

        try:
            ElevationsImages = []
            try:ElevationsImag1 = response.xpath('//*[@class="et_pb_lightbox_image"]/@href').extract()
            except :ElevationsImag1 = ''
            try:ElevationsImag2 = response.xpath('//div[@class=" et_pb_row et_pb_row_0"]/div//img/@src').extract()
            except:ElevationsImag2 = ''
            ElevationsImag = ElevationsImag1 + ElevationsImag2
            for i in ElevationsImag:
                ElevationsImages.append(i)
        except Exception as e:
            print("ElevationsImages: ",e)

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
        item[
            'Description'] = 'We have access to building sites, in nearly every development in the area! Bring us your custom home plans or choose from one of the many popular plans in our library. Click one of the thumbnails below for a PDF sheet with full details.'
        item['ElevationImage'] = '|'.join(ElevationsImages)
        item['PlanWebsite'] = PlanWebsite
        yield item


# if __name__ == '__main__':
    # execute("scrapy crawl hallmark".split())