# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from scrapy.utils.response import open_in_browser

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class AderaHomesSpider(scrapy.Spider):
    name = 'adera_homes'
    allowed_domains = ['www.aderahomes.com']
    start_urls = ['http://www.aderahomes.com/index.html']

    builderNumber = "49097"


    def parse(self, response):
        images = ''
        image = response.xpath('//*[@class="slider"]//img/@src').extract()
        for i in image:
            images = images + 'http://www.aderahomes.com/' + i + '|'
        images = images.strip('|')
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = "6168 Barber Dr"
        item['City'] = "Boise"
        item['State'] = "ID"
        item['ZIP'] = "83716"
        item['AreaCode'] = "208"
        item['Prefix'] = "870"
        item['Suffix'] = "8292"
        item['Extension'] = ""
        item['Email'] = "LYSI@LYSIBISHOP.COM"
        item['SubDescription'] = "Adera Homes builds beautiful, well designed houses in the Treasure Valley's best communities. Our focus is on creating quality homes that reflect exceptional value. It's the dedication and focus we want for our customer, our trades and our craft. Adera Homes makes the home building process an easy one, like it should be - exciting & fun. Our commitment is to customer satisfaction, time management, and house building methods,striving for perfection, every step along the way."
        item['SubImage'] = images
        item['SubWebsite'] = ""
        item['AmenityType'] = ''
        yield item
        try:
            links = response.xpath('//a[contains(text(), "Gallery")]/../ul/li/a/@href').extract()
            for link in links:
                yield scrapy.Request(url='http://www.aderahomes.com/' + str(link),callback=self.plans_details,dont_filter=True)
        except Exception as e:
            print(e)


    def plans_details(self,response):

        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = self.builderNumber
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('normalize-space(//h4/text())').extract_first(default='').strip()
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

        details = response.xpath('//*[@class="two_col"]/p[2]/text()').extract_first()
        if 'bath' in details:
            try:
                Baths = re.findall(r'bed(.*?)bath', details)[0].strip()
                tmp = re.findall(r"(\d+)", Baths)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                print(e)

            try:
                Bedrooms = re.findall(r'sqft. (.*?) bed', details)[0]
            except Exception as e:
                print(e)
            try:
                Garage = re.findall(r'bath (.*?) garage', details)[0]
                BaseSqft = re.findall(r'^(.*?) sqft', details)[0]
            except Exception as e:
                print(e)

            try:
                Description = response.xpath('normalize-space(//*[@class="two_col"]/p[3]/text())').extract_first(default='').strip()
            except Exception as e:
                print(e)

            try:
                ElevationImage = '|'.join(response.urljoin('http://www.aderahomes.com/' + i) for i in response.xpath('//*[@class="right_img"]/img/@src').extract())
            except Exception as e:
                print(e)

            try:
                PlanWebsite = response.url
            except Exception as e:
                print(e)

            SubdivisionNumber = SubdivisionNumber #if subdivision is there
            #SubdivisionNumber = self.builderNumber #if subdivision is not available
            unique = str(PlanNumber)+str(SubdivisionNumber)
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
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
    execute('scrapy crawl adera_homes'.split())
