
import re
import scrapy
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class ImagineHomesSpider(scrapy.Spider):
    name = 'insigniahomesinc'
    allowed_domains = ['http://www.insigniahomesinc.com/']
    start_urls = ['http://www.imaginehomessa.com/']

    builderNumber = 13327


    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        # img = response.xpath('//div[@class="ws_images"]/ul/li/img/@src').getall()
        # images = []
        # for i in img:
        #     img1 = 'https://www.imaginehomessa.com' + str(i)
        #     images.append(img1)
        # images = '|'.join(images)

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '11115 Repp Rd'
        item['City'] = 'Union Bridge'
        item['State'] = 'MD'
        item['ZIP'] = '21791'
        item['AreaCode'] = ''
        item['Prefix'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = 'Welcome to Insignia Homes, where you will always get the home that you want, built the way you want it. Choose from a dozen floor plans we have on hand, or bring your own. Either way, we will give you our absolute best price in either of our premier communities or on your own lot. You choose to do it your wayDan Veronica of Gaithersburg, Maryland had been searching for a builder to give him the home he wanted in a neighborhood where he could walk to the train for his commute to his job in Washington, DC. He found it with Insignia Homes. "These guys knew exactly what I wanted and helped me find a plan that worked for me at a price I could afford. I was able to build a fully custom home with all the amenities I desired and I got my big garage too! My hats off to Insignia for giving me the opportunity to build what is truly my dream home, my way'
        item['SubImage'] = 'http://www.insigniahomesinc.com/_images/banner/5.jpg|http://www.insigniahomesinc.com/_images/banner/1.jpg|http://www.insigniahomesinc.com/_images/banner/2.jpg|http://www.insigniahomesinc.com/_images/banner/3.jpg|http://www.insigniahomesinc.com/_images/banner/4.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl insigniahomesinc".split())