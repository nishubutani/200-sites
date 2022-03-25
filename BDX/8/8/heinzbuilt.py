import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision


class HeinzbuiltSpider(scrapy.Spider):
    name = 'heinzbuilt'
    allowed_domains = ['www.heinzbuilt.com']
    start_urls = ['http://www.heinzbuilt.com']
    builderNumber = '49123'

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
        item['Street1'] = '6261 W Founders Dr'
        item['City'] = 'Eagle'
        item['State'] = 'ID'
        item['ZIP'] = '83616'
        item['AreaCode'] = '208'
        item['Prefix'] = '288'
        item['Suffix'] = '5495'
        item['Extension'] = ""
        item['Email'] = 'heinzbuilt@yahoo.com'
        item[
            'SubDescription'] = 'Heinz Built Homes LLC, is primarily a “custom” builder, not a “spec” builder. This means that we design and build for our clients what they want, where they want. This reduces the costs of the home, as we are not building in holding costs while we wait for a buyer. This also means you pay for all the things you love about your home without getting those few features or designs you don’t really care about that someone else thought you should have. It’s a home built for you.'
        # image = response.xpath('//li[@class="dropdown"][1]//ul//a/@href').getall()

        item[
            'SubImage'] = '|'.join(response.urljoin(self.start_urls[0] + i) for i in response.xpath('//li[@class="dropdown"][1]//ul//a/@href').getall())
        item['SubWebsite'] = response.url
        yield item

from scrapy.cmdline import execute
# execute("scrapy crawl heinzbuilt".split())
