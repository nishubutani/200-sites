# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan


class HuguenotSpider(scrapy.Spider):
    name = 'huguenotbuildersinc'
    allowed_domains = []
    start_urls = ['http://huguenotbuildersinc.com/index.html']

    builderNumber = "33598"


    def parse(self, response):
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '14430 Sommerville Court, Suite C'
        item['City'] = 'MIdlothian'
        item['State'] = 'VA'
        item['ZIP'] = '23113'
        item['AreaCode'] = '804'
        item['Prefix'] = '350'
        item['Suffix'] = '7794'
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = "Welcome to the Huguenot Builders Website. We hope you enjoy your visit and we look forward to building a quality home for you soon!!!. For Huguenot Builders it's not just a business - It's something we enjoy doing!!. We build our reputation everyday one house at a time!!!"
        item['SubImage'] = 'http://huguenotbuildersinc.com/Resources/hugmontoge_new.jpg'
        item['SubWebsite'] = 'http://huguenotbuildersinc.com/index.html'
        yield item

        yield scrapy.Request(url="http://huguenotbuildersinc.com/what.html", callback=self.plan_links)


    def plan_links(self, response):
        links = response.xpath('//p[contains(text(),"Exterior Showcase")]/../../following-sibling::tr//a/@href').getall()
        for link in links:
            yield scrapy.Request(url='http://huguenotbuildersinc.com/'+link, callback=self.plans)
            # yield scrapy.Request(url='http://huguenotbuildersinc.com/media/Exteriors/therenee.html', callback=self.plans)


    def plans(self, response):
        try:PlanName = response.xpath('//span[@class="textbig"]/text()').get(default='').strip()
        except:PlanName = ''

        try:BaseSqft = response.xpath('//span[@class="textbold"]/text()').get(default='').replace('Sq. Ft.','').replace('square','').replace('feet','').strip()
        except:BaseSqft = ''

        text = response.xpath('//p[@class="style50 _lp"]/text()|//p[@class="style23 _lp"]/text()').getall()

        try:
            t = [i for i in text if 'baths' in i or 'Baths' in i or 'Bathrooms' in i]
            if t != []:
                if '2 ½ baths' in t[0]:
                    Baths = 2
                    HalfBaths = 1
                else:
                    try:
                        tmp = re.findall(r"(\d+)", t[0])
                        if len(tmp) > 1:
                            Baths = tmp[0]
                            HalfBaths = 1
                        else:
                            Baths = tmp[0]
                            HalfBaths = 0
                    except:
                        Baths = 0
                        HalfBaths = 0
        except:
            Baths = 0
            HalfBaths = 0

        try:
            t = [i for i in text if 'Bedrooms' in i or 'bedrooms' in i or 'Bedroom' in i]
            if t != []:
                try:Bedrooms = t[0].replace('Bedrooms', '').replace('Bedroom', '').replace('bedrooms', '').replace('Upstairs', '').strip()
                except:Bedrooms = 0
        except:
            Bedrooms = 0

        t = [i for i in text if 'garage' in i]
        if t != []:
            try:Garage = t[0].replace('car', '').replace('garage', '').strip()
            except:Garage = 0.0
        else:
            Garage = 0.0

        if Garage == 'Two':
            Garage = '2'

        if Garage == 'Single':
            Garage = '1'

        try:ElevationImage = ['http://huguenotbuildersinc.com/media/Exteriors/'+i for i in response.xpath('//p[@class="style21"]/img/@src').getall()]
        except:ElevationImage = ''

        PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)

        unique = str(PlanNumber) + str(PlanName) + str(response.url) + str(ElevationImage)
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
        item['Description'] = "Huguenot Builders, Inc builds from transitional and traditional home plans. We currently have approximately 40 different plans to choose from. We build in the price range of $225,000 to $825,000. We currently build in 5 to 6 different subdivisions. We will build a Buyers Plan if so desired. We have loyal subcontractors who do excellent work and have been with Huguenot Builders, Inc for many years. We build: Ranch Plans, 2-story Plans, Plans with a First Floor Master Bedroom, Plans with 5 bedrooms and most all plans have 2 car garages"
        item['ElevationImage'] = '|'.join(ElevationImage)
        item['PlanWebsite'] = response.url
        yield item

# from scrapy.cmdline import execute
# execute("scrapy crawl huguenotbuildersinc".split())