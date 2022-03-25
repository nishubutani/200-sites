import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class castleBuilderSpider(scrapy.Spider):
    name = 'castle_builder'
    allowed_domains = []
    start_urls = ['https://castle-builders.com']
    builderNumber = 14985

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
        item['Street1'] = '6616 Ruppsville Road'
        item['City'] = 'Allentown'
        item['State'] = 'PA'
        item['ZIP'] = '18106'
        item['AreaCode'] = ''
        item['Prefix'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] = 'INFO@CASTLE-BUILDERS.COM'
        item[
            'SubDescription'] = 'Castle Builders Inc. is currently developing several new communities across the Lehigh Valley area, with several more coming soon! Please contact us with any inquiries regarding our upcoming neighborhoods or if you are a lot owner in search of a builder.'
        item[
            'SubImage'] = 'https://castle-builders.com/wp-content/uploads/2013/11/slide13.jpg|https://castle-builders.com/wp-content/uploads/2013/11/slide4.jpg|https://castle-builders.com/wp-content/uploads/2013/11/slide11.jpg|https://castle-builders.com/wp-content/uploads/2013/11/slide21.jpg'
        item['SubWebsite'] = response.url
        yield item

        # links = response.xpath('//div[@class="one-half"]/div[4]/ul/li/a/@href').extract()
        # div = ''.join(response.xpath('//div[@class="entry-content"]').extract())
        # links = re.findall(r'<a href=(.*?)>',div)
        # for link in links:
        #     link = link.replace('.','').replace('"','')
        #     url = "https://castle-builders.com"+str(link)
        #     print(url)
        #     yield scrapy.FormRequest(url=str(url),callback=self.parse1,dont_filter=True)
    #
    # def parse1(self,response):
    #     subdivisonName = response.xpath('//ul[@class="tabs-model-list cf"]/li/a/h3/text()').extract()
    #     for subdivisonName in subdivisonName:
    #         subdivisonName = subdivisonName
    #         print(subdivisonName)
    #     subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
    #     f = open("html/%s.html" % subdivisonNumber, "wb")
    #     f.write(response.body)
    #     f.close()
    #
    #     item2 = BdxCrawlingItem_subdivision()
    #     item2['sub_Status'] = "Active"
    #     item2['SubdivisionName'] = subdivisonName
    #     item2['SubdivisionNumber'] = subdivisonNumber
    #     item2['BuilderNumber'] = self.builderNumber
    #     item2['BuildOnYourLot'] = 0
    #     item2['OutOfCommunity'] = 1
    #     item2['Street1'] = '6616 Ruppsville Road'
    #     item2['City'] = 'Allentown'
    #     item2['State'] = 'PA'
    #     item2['ZIP'] = '18106'
    #     item2['AreaCode'] = ''
    #     item2['Prefix'] = ''
    #     item2['Suffix'] = ''
    #     item2['Extension'] = ""
    #     item2['Email'] = "INFO@CASTLE-BUILDERS.COM"
    #     item2['SubDescription'] = response.xpath('//*[@class="entry-content"]/center/text()').extract_first(default="")
    #     item2['SubImage'] = response.xpath('//div[@class="entry-content"]/p/a/img/@src').extract_first(default="")
    #     item2['SubWebsite'] = response.url
    #     yield item2

# execute("scrapy crawl castle_builder".split())