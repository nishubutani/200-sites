import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class BuilthomesteadSpider(scrapy.Spider):
    name = 'builthomestead'
    allowed_domains = []
    start_urls = ['https://www.buildhomestead.com/']
    builderNumber = 28474
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
        item['Street1'] = '12339 Wake Union Church Rd'
        item['City'] = 'Wake Forest'
        item['State'] = 'NC'
        item['ZIP'] = '27587'
        item['AreaCode'] = '402'
        item['Prefix'] ='884'
        item['Suffix'] = '4124'
        item['Extension'] = ""
        item['Email'] ='info@buildhomestead.com'
        item['SubDescription'] ="Homestead Custom Builders, LLC was founded with the intent on building modern, high efficiency homes without losing character. We strive to make sure that every home we build is a direct reflection of the home owners' style and preferences. A custom home should be unique for the people and families who occupy it and that's why we take every measure possible to make sure our homes are the true definition of custom. Our pricing, plans and features are as unique as our home owners. We can either start from one of our existing plans, design a complete custom home or even build something based on a plan you may already have. We realize it isn’t just about building a house; it’s about building a home. Homestead Custom Builders, LLC would love the opportunity to sit down with you and build your home, together. Please give us a call today!"
        item['SubImage']= 'https://static.wixstatic.com/media/b609be_d7e10b924ad44e309c9a3e6f1820ff35.jpg/v1/fill/w_1874,h_1155,al_c,q_90,usm_0.66_1.00_0.01/b609be_d7e10b924ad44e309c9a3e6f1820ff35.webp|https://static.wixstatic.com/media/b609be_5c5ac48939dc449f87564bdc9ed0662a.jpg/v1/fill/w_1075,h_738,al_c,q_85,usm_0.66_1.00_0.01/b609be_5c5ac48939dc449f87564bdc9ed0662a.jpg|https://static.wixstatic.com/media/b609be_3302a872a9f84d35a5cb83cce6d17b4b.jpg/v1/fill/w_983,h_738,al_c,q_85,usm_0.66_1.00_0.01/b609be_3302a872a9f84d35a5cb83cce6d17b4b.jpg|https://static.wixstatic.com/media/b609be_c4d655e23e7347838e043f1d19826ab1~mv2_d_1371_1920_s_2.jpg|https://static.wixstatic.com/media/b609be_04be2565fcdf41aa919435bb46b03c75~mv2_d_1920_2880_s_2.jpg|https://static.wixstatic.com/media/b609be_e498fe3f97e74eaabe7408d73ad36912~mv2_d_1920_1280_s_2.jpg|https://static.wixstatic.com/media/b609be_d6f21cf90c5a44e1a94b066090978e8a~mv2_d_1920_2688_s_2.jpg|https://static.wixstatic.com/media/b609be_dea79322d022498f98900e32eafb0028~mv2_d_2880_1920_s_2.jpg|https://static.wixstatic.com/media/b609be_674115b3292a44738405a7710f4ac5f2.jpg|https://static.wixstatic.com/media/b609be_5598e10544b84026aa55c98537ea08f5.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item


if __name__ == '__main__':
    execute('''scrapy crawl builthomestead'''.split())