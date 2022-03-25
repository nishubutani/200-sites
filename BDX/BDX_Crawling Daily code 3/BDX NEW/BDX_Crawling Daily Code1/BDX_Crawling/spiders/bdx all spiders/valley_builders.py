# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from scrapy.cmdline import execute
from scrapy.utils.response import open_in_browser

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class valleybuildersSpider(scrapy.Spider):
    name = 'valley_builders'
    allowed_domains = ['www.2valleybuilders.com/']
    start_urls = ['http://2valleybuilders.com/']
    builderNumber = 51526

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
        item['Street1'] = ""
        item['City'] = "Windsor"
        item['State'] = "CO"
        item['ZIP'] = "80634"
        item['AreaCode'] = "970"
        item['Prefix'] = "396"
        item['Suffix'] = "1516"
        item['Extension'] = ""
        item['Email'] = "2valleybuilders@gmail.com"
        item['SubDescription'] = "2 Valley Builders proudly offers six house plans to suit your needs. Each model features a living room, dining area, 3 to 4 bedrooms, 2 to 2 ½ baths (depending on model), master bedroom walk-in closet, unfinished basement and functional front porches. Whether you want a two story home or a ranch, each model can be designed and modified to meet your specifications and lifestyle. We can upgrade, customize, and add functionality to your dream home."
        item['SubImage'] = "http://2valleybuilders.com/img/2ValleyBuilders-ItsPersonal-Family.jpg|http://2valleybuilders.com/img/Banner_Avail_17v2.jpg|http://2valleybuilders.com/img/stmichaelssign_index.jpg"
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        url = 'http://2valleybuilders.com/availability.html'
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.plandetail,
                                 meta={'sbdn': self.builderNumber})

    def plandetail(self, response):
        divs=response.xpath('//div[@class="vbmodel"]')
        for div in divs:

            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                SubdivisionNumber = response.meta['sbdn']
            except Exception as e:
                print(e)

            try:
                PlanName = div.xpath('.//*[@class="vbmodel-specs"]/h6/text()').extract_first(default='').strip()
                print(PlanName)
            except Exception as e:
                print(e)

            try:
                PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % PlanNumber, "wb")
                f.write(response.body)
                f.close()
            except Exception as e:
                print(e)

            try:
                PlanNotAvailable = 0
            except Exception as e:
                print(e)

            try:
                PlanTypeName = 'Single Family'
            except Exception as e:
                print(e)

            try:
                BasePrice = '0'
            except Exception as e:
                print(e)

            try:

                if PlanName == 'THE YAMPA':
                    Baths = '2'
                    HalfBaths = '1'

                elif PlanName == 'THE SONOMA':
                    Baths = '2'
                    HalfBaths = '1'
                else:
                    Baths = str(response.xpath(
                        './/*[contains(text(),"Baths")]').extract_first(
                        default='0').strip()).replace(",", "")
                    Baths = re.sub('<[^<]+?>', '', str(Baths))

                    Baths = Baths.split(' Ba')[-2]
                    Baths = Baths.split('s ')[-1]
                    tmp = re.findall(r"(\d+)", Baths)
                    Baths = tmp[0]
                    if len(tmp) > 1:
                        HalfBaths = 1
                    else:
                        HalfBaths = 0
            except Exception as e:
                print(e)

            try:
                Bedrooms = str(div.xpath(
                    './/*[contains(text(),"Baths")]').extract_first(
                    default='0').strip()).replace(",", "")

                if Bedrooms == '0':
                    Bedrooms = str(div.xpath(
                        './/*[contains(text(),"bed")]').extract_first(
                        default='0').strip()).replace(",", "")

                Bedrooms = re.sub('<[^<]+?>', '', str(Bedrooms))
                print(Bedrooms)
                if ' Be' in Bedrooms:
                    Bedrooms = Bedrooms.split(' Be')[-2]
                else:
                    Bedrooms = Bedrooms.split(' be')[-2]
                # tmp = re.findall(r"(\d+)", Bedrooms)
                # bedrooms = tmp.split(',')[-2]
                # Bedrooms = bedrooms.split(' ')[-2]
                print(Bedrooms)
                # Bedrooms = re.findall(r'(\d+)', Bedrooms)[0]
            except Exception as e:
                print(e)

            try:
                if PlanName == 'THE YAMPA':
                    Garage = '3'
                else:
                    Garage = div.xpath(
                        './/*[contains(text(),"car garage")]').extract_first(default='0')
                    Garage = re.findall(r"(\d+)", Garage)[0]
                    print(Garage)

                if PlanName == 'THE SONOMA':
                    BaseSqft = '2992'
                else:
                    BaseSqft = str(div.xpath('.//*[contains(text(),"square feet finished")]').extract_first(default='0').strip()).replace(",", "")
                    if BaseSqft not in "square feet finished":
                        BaseSqft= str(div.xpath('.//*[contains(text(),"square feet")]').extract_first(default='0').strip()).replace(",", "")
                        if BaseSqft == '0':
                            BaseSqft= str(div.xpath('.//*[contains(text(),"Square Feet")]').extract_first(default='0').strip()).replace(",", "")
                    if not BaseSqft:
                        BaseSqft=0

                    BaseSqft = re.sub('<[^<]+?>', '', str(BaseSqft))
                    if 'squar' in BaseSqft:
                        BaseSqft =BaseSqft.split(' squar')[-2]
                    else:
                        BaseSqft = BaseSqft.split(' Squar')[-2]
                    print(BaseSqft)
            except Exception as e:
                print(e)

            try:
                Description = div.xpath('.//*[@class="vbmodel-specs"]/p/text()').extract_first(
                    default='').strip()
                if Description == '':
                    Description = '2 Valley Builders proudly offers six house plans to suit your needs. Each model features a living room, dining area, 3 to 4 bedrooms, 2 to 2 ½ baths (depending on model), master bedroom walk-in closet, unfinished basement and functional front porches. Whether you want a two story home or a ranch, each model can be designed and modified to meet your specifications and lifestyle. We can upgrade, customize, and add functionality to your dream home.'
            except Exception as e:
                print(e)



            images = ''
            image = div.xpath('.//div[@class="vbmodel-imgs"]//*[contains(@src,"img")]/@src').extract()
            for i in image:
                images = images + 'https://2valleybuilders.com/'+ i + '|'
            images = images.strip('|')
            print(images)

            try:
                PlanWebsite = response.url
            except Exception as e:
                print(e)

            unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
                    10 ** 30)  # < -------- Changes here
            item = BdxCrawlingItem_Plan()
            item['Type'] = Type
            item['PlanNumber'] = PlanNumber
            item['unique_number'] = unique_number  # < -------- Changes here
            item['SubdivisionNumber'] = SubdivisionNumber
            item['PlanName'] = PlanName
            item['PlanNotAvailable'] = PlanNotAvailable
            item['PlanTypeName'] = PlanTypeName
            item['BasePrice'] = BasePrice
            item['BaseSqft'] = BaseSqft
            item['Baths'] = Baths
            print(item['Baths'])
            item['HalfBaths'] = HalfBaths
            print(item['HalfBaths'])
            item['Bedrooms'] = Bedrooms
            item['Garage'] = Garage
            item['Description'] = Description
            item['ElevationImage'] = images
            item['PlanWebsite'] = PlanWebsite
            yield item



# from scrapy.cmdline import execute
#execute("scrapy crawl valley_builders".split())

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl valley_builders'.split())