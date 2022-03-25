

# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class vtshomeshomesSpider(scrapy.Spider):
    name = 'biltmoreco'
    allowed_domains = []
    start_urls = ['https://biltmoreco.com/gallery/?id=60']


    builderNumber = "49106"

    def parse(self, response):
        print('--------------------')

        com_images = []
        images = response.xpath('//li/@data-thumb').extract()
        for image in images:
            image = 'https://biltmoreco.com' + image
            com_images.append(image)

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
        item['Street1'] = '1580 W Cayuse Creek Dr'
        item['City'] = 'Meridian'
        item['State'] = 'ID'
        item['ZIP'] = '83646'
        item['AreaCode'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Prefix'] = ""
        item['Email'] = ''
        item['SubDescription'] = "Biltmore begins with PEOPLE. Certainly, we value each homeowner that lives in a Biltmore home, but we are also referring to the valuable people that engineer our subdivisions, pave the streets for our kids to play on, pour sturdy foundations, supply the lumber, pound the nails, install our doors and market our communities. It’s hundreds of important people who make Biltmore Co. who we are. We believe in them and their strengths and we know they believe in us."
        item['SubImage'] = "".join(com_images)
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link= 'https://biltmoreco.com/floor-plans/'
        yield scrapy.Request(url=link, callback=self.plan_links_inner)

    def plan_links_inner(self,response):

        links =  response.xpath('//div[@class="SearchListingWrapper"]/a/@href').extract()
        for link in links:
            link = 'https://biltmoreco.com' + link
            yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)
        #
        # yield scrapy.FormRequest(url='https://biltmoreco.com/floor-plan-details/?id=95',callback=self.parse2,dont_filter=True)

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
            Baths = response.xpath("//*[contains(text(),'Baths')]/../text()").extract_first(default='0').strip().replace(",", "")
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
            Bedrooms = response.xpath("//*[contains(text(),'Beds')]/../text()").extract_first(default='0').strip().replace(",", "")
            Bedrooms = Bedrooms.split(" ")[0]
            print(Bedrooms)
        except Exception as e:
            print(e)

        try:
            Garage = response.xpath("//*[contains(text(),'Garage')]/../text()").extract_first(default='0').strip().replace(",", "")
            Garage = Garage.split(" ")[0]
            Garage = re.findall(r"(\d+)", Garage)[0]
            print(Garage)
        except Exception as e:
            print(e)
            Garage = 0.0


        try:
            BaseSqft = response.xpath("//*[contains(text(),'SqF')]/../text()").extract_first(
                default='0').strip().replace(",", "")
            BaseSqft = BaseSqft.split(" ")[0]
            print(BaseSqft)

        except Exception as e:
            print(e)

        try:
            Description = "".join(response.xpath("//h2/following-sibling::div/p//text()").extract()[-1:]).replace("\n","").strip()

            print(Description)
        except Exception as e:
            Description = ''

        try:
            images = []
            image1 = response.xpath('//li/@data-thumb').extract_first('')
            image2 = response.xpath("//img[contains(@src,'https://biltmoreco.visualwebb4.com/files')]/@src").extract()
            image3 = response.xpath('//div[@class="jig-overflow"]/a/@href').extract()
            if image1 != "":
                if 'https://biltmoreco.com' not in image1:
                    image1 = 'https://biltmoreco.com' + image1
                images.append(image1)
            if image2 != []:
                for im in image2:
                    im = 'https://biltmoreco.com' + im
                    images.append(im)
            if image3 != []:
                for im2 in image3:
                    im2 = 'https://biltmoreco.com' + im2
                    images.append(im2)
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
    execute("scrapy crawl biltmoreco".split())