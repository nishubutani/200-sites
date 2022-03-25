# -*- coding: utf-8 -*-
import hashlib
import re
import json
import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class HappeHomesSpider(scrapy.Spider):
    name = 'Happehome'
    allowed_domains = []
    start_urls = ['https://happehomes.com/']

    builderNumber = '34720'

    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()


        imgs=''.join(re.findall('background-image:url(.*?)class',response.text,re.DOTALL))
        imgss='https://happehomes.com/wp-content'+'|https://happehomes.com/wp-content'.join(re.findall('https://happehomes.com/wp-content(.*?)"',imgs,re.DOTALL))
        if ')' in imgss:
            imgss=imgss.replace(')','')

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = self.builderNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '2575 N Ankeny Blvd #211'
        item['City'] = 'Ankeny'
        item['State'] = 'IA'
        item['ZIP'] = '50023'
        item['AreaCode'] = '515'
        item['Prefix'] = '963'
        item['Suffix'] = '0824'
        item['Extension'] = ""
        item['Email'] = 'info@happehomes.com'
        item['SubDescription'] = 'Are you ready to build the house of your dreams? We’ll build it together! Our team is responsive, professional and patient, and we pride ourselves on providing` both an extraordinary customer experience and a high-quality turnkey product.At Happe Homes, we are committed to exceeding our clients’ expectations and delivering the absolute best product at a fair price.You’re going to love our state-of-the-art showroom, which offers a seamless one-stop-shop for customizing your new home. Come on in, meet the team of experts, and let’s get started!'
        item['SubImage'] = imgss
        item['SubWebsite'] = response.url

        yield item

        link=response.xpath('//ul[@class="sub-menu"][1]/li/a/@href').getall()
        for k in link:
            if k=="https://www.happehomes.com":
               continue

            yield scrapy.Request(url=k, callback=self.plan_details,dont_filter=True)


    def plan_details(self, response):


        PlanNumber = int(hashlib.md5(bytes(response.url,"utf8")).hexdigest(), 16) % (10 ** 30)
        name=response.xpath('//div[@class="header-content"]/h1/text()').get()

        data=response.xpath('//div[@class="header-content"]/div//text()').get()
        datas=data.split('|')

        sqft = datas[0]
        sqft=''.join(re.findall('\d+',sqft,re.DOTALL))
        bath= datas[-1].strip()
        if '.' in bath:
            bath=bath.split('.')
            bath=bath[0]
            halfbath=1
        else:
            bath=bath
            halfbath=0
        bath = ''.join(re.findall('\d+', bath, re.DOTALL))

        bed= datas[1].strip()
        bed = ''.join(re.findall('\d+', bed, re.DOTALL))

        desc=data

        try:
            img1 = '|'.join(response.xpath('//div[@class="et_pb_gallery_image landscape"]/a/@href').getall())
            img2='|'.join(response.xpath('//div[@class="et_pb_module et_pb_image et_pb_image_0"]//img/@src').getall())
            ElevationImage=img1+"|"+img2
            print(ElevationImage)
        except Exception as e:
            print(str(e))

        unique = str(PlanNumber) + str(self.builderNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number  # < -------- Changes here
        item['SubdivisionNumber'] = self.builderNumber
        item['PlanName'] =name
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0.00
        item['BaseSqft'] =sqft
        item['Baths'] =bath
        item['HalfBaths'] = halfbath
        item['Bedrooms'] = bed
        item['Garage'] = 0
        item['Description'] = desc
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = response.url
        yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl Happehome".split())