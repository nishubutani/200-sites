import re

import scrapy
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision


class GatliffcustomHomesSpider(scrapy.Spider):
    name = 'gatliffcustom_Homes'
    # allowed_domains = ['www.gatliffcustomhomes.com']
    start_urls = ['http://www.gatliffcustomhomes.com/']
    builderNumber = 26088

    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        item = BdxCrawlingItem_subdivision()
        sub_image = '|'.join(response.xpath('//ul/li/img/@src').getall())
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '155 College Street'
        item['City'] = 'Wadsworth'
        item['State'] = 'OH'
        item['ZIP'] = '44281'
        item['AreaCode'] = '330'
        item['Prefix'] = '335'
        item['Suffix'] = '5262'
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = '''If you are looking for a Concept to Completion custom home builder that will consider YOU to be the most important partner in the construction of your new home or home remodeling project, then Gatliff Custom Builders should be your first choice.Gatliff Custom Builders will help you develop a home design that is practical, yet uniquely “You”. There will be no surprise construction delays because you will receive a well-planned schedule of events detailing the process of construction all the way through the date of completion.Partner up with Gatliff Custom Builders to build your ultimate custom home or for your next home remodeling project.'''
        item['SubImage'] = sub_image
        item['SubWebsite'] = response.url
        yield item

        url = 'https://www.gatliffcustomhomes.com/inspiration-gallery-from-gatliff-custom-builders/'
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.Plans_link)

    def Plans_link(self, response):
        urls = response.xpath('//div[@class="planimage"]/a/@href').extract()
        for i in urls:
            url = str(i)
            print('PLANS------------------->', url)
            yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.Plans_Details)

    def Plans_Details(self, response):

        Type = 'SingleFamily'

        PlanName = response.xpath('//div[@class="plantitledetail"]/text()').extract_first().strip()

        PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)

        SubdivisionNumber = self.builderNumber

        PlanNotAvailable = 0

        PlanTypeName = 'Single Family'

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

        Bedrooms = response.xpath('//div[@class="planinfo"]/text()[2]').get().replace('Bedrooms: ','')

        a = response.xpath('//div[@class="planinfo"]/text()[3]').get()
        a = a.split(':')[1].strip()
        Baths = a[0]
        HalfBaths = a[-1]
        # Bath = re.findall(r"(\d+)", a)
        # tmp = Bath
        # if len(tmp) > 1:
        #     HalfBaths = 1
        # else:
        #     HalfBaths = 0

        # try:
        #     Garage = response.xpath('//div[@class="table-2"]/table/tbody/tr[7]/td[2]/text()').extract_first()
        #     Garage = re.findall(r"(\d+)", Garage)
        #     Garage = Garage[0]
        # except:
        Garage = 0

        BaseSqft = response.xpath('//div[@class="planinfo"]/text()[1]').extract_first().replace(' SF','')

        try:
            Description = response.xpath('//p/text()').get().strip()
        except:
            Description = ''

        try:
            ElevationImage = '|'.join(response.xpath('//div[@class="planboxdetail"]/img/@src').getall())

        except Exception as e:
            ElevationImage = ''
            print(str(e))

        unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['Type'] = Type
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number  # < -------- Changes here
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = PlanName
        item['PlanNotAvailable'] = PlanNotAvailable
        item['PlanTypeName'] = PlanTypeName
        item['BasePrice'] = 0
        item['BaseSqft'] = BaseSqft
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = Description
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item

# from scrapy.cmdline import execute
# execute("scrapy crawl gatliffcustom_Homes".split())

