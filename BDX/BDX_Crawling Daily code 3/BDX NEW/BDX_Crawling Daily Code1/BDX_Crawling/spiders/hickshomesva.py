import hashlib
import re
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class autumnhomeSpider(scrapy.Spider):
    name ='hickshomesva'
    allowed_domains = []
    start_urls = ['https://www.autumnhomesinc.com/']

    builderNumber = "32568"

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
        item['Street1'] = ''
        item['City'] = 'Midlothian'
        item['State'] = 'VA'
        item['ZIP'] = '23113'
        item['AreaCode'] = ''
        item['Prefix'] =''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] =''
        item['SubDescription'] = "Hicks Home Builders is a custom home designer and builder and has served residential clients in Richmond, Virginia and surrounding counties some of which include Henrico, Chesterfield, Powhatan, and Goochland.  The company was founded in 1991 by brothers, Charles Hicks and Al Hicks"
        item['SubImage']= "http://hickshomesva.com/wp-content/uploads/2018/01/33.jpg|http://hickshomesva.com/wp-content/uploads/2018/01/58.jpg|http://hickshomesva.com/wp-content/uploads/2018/01/8.jpg"
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl hickshomesva".split())