
# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'horizonbuilt'
    allowed_domains = ['horizonbuilt.com']
    start_urls = ['https://www.horizonbuilt.com/community/']
    builderNumber = 33414


    def parse(self, response):
        links = response.xpath('//div[@class="cta-container-right"]/a/@href').extract()
        for link in links:
            yield scrapy.FormRequest(url=link,callback=self.community_detail,dont_filter=True)

    def community_detail(self,response):

        try:
            subdivisonName = response.xpath("//h1/text()").extract_first('')
            print(subdivisonName)
        except Exception as e:
            print(e)
            subdivisonName = ''

        try:
            street = response.xpath("//*[contains(text(),'COMMUNITY LOCATION')]/../text()[1]").extract_first('').replace("\n","")
            print(street)
        except Exception as e:
            print(e)
            street = ''

        try:
            add2 = response.xpath("//*[contains(text(),'COMMUNITY LOCATION')]/../text()[2]").extract_first('').replace("\n","")
            print(add2)
            city = add2.split(",")[0]
            print(city)

            state = add2.split(",")[1].strip().split(" ")[0]
            zip = add2.split(",")[1].strip().split(" ")[1]
        except Exception as e:
            print(e)
            city,state,zip = '','',''


        try:
            desc = response.xpath('//div[@class="ov-text-content"]/p/text()').extract_first('')
            print(desc)
        except Exception as e:
            print(e)
            desc = ''

        try:
            sub_imagwe = []
            image = response.xpath('//div[@class="gallery-image"]/@style').extract()

            if image != []:

                for ii in image:
                    ii = ii.replace("background-image: url(","").replace(");","")
                    sub_imagwe.append(ii)


                sub_imagwe = "|".join(sub_imagwe)
                print(sub_imagwe)
            else:
                sub_imagwe = ''



        except Exception as e:
            print(e)
            sub_imagwe = ""



        subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = subdivisonNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = subdivisonName
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = street
        item['City'] = city
        item['State'] = state
        item['ZIP'] = zip
        item['AreaCode'] = ''
        item['Prefix'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = desc
        item['SubImage'] = sub_imagwe
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl horizonbuilt'.split())
