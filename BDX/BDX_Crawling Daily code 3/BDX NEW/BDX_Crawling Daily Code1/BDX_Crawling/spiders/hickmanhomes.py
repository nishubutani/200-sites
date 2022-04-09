import hashlib
import re

import scrapy
from scrapy.utils.response import open_in_browser

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan


class HickmanhomesSpider(scrapy.Spider):
    name = 'hickmanhomes'
    allowed_domains = ['hickmanhomes.net']
    start_urls = ['https://hickmanhomes.net/']
    builderNumber = '32556'

    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = self.builderNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '5412 Strickland Ave'
        item['City'] = 'Lakeland'
        item['State'] = 'FL'
        item['ZIP'] = '33812'
        item['AreaCode'] = '863'
        item['Prefix'] = '646'
        item['Suffix'] = '1166'
        item['Extension'] = ""
        item['Email'] = 'info@hickmanhomes.net'
        item['SubDescription'] = 'Our dedicated team of professionals will be there for you from loan application to closing, delivering the right product at the best rates available.'
        image = response.xpath('//img[@class="sp-image"]/@src').getall()
        item['SubImage'] = '|'.join(image)
        item['SubWebsite'] = response.url
        yield item

        headers = {

            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,gu;q=0.7',
            'cache-control': 'max-age=0',
            # 'cookie': 'PHPSESSID=545aced8c91404668609ed9531df008c',
            # 'referer': 'https://hickmanhomes.net/custom-homes/',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
        }

        link = 'https://hickmanhomes.net/floorplans/'
        yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True,headers=headers)

    def parse2(self,response):
        open_in_browser(response)
        divs = response.xpath('//div[@class="elementor-row"]//h2/../../../../../..')
        for div in divs[1:]:
            try:
                PlanName = div.xpath('.//h2/text()').extract_first()
                # print(PlanName)
            except Exception as e:
                print("PlanName: ", e)

            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
            except Exception as e:
                print(e)

            try:
                SubdivisionNumber = response.meta['sbdn']
                # print(SubdivisionNumber)
            except Exception as e:
                print(str(e))

            try:
                PlanNotAvailable = 0
            except Exception as e:
                print(e)

            try:
                PlanTypeName = 'Single Family'
            except Exception as e:
                print(e)

            try:
                BasePrice = 0
            except Exception as e:
                print(str(e))

            try:
                PlanWebsite = response.url
            except Exception as e:
                print(e)
            try:
                Bedroo = div.xpath(".//*[contains(text(),'Bedrooms')]/text()").extract_first().strip()
                Bedrooms = re.findall(r"(\d+)", Bedroo)
            except Exception as e:
                Bedrooms = 0
                print("Bedrooms: ", e)

            try:
                Bathroo = div.xpath('.//*[contains(text(),"Bath")]/text()').extract_first().strip()
                tmp = re.findall(r"(\d+)", Bathroo)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                Baths = 0
                print("Baths: ", e)


            try:
                Garage = div.xpath('.//*[contains(text(),"Car")]/text()').extract_first('').strip()
                print(Garage)
            except Exception as e:
                print(e)
                Garage = 0

            try:
                BaseSqft = div.xpath('.//*[contains(text(),"Total")]').extract_first().strip().replace(',', '')
                BaseSqft = ''.join(re.findall(r"(\d+)", BaseSqft))
                BaseSqft = re.findall(r"(\d+)", BaseSqft)
            except Exception as e:
                print("BaseSQFT: ", e)

            try:
                ElevationImages = []
                image  = div.xpath('.//a/@href').extract()
                if image != []:
                    for link in image:
                        ElevationImages.append(link)
                ElevationImages = "|".join(ElevationImages)
            except Exception as e:
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
            item['BasePrice'] = BasePrice
            item['BaseSqft'] = BaseSqft
            item['Baths'] = Baths
            item['HalfBaths'] = HalfBaths
            item['Bedrooms'] = Bedrooms
            item['Garage'] = Garage
            item['Description'] = ''
            item['ElevationImage'] = ElevationImages
            item['PlanWebsite'] = PlanWebsite
            yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl hickmanhomes".split())