
# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class vtshomeshomesSpider(scrapy.Spider):
    name = 'apmhomessantarosa'
    allowed_domains = []
    start_urls = ['https://apmhomessantarosa.com/']

    builderNumber = "51152"

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
        item['Street1'] = 'PO Box 6858'
        item['City'] = 'Santa Rosa'
        item['State'] = 'CA'
        item['ZIP'] = '95406'
        item['AreaCode'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Prefix'] = ""
        item['Email'] = ''
        item['SubDescription'] = "Our company builds homes in Sonoma County. We have a long family history for building neighborhoods throughout Santa Rosa and are locally owned and operated. In the last 6 years we have built in excess of 160 homes in incorporated Santa Rosa."
        item['SubImage'] = 'https://apmhomessantarosa.com/wp-content/uploads/2018/02/182_Va_02.jpg|https://apmhomessantarosa.com/wp-content/uploads/2018/02/177-181_Vc_02.jpg|https://apmhomessantarosa.com/wp-content/uploads/2014/07/BWE1028-2-copy-1030x823.jpg|https://apmhomessantarosa.com/wp-content/uploads/2017/11/glennview2-1030x735.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link= 'https://apmhomessantarosa.com/rebuild-home-options/'
        yield scrapy.Request(url=link, callback=self.plan_links_inner)

    def plan_links_inner(self,response):

        divs =  response.xpath("//div[contains(@class,'flex_column av_one_half ')]")
        for div in divs:
            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)


            try:
                PlanName = div.xpath('.//h2/text()').extract_first(
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
                Baths = div.xpath(".//*[contains(text(),'BATH')]/text()").extract_first(default='0').strip().replace(",", "")
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
                Bedrooms = div.xpath(".//*[contains(text(),'BR')]/text()").extract_first(default='0').strip().replace(",", "")
                Bedrooms = Bedrooms.split(" ")[0]
                print(Bedrooms)
            except Exception as e:
                print(e)

            try:
                Garage = div.xpath(".//*[contains(text(),'Garage')]/text()").extract_first(default='0').strip().replace(",", "")
                Garage = Garage.split(" ")[0]
                Garage = re.findall(r"(\d+)", Garage)[0]
                print(Garage)
            except Exception as e:
                print(e)
                Garage = 0.0


            try:
                BaseSqft = div.xpath(".//*[contains(text(),'SQ.')]/text()").extract_first(
                    default='0').strip().replace(",", "")
                BaseSqft = BaseSqft.split(" ")[0]
                print(BaseSqft)

            except Exception as e:
                print(e)

            try:
                Description = ""

                print(Description)
            except Exception as e:
                Description = ''

            try:
                images = []
                image1 = div.xpath('.//div/a/@href').extract_first('')
                image2 = div.xpath('.//div/a/span/img/@src').extract_first('')
                if image1 != "":
                    images.append(image1)
                if image2 != '':
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
    execute("scrapy crawl apmhomessantarosa".split())