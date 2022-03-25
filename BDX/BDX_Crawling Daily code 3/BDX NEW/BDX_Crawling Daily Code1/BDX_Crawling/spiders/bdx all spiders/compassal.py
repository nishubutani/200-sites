

# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class vtshomeshomesSpider(scrapy.Spider):
    name = 'compassal'
    allowed_domains = []
    start_urls = ['https://cedarloghomesofokla.com/']

    builderNumber = "48380"

    def parse(self, response):
        print('--------------------')

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = '51152'
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '2225 Highway 72 East'
        item['City'] = 'Huntsville'
        item['State'] = 'AL'
        item['ZIP'] = '35811'
        item['AreaCode'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Prefix'] = ""
        item['Email'] = ''
        item['SubDescription'] = "The ELM Foundation was built on the idea that, together, we have the power to create transformational change. ELM works every day to take on the fundamental issues that challenge the growth and success of the people in our communities, supporting those in need in our region and supporting those who support others."
        item['SubImage'] = "https://compassal.com/wp-content/uploads/sites/97/artisan-birch-signature-elevation.jpg|https://compassal.com/wp-content/uploads/sites/97/artisan-weston-premier-elevation.jpg|https://compassal.com/wp-content/uploads/sites/97/artisan-birch-premier-elevation.jpg|https://compassal.com/wp-content/uploads/sites/97/artisan-hardin-premier-elevation.jpg"
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link= 'https://compassal.com/our-collections/'
        yield scrapy.Request(url=link, callback=self.parse_links)

    def parse_links(self,response):
        links = response.xpath('//div[@class="cta-box"]/a/@href').extract()
        for link in links:
            link = 'https://compassal.com' + link
            yield scrapy.FormRequest(url=link,callback=self.parse3,dont_filter=True)

    def parse3(self,response):
        links = response.xpath('//div[@class="cta-box"]/a/@href').extract()
        for link in links:
            link = 'https://compassal.com' + link
            yield scrapy.FormRequest(url=link, callback=self.parse2, dont_filter=True)

    def parse2(self,response):

        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//h1/text()').extract_first(
                default='').strip()
            print(PlanName)
        except Exception as e:
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
            print(PlanName)
            f = open("html/%s.html" % PlanNumber, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
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
            BasePrice = '0'
        except Exception as e:
            print(e)

        try:
            Baths = response.xpath("//*[contains(text(),'Baths')]/../span/text()").extract_first(default='0').strip().replace(",", "")
            if '-' in Baths:
                Baths = Baths.split("-")[1].strip()
            Baths = Baths.split(" ")[0]
            Baths = re.findall(r"(\d+)", Baths)
            Bath = Baths[0]
            print(Baths)
            if len(Baths) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            print(e)

        try:
            Bedrooms = response.xpath("//*[contains(text(),'Beds')]/../span/text()").extract_first(default='0').strip().replace(",", "")
            if '-' in Bedrooms:
                Bedrooms = Bedrooms.split("-")[1].strip()
            Bedrooms = Bedrooms.split(" ")[0]
            print(Bedrooms)
        except Exception as e:
            print(e)

        try:
            Garage = response.xpath("//*[contains(text(),'Garage')]/../span/text()").extract_first(default='0').strip().replace(",", "")
            if '-' in Garage:
                Garage = Garage.split("-")[1].strip()
            Garage = Garage.split(" ")[0]
            Garage = re.findall(r"(\d+)", Garage)[0]
            print(Garage)
        except Exception as e:
            print(e)
            Garage = 0.0


        try:
            BaseSqft = response.xpath("//*[contains(text(),'Sq.Ft')]/../span/text()").extract_first(
                default='0').strip().replace(",", "")
            if '-' in BaseSqft:
                BaseSqft = BaseSqft.split("-")[1]
            BaseSqft = BaseSqft.split(" ")[0]
            print(BaseSqft)

        except Exception as e:
            print(e)

        try:
            # Description = response.xpath("//h2/following-sibling::div/p[2]/text()").extract_first('')
            Description = ''
            print(Description)
        except Exception as e:
            Description = ''

        try:
            images = []
            image1 = response.xpath('//div[@class="lazy"]/@style').extract_first('')
            image1 = image1.split("background-image:url(")[1]
            image1 = image1.split(');')[0]

            if image1 != "":
                images.append(image1)

            image2 = response.xpath("//p/img/@src").extract()
            if image2 != []:
                for im in image2:
                    image2 = 'https://compassal.com' + im
                    images.append(image2)

            ElevationImage = "|".join(images)
            print(ElevationImage)
        except Exception as e:
            print(e)
            ElevationImage = ''

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

            # SubdivisionNumber = SubdivisionNumber #if subdivision is there
        SubdivisionNumber = self.builderNumber  # if subdivision is not available
        unique = str(PlanName) + str(SubdivisionNumber)
        print(unique)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

        item = BdxCrawlingItem_Plan()
        item['Type'] = Type
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = PlanName
        item['PlanNotAvailable'] = PlanNotAvailable
        item['PlanTypeName'] = PlanTypeName
        item['BasePrice'] = BasePrice
        item['BaseSqft'] = BaseSqft
        item['Baths'] = Bath
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = Description
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item






if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl compassal".split())