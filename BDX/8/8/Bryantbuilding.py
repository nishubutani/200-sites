import hashlib
import re

import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class BryantSpider(scrapy.Spider):
    name = 'BryantBulding'
    allowed_domains = []
    start_urls = ['http://www.bryantbuildingcompany.com/']

    builderNumber = "23122"

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
        item['Street1'] = 'P.O. Box 700876'
        item['City'] = 'St. Cloud'
        item['State'] = 'FL'
        item['ZIP'] = '34770'
        item['AreaCode'] = '407'
        item['Prefix'] = '892'
        item['Suffix'] = '0005'
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = "At Bryant Building Company we offer time-tested homes of tradition with quality construction. Bryant Building Company has been building homes for over three decades throughout Osceola and South Orange Counties. All our custom built homes are built with 'Pride and Quality Workmanship' at an affordable price. We have a variety of plans to choose from providing a wide array of Standard Features that are considered Custom add-ons by most builders."
        item['SubImage'] = 'http://www.bryantbuildingcompany.com/images/header_2.jpg|http://www.bryantbuildingcompany.com/images/TrysibakExterior.jpg'
        item['SubWebsite'] = response.url
        yield item

        plan_link = ['http://www.bryantbuildingcompany.com/barrington_floorplan.htm','http://www.bryantbuildingcompany.com/biancavilla_floorplan.htm','http://www.bryantbuildingcompany.com/brentmoore_II_floorplan.htm','http://www.bryantbuildingcompany.com/berringer_floorplan.htm','http://www.bryantbuildingcompany.com/barrington_II_floorplan.htm','http://www.bryantbuildingcompany.com/barrington_II_b_floorplan.htm','http://www.bryantbuildingcompany.com/briante_floorplan.htm','http://www.bryantbuildingcompany.com/biancavilla_II_floorplan.htm','http://www.bryantbuildingcompany.com/welston_floorplan.htm',
                     'http://www.bryantbuildingcompany.com/homestead_floorplan.htm','http://www.bryantbuildingcompany.com/traditional_1_floorplan.htm','http://www.bryantbuildingcompany.com/brighton_floorplan.htm','http://www.bryantbuildingcompany.com/brookhaven_floorplan.htm','http://www.bryantbuildingcompany.com/bungalow_floorplan.htm','http://www.bryantbuildingcompany.com/franklin_floorplan.htm','http://www.bryantbuildingcompany.com/traditional_II_floorplan.htm','http://www.bryantbuildingcompany.com/danbury_floorplan.htm']
        for i in plan_link:
            plan_link=i
            yield scrapy.Request(url=plan_link, callback=self.plan_link_page,dont_filter=True)
    def plan_link_page(self,response):

        name = response.xpath('//font[@color="#B4422E"]/text()').extract_first().strip()

        PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)

        info = ''.join(response.xpath('//ul[@type="square"]//font/text()').extract()).strip().replace('\t','').split('\n')

        BSft = info[0]
        BaseSqft = ''.join(re.findall(r"(\d+)", BSft, re.DOTALL))
        print(BaseSqft)

        data = info[1]
        if '-' in data:
            data=data.split('-')
        else:
            data=data.split('/')
        print(data)

        Bed=data[0]
        if '/' in Bed:
            Bed=Bed.split('/')
            Bed=Bed[-1]

        Bed=re.findall(r"(\d+)", Bed)[0]
        if '/' in Bed:
            print(Bed)

        Baths = data[1].replace('\r','').replace('Bath','').strip()
        if '.' in Baths:
            Bath = Baths.split('.')
            Bath = Bath[0]
            Halfbath = 1

        else:
            Bath = Baths
            Halfbath = 0


        Desc = "At Bryant Building Company we offer time-tested homes of tradition with quality construction. Bryant Building Company has been building homes for over three decades throughout Osceola and South Orange Counties. All our custom built homes are built with 'Pride and Quality Workmanship' at an affordable price. We have a variety of plans to choose from providing a wide array of Standard Features that are considered Custom add-ons by most builders."

        try:
            img = response.xpath('//p[@align="center"]//img/@src').extract()
            img='http://www.bryantbuildingcompany.com/'+ img[1]

        except:
            img = ''

        SubdivisionNumber = self.builderNumber  # if subdivision is not available
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = name
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0
        item['BaseSqft'] = BaseSqft
        item['Baths'] = Bath
        item['HalfBaths'] = Halfbath
        item['Bedrooms'] = Bed
        item['Garage'] = 0
        item['Description'] = Desc
        item['ElevationImage'] = img
        item['PlanWebsite'] = response.url
        yield item


# from scrapy.cmdline import execute
# execute("scrapy crawl BryantBulding".split())