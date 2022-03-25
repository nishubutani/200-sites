import hashlib
import re
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class haldemanhome(scrapy.Spider):
    name ='haldemanhome'
    allowed_domains = []
    start_urls = ['http://www.haldemanhomes.com/']
    builderNumber = 51544

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
        item['Street1'] = '530-823-2059 P.O. BOX'
        item['City'] = 'Auburn'
        item['State'] = 'CA'
        item['ZIP'] = '95602'
        item['AreaCode'] = ''
        item['Prefix'] =''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] =''
        item['SubDescription'] = "Our portfolio of projects include hundreds of custom homes featuring varying architectural styles such as Tuscan, Contemporary, Spanish, Craftsman Storybook, Tahoe, Victorian and more. We have commercial projects up to 40,000 square feet using various types of construction including wood framed, steel and concrete tilt up."
        item['SubImage']= "https://images.squarespace-cdn.com/content/v1/54eac5fae4b0feaa47752295/1425208063950-IX8VL4ROU79IX2I7RMCD/2485Vineyard-11.jpg?format=1000w|https://images.squarespace-cdn.com/content/v1/54eac5fae4b0feaa47752295/1425208067430-VPARXMSO2KUCZWQX39ZT/2485Vineyard-24.jpg?format=1000w|https://images.squarespace-cdn.com/content/v1/54eac5fae4b0feaa47752295/1425208066874-VHFQQY9DCO71R3UXOC3X/2485Vineyard-33.jpg?format=1000w|https://images.squarespace-cdn.com/content/v1/54eac5fae4b0feaa47752295/1425208069025-2FMS5EOX8WTV7G9TV0HN/2485Vineyard-45.jpg?format=1000w|https://images.squarespace-cdn.com/content/v1/54eac5fae4b0feaa47752295/1425208069906-83D1FD2VU8YJ6LY2RFQS/2485Vineyard-71_HDR.jpg?format=1000w|https://images.squarespace-cdn.com/content/v1/54eac5fae4b0feaa47752295/1425208071378-HGMMHCJI38ONZAUK9T9F/2485Vineyard-88-Edit.jpg?format=1000w|https://images.squarespace-cdn.com/content/v1/54eac5fae4b0feaa47752295/1425208074059-SFIPB1VJYTH8PS5H1OFQ/2485Vineyard-124.jpg?format=1000w"
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl haldemanhome".split())
