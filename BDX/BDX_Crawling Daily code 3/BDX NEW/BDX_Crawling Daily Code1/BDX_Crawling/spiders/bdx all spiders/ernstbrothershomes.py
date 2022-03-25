
# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'ernstbrothershomes'
    allowed_domains = ['https://ernstbrothershomes.com/']
    start_urls = ['https://ernstbrothershomes.com/']

    builderNumber = "32124"

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
        item['Street1'] = '1104 N Bethlehem Pike'
        item['City'] = 'Gwynedd '
        item['State'] = 'PA'
        item['ZIP'] = '19002'
        item['AreaCode'] = ''
        item['Prefix'] =''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = 'Ernst Brothers Construction was started in October of 1987, when owners Matt and Mark Ernst started their concrete flatwork company. Five years later they started Ernst Brother’s Properties building rental property for investments purposes. With the success of these projects, they started the home construction company known today as Ernst Brother’s Home Construction. The company has built over 200 homes, villas, and duplexes in the Platte and Clay Counties over the past 20 years'
        item['SubImage'] = 'https://ernstbrothershomes.com/wp-content/uploads/2019/04/12404837343047491270746268668012131213128474122213131313131511777568121612181312151413221321151171776828818026191619202015131913211313131313131313.jpg|https://ernstbrothershomes.com/wp-content/uploads/2020/01/Screen-Shot-2020-01-27-at-7.16.38-PM.png|https://ernstbrothershomes.com/wp-content/uploads/2020/01/Screen-Shot-2020-01-27-at-7.18.15-PM.png'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'https://ernstbrothershomes.com/floor-plans'
        yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)

    def parse2(self, response):
        divs = response.xpath('//div[@class="grid-row"]/article')
        for div in divs:

            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                PlanName = div.xpath('.//h1/a/text()').get()
            except Exception as e:
                PlanName = ''
                print(e)

            try:
                PlanNumber = int(hashlib.md5(bytes(PlanName + response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
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
                BasePrice = 0
            except Exception as e:
                print(e)


            BaseSqft = ''

            try:
                desc = div.xpath(".//div[@class='entry-summary']/p/text()").extract_first('')
                print(desc)
            except Exception as e:
                print(e)
                desc = ""

            try:
                bath = div.xpath("//div[@class='entry-summary']/p/text()").extract_first()
                bath = bath.split("edrooms, ")[1]
                bath = bath.replace("three ","3").replace("four ","4").replace("two","2").replace("three","3")

                tmp = re.findall(r"(\d+)", bath)[0]
                Baths = tmp[0]

                if 'half baths' in desc:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                print(e)

            try:
                Bedrooms = div.xpath(".//div[@class='entry-summary']/p/text()").extract_first()
                Bedrooms = Bedrooms.split("bedrooms")[0]
                Bedrooms = Bedrooms.replace("three ", "3").replace("four ", "4")
                Bedrooms = re.findall(r"(\d+)", Bedrooms)[-1]
                print(Bedrooms)
            except Exception as e:
                print(e)

            try:
                Garage = div.xpath(".//div[@class='entry-summary']/p/text()").extract_first()
                Garage = Garage.split(" car garage")[0].replace("four ","4").replace("two","2").replace("three","3")
                Garage = re.findall(r"(\d+)", Garage)[-1]
            except Exception as e:
                print(e)
                Garage = 0

            try:
                Description = desc
            except Exception as e:
                print(e)
                Description = ''


            price = 0

            try:

                images1 = div.xpath('.//div[@class="entry-thumbnail"]/a/img/@src').extract_first('')
            except Exception as e:
                print(e)

            try:
                PlanWebsite = response.url
            except Exception as e:
                print(e)

                # ----------------------- Don't change anything here --------------
            unique = str(PlanNumber) + str(SubdivisionNumber) + str(Baths) + str(Bedrooms)  # < -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
            item = BdxCrawlingItem_Plan()
            item['Type'] = Type
            item['PlanNumber'] = PlanNumber
            item['unique_number'] = unique_number  # < -------- Changes here
            item['SubdivisionNumber'] = SubdivisionNumber
            item['PlanName'] = PlanName
            item['PlanNotAvailable'] = PlanNotAvailable
            item['PlanTypeName'] = PlanTypeName
            item['BasePrice'] = price
            item['BaseSqft'] = BaseSqft
            item['Baths'] = Baths
            item['HalfBaths'] = HalfBaths
            item['Bedrooms'] = Bedrooms
            item['Garage'] = Garage
            item['Description'] = Description
            item['ElevationImage'] = images1
            item['PlanWebsite'] = PlanWebsite
            yield item

            # --------------------------------------------------------------------- #




if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl ernstbrothershomes'.split())

