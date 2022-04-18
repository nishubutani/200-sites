# -*- coding: utf-8 -*-
import hashlib
import json
import re
import scrapy
from scrapy.http import HtmlResponse

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from lxml import html

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'davelargenthomes'
    allowed_domains = ['https://www.davelargenthomes.com']
    start_urls = ['https://www.davelargenthomes.com/']

    builderNumber = "37684"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

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
        item['Street1'] = '1402 N. River Vista Street'
        item['City'] = 'Spokane'
        item['State'] = 'WA'
        item['ZIP'] = '99224'
        item['AreaCode'] = ''
        item['Prefix'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = 'At Dave Largent Homes, Inc. we take great pride in building relationships before structures.  This philosophy helps ensure our projects are done in a timely fashion and accurate to the customer"s specifications, leaving them satisfied beyond their wildest dreams.'
        item['SubImage'] = "https://static.wixstatic.com/media/a3b9ec_4b2f1dd9570c41e7b3ca7532ff5232fc~mv2.jpg|https://static.wixstatic.com/media/e05021_9856bace3b0c72d3ff34d2db76ab6334.png|https://static.wixstatic.com/media/e05021_5b2b0f30e1fe46659cd215baecc4e6bb.png|https://static.wixstatic.com/media/e05021_d83b8e9eeffa46ffabbdc2c697379168.png|https://static.wixstatic.com/media/e05021_a4f21e135ae1bae7eb8066222906d3a3.png"
        item['SubWebsite'] = 'https://www.davelargenthomes.com/'
        item['AmenityType'] = ''
        yield item


        links = response.xpath('//p[contains(text(),"Model Homes")]/../../../../..//a[@data-testid="linkElement"]/@href').extract()[1:]
        for link in links:
            yield scrapy.FormRequest(url=link, callback=self.parse3, dont_filter=True)

    def parse3(self, response):

        try:
            jodi1 = []
            temp = response.xpath('//div[@class="_1Q9if"]/p[@style="font-size:12px;"]/text()').extract()
            total = len(temp) // 2
            try:
                for a in range(0,len(temp),2):
                    value1 = temp[a]
                    key = temp[a+total]
                    jodi =  "<p>" +  str(key) + str(value1) + "</p>" + "<\\n>"
                    jodi1.append(jodi)
            except Exception as e:
                pass

            res = "".join(jodi1)
            text_encoded = res.encode('utf-8')
            text_in_html = HtmlResponse(url='some url', body=text_encoded, encoding='utf-8')

        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//h2/text()').extract_first('')
            if PlanName == '':
                PlanName = response.xpath('//h2/span/text()').extract_first('')
            # PlanName = PlanName.split(":")[1]
            print(PlanName)
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
            SubdivisionNumber = self.builderNumber
            print(SubdivisionNumber)
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
            Bedroo = text_in_html.xpath('//*[contains(text(),"Bed")]/text()').extract_first('').replace("\n","").strip()
            # Bedroom = Bedroo.split(',')[0]
            Bedrooms = re.findall(r"(\d+)", Bedroo)[0]
            # Bedrooms = Bedroom.split(' Bed')[0].strip()

        except Exception as e:
            Bedrooms = 0
            print("Bedrooms: ", e)

        try:
            Bathroo = text_in_html.xpath('//*[contains(text(),"Bath")]/text()').extract_first('').strip().replace("\n","").strip()
            # Baths = Bathroo.split(',')[1]
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
            desc = ''
            print(desc)
        except Exception as e:
            print(e)
            desc = ''

        try:
            Garage = text_in_html.xpath('//*[contains(text(),"Garag")]/text()').extract_first('').strip().replace(',', '')
            Garage = re.findall(r"(\d+)", Garage)[0]
        except Exception as e:
            print("Garage: ", e)
            Garage = 0

        try:
            BaseSqft = text_in_html.xpath('//*[contains(text(),"Total Square")]/text()').extract_first('').strip().replace(',', '')
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
        except Exception as e:
            print("BaseSQFT: ", e)

        try:
            ElevationImages = []
            ElevationImage1 = response.xpath('//wix-image[@id="img_undefined"]/@data-image-info').extract_first('')

            dtaa = json.loads(ElevationImage1)
            ElevationImage1 = dtaa['imageData']['uri']
            ElevationImage1 = "https://static.wixstatic.com/media/" + ElevationImage1

            ElevationImage2 = response.xpath("//img//@src").extract()[1:]
            if ElevationImage2 != []:
                for image in ElevationImage2:
                    image = image.split(".png")[0]
                    image = image + ".png"
                    ElevationImages.append(image)
                ElevationImages.append(ElevationImage1)

            ElevationImage = "|".join(ElevationImages)

        except Exception as e:
            print(str(e))
            ElevationImage = ""

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
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = desc
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item

    # ---------------------------------------------------------------------


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl davelargenthomes'.split())
