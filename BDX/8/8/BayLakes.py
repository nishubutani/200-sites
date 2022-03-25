import hashlib
import re
import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class BaylakesSpider(scrapy.Spider):
    name ='Baylakes'
    allowed_domains = []
    start_urls = ['https://baylakesbuilders.com/index.htm']

    builderNumber = "54144"

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
        item['Street1'] = '1411 S. Webster Ave'
        item['City'] = 'Green Bay'
        item['State'] = 'WI'
        item['ZIP'] = '54301'
        item['AreaCode'] = '920'
        item['Prefix'] ='437'
        item['Suffix'] = '7700'
        item['Extension'] = ""
        item['Email'] ='info@baylakesbuilders.com'
        item['SubDescription'] ="Our Mission Statement:'To provide satisfaction and value to the discerning customer through innovative design, meticulous craftsmanship,and empathetic service.For the past 19 years, Bay Lakes Builders & Development has been recognized as one of the premier builders of custom homes in Green Bay, the Fox Cities, Door County, and throughout Northeast Wisconsin. Guided by the integrity and vision of founder and President Paul E. Soletski, he and his dedicated staff continue to raise the bar when it comes to building homes the right way. Inspired by his grandfather, who was a successful general contractor in the area, Paul’s entire 30-year career has been in the housing industry. Since founding Bay Lakes Builders & Development in 1989, Paul has worked with some of the finest subcontractors and suppliers in the area to construct over 500 attractive and quality-built homes as well as dozens of remodeling and addition projects."
        item['SubImage']= 'https://baylakesbuilders.com/images/main/1370_Sonata.gif|https://baylakesbuilders.com/images/main/4292_Sawgrass_mBath.gif|https://baylakesbuilders.com/images/main/Randall_Kitchen.gif|https://baylakesbuilders.com/images/main/4292_Sawgrass_Office.gif'
        item['SubWebsite'] = response.url
        yield item


# from scrapy.cmdline import execute
# execute("scrapy crawl Baylakes".split())