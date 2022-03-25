import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header


class ErbesConstructionSpider(scrapy.Spider):
    name = 'erbesconstruction'
    allowed_domains = []
    start_urls = ['http://www.erbesconstruction.com/']
    builderNumber = 32062

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
        item['Street1'] = '3010 Cleveland Ave'
        item['City'] = 'Plover'
        item['State'] = 'WI'
        item['ZIP'] = '54467'
        item['AreaCode'] = '715'
        item['Prefix'] = '344'
        item['Suffix'] = '7499'
        item['Extension'] = ""
        item['Email'] = 'Erbes@erbesconstruction.com'
        item[
            'SubDescription'] = 'We have an office showroom for your convenience and staff available to help you through each step of the building process from designing, drafting, 3-D presentation, product selecting & interior décor for both new construction and renovations. We also offer full Real Estate Services.Our goal is to make your home building experience an enjoyable and rewarding one that not only makes you a very satisfied and happy customer, but a friend to our business as well.Building a home is undoubtedly one of the more important personal and financial commitments you’ll make in your life. Yet, it’s a decision you’ll make with relatively little experience to guide you.Quality home construction today requires ongoing evaluation and incorporation of ever-changing building materials and techniques.'
        item[
            'SubImage'] = 'https://www.stevenspointbusinessdirectory.com/images/stevenspointbusinessdirectorycom/bizcategories/3496/custompages/25677/04D51863-image_1.jpg|https://www.stevenspointbusinessdirectory.com/images/stevenspointbusinessdirectorycom/bizcategories/3496/custompages/25678/04D6ADD3-image_2.jpg|https://www.stevenspointbusinessdirectory.com/images/stevenspointbusinessdirectorycom/bizcategories/3496/custompages/25679/04D84D51-image_3.jpg|https://www.stevenspointbusinessdirectory.com/images/stevenspointbusinessdirectorycom/bizcategories/3496/custompages/25680/04DA5384-image_4.jpg|https://www.stevenspointbusinessdirectory.com/images/stevenspointbusinessdirectorycom/bizcategories/3496/custompages/25694/04DE2FDE-image_5.jpg|https://www.stevenspointbusinessdirectory.com/images/stevenspointbusinessdirectorycom/bizcategories/3496/custompages/25695/04E07C7B-image_6.jpg'
        item['SubWebsite'] = response.url
        yield item
# execute("scrapy crawl erbesconstruction".split())