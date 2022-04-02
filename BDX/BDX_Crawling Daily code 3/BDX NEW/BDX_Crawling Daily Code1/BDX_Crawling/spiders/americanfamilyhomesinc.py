# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'americanfamilyhomesinc'
    allowed_domains = ['https://www.americanfamilyhomesinc.com/']
    start_urls = ['https://www.americanfamilyhomesinc.com/']

    builderNumber = "50820"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

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
        item['Street1'] = '312 South Bay Street'
        item['City'] = 'Eustis'
        item['State'] = 'FL'
        item['ZIP'] = '32726'
        item['AreaCode'] = ''
        item['Prefix'] =''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = 'American Family Homes founding principle and stated goal of “Commitment to Quality and Satisfaction” has consistently guided its founder and employees, and has been the company’s expectation of its sub-contractors and suppliers in every aspect of the home building and remodeling business. With that motto it is very clear that 100% Customer Satisfaction is our #1 priority'
        item['SubImage'] = "https://www.americanfamilyhomesinc.com/zupload/library/20/-86-525x370-1.jpg?ztv=20180228112317|https://www.americanfamilyhomesinc.com/zupload/library/20/-85-525x370-1.jpg?ztv=20180228112317|https://www.americanfamilyhomesinc.com/zupload/library/20/-84-525x370-1.jpg?ztv=20180228112317|https://www.americanfamilyhomesinc.com/zupload/library/20/-83-525x370-1.jpg?ztv=20180228112317|https://www.americanfamilyhomesinc.com/zupload/library/20/-82-525x370-1.jpg?ztv=20180228112317"
        item['SubWebsite'] = 'https://www.americanfamilyhomesinc.com/'
        item['AmenityType'] = ''
        yield item

        link = 'https://www.americanfamilyhomesinc.com/homes/index'
        yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)

    def parse2(self,response):
        links = response.xpath("//a[contains(text(),'Learn More')]/@href").extract()
        for link in links:
            link = 'https://www.americanfamilyhomesinc.com' + link
            yield scrapy.FormRequest(url=link,callback=self.parse3,dont_filter=True)
            
    def parse3(self,response):
        
        try:
            PlanName = response.xpath('//div[@class="head z-t-48 mont z-pb-20"]/text()').extract_first()
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
            Bedroo = response.xpath('//div[@class="text z-t-20 z-text-white"]/text()[4]').extract_first().strip()
            print(Bedroo)
            Bedroom = Bedroo.split(',')[0]
            Bedrooms = re.findall(r"(\d+)", Bedroom)[0]
            # Bedrooms = Bedroom.split(' Bed')[0].strip()

        except Exception as e:
            Bedrooms = 0
            print("Bedrooms: ", e)

        try:
            Bathroo = response.xpath('//div[@class="text z-t-20 z-text-white"]/text()[5]').extract_first().strip()
            # Baths = Bathroo.split(',')[1]
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
            Garage = response.xpath('//div[@class="text z-t-20 z-text-white"]/text()[6]').extract_first().strip().replace(',', '')
            Garage = re.findall(r"(\d+)", Garage)[0]
        except Exception as e:
            print("Garage: ", e)
            Garage = 0

        try:
            BaseSqft = response.xpath('//div[@class="text z-t-20 z-text-white"]/text()[7]').extract_first().strip().replace(',', '')
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
        except Exception as e:
            print("BaseSQFT: ", e)

        try:
            ElevationImages = []
            ElevationImage1 = response.xpath('//div[@class="left z-float-left"]/img/@src').extract_first('')
            ElevationImage2 = response.xpath('//a[@title="Image 1"]/@href').extract_first('')
            if ElevationImage1 != '':
                ElevationImage1 = 'https://www.americanfamilyhomesinc.com' + ElevationImage1
            if ElevationImage2 != '':
                ElevationImage2 = 'https://www.americanfamilyhomesinc.com' + ElevationImage2
                ElevationImages.append(ElevationImage2)
                ElevationImages.append(ElevationImage1)

            ElevationImage = "|".join(ElevationImages)

        except Exception as e:
            print(str(e))

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

    # ---------------------------------------------------------------------

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl americanfamilyhomesinc'.split())
