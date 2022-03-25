# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from scrapy.cmdline import execute
from scrapy.utils.response import open_in_browser

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class byrdhomebuildersSpider(scrapy.Spider):
    name = 'byer_builders'
    allowed_domains = ['www.byerbuilders.com/']
    start_urls = ['https://byerbuilders.com/']
    builderNumber = "54572"

    def parse(self, response):
        images = ''
        image = response.xpath('//*[contains(@src,"")]//img/@src').extract()
        for i in image:
            images = images + self.start_urls[0] + i + '|'
        images = images.strip('|')
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
        item['Street1'] = '763 E 7th Street'
        item['City'] = 'Lexington '
        item['State'] = 'KY '
        item['ZIP'] = '40509'
        item['AreaCode'] = '859'
        item['Prefix'] ='983'
        item['Suffix'] = '8400'
        item['Extension'] = ""
        item['Email'] ='jon@byerbuilders.comm'
        item['SubDescription'] ='Byer Builders provide quality new construction services and residential remodeling in the Central Kentucky area.'
        item['SubImage']= images
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item



        url = 'https://byerbuilders.com/'
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.parse_planlink,
                                 meta={'sbdn': self.builderNumber})

    def parse_planlink(self,response):

        try:
            links = response.xpath('//*[@id="nav-menu-item-120"]/div/div/ul/li/a/@href').extract()
            plandetains = {}
            for link in links:
                yield scrapy.Request(url="https://byerbuilders.com/the-walker-floor-plan/" + str(link),callback=self.plans_details, meta={'sbdn':self.builderNumber,'PlanDetails':plandetains},dont_filter=True)
        except Exception as e:
            print(e)

    def plans_details(self,response):
        plandetails = response.meta['PlanDetails']
        item = BdxCrawlingItem_Plan()
        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = response.meta['sbdn']
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//div[@class="vc_column-inner "]//div//h2/text()').extract_first(default='').strip()
            PlanName = PlanName.split(":")[1]
            print(PlanName)

            if not PlanName:
                PlanName=response.xpath('//div[@class="vc_column-inner "]//div//h2/text()').extract_first(default='').strip()
                print(PlanName)

        except Exception as e:
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
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

            Baths = str(response.xpath('normalize-space(//div[@class="vc_column-inner "]//div/div[@class="wpb_wrapper"]/p[2])').extract_first(
                default='0').strip()).replace(",", "")
            Baths1 = Baths.split(":")[1]
            Baths = re.findall(r"(\d+)", Baths1)[0]
            print(Baths)
            if len(Baths1) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0

            item['HalfBaths'] = HalfBaths
        except Exception as e:
            print(e)


        try:

            Bedrooms = str(response.xpath('//div[@class="vc_column-inner "]//div/div[@class="wpb_wrapper"]/p[3]').extract_first(
                default='0').strip()).replace(",", "")
            Bedrooms = re.findall(r"(\d+)",Bedrooms)[0]
            print(Bedrooms)
        except Exception as e:
            print(e)

        try:

            Garage = 0.0


            if 'isabella' in response.url:
                BaseSqft = str(response.xpath('//*[contains(text(),"Total")]').extract_first(default='0').strip()).replace(",", "")
                BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]

            else:
                BaseSqft = str(response.xpath('//*[contains(text(),"Total")]').extract_first(default='0').strip()).replace(",", "")
                BaseSqft = BaseSqft.split(" Total")[1]
                BaseSqft = BaseSqft.split(" ")[-3]
                print(BaseSqft)


        except Exception as e:
            print(e)


        try:
            Description=response.xpath('normalize-space(//div[@class="vc_column-inner "]//div/div[@class="wpb_wrapper"]/p[1])').extract_first(default='').strip()
            Description= Description.split(": ")[1].replace("′","")
            print(Description)
        except Exception as e:
            print(e)

        try:
            images = ''
            image = response.xpath('//div[@id="gallery-1"]/dl/dt/a/img/@src').extract()
            for i in image:
                images = images + '' + str(i) + '|'
            images = images.strip('|')
            ElevationImage = images
            print(ElevationImage)
        except Exception as e:
            ElevationImage = ''

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

        SubdivisionNumber = SubdivisionNumber #if subdivision is there
        #SubdivisionNumber = self.builderNumber #if subdivision is not available
        unique = str(PlanNumber)+str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        plandetails[PlanName] = unique_number

        item = BdxCrawlingItem_Plan()
        item['Type'] = Type
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
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
        item['Description'] = Description
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl byer_builders'.split())

