import hashlib
import re

import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class HinkleHomesSpider(scrapy.Spider):
    name = 'hinkle_Homes'
    allowed_domains = ['www.hinklehomesinc.com']
    start_urls = ['http://www.hinklehomesinc.com/']

    builderNumber = 32740

    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        Images = 'https://www.hinklehomesinc.com/wp-content/uploads/2017/01/home_back.jpg' + '|' +'|'.join(response.xpath('//div[@class="homebox"]/p/a/img/@src').getall())
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '7448 Creekside Ln SW'
        item['City'] = 'Rochester'
        item['State'] = 'WA'
        item['ZIP'] = '98579'
        item['AreaCode'] = '360'
        item['Prefix'] = '239'
        item['Suffix'] = '3555'
        item['Extension'] = ""
        item['Email'] = ' info@hinklehomesinc.com'
        item['SubDescription'] = '''Hinkle Homes Inc. has been a leading Northwest Home Builder for many years. Our founder, John Hinkle, believes that a home should reflect the personality of the home owner. That is why he got into the business. When he was looking for a builder for his own home, he couldn’t find one that provided the options that he wanted, the quality that he was looking for and the price range that was reasonable. John built his own home that year and started his career as a Home Builder. Today, Hinkle Homes Inc. provides a quality built home at a great value. We do this for every customer, every time. Since our inception in 1997, we have been privileged with an A+ rating with the Better Business Bureau. The core values that flow through the blood lines of this company are more than just words because this is a family owned business. When we say that we have a name to live up to, we mean it.'''
        item['SubImage'] = Images
        item['SubWebsite'] = response.url
        yield item



# from scrapy.cmdline import execute
# execute("scrapy crawl hinkle_Homes".split())

