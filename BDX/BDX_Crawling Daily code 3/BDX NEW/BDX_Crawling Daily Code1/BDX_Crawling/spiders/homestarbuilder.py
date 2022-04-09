import hashlib
import re

import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan


class HomestarbuilderSpider(scrapy.Spider):
    name = 'homestarbuilder'
    allowed_domains = ['homestarbuilder.com/']
    start_urls = ['https://homestarbuilder.com/']
    builderNumber = '53141'

    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = self.builderNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '9770 Carroll Centre Rd'
        item['City'] = 'San Diego'
        item['State'] = 'CA'
        item['ZIP'] = '92126'
        item['AreaCode'] = '305'
        item['Prefix'] = '607'
        item['Suffix'] = '4454'
        item['Extension'] = ""
        item['Email'] = 'op@ophomes.net'
        item['SubDescription'] = 'We work directly with our manufacturers to provide the best quality and the best price in the market. Even the best of the best products can fail without proper installation so we have our own experienced, trained technicians to install all our products'
        item['SubImage'] = 'https://homestarbuilder.com/wp-content/uploads/2015/10/Captiva_Model.png'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        planlinks = response.xpath('//*[@id="menu-item-36"]/ul//a/@href').getall()
        for link in planlinks:
            yield scrapy.Request(url=link, callback=self.parse_planlink, dont_filter=True)

    def parse_planlink(self,response):


        planname = re.findall(r'<h1 class="intro_title"><span>(.*?)</span>',response.text)[0]
        try:
            bedroom = re.findall(r'(\d+) Bedroom',response.text)[-1]
        except:
            try:
                bedroom = re.findall(r'(\d+)  Bedroom', response.text)[-1]
            except:
                bedroom = 0

        try:
            bathroom = re.findall(r'(\d.\d) Bath',response.text)[0]
        except:
            bathroom = re.findall(r'(\d) Bath', response.text)[-1]
        if len(bathroom)>1:
            bathroom = bathroom[0]
            halfbath = 1
        else:
            halfbath = 0



        garage = re.findall(r'(\d+) Car',response.text)[-1]

        try:
            sqft = re.findall(r'(\d{4}) SQ.FT.',(response.text.replace(',','')))[-1]
        except:
            sqft = 0

        image = response.xpath('//*[@id="content_inner"]//img/@src').getall()

        PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
        f = open("html/%s.html" % PlanNumber, "wb")
        f.write(response.body)
        f.close()

        SubdivisionNumber = self.builderNumber #if subdivision is not available
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = planname
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0
        item['BaseSqft'] = sqft
        item['Baths'] = bathroom
        item['HalfBaths'] = halfbath
        item['Bedrooms'] = bedroom
        item['Garage'] = garage
        item['Description'] = 'Ask your sales consultant for prices and details'
        item['ElevationImage'] = "|".join(image)
        item['PlanWebsite'] = response.url
        yield item



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl homestarbuilder".split())