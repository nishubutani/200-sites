import re

import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision


class HofmanndbSpider(scrapy.Spider):
    name = 'hofmanndb'
    allowed_domains = ['www.hofmanndb.com/']
    start_urls = ['https://www.hofmanndb.com/']
    builderNumber = '32838'

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
        item['Street1'] = '365 South Street'
        item['City'] = 'Morristown'
        item['State'] = 'NJ'
        item['ZIP'] = '07960'
        item['AreaCode'] = '973'
        item['Prefix'] = '998'
        item['Suffix'] = '6820'
        item['Extension'] = ""
        item['Email'] = 'ernie@hofmanndb.com'
        item[
            'SubDescription'] = 'Ernie Hofmann has been in the construction industry for forty-three years. He began his career as an apprentice carpenter and worked in the field for ten years before earning a degree in civil engineering technology. In 1983 Ernie went on to establish Hofmann Design Build Inc., a full line design/build firm specializing in residential remodeling, custom home construction, historic restoration and light commercial remodeling. The company quickly earned its long standing reputation for innovative designs, dedication to quality, service, attention to details and completing projects on schedule, for which it has earned many awards'

        item[
            'SubImage'] = 'https://www.hofmanndb.com/wp-content/uploads/2015/02/hofmanndb-home-1.jpg'
        item['SubWebsite'] = response.url
        yield item

from scrapy.cmdline import execute
# execute("scrapy crawl hofmanndb".split())