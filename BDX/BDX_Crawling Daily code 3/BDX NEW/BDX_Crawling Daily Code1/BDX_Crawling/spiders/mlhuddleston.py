
import hashlib
import re
import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class eglecreckSpider(scrapy.Spider):
    name ='mlhuddleston'
    allowed_domains = []
    start_urls = ['https://eaglecreekhomes.net/']

    builderNumber = 51328

    def parse(self, response):
        url='http://mlhuddleston.com/communities.html'
        yield scrapy.FormRequest(url=url, callback=self.page, dont_filter=True)

    def page(self,response):

        links = ["http://mlhuddleston.com/bexleyhills.html",
                 "http://mlhuddleston.com/huntersridge.html",
                 "http://mlhuddleston.com/scarborough.html",
                 "http://mlhuddleston.com/tarafalls.html"]
        for link in links:
            yield scrapy.FormRequest(url=link, callback=self.community, dont_filter=True)

    def community(self, response):

        try:
            SubdivisionName = response.xpath('//h1/text()').extract_first(default='').strip()
            print(SubdivisionName)
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = int(hashlib.md5(bytes(SubdivisionName, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        try:
            desc=''.join(response.xpath('//div[@id="content-fullwidth"]/p/text()').extract())
        except:
            desc=""

        try:
            img=response.xpath('//div[@id="banner"]/img/@src').extract_first('')
            img = 'http://mlhuddleston.com/' + img
            images = img
        except:
            images=''

        try:
            a = []
            aminity = desc
            amenity_list = ["Pool", "Playground", "GolfCourse", "Tennis", "Soccer", "Volleyball", "Basketball",
                            "Baseball", "Views", "Lake", "Pond", "Marina", "Beach", "WaterfrontLots", "Park",
                            "Trails", "Greenbelt", "Clubhouse", "CommunityCenter"]
            for i in amenity_list:
                if i in aminity:
                    a.append(i)
            ab = '|'.join(a)
        except Exception as e:
            print(e)


        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = SubdivisionNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = SubdivisionName
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = ''
        item['City'] = 'Beavercreek'
        item['State'] = 'OH'
        item['ZIP'] = '45434'
        item['AreaCode'] = ''
        item['Prefix'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = desc
        item['SubImage']= images
        item['SubWebsite'] = response.url
        item['AmenityType'] = ab
        yield item



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl mlhuddleston".split())