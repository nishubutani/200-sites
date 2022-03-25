# -*- coding: utf-8 -*-
import scrapy
import hashlib
import re
import scrapy
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class WeaverHomesSpider(scrapy.Spider):
    name = 'weaver_homes'
    allowed_domains = ['www.weaver-homes.com']
    start_urls = ['http://www.weaver-homes.com/community/']
    builderNumber = "21458"

    def parse(self, response):
        item = BdxCrawlingItem_subdivision()

        # SubdivisionName = response.xpath('//div[@class="house"]/h2/a/text()').extract_first()

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        item['sub_Status'] = "Active"
        # SubdivisionNumber = int(
        #     hashlib.md5(bytes(str(SubdivisionName) + str(self.builderNumber), "utf8")).hexdigest(), 16) % (10 ** 30)

        item['SubdivisionNumber'] = self.builderNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = "350 Wagoner Drive"
        item['City'] = "Fayetteville"
        item['State'] = "NC"
        item['ZIP'] = "28303"
        item['AreaCode'] = "910"
        item['Prefix'] = "630"
        item['Suffix'] = "2100"
        item['Extension'] = ""
        item['Email'] = "warranty@weaver-homes.com"

        item[
            'SubDescription'] = response.xpath(
            '//div[@class="house"]/p/text()').extract_first(
            default="")
        item['SubImage'] = response.xpath(
            '//div[@class="house"]/a/img/@src').extract_first(
            default="")
        item['SubWebsite'] = response.url
        yield item

        try:
            plan_link = "http://www.weaver-homes.com/floorplans/"
            print(plan_link)


            yield scrapy.Request(url=plan_link, callback=self.parse_planlink,
                                     dont_filter=True)
        except Exception as e:
            print(e)
    def parse_planlink(self,response):
        plandetains = {}

        plans = response.xpath('//div[@class="house"]')
        # plans = response.xpath('/html/body/div[3]/table[2]/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td[1]/div')
        # print(plans)
        try:
            for plan in plans:


                planname = plan.xpath('.//h2/a/text()').get()

                feet = plan.xpath('.//strong[1]/text()').get()
                bedroom = plan.xpath('.//strong[2]/text()').get()
                bathroom = plan.xpath('.//strong[3]/text()').get()
                url = plan.xpath('.//h2/a/@href').get()
                image = plan.xpath('.//img/@src').get()
                yield scrapy.Request(url=url, callback=self.plandetail, meta={'planname':planname,'feet':feet,'bedroom':bedroom,'bathroom':bathroom,'PlanDetails':plandetains,'image':image},
                                     dont_filter=True)
        except Exception as e:
            print(e)

    def plandetail(self,response):

        plandetails = response.meta['PlanDetails']

        PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
        f = open("html/%s.html" % PlanNumber, "wb")
        f.write(response.body)
        f.close()


        SubdivisionNumber = self.builderNumber
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['PlanName'] = response.meta['planname']
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        plandetails[response.meta['planname']] = unique_number
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0
        item['BaseSqft'] = response.meta['feet']
        bathroom = response.meta['bathroom']
        # bathroom = re.findall(r'(\d+)',bathroom)[0]

        if len(bathroom) > 1:
            bathroom = bathroom.split('.')[0]
            HalfBaths = 1
        else:
            HalfBaths = 0
        item['Baths'] = bathroom
        item['HalfBaths'] = HalfBaths
        bedroom = response.meta['bedroom']
        bedroom = re.findall(r'(\d+)',bedroom)[0]
        item['Bedrooms'] = bedroom
        item['Garage'] = 0
        item[
            'Description'] = 'Weaver Homes is “two builders in one.” We build a wide range of “production” (or) “spec-built” homes as well as our Weaver Homes Platinum Collection of custom designed homes built to each owners specifications.'
        # a = item['PlanName'].replace('-','').replace(' ','')
        # ElevationImage = re.findall(r'(http://www.weaver-homes.com/wp-content/uploads(.*?).pdf)',response.text)[0]
        # print(ElevationImage)
        item['ElevationImage'] = response.meta['image']

        item['PlanWebsite'] = response.url

        yield item
        yield scrapy.Request(url=response.url, callback=self.home, meta={"PN": plandetails}, dont_filter=True)

    def home(self,response):
        PN = response.meta['PN']
        try:
            home_link = 'http://www.weaver-homes.com/houses/'
            yield scrapy.Request(url=home_link, callback=self.home_list, meta={"PN": PN}, dont_filter=True)

        except Exception as e:
            print(e)

    def home_list(self, response):
        try:
            PN = response.meta['PN']
            # home_div = response.xpath('//div[@class="house"]')
            # for div in home_div:
            link = response.xpath('//div[@class="house"]/h2/a/@href').extract_first()
            addr = response.xpath('//div[@class="house"]/h2/a/text()').extract_first()


            yield scrapy.Request(url=str(link), callback=self.HomesDetails, meta={'addr':addr,'PN':PN,},dont_filter=True)

        except Exception as e:
            print(e)

    def HomesDetails(self, response):
        PN = response.meta['PN']
        planName = response.xpath('normalize-space(//td[2]/h1[@class="smaller"]/a/text())').extract_first(
            default='').strip()
        try:
            PlanNumber = PN[planName]
        except Exception as e:
            print(e)

        address = response.meta['addr']
        SpecStreet1 = address.split(",")[0].strip().rsplit(' ',1)[0].strip()
        SpecCity = address.split(",")[0].strip().rsplit(' ',1)[1].strip()
        SpecState = address.split(",")[1].strip().split(' ')[0]
        SpecZIP = address.split(",")[1].split(' ')[-1]

        try:
            unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
            SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % SpecNumber, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
            print(e)

        try:
            SpecCountry = "USA"
        except Exception as e:
            print(e)

        try:
            SpecPrice = str(response.xpath('normalize-space(//*[contains(text(),"Price")]/following-sibling::text()[1])').get().strip()).replace(",", "")
            SpecPrice = re.findall(r'(\d+)',SpecPrice)[0]
        except Exception as e:
            print(e)

        try:
            SpecSqft = str(response.xpath(
                'normalize-space(//*[contains(text(),"Sq. Footage")]/following-sibling::text()[1])').extract_first(
                default='0').strip()).replace(",", "")
            SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
        except Exception as e:
            print(e)

        try:
            SpecBaths = str(response.xpath(
                'normalize-space(//*[contains(text(),"Baths")]/following-sibling::text())').extract_first(
                default='0').strip()).replace(",", "")
            tmp = re.findall(r"(\d+)", SpecBaths)
            SpecBaths = tmp[0]
            if len(tmp) > 1:
                SpecHalfBaths = 1
            else:
                SpecHalfBaths = 0
        except Exception as e:
            print(e)

        try:
            SpecBedrooms = str(response.xpath(
                'normalize-space(//*[contains(text(),"Bedrooms")]/following-sibling::text())').extract_first(
                default='0').strip()).replace(",", "")
            SpecBedrooms = re.findall(r'(\d+)', SpecBedrooms)[0]
        except Exception as e:
            print(e)

        try:
            MasterBedLocation = "Down"
        except Exception as e:
            print(e)

        try:
            SpecGarage = response.xpath(
                'normalize-space(//*[contains(text(),"Garage")]/following-sibling::text())').extract_first(
                default='0')
            SpecGarage = re.findall(r"(\d+)", SpecGarage)[0]
        except Exception as e:
            print(e)
            SpecGarage = 0

        try:
            SpecDescription = response.xpath(
                'normalize-space(//table[@width="1131"]//table//table/following-sibling::p/text())').extract_first(default='').strip()
        except Exception as e:
            print(e)

        url_add = 'http://www.weaver-homes.com'
        try:
            ElevationImage = '|'.join(i for i in
                                      response.xpath('//div[@id="gallery-1"]//img/@src').extract())
            # ElevationImage = ElevationImage + '|' + '|'.join(response.urljoin(self.start_urls[0] + i) for i in
            #                                                  response.xpath(
            #                                                      '//*[@class="sn-156"]//a/@href').extract())
            # SpecElevationImage = ElevationImage + '|' + '|'.join(
            #     response.urljoin(self.start_urls[0] + i) for i in
            #     response.xpath('//*[@class="zoomImg"]/@src').extract())
            SpecElevationImage = ElevationImage.strip('|')
        except Exception as e:
            print(e)

        try:
            SpecWebsite = response.url
        except Exception as e:
            print(e)

            # ----------------------- Don't change anything here ---------------- #
        item = BdxCrawlingItem_Spec()
        item['SpecNumber'] = SpecNumber
        item['PlanNumber'] = PlanNumber
        item['SpecStreet1'] = SpecStreet1
        item['SpecCity'] = SpecCity
        item['SpecState'] = SpecState
        item['SpecZIP'] = SpecZIP
        item['SpecCountry'] = SpecCountry
        item['SpecPrice'] = SpecPrice
        item['SpecSqft'] = SpecSqft
        item['SpecBaths'] = SpecBaths
        item['SpecHalfBaths'] = SpecHalfBaths
        item['SpecBedrooms'] = SpecBedrooms
        item['MasterBedLocation'] = MasterBedLocation
        item['SpecGarage'] = SpecGarage
        item['SpecDescription'] = SpecDescription
        item['SpecElevationImage'] = SpecElevationImage
        item['SpecWebsite'] = SpecWebsite
        yield item


from scrapy.cmdline import execute
# execute("scrapy crawl weaver_homes".split())