import hashlib
import re
import scrapy
from scrapy.cmdline import execute
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan


class DomegahomesSpider(scrapy.Spider):
    name = 'collinhomesinc'
    allowed_domains = ['collinhomesinc.com']
    start_urls = ['http://www.collinhomesinc.com/']
    builderNumber = '51644'

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
        item['Street1'] = '90 Shadagee Rd #102'
        item['City'] = 'Saco'
        item['State'] = 'ME'
        item['ZIP'] = '04072'
        item['AreaCode'] = ''
        item['Prefix'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = 'Whether you have your heart set on a brand new home or are about to begin a bit of remodeling, you have come to the right place. Brothers Gary and Danny Collin have a combined history of forty-six years of happy customers behind them, and they are ready to begin another venture. Throughout their years as carpenters and contractors, they have learned that what it takes to deliver a finished product are satisfied customers. They learned, as you will, that standing behind their work long after the last nail has been driven and the grass grown smoothly into a great yard is the hallmark of a successful business.'
        item['SubImage'] = 'http://www.collinhomesinc.com/images/gallery/123_2327.jpg|http://www.collinhomesinc.com/images/gallery/123_2328.jpg|http://www.collinhomesinc.com/images/gallery/P6201401.JPG|http://www.collinhomesinc.com/images/gallery/041.JPG|http://www.collinhomesinc.com/images/gallery/043.JPG'
        item['SubWebsite'] = 'http://www.collinhomesinc.com/'
        item['AmenityType'] = ''

        yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl collinhomesinc".split())