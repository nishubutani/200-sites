import hashlib
import re

import requests
import scrapy
from scrapy.utils import request
from scrapy.selector import Selector

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan


class EpickhomesSpider(scrapy.Spider):
    name = 'epickhomes'
    allowed_domains = ['epickhomes.com']
    start_urls = ['http://epickhomes.com/']
    builderNumber = '13783'

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
            item['Street1'] = '901 Bruce Road Suite #100'
            item['City'] = 'Chico'
            item['State'] = 'CA'
            item['ZIP'] = '95928'
            item['AreaCode'] = '530'
            item['Prefix'] = '891'
            item['Suffix'] = '4757'
            item['Extension'] = ""
            item['Email'] = 'office@addison-homes.com'
            item['SubDescription'] = "Founded in 1977 by Pete Giampaoli, the name was derived from the Giampaoli family. EPICK is 'Elizabeth, Pete Including Chris and Kyle.'Our company has earned a reputation for timeless design, old world craftsmanship, and a relentless dedication to customer satisfaction. Epick does not just build homes, we create quality neighborhoodsFlexibility is a wonderful quality in both people and floor plans. That's why Epick Homes features many ways to personalize your living space to your lifestyle. Large bonus spaces are provided for hobby and shop areas. These can also be expanded and incorporated in to super family rooms. Dens can become home offices or guest rooms. The kitchens invite culinary excellence and are open for entertaining."
            res = requests.get('https://epickhomes.com/gallery.php')
            r = res.text
            R = Selector(text=r)
            image = '|'.join(response.urljoin(self.start_urls[0] + i) for i in R.xpath('//*[@class="nivobox"]/img/@src').getall())
            item[
                'SubImage'] = image
            item['SubWebsite'] = response.url
            yield item

            try:
                links = response.xpath('//*[@class="thumbnail"]/a/@href').getall()
                for link in links :
                    link = 'https://epickhomes.com/' +str(link)
                    yield scrapy.Request(url=link, callback=self.parse_planlink, dont_filter=True)
            except Exception as e:
                print(e)

    def parse_planlink(self,response):
        divs = response.xpath('//*[@class="thumbnail"]')
        for div in divs:
            link = 'https://epickhomes.com/' +str(div.xpath('./a/@href').get())
            print(link)
            detail = div.xpath('.//p/text()').get()
            planname = div.xpath('.//h3/text()').get()
            yield scrapy.Request(url=link, callback=self.plan, dont_filter=True,meta={'detail':detail,'planname':planname})

    def plan(self,response):

        item = BdxCrawlingItem_Plan()

        detail = response.meta['detail']
        try:
            bed = detail.split('|')[0]
            bedrooms = re.findall(r'(\d+)',bed)[0]
            item['Bedrooms'] = bedrooms

            bath = detail.split('|')[1]
            bathrooms = re.findall(r'(\d+)', bath)
            tmp = bathrooms[0]
            item['Baths'] = tmp
            if len(bathrooms) > 1:
                item['HalfBaths'] = 1
            else:
                item['HalfBaths'] = 0
        except:
            item['Bedrooms'] = 0
            item['Bathrooms'] = 0
            item['HalfBaths'] = 0

        try:
            feet = detail.split('|')[2].replace(',','')
            item['BaseSqft'] = re.findall(r'(\d+)', feet)[0]
        except:
            item['BaseSqft'] = 0

        try :
           item['PlanName'] = response.meta['planname']
        except :
            item['PlanName'] = ''

        try :
            a = []
            des = response.xpath('//*[@class="blog-para"]/p/text()').getall()
            for d in des:
                if len(d) >5 :
                    a.append(d)
            item['Description'] = ''.join(a)
        except :
            item['Description'] = ''

        try :
           elevation = '|'.join(response.urljoin(self.start_urls[0] + i) for i in response.xpath('//*[@class="blog-post"]//img/@src').getall())
           item['ElevationImage'] = elevation
        except:
            item['ElevationImage'] = ''



        try:
            PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % PlanNumber, "wb")
            f.write(response.body)
            f.close()


            SubdivisionNumber = self.builderNumber  # if subdivision is there
            # SubdivisionNumber = self.builderNumber #if subdivision is not available
            unique = str(PlanNumber) + str(SubdivisionNumber)
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

            item['PlanNumber'] = PlanNumber
            item['unique_number'] = unique_number
            item['SubdivisionNumber'] = SubdivisionNumber

        except Exception as e:
            print(e)


        item['Type'] = 'SingleFamily'
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0
        item['Garage'] = 0
        item['PlanWebsite'] = response.url
        yield item





from scrapy.cmdline import execute
# execute("scrapy crawl epickhomes".split())
