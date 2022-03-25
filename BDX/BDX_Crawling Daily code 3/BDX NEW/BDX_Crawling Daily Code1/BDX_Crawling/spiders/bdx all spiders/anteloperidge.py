import json
import scrapy
import hashlib
import re
from scrapy.http import HtmlResponse
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
import requests


class homesspider(scrapy.Spider):

    name = "antelophomes"

    start_urls = ['https://www.antelope-ridge.com/']

    builderNumber = "62732"

    def parse(self, response, **kwargs):

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = self.builderNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "Antelope Ridge"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = "321 Hunt Drive"
        item['City'] = "Box Elder"
        item['State'] = "SD"
        item['ZIP'] = "57719"
        item['AreaCode'] = "833"
        item['Prefix'] = "498"
        item['Suffix'] = "6445"
        item['Extension'] = ""
        item['Email'] = 'anteloperidgeleasing@huntcompanies.com'
        item['SubDescription'] = "".join(response.xpath('//*[@class="normaltext"]/p/text()').getall())
        item['SubImage'] = "|".join(response.xpath('//*[@class="carousel-inner"]//img/@src|//*[@class="carousel-inner"]//img/@data-src').getall())
        item['SubWebsite'] = response.url

        amenity_list = ["Pool", "Playground", "GolfCourse", "Tennis", "Soccer", "Volleyball", "Basketball", "Baseball",
                        "Views", "Lake", "Pond", "Marina", "Beach", "WaterfrontLots", "Park", "Trails", "Greenbelt",
                        "Clubhouse", "CommunityCenter"]

        res = requests.get("https://www.antelope-ridge.com/" + response.xpath('//*[@id="amenitiesaspx_SubmenuLink"]/@href').get())

        res = HtmlResponse(url=res.url, body=res.text, encoding="utf-8")

        comm_amenity_list = res.xpath('//*[contains(text(),"Community Amenities ")]/../..//*[@class="amenity_title"]/span/text()').getall()

        unique_list = list()

        for items in amenity_list:
            for items2 in comm_amenity_list:
                if items.lower().strip().replace(' ', '') in items2.lower().strip().replace(' ', ''):
                    unique_list.append(items)

        unique_list = list(set(unique_list))

        item['AmenityType'] = "|".join(unique_list)
        yield item

        floor_page_link = "https://www.antelope-ridge.com/" + response.xpath("//*[contains(text(),'Floor Plans')]/@href").get()

        yield scrapy.FormRequest(url=floor_page_link, method="GET", callback=self.parse2)

    def parse2(self, response):

        # a = response.text.split('var pageData = ')[-1].split(';</script>')[0].replace("\r", '').replace('\n', '')
        # print(a)
        #
        # json_obj = json.loads(response.text.split('var pageData = ')[-1].split(';</script>')[0].replace("\r", '').replace('\n', ''))
        #
        # # blocks = response.xpath('//a[contains(text(),"View Details")]//ancestor::div[@class="fp-card"]')
        #
        # for block in json_obj['floorplans']:
        #     if block['availabeCount']:
        try:
            plan_name = "Dakota Acres 2 Bed"
        except Exception as e:
            print("Plan Name is Not There or Error")

        try:
            type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            plan_number = int(hashlib.md5(bytes(plan_name, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            plan_number = ""

        try:
            plannotavailable = 0
        except Exception as e:
            print(e)

        try:
            plantypename = 'Single Family'
        except Exception as e:
            print(e)

        try:
            baseprice = '0'
        except Exception as e:
            print(e)
            baseprice = '0'

        try:
            baths = str("1.5")
            fullbaths = baths[0]
            if len(fullbaths.replace(' ', '')) > 1:
                halfbaths = 1
            else:
                halfbaths = 0
        except Exception as e:
            fullbaths = 0
            halfbaths = 0
            print(e)

        try:
            bedrooms = str(2)
        except Exception as e:
            bedrooms = "0"
            print(e)

        try:
            garage = 0
            basesqft = int("1066")
        except Exception as e:
            basesqft = "0"
            garage = 0
            print(e)

        try:
            description = ""
        except Exception as e:
            print(e)

        try:
            elevationimage = "https://cdngeneral.rentcafe.com/dmslivecafe/3/231605/AntelopeRidge_DakotaAcres_2Bed_15Bath_1066sqft.png?quality=85?maxheight=245&scale=both&quality=50"
        except Exception as e:
            print(e)

        try:
            planwebsite = response.url
        except Exception as e:
            print(e)

        unique = str(plan_number)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['Type'] = type
        item['PlanNumber'] = plan_number
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = self.builderNumber
        item['PlanName'] = plan_name
        item['PlanNotAvailable'] = plannotavailable
        item['PlanTypeName'] = plantypename
        item['BasePrice'] = baseprice
        item['BaseSqft'] = basesqft
        item['Baths'] = fullbaths
        item['HalfBaths'] = halfbaths
        item['Bedrooms'] = bedrooms
        item['Garage'] = garage
        item['Description'] = description
        item['ElevationImage'] = elevationimage
        item['PlanWebsite'] = planwebsite
        yield item

        # urls_for_plans = re.findall(r'urlname: "(.*?)",', response.text)
        #
        # for url in urls_for_plans:
        #     plan_link = "https://www.antelope-ridge.com/floorplans/" + url.replace(' ', '-').lower()
        #     try:
        #         plan_name = response.xpath('//*[@id="floorplanPage"]//h1/text()').get()
        #     except Exception as e:
        #         print('Error in Plan name', e)
        #         plan_name = ""

            # yield scrapy.FormRequest(url=plan_link, method="GET", callback=self.parse3)

    # def parse3(self, response):
    #     try:
    #         plan_name = response.xpath('//*[@id="floorplanPage"]//h1/text()').get()
    #     except Exception as e:
    #         print('Error in Plan name', e)
    #         plan_name = ""
    #
    #     try:
    #         type = 'SingleFamily'
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         plan_number = int(hashlib.md5(bytes(plan_name, "utf8")).hexdigest(), 16) % (10 ** 30)
    #     except Exception as e:
    #         plan_number = ""
    #
    #     try:
    #         plannotavailable = 0
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         plantypename = 'Single Family'
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         baseprice = '0'
    #     except Exception as e:
    #         print(e)
    #         baseprice = '0'
    #
    #     try:
    #         baths = re.findall(r'[ ]*(\d+[ ]*[½]*)[ ]*[bB][aA][tT][hH]', "".join(response.xpath('//*[contains(@class,"single-fp-details")]//*[@class="single-fp-flexcontainer fp-phone-only"]//text()').getall()).strip())
    #         fullbaths = baths[0]
    #         if len(fullbaths.replace(' ', '')) > 1:
    #             halfbaths = 1
    #         else:
    #             halfbaths = 0
    #     except Exception as e:
    #         fullbaths = 0
    #         halfbaths = 0
    #         print(e)
    #
    #     try:
    #         bedrooms = re.findall(r'[ ]*(\d+)[ ]*[bB][Ee][Dd][Rr][Oo][Oo][Mm]', "".join(response.xpath('//*[contains(@class,"single-fp-details")]//*[@class="single-fp-flexcontainer fp-phone-only"]//text()').getall()).strip())[0]
    #     except Exception as e:
    #         bedrooms = "0"
    #         print(e)
    #
    #     try:
    #         garage = 0
    #         basesqft = int(re.findall(r'(\d+[,]*\d+)[ ]*[sS][qQ][.]*[ ]*[fF][Tt][.]*', "".join(response.xpath('//*[contains(@class,"single-fp-details")]//*[@class="single-fp-flexcontainer fp-phone-only"]//text()').getall()).strip())[0])
    #     except Exception as e:
    #         basesqft = "0"
    #         garage = 0
    #         print(e)
    #
    #     try:
    #         description = " ".join(response.xpath('//*[@class="fp-features-amenities"]//text()').getall()).strip().replace('\r', '').replace('\n', '').replace('  ', '')
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         elevationimage = response.xpath('//*[@id="floorplanPage"]//img/@src').extract()
    #
    #         unique_image = list()
    #
    #         for images in elevationimage:
    #             unique_image.append("https://cdngeneral.rentcafe.com/" + images)
    #
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         planwebsite = response.url
    #     except Exception as e:
    #         print(e)
    #
    #     unique = str(plan_number)
    #     unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
    #     item = BdxCrawlingItem_Plan()
    #     item['Type'] = type
    #     item['PlanNumber'] = plan_number
    #     item['unique_number'] = unique_number
    #     item['SubdivisionNumber'] = self.builderNumber
    #     item['PlanName'] = plan_name
    #     item['PlanNotAvailable'] = plannotavailable
    #     item['PlanTypeName'] = plantypename
    #     item['BasePrice'] = baseprice
    #     item['BaseSqft'] = basesqft
    #     item['Baths'] = fullbaths
    #     item['HalfBaths'] = halfbaths
    #     item['Bedrooms'] = bedrooms
    #     item['Garage'] = garage
    #     item['Description'] = description
    #     item['ElevationImage'] = "|".join(unique_image)
    #     item['PlanWebsite'] = planwebsite
    #     yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl antelophomes".split())
