

# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'blvdhomes'
    allowed_domains = ['https://blvdhomes.com/']
    start_urls = ['https://blvdhomes.com/']

    builderNumber = "63656"

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
        item['Street1'] = ''
        item['City'] = 'Franklin'
        item['State'] = 'TN'
        item['ZIP'] = '37064'
        item['AreaCode'] = '615'
        item['Prefix'] ='799'
        item['Suffix'] = '5391'
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = 'Boulevard Homes is a home design and construction company building in Metro Nashville, TN and throughout Williamson county including Franklin, Brentwood and Fairview. We custom design and draw the majority of our home plans. This gives us the ability to play upon the special features of a home site to help create a truly unique home!'
        item['SubImage'] = 'https://blvdhomes.com/wp-content/uploads/2017/09/10_TNHometour-017_mls.jpg|https://blvdhomes.com/wp-content/uploads/2019/09/0.jpg|https://blvdhomes.com/wp-content/uploads/2019/09/0-1.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'https://blvdhomes.com/homes'
        yield scrapy.FormRequest(url=link, callback=self.parse2, dont_filter=True)

    def parse2(self, response):
        links = response.xpath('//div[@class="home-btn"]/a/@href').extract()
        for link in links:
            print(link)
            yield scrapy.FormRequest(url=link, callback=self.parse3, dont_filter=True)

    def parse3(self, response):

        try:
            status = response.xpath("//span[contains(text(),'Status: ')]/../text()").extract_first('')
            print(status)
        except Exception as e:
            print(e)
            status = ''


        if status == 'Available':

            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                PlanName = response.xpath('//h3/text()').get()
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
                Bas = response.xpath("//span[contains(text(),'Price')]/../text()").extract_first('')
                Bas = Bas.replace(",","")
                BasePrice = re.findall(r"(\d+)", Bas)[0]
            except Exception as e:
                print(e)
                BasePrice = 0

            try:
                sqft = response.xpath("//span[contains(text(),'SQFT')]/../text()").extract_first('')
                sqft = sqft.replace(',', '').replace(".","").strip()
                BaseSqft = re.findall(r"(\d+)", sqft)[0]

            except Exception as e:
                print(e)
                BaseSqft = ''

            try:
                bath = response.xpath("//span[contains(text(),'Baths')]/../text()").extract_first()
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
                Bedrooms = response.xpath("//span[contains(text(),'Bedrooms: ')]/../text()").extract_first()
                if '-' in Bedrooms:
                    Bedrooms = Bedrooms.split("-")[1]
                # Bedrooms = Bedrooms.split("|")[1].split("|")[0]
                Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            except Exception as e:
                print(e)
                Bedrooms = ''

            try:
                Garage = response.xpath("//span[contains(text(),'Garage')]/../text()").extract_first()
                Garage = re.findall(r"(\d+)", Garage)[0]
            except Exception as e:
                print(e)
                Garage = 0



            try:
                Description = response.xpath("//h3/../p/text()").extract_first('').strip()
                print(Description)
                # if Description == '':
                #     Description = 'Boulevard Homes is a home design and construction company building in Metro Nashville, TN and throughout Williamson county including Franklin, Brentwood and Fairview. We custom design and draw the majority of our home plans. This gives us the ability to play upon the special features of a home site to help create a truly unique home!'
            except Exception as e:
                print(e)


            try:

                # images1 = response.xpath('//li[@class="dmCoverImgContainer"]/img/@src').extract()
                #
                # images2 = response.xpath('//div[@class="u_1929991324 imageWidget align-center"]/a/img/@src').extract_first('')
                images = []
                imagedata = response.xpath('//div[@class="image-listing"]/img/@src').extract()
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
            unique = str(PlanNumber) + str(SubdivisionNumber) + str(Baths) + str(Bedrooms) #< -------- Changes here
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
            item['Description'] = Description
            item['ElevationImage'] = "|".join(ElevationImage)
            item['PlanWebsite'] = PlanWebsite
            yield item



    # --------------------------------------------------------------------- #

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl blvdhomes'.split())