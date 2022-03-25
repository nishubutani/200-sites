import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header


class westrendhomeSpider(scrapy.Spider):
    name = 'westrendhome'
    allowed_domains = ['']
    start_urls = ['https://www.westrendhomes.com/index.htm']
    builderNumber = 21622

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
        item['Street1'] = '	WesTrend Homes, LLC 612 E. 2nd St.'
        item['City'] = 'Newberg'
        item['State'] = 'OR'
        item['ZIP'] = '77303'
        item['AreaCode'] = ''
        item['Prefix'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] = ''
        item[
            'SubDescription'] = 'WesTrend Homes is an Oregon family owned business that for over 30 years has been building "Affordable Homes With Style" in the greater Salem/ Portland area. Come to one of our communities and see our "Affordable Homes With Style".'
        item['SubImage'] = ''
        item['SubWebsite'] = response.url
        yield item
        url = 'https://www.westrendhomes.com/HTML/Communities/West_Meadow_Estates/West_Meadow_Estates.htm'
        yield scrapy.FormRequest(url=str(url), callback=self.plandetail, meta={'sbdn': self.builderNumber})

    def plandetail(self, response):
            PlanNames = ['Alder C', 'Alder', 'Cedar', 'Alder B', 'Cypress', 'Elmwood', 'Spruce A', 'Juniper',
                         'Spruce B', 'Hawthorn C', 'Laurel', 'Hawthorn D', 'Hawthorn', 'Oakleaf A', 'Redwood',
                         'Ponderosa A', 'Oakleaf B', 'Ponderosa B', 'Aspen', 'Tamarack']
            for PlanName in PlanNames:
                if PlanName == 'Alder C':
                    PlanImage = 'https://www.westrendhomes.com/Images/Plan_Images/Alder_C/Alder_C_Elevation_A.jpg'
                    PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % PlanNumber, "wb")
                    f.write(response.body)
                    f.close()
                    SubdivisionNumber = response.meta['sbdn']
                    PlanNotAvailable = 0
                    BasePrice = 0.00
                    BaseSqft = '1516'
                    planbeds = '3'
                    planbath = '2'
                    cargarage = '2'
                    PlanWebsite = response.url
                elif PlanName == 'Alder':
                    PlanImage = 'https://www.westrendhomes.com/Images/Plan_Images/Alder/Alder_Elevation_B.jpg'
                    PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % PlanNumber, "wb")
                    f.write(response.body)
                    f.close()
                    SubdivisionNumber = response.meta['sbdn']
                    PlanNotAvailable = 0
                    BasePrice = 0.00
                    BaseSqft = '1522'
                    planbeds = '3'
                    planbath = '2'
                    cargarage = '2'
                    PlanWebsite = response.url
                elif PlanName == 'Cedar':
                    PlanImage = 'https://www.westrendhomes.com/Images/Plan_Images/Cedar/Cedar_Elevation_B_Rendering.jpg'
                    PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % PlanNumber, "wb")
                    f.write(response.body)
                    f.close()
                    SubdivisionNumber = response.meta['sbdn']
                    PlanNotAvailable = 0
                    BasePrice = 0.00
                    BaseSqft = '1564'
                    planbeds = '3'
                    planbath = '2'
                    cargarage = '2'
                    PlanWebsite = response.url
                elif PlanName == 'Alder B':
                    PlanImage = 'https://www.westrendhomes.com/Images/Plan_Images/Alder_B/Alder_B_Elevation_A.jpg'
                    PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % PlanNumber, "wb")
                    f.write(response.body)
                    f.close()
                    SubdivisionNumber = response.meta['sbdn']
                    PlanNotAvailable = 0
                    BasePrice = 0.00
                    BaseSqft = '1626'
                    planbeds = '3'
                    planbath = '2'
                    cargarage = '2'
                    PlanWebsite = response.url
                elif PlanName == 'Cypress':
                    PlanImage = 'https://www.westrendhomes.com/Images/Plan_Images/Cypress/Cypress_(1643_sf)_Elevation.jpg'
                    PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % PlanNumber, "wb")
                    f.write(response.body)
                    f.close()
                    SubdivisionNumber = response.meta['sbdn']
                    PlanNotAvailable = 0
                    BasePrice = 0.00
                    BaseSqft = '1643'
                    planbeds = '4'
                    planbath = '2'
                    cargarage = '2'
                    PlanWebsite = response.url
                elif PlanName == 'Elmwood':
                    PlanImage = 'https://www.westrendhomes.com/Images/Plan_Images/Elmwood/Elmwood_Elevation_B_Rendering.jpg'
                    PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % PlanNumber, "wb")
                    f.write(response.body)
                    f.close()
                    SubdivisionNumber = response.meta['sbdn']
                    PlanNotAvailable = 0
                    BasePrice = 0.00
                    BaseSqft = '1697'
                    planbeds = '3'
                    planbath = '2'
                    cargarage = '2'
                    PlanWebsite = response.url
                elif PlanName == 'Spruce A':
                    PlanImage = 'https://www.westrendhomes.com/Images/Plan_Images/Spruce_A/Spruce_A_(1729%20sf)_Elevation_B.jpg'
                    PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % PlanNumber, "wb")
                    f.write(response.body)
                    f.close()
                    SubdivisionNumber = response.meta['sbdn']
                    PlanNotAvailable = 0
                    BasePrice = 0.00
                    BaseSqft = '1729'
                    planbeds = '4'
                    planbath = '2'
                    cargarage = '2'
                    PlanWebsite = response.url
                elif PlanName == 'Juniper':
                    PlanImage = 'https://www.westrendhomes.com/Images/Plan_Images/Juniper/Juniper_(1733_SF)_Elevation_Picture_(Similiar_To).jpg'
                    PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % PlanNumber, "wb")
                    f.write(response.body)
                    f.close()
                    SubdivisionNumber = response.meta['sbdn']
                    PlanNotAvailable = 0
                    BasePrice = 0.00
                    BaseSqft = '1733'
                    planbeds = '4'
                    planbath = '2'
                    cargarage = '2'
                    PlanWebsite = response.url
                elif PlanName == 'Spruce B':
                    PlanImage = 'https://www.westrendhomes.com/Images/Plan_Images/Spruce_B/Spruce_B_Elevation_B.jpg'
                    PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % PlanNumber, "wb")
                    f.write(response.body)
                    f.close()
                    SubdivisionNumber = response.meta['sbdn']
                    PlanNotAvailable = 0
                    BasePrice = 0.00
                    BaseSqft = '2014'
                    planbeds = '4'
                    planbath = '2'
                    cargarage = '2'
                    PlanWebsite = response.url
                try:
                    unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
                    unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
                            10 ** 30)  # < -------- Changes here
                    item = BdxCrawlingItem_Plan()
                    item['PlanNumber'] = PlanNumber
                    item['unique_number'] = unique_number  # < -------- Changes here
                    item['SubdivisionNumber'] = SubdivisionNumber
                    item['PlanName'] = PlanName
                    item['PlanNotAvailable'] = PlanNotAvailable
                    item['PlanTypeName'] = 'SingleFamily'
                    item['BasePrice'] = BasePrice
                    item['BaseSqft'] = BaseSqft
                    item['Baths'] = planbath
                    item['HalfBaths'] = 0
                    item['Bedrooms'] = planbeds
                    item['Garage'] = cargarage
                    item['Description'] = ''
                    item['ElevationImage'] = PlanImage
                    item['PlanWebsite'] = PlanWebsite
                    yield item
                except Exception as e:
                    print(e)

# execute("scrapy crawl westrendhome".split())