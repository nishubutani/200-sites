import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision


class HickmanhomesSpider(scrapy.Spider):
    name = 'hickmanhomes'
    allowed_domains = ['hickmanhomes.net']
    start_urls = ['https://hickmanhomes.net/']
    builderNumber = '32556'

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
        item['Street1'] = '5412 Strickland Ave'
        item['City'] = 'Lakeland'
        item['State'] = 'FL'
        item['ZIP'] = '33812'
        item['AreaCode'] = '863'
        item['Prefix'] = '646'
        item['Suffix'] = '1166'
        item['Extension'] = ""
        item['Email'] = 'info@hickmanhomes.net'
        item[
            'SubDescription'] = 'Our dedicated team of professionals will be there for you from loan application to closing, delivering the right product at the best rates available.'
        image = response.xpath('//img[@class="sp-image"]/@src').getall()
        item[
            'SubImage'] = '|'.join(image)
        item['SubWebsite'] = response.url
        yield item

from scrapy.cmdline import execute
# execute("scrapy crawl hickmanhomes".split())