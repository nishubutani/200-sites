
import hashlib
import json
import re
import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.cmdline import execute

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class TollBrothersSpider(scrapy.Spider):
    name = 'toll_brothers'
    allowed_domains = []
    start_urls = ['https://www.tollbrothers.com/luxury-homes/Idaho?homes=for-sale&ch=y&']
    not_export_data = True

    builderNumber = "898179281410216340606974859114"

    # ---------------------------Community Urls ------------------------------------ #
    def parse(self, response):
        all_floor_plan = response.xpath('//*[@class="optCommLink"]/@href').extract()
        for pn in all_floor_plan:
            yield scrapy.Request(url=pn, callback=self.process_communities, meta={'url': pn})

    def process_communities(self, response):
        try:
            SubdivisionName = response.xpath('//*[@class="heading page-margins"]/h1/text()').extract_first().strip()
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = int(hashlib.md5(bytes(SubdivisionName, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        try:
            Street1 = response.xpath('//*[@class="js-external-map-mobile"]//p[1]/text()').extract_first().strip()
        except Exception as e:
            print(e)

        try:
            City = response.xpath('//*[@class="js-external-map-mobile"]//p[2]/text()').extract_first().strip().split(
                ',')
            City = City[0]
        except Exception as e:
            City = ''
            print(e)

        try:
            State = response.xpath('//*[@class="js-external-map-mobile"]//p[2]/text()').extract_first().strip().split(
                ',')
            State = State[1].strip().split()[0]
        except Exception as e:
            State = ''
            print(e)

        try:
            ZIP = response.xpath('//*[@class="js-external-map-mobile"]//p[2]/text()').extract_first().strip().split(',')
            ZIP = ZIP[1].strip().split()[1]
        except Exception as e:
            ZIP = ''
            print(e)

        try:
            AreaCode = response.xpath('//*[@class="tel gtm-tel-rep"]/text()').extract_first().strip().split('-')[0]
        except Exception as e:
            AreaCode = ''
            print(e)

        try:
            Prefix = response.xpath('//*[@class="tel gtm-tel-rep"]/text()').extract_first().strip().split('-')[1]
        except Exception as e:
            Prefix = ''
            print(e)

        try:
            Suffix = response.xpath('//*[@class="tel gtm-tel-rep"]/text()').extract_first().strip().split('-')[2]
        except Exception as e:
            Suffix = ''
            print(e)

        try:
            SubDescription = " ".join(response.xpath('//*[@class="desc-text col-md-9"]/p/text()').extract())
        except Exception as e:
            SubDescription = ''
            print(e)

        try:
            SubImage = "|".join(response.xpath('//h2[contains(text(),"Photo Gallery")]/../..//a/@href').extract())
        except Exception as e:
            SubImage = ''
            print(e)

        ab = response.xpath('//li[@class="amenity-item"]/span[2]/text()').extract()
        if ab != []:
            ab = "|".join(ab)
            print(ab)

        Ameniity = ab

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionName'] = SubdivisionName
        item['SubdivisionNumber'] = SubdivisionNumber
        item['BuilderNumber'] = self.builderNumber
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = Street1  # 709 Plaza Drive #2-253, Chesterton, IN"
        item['City'] = City
        item['State'] = State
        item['ZIP'] = ZIP
        item['AreaCode'] = AreaCode  # 219-221-6500 Ext. 1
        item['Prefix'] = Prefix  # 999-3330
        item['Suffix'] = Suffix
        item['Extension'] = ""
        item['Email'] = 'socialmedia@tollbrothers.com'
        item['SubWebsite'] = response.url
        item['SubDescription'] = SubDescription
        item['SubImage'] = SubImage
        item['AmenityType'] = Ameniity
        yield item

        plan_link = response.meta['url']
        yield scrapy.Request(url=plan_link, callback=self.plan_link_page, meta={'sbdn': SubdivisionNumber},
                             dont_filter=True)

    def plan_link_page(self, response):
        sbdn = response.meta['sbdn']
        plan_links = response.xpath('//*[contains(@class,"plan js-plan")]/a/@href').extract()
        for plan in plan_links:
            yield scrapy.Request(url=plan, callback=self.plan_details, meta={'sbdn': sbdn})

    def plan_details(self, response):
        # print(response.text)
        try:
            PlanName = response.xpath('//*[@class="heading page-margins"]/h1/text()').extract_first().strip()
        except Exception as e:
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        try:
            PlanNotAvailable = 0
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = response.meta['sbdn']
        except Exception as e:
            print(str(e))

        try:
            BasePrice = response.xpath('//span[@class="price"]/text()').extract_first().replace('$', '').replace(',',
                                                                                                                 '').strip()
        except Exception as e:
            BasePrice = ''
            print(e)

        try:
            BaseSqft = response.xpath('//*[@class="icon icon-Square-Feet"]/span[2]/text()').extract_first().strip()
        except Exception as e:
            BaseSqft = '0'
            print(e)

        try:
            Baths = response.xpath('//*[@class="icon icon-bath"]/span[2]/text()').extract_first().strip().split('–')
            Baths = max(Baths)
        except Exception as e:
            Baths = '0'
            print(e)

        try:
            HalfBaths = response.xpath(
                '//*[@class="icon icon-Half-Bath"]/span[2]/text()').extract_first().strip().split('–')
            HalfBaths = max(HalfBaths)
        except Exception as e:
            HalfBaths = '0'
            print(e)

        try:
            Bedrooms = response.xpath('//*[@class="icon icon-bed"]/span[2]/text()').extract_first().strip().split('–')
            Bedrooms = max(Bedrooms)
        except Exception as e:
            Bedrooms = '0'
            print(e)

        try:
            Garage = response.xpath('//*[@class="icon icon-garage"]/span[2]/text()').extract_first().strip().split('–')
            Garage = max(Garage)
        except Exception as e:
            Garage = ''
            print(e)

        try:
            Description = " ".join(response.xpath(
                '//div[@class="desc-text col-md-9 read-more-container js-desc-expand"]/p/text()').extract())
        except Exception as e:
            Description = ''
            print(e)

        try:
            ElevationImage1 = response.xpath('//h2[contains(text(),"Photo Gallery")]/../..//div/a/@href').extract()
            ElevationImage2 = response.xpath('//*[@class="hero-media js-media js-isheadshot"]/a/@href').extract()
            ElevationImage3 = response.xpath(
                '//h2[contains(text(),"Available Exteriors")]/../..//div/a/@href').extract()
            ElevationImage = "|".join(ElevationImage1 + ElevationImage2 + ElevationImage3)
        except Exception as e:
            ElevationImage = ''
            print(e)

        unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number  # < -------- Changes here
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = PlanName
        item['PlanNotAvailable'] = PlanNotAvailable
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = BasePrice
        item['BaseSqft'] = BaseSqft
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = Description
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = response.url
        yield item


# execute("scrapy crawl toll_brothers".split())