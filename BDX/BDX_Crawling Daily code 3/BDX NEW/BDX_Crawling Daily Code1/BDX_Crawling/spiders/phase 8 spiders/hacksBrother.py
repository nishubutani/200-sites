import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header


class HacksBrotherSpider(scrapy.Spider):
    name = 'hacksBrother'
    allowed_domains = []
    start_urls = ['http://www.erbesconstruction.com/']
    builderNumber = 54531

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
        item['Street1'] = '425 South Telshor, Bldg C.'
        item['City'] = 'Las Cruces'
        item['State'] = 'NM'
        item['ZIP'] = '88011'
        item['AreaCode'] = '575'
        item['Prefix'] = '373'
        item['Suffix'] = '8300'
        item['Extension'] = ""
        item['Email'] = 'info@hakesbrothers.com'
        item[
            'SubDescription'] = "The Hakes Brothers began working in residential construction at an early age, developing a love for construction work, new home design, and the hard-working people in the construction industry. In 2006, realizing they had developed complementary skills, they came together with a vision to raise the bar for new home construction in Las Cruces, NM, and Hakes Brothers officially began.The brothers initially built luxury custom homes. After a few years, they turned their attention to semi-custom homes, offering the same luxurious look and feel of their custom homes, but at affordable prices. It was a success! Over the years, they've found that homeowners love their professional designs and custom amenities, and always at competitive prices. Hakes Brothers has an unwavering commitment to customer service. We know that our reputation is a major part of your decision to trust us as your builder. We will strive to earn your highest recommendation."
        item[
            'SubImage'] = 'https://www.hakesbrothers.com/storage/app/medialibrary/public/2020/07/1759/responsive-images/5f2351c9ef34a367789340___hero_3000_2000.jpg|https://www.hakesbrothers.com/storage/app/medialibrary/public/2020/07/1758/responsive-images/5f2351c9bb9a1098865525___hero_2000_1333.jpg|https://www.hakesbrothers.com/storage/app/medialibrary/public/2020/07/1764/responsive-images/5f2351cee5827360220682___hero_3000_2000.jpg|https://www.hakesbrothers.com/storage/app/medialibrary/public/2020/07/1765/responsive-images/5f2351cf3c7f2706712800___hero_3000_2000.jpg'

        item['SubWebsite'] = response.url
        yield item
# execute("scrapy crawl hacksBrother".split())