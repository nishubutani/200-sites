import re

import scrapy
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class ImagineHomesSpider(scrapy.Spider):
    name = 'imagine_homes'
    allowed_domains = ['www.imaginehomessa.com']
    start_urls = ['http://www.imaginehomessa.com/']

    builderNumber = 15927

    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        img = response.xpath('//div[@class="ws_images"]/ul/li/img/@src').getall()
        images = []
        for i in img:
            img1 = 'https://www.imaginehomessa.com' + str(i)
            images.append(img1)
        images = '|'.join(images)

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '11467 Huebner Road, Suite 225'
        item['City'] = 'San Antonio'
        item['State'] = 'TX'
        item['ZIP'] = '78230'
        item['AreaCode'] = '210'
        item['Prefix'] = '877'
        item['Suffix'] = '5900'
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = '''San Antonio's Imagine Homes is leading the nation in new green building technology. Our national award winning system delivers high performance new homes to San Antonio home buyers that result in savings of over 50% on new home heating and cooling costs.With homes certified by the Energy Star  program, our home owners not only enjoy lower energy costs and increased comfort, but they have peace of mind knowing that our building system helps reduce energy use, water consumption, greenhouse gases, and solid waste generation, while creating a home of value that is ahead of its time. '''
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        yield item

        url = 'https://www.imaginehomessa.com/floor-plans.php'
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.Plans_link)
    #
    def Plans_link(self, response):
        urls = response.xpath('//tr[@valign="top"]/td[1]/a/@href').extract()
        name = response.xpath('//tr[@valign="top"]/td[1]/a/text()').extract()
        sqft = response.xpath('//tr[@valign="top"]/td[3]/text()').getall()
        bed = response.xpath('//tr[@valign="top"]/td[4]/text()').getall()
        bath = response.xpath('//tr[@valign="top"]/td[5]/text()').getall()
        garage = response.xpath('//tr[@valign="top"]/td[8]/text()').getall()
        for i,name,sqft,bed,bath,garage in zip(urls,name,sqft,bed,bath,garage):
            url = 'https://www.imaginehomessa.com/' + str(i)
            PN = name
            PSF = sqft
            PB = bed
            PBTH = bath
            PG = garage
            print('PLANS------------------->', url)
            yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.Plans_Details,meta={'PN':PN,'PSF':PSF,'PB':PB,'PBTH':PBTH,'PG':PG})
    #
    def Plans_Details(self, response):

        Type = 'SingleFamily'

        PlanName = response.meta['PN']

        PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)

        SubdivisionNumber = self.builderNumber

        PlanNotAvailable = 0

        PlanTypeName = 'Single Family'


        PlanWebsite = response.url


        Bedrooms = response.meta['PB']

        a = response.meta['PBTH']
        Baths = str(a).split('.')[0]
        HB = str(a).split('.')[-1]
        if '0' in HB:
            HalfBaths = 0
        else:
            HalfBaths = 1

        Garage = response.meta['PG']

        BaseSqft = response.meta['PSF']

        try:
            Description = '''With homes certified by the Energy Star  program, our home owners not only enjoy lower energy costs and increased comfort, but they have peace of mind knowing that our building system helps reduce energy use, water consumption, greenhouse gases, and solid waste generation, while creating a home of value that is ahead of its time. Start Your Home Building Experience with Imagine Homes!Imagine Homes has a rich history of San Antonio new home building experience. From the sales team to your personal builder, we strive to make you a raving fan through the home building process and beyond.'''
        except:
            Description = ''


        try:
            img = response.xpath('//p[@class="floorplan"]/img/@src').get()
            ElevationImage = 'https://www.imaginehomessa.com/' + str(img)
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
# execute("scrapy crawl imagine_homes".split())

