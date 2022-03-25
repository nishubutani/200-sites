import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class BruchWeichertSpider(scrapy.Spider):
    name = 'Bruch_wiechert_homes'
    allowed_domains = []
    start_urls = ['https://www.wiecherthomes.com/']
    builderNumber = 51333
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
        item['Street1'] = '3073 SKYVIEW LANE'
        item['City'] = 'EUGENE'
        item['State'] = 'OR'
        item['ZIP'] = '97405'
        item['AreaCode'] = '541'
        item['Prefix'] ='686'
        item['Suffix'] = '9458'
        item['Extension'] = ""
        item['Email'] ='wiecherthomes@comcast.net'
        item['SubDescription'] ='Gorgeous Wiechert built home in NEW North Gilham - The Nines Subdivision! 4 Bedrooms PLUS Bonus room AND office, Upscale Finishes, Bright & Spacious. Hardwood Floors, Quartz Counters, Custom Cabinets w/Soft Close Doors & Drawers, Stainless Appliances, 2 walk-in tile showers, Front & Back Landscaping w/Sprinklers, Covered Patio. Taxes not yet assessed. Home is Complete and Ready to View! CHECK OUT THE VIRTUAL TOUR!'
        item['SubImage']= ''
        item['SubWebsite'] = response.url
        yield item

        links = 'https://www.wiecherthomes.com/models-floorplans'
        yield scrapy.FormRequest(url=links,callback=self.plan_link,dont_filter=True)

    def plan_link(self,response):
        links = response.xpath('//div[@class="summary-content sqs-gallery-meta-container"]//*[@class="summary-title"]/a/@href').extract()
        print(len(links))
        for link in links:
            link1 = 'https://www.wiecherthomes.com'+str(link)
            # print(link1)
            # link2 = 'https://www.wiecherthomes.com/the-lakewood'
            yield scrapy.FormRequest(url=link1,callback=self.planDetail)

    def planDetail(self,response):
        print(response.url)
        try:
            PlanName = response.xpath('//*[contains(text(),"The")]/text()').extract_first()
            print(PlanName)
        except Exception as e:
            print("PlanName ", e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % PlanNumber, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
            print(e)

        try:
            # BasePrice = response.xpath('//*[contains(text(),"Priced")]/text()').extract_first()
            # if BasePrice == None or BasePrice == '':
            #     BasePrice = response.xpath('//*[contains(text(),"Starting at")]/text()').extract_first().replace(',',
            #                                                                                                      '')
            # BasePrice = BasePrice.replace(',', '')
            #BasePrice = re.findall(r"(\d+)", BasePrice)[0]
            #print(BasePrice)
            BasePrice = 0
        except Exception as e:
            BasePrice = 0
        try:
            BaseSqft = response.xpath('//*[contains(text(),"sq. ft.")]/text()').extract_first()
            print(BaseSqft)
            if BaseSqft == '' or BaseSqft == None or BaseSqft == "The Sequoia is an excellent 1700 sq. ft., three-bedroom, plus den/flex room, two-bath floor plan with a spacious great room. The elegant vaulted ceiling and gas fireplace with tile surround make the great room spacious and comfortable. The kitchen includes a center island with eating bar, pantry and custom cabinets galore!":
                BaseSqft = response.xpath('//*[contains(text(),"Sq. Ft.")]/text()').extract_first()
            BaseSqft = BaseSqft.replace(',','')
            BaseSqft = re.findall(r"(\d+)", BaseSqft)
            if BaseSqft == ['1700']:
                BaseSqft = 1700
            elif BaseSqft == ['2001']:
                BaseSqft = 2001
            elif len(BaseSqft) == 3:
                BaseSqft = BaseSqft[2]
            print(BaseSqft)
        except Exception as e:
            BaseSqft = 0
        try:
            Bedrooms = response.xpath('//*[contains(text()," bed ")]/text()').extract_first()
            if Bedrooms == '' or Bedrooms == None:
                Bedrooms = response.xpath('//*[contains(text()," Bed")]/text()').extract_first()
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            print(Bedrooms)
        except Exception as e:
            Bedrooms = 0
        try:
            Baths = response.xpath('//*[contains(text()," bed ")]/text()').extract_first()
            if Baths == '' or Baths == None:
                Baths = response.xpath('//*[contains(text()," Bath")]/text()').extract_first()
            Baths = Baths.split('d · ')[-1].split(' ')[0]
            tmp = re.findall(r"(\d+)", Baths)
            print(Baths)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
                print(HalfBaths)
            else:
                HalfBaths = 0
                print(HalfBaths)
        except Exception as e:
            Baths = 0
            HalfBaths = 0

        try:
            Garage = response.xpath('//*[contains(text(),"Car Garage")]/text()').extract_first()
            Garage = re.findall(r"(\d+)", Garage)[0]
            print(Garage)
        except Exception as e:
            Garage = 0


        try:
            ElevationImage = response.xpath('//*[contains(@src,"image")]/@src').extract()
            if ElevationImage == [] or ElevationImage == '':
                ElevationImage = response.xpath('//div[@class="banner-thumbnail-wrapper"]/figure/img/@src').extract()
                print(ElevationImage)
            elif ElevationImage == '':
                ElevationImage = re.findall(r'style="position: fixed; width: 100%; background-image: url(\(.*?)\)',
                                            response.text)
            elif ElevationImage == '':
                ElevationImage = response.xpath('//div[@class="banner-thumbnail-wrapper"]/figure/img/@src').extract()
            ElevationImage = '|'.join(ElevationImage).replace("'", "").replace("(", "")
            print(ElevationImage)
        except ElevationImage as e:
            ElevationImage = ""

        SubdivisionNumber = self.builderNumber  # if subdivision is not available
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = PlanName
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = BasePrice
        item['BaseSqft'] = BaseSqft
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = "Wiechert Custom Homes blends creativity with materials to design a truly unique living environment for you and your family. Every home built is crafted to include those special custom features that make your house a home. Explore the various Models/Floorplans below! Please be advised that the same floor plans are regularly built at varying sizes both larger and smaller and with different specifications.  The floor plans shown here are simply representative of ideas of the general floor plan layout."
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = response.url
        yield item

# execute("scrapy crawl Bruch_wiechert_homes".split())