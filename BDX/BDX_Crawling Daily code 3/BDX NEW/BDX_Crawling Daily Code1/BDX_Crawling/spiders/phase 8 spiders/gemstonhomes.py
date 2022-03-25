import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header


class GemstonHomesSpider(scrapy.Spider):
    name = 'gemstonhomes'
    allowed_domains = []
    start_urls = ['https://www.gemstoneproperties.com/']
    builderNumber = 26156
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
        item['Street1'] = '2608 W 510 N Hurricane'
        item['City'] = 'Hurricane'
        item['State'] = 'UT'
        item['ZIP'] = '84737'
        item['AreaCode'] = '435'
        item['Prefix'] = '862'
        item['Suffix'] = '6202'
        item['Extension'] = ""
        item['Email'] = ' stacie@gemstoneproperties.com'
        item[
            'SubDescription'] = "Come in and choose your own home selections today! You are involved throughout the whole home building process. Including you in the construction process helps us better serve your needs and wants, giving you the home you've always dreamed and making your next house a place you love to call home. Surrounded by mountain views of Pine Valley, Snow Canyon, and Zion National Park that you don't want to miss. Call us today to schedule an appointment or stop by our office."
        item[
            'SubImage'] = 'https://www.gemstoneproperties.com/images/banner.jpg'
        item['SubWebsite'] = response.url
        yield item

# execute("scrapy crawl gemstonhomes".split())