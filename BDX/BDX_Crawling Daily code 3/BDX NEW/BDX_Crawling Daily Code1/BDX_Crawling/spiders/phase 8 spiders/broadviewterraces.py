# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan


class BroadviewterracesSpider(scrapy.Spider):
    name = 'broadviewterraces'
    # allowed_domains = ['broadviewterraces.com']
    start_urls = ['http://broadviewterraces.com/']
    builderNumber = '14827'

    def parse(self, response):
        community_links = ['https://broadviewterraces.com/about/']
        for links in community_links:
            print("Communities------------->", links)
            yield scrapy.FormRequest(url=links, callback=self.property_details)

    def property_details(self,response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        SubdivisionName = response.xpath('//div[@itemprop="address"]//text()[1]').get()
        SubdivisionNumber = int(hashlib.md5(bytes(str(SubdivisionName) + str(self.builderNumber), "utf8")).hexdigest(), 16) % (10 ** 30)
        item['SubdivisionNumber'] = SubdivisionNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = SubdivisionName
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = response.xpath('//div[@itemprop="address"]//text()[2]').get().replace('\r','')
        cityzip = response.xpath('//div[@itemprop="address"]//text()[3]').get()
        item['City'] = cityzip.split(',')[0]
        item['State'] = cityzip.split(',')[1].split()[0]
        item['ZIP'] = cityzip.split(',')[1].split()[1]
        phone = response.xpath('//*[@itemprop="telephone"]//text()').get()
        item['AreaCode'] = phone.split('-')[0]
        item['Prefix'] = phone.split('-')[1]
        item['Suffix'] = phone.split('-')[2]
        item['Extension'] = ""
        item['Email'] = 'bigelow@bigelowhomes.net'
        item[
            'SubDescription'] = response.xpath('//*[@class="entry-content"]/p[2]//text()').get()
        item[
            'SubImage'] = 'https://broadviewterrace.files.wordpress.com/2017/07/lr-from-door.jpg'
        item['SubWebsite'] = response.url
        yield item

        planlink = 'https://broadviewterraces.com/floor-plans/'

        yield scrapy.FormRequest(url=planlink, callback=self.plandetail,meta={'SubdivisionNumber':SubdivisionNumber})


    def plandetail(self,response):

        divs = response.xpath('//p[contains(text(),"baths")]')

        for div in divs:
            PlanDetains = {}

            SubdivisionNumber = response.meta['SubdivisionNumber']

            planname = div.xpath('./a/text()').get().replace(":",'').replace('\xa0','')
            print(planname)

            PlanNumber = int(hashlib.md5(bytes(planname, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % PlanNumber, "wb")
            f.write(response.body)
            f.close()

            detail = div.xpath('./text()').get()

            try:
                Bedrooms = re.findall(r'(\d+) bedrooms',detail)[0]
                print(Bedrooms)


            except Exception as e:
                Bedrooms = 0

            try:
                feet = re.findall(r'(\d+) square feet',detail)[0]

            except Exception as e:
                feet = 0
                print(e)

            url = div.xpath('./a/@href').get()
            bathrooms1 = re.findall(r'(\d+) baths',detail.replace(".5", "1"))[0]

            bathrooms = bathrooms1[0]
            print(bathrooms1)

            if len(bathrooms1) > 1:
                HalfBaths = bathrooms1[1]
            else:
                HalfBaths = 0

            yield scrapy.FormRequest(url=url, callback=self.plandata,
                                     meta={'SubdivisionNumber': SubdivisionNumber,'feet':feet,'bathrooms':bathrooms,'Bedrooms':Bedrooms,'HalfBaths':HalfBaths,'PlanNumber':PlanNumber,
                                           'planname':planname})

    def plandata(self,response):

        item = BdxCrawlingItem_Plan()

        PlanNumber = response.meta['PlanNumber']
        SubdivisionNumber = response.meta['SubdivisionNumber']
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

        item['Type'] = "SingleFamily"
        item['PlanNumber'] = response.meta['PlanNumber']
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = response.meta['planname']
        item['Baths'] = response.meta['bathrooms']
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0
        item['BaseSqft'] = response.meta['feet']
        item['HalfBaths'] = response.meta['HalfBaths']
        item['Bedrooms'] = response.meta['Bedrooms']
        item['Garage'] = 2
        description = response.xpath('//*[@class="entry-content"]/p[3]/text()').get()
        if not description:
            description = response.xpath('//*[@class="entry-content"]/p[4]/text()').get()
            if len(description) > 25:
                description = response.xpath('//*[@class="entry-content"]/p[4]/text()').get()
        item[
            'Description'] = description.replace('\xa0','')
        elevationimage = response.xpath('//div[@class="content-area"]//@src').getall()
        item['ElevationImage'] = "|".join(elevationimage)

        item['PlanWebsite'] = response.url
        yield item

from scrapy.cmdline import execute
# execute("scrapy crawl broadviewterraces".split())
