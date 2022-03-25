import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class HickhomesvaSpider(scrapy.Spider):
    name = 'hickhomesva'
    allowed_domains = []
    start_urls = ['http://hickshomesva.com/']
    builderNumber = 32568
    def parse(self, response):
        SubImage = []
        SubImages = re.findall(r'<div class="et_pb_slide_image"><img src="(.*?)" alt="" /></div>',response.text)
        for SubImag in SubImages:
            SubImage.append(SubImag)
        SubImage = '|'.join(SubImage)

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
        item['Street1'] = '1511 Salisbury Dr'
        item['City'] = 'Midlothian'
        item['State'] = 'VA'
        item['ZIP'] = '23113'
        item['AreaCode'] = '804'
        item['Prefix'] = '382'
        item['Suffix'] = '2391'
        item['Extension'] = ""
        item['Email'] = 'charles@hickshomesva.com'
        item[
            'SubDescription'] = 'We customize homes based on our customer’s vision, needs, and budget. Whether we build on your land or ours, we can fashion a project from blueprint to completion. We also have an expansive portfolio of “ready to build” homes that are sure to fit your unique specifications and budget. Our homes range in square footage as well as style.'
        item[
            'SubImage'] = SubImage
        item['SubWebsite'] = response.url
        yield item

# execute("scrapy crawl hickhomesva".split())
