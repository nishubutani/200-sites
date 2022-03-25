# -*- coding: utf-8 -*-
import re
import scrapy
import os
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision
import hashlib

class DurandbuildersllcSpiderSpider(scrapy.Spider):
    name = 'durandbuildersllc_spider'
    allowed_domains = ['durandbuildersllc.com']
    start_urls = ['https://durandbuildersllc.com/']
    builderNumber = 306530037368356511907197446571

    def parse(self, response):

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['SubdivisionNumber'] = self.builderNumber
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 1
        item['Street1'] = '6505 Masonic Dr'
        item['City'] = 'Alexandria'
        item['State'] = 'LA'
        item['ZIP'] = '71301'
        item['AreaCode'] = '318'
        item['Prefix'] = "446"
        item['Suffix'] = "1223"
        item['Extension'] = ""
        item['Email'] = "Durandbuildersllc@yahoo.com"
        item['SubDescription'] = 'Our construction knowledge, superior craftsmanship, quality materials, and meticulous workmanship sets us apart from other local contractors. Our mission is to provide a seamless building process, construct your perfect modern home, and ensure Durand builders delivers construction excellence with the highest level of professional service. You can feel at ease throughout our custom home building process and our luxury home remodeling services. Contact us today for a free consultation to discuss your new custom home project in Louisiana'
        item['SubImage'] = "https://durandbuildersllc.com/wp-content/uploads/2021/02/IMG_0368.jpeg"
        item['SubWebsite'] = "http://durandbuildersllc.com"
        item['AmenityType'] = ''
        yield item

        plan_url = 'https://durandbuildersllc.com/floor-plan-examples/'
        yield scrapy.Request(url=plan_url, callback=self.plans_details, meta={'sbdn': item['SubdivisionNumber']})

    def plans_details(self,response):

        divs = response.xpath('//div[@class="et_pb_section et_pb_section_1 et_section_regular section_has_divider et_pb_bottom_divider"]/div/div')

        for div in divs:
            try:
                plan_name = div.xpath('.//h5[@class="et_pb_toggle_title"]/text()').extract_first('')
                print(plan_name)
            except Exception as e:
                print(e)
                plan_name = ''

            try:
                PlanNumber = int(hashlib.md5(bytes(plan_name, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % PlanNumber, "wb")
                f.write(response.body)
                f.close()
            except Exception as e:
                print(e)

            try:
                bed = div.xpath('.//div[@class="text-wrapper    "]/p[contains(text(),"Bed")]/text()|.//div[@class="et_pb_toggle_content clearfix"]/p[contains(text(),"Bed")]/text()').extract_first('')
                bed = tmp = re.findall(r"(\d+)", bed)[0]
                # bed = div.xpath('.//div[@class="et_pb_toggle_content clearfix"]/p[contains(text(),"Bed")]').extract_first('')
                print(bed)
            except Exception as e:
                print(e)
                bed = ''

            try:
                bath = div.xpath('.//div[@class="text-wrapper    "]/p[contains(text(),"Bath")]/text()|.//div[@class="et_pb_toggle_content clearfix"]/p[contains(text(),"Bath")]/text()').extract_first('')
                tmp = re.findall(r"(\d+)", bath)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0

                # bath = div.xpath('.//div[@class="et_pb_toggle_content clearfix"]/p[contains(text(),"Bath")]').extract_first('')
                print(Baths)
            except Exception as e:
                print(e)
                Baths,HalfBaths = '', ''

            try:
                sqft = div.xpath('.//div[@class="text-wrapper    "]/p[contains(text(),"sq ft")]/text()|.//div[@class="et_pb_toggle_content clearfix"]/p[contains(text(),"sq ft")]/text()').extract_first('')
                if sqft != '':
                    sqft = sqft.replace(",","")
                    sqft = tmp = re.findall(r"(\d+)", sqft)[0]
                # sqft = div.xpath('.//div[@class="et_pb_toggle_content clearfix"]/p[contains(text(),"sq ft")]').extract_first('')
                print(sqft)
            except Exception as e:
                print(e)
                sqft = ''

            try:
                image = div.xpath('.//a/@href').extract()
                if image != []:
                    image = "".join(image)
                print(image)
            except Exception as e:
                print(e)
                image = ''


            SubdivisionNumber = self.builderNumber #if subdivision is not available
            unique = str(PlanNumber) + str(SubdivisionNumber)
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            item = BdxCrawlingItem_Plan()
            item['Type'] = 'SingleFamily'
            item['PlanNumber'] = PlanNumber
            item['unique_number'] = unique_number
            item['SubdivisionNumber'] = self.builderNumber
            item['PlanName'] = plan_name
            item['PlanNotAvailable'] = 1
            item['PlanTypeName'] = 'Single Family'
            item['BasePrice'] = 0
            item['BaseSqft'] = 0
            item['Baths'] = Baths
            item['HalfBaths'] = HalfBaths
            item['Bedrooms'] = bed
            item['Garage'] = 0
            item['Description'] = ''
            item['ElevationImage'] = image
            item['PlanWebsite'] = response.url

            yield item




if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl durandbuildersllc_spider'.split())