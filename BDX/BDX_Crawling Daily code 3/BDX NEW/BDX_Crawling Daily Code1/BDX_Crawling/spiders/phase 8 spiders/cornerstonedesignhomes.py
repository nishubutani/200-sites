# -*- coding: utf-8 -*-
import hashlib
import scrapy
import re
import requests
from scrapy.http import HtmlResponse

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Spec, BdxCrawlingItem_Plan


class CornerStoneHomesSpider(scrapy.Spider):
    name = 'cornerstonehomes'
    allowed_domains = []
    start_urls = ['https://cornerstonedesignhomes.com/']

    builderNumber = "14081"


    def parse(self, response):
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '2200 East 88th Dr'
        item['City'] = 'Merrillville'
        item['State'] = 'IN'
        item['ZIP'] = '46410'
        item['AreaCode'] = '219'
        item['Prefix'] = '663'
        item['Suffix'] = '3840'
        item['Extension'] = ""
        item['Email'] = ""
        item['SubDescription'] = "From design to final inspection, we measure our success by your approval. We have built several communities throughout Northwest Indiana and have plans for many more, so check back often to see what’s new at Cornerstone. When you build with Cornerstone, we will make the place you live, the home you love!"
        item['SubImage'] = 'https://cornerstonedesignhomes.com/wp-content/uploads/2014/11/cornerstone-home-slide.jpg'
        item['SubWebsite'] = "https://cornerstonedesignhomes.com/"
        yield item

        links = response.xpath('//span[contains(text(),"Our Home Models")]/../following-sibling::ul//ul/li/a/@href').getall()
        for link in links:
            yield scrapy.Request(url=link, callback=self.plans)
            # yield scrapy.Request(url='https://cornerstonedesignhomes.com/models-for-hampton-manor/the-cavanaugh/', callback=self.plans)



    def plans(self, response):
        try:PlanName = response.url.split('/')[-2].replace('-',' ').title()
        except Exception as e:print(e)

        try:Description = ', '.join(i for i in response.xpath('//div[@class="fusion-column-wrapper"]/p/text()|//div[@class="fusion-column-wrapper"]//ul/li/text()|//div[@class="fusion-text fusion-text-1"]/p/text()|//div[@class="fusion-text fusion-text-1"]/ul/li/text()|//div[@class="fusion-text fusion-text-1"]/div/text()|//div[@class="fusion-text fusion-text-1"]//text()').getall() if i!='').replace('\n',' ').replace(',  ,',',').strip()
        except:Description = ''

        try:BaseSqft = ''.join(re.findall(r'(\d,\d+)-square-foot|(\d,\d+) square feet|(\d,\d+) square-foot|(\d,\d+)- Sq. Ft|(\d+)- Sq. Ft|(\d+) Sq. Ft', Description)[0]).replace(',','').strip()
        except:BaseSqft = ''

        try:Bedrooms = ''.join(re.findall(r'(\d) bedroom|(\d)-bedroom|Bedrooms – (\d+)', Description)[0])
        except:Bedrooms = 0

        try:
            Baths = ''.join(re.findall(r', (\d+) bath|, (\d+.*) bath|, (\d+.*)-bath|(\d+)-bath|Baths – (\d+)', Description)[0])
            if ',' in Baths:
                Baths = Baths.split(',')[-1]
            if '2 ½' in Description:
                Baths = 2
                HalfBaths = 1
            elif '2 1/2-bath' in Description:
                Baths = 2
                HalfBaths = 1
            else:
                tmp = re.findall(r"(\d+)", Baths)
                if len(tmp) > 1:
                    Baths = tmp[0]
                    HalfBaths = 1
                else:
                    HalfBaths = 0
        except:
            Baths = 0
            HalfBaths = 0

        try:Garage = ''.join(re.findall('(\d)-car|(\d) car', Description)[0]).strip()
        except:Garage = 0.0

        try:ElevationImage = response.xpath('//ul[@class="slides"]/li//img/@src|//span[@class=" fusion-imageframe imageframe-none imageframe-1 hover-type-none"]/img/@src').getall()
        except:ElevationImage = ''

        PlanNumber = int(hashlib.md5(bytes(str(PlanName)+str(BaseSqft), "utf8")).hexdigest(), 16) % (10 ** 30)

        unique = str(PlanNumber) + str(PlanName) + str(BaseSqft) + str(Baths) + str(Bedrooms) + str(Garage) + str(response.url)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number  # < -------- Changes here
        item['SubdivisionNumber'] = self.builderNumber
        item['PlanName'] = PlanName
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0
        item['BaseSqft'] = BaseSqft
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = Description
        item['ElevationImage'] = '|'.join(ElevationImage)
        item['PlanWebsite'] = response.url
        yield item


# from scrapy.cmdline import execute
# execute("scrapy crawl cornerstonehomes".split())
