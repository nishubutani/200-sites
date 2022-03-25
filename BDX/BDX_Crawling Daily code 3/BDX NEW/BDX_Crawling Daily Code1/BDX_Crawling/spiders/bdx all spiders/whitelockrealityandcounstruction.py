import hashlib
import re
import scrapy
from scrapy.utils.response import open_in_browser

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class WhitelockrealityAndConstructionSpider(scrapy.Spider):
    name = 'whitelockrealityandcounstruction'
    allowed_domains = ['www.whitlockrealty.net']
    start_urls = ['http://www.whitlockrealty.net/index.cfm']

    builderNumber = "332059562189187880025779966739"

    def parse(self, response):
        images = '|'.join(response.urljoin(self.allowed_domains[0] + i) for i in re.findall(r'\["(.*?)\"\, \"\"',response.text))
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = "4280 Sterlington Rd."
        item['City'] = "Monroe"
        item['State'] = "LA"
        item['ZIP'] = "71203"
        item['AreaCode'] = "318"
        item['Prefix'] = "343"
        item['Suffix'] = "4170"
        item['Extension'] = ""
        item['Email'] = "whitlockrealty@comcast.net"
        item['SubDescription'] = "Whitlock Realty & Construction was founded in 1963 by Gratia Whitlock. She has grown the company along with Whitlock Realty from a one - house - at - time company, to a peak volume of 72 house closings in 1979. Gratia has managed this family operation, developing land in the Monroe area, building and selling new homes and multifamilies, and listing and selling existing properties. Gratia was president of the local Northeast Louisiana Homebuilders Association in 1974. She served as Director for the Louisiana State Homebuilders Association and National Homebuilders Association for seven years."
        item['SubImage'] = images
        item['SubWebsite'] = ""
        yield item

        unique = str("Plan Unknown") + str(self.builderNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['unique_number'] = unique_number
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = "Plan Unknown"
        item['SubdivisionNumber'] = self.builderNumber
        item['PlanName'] = "Plan Unknown"
        item['PlanNotAvailable'] = 1
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0
        item['BaseSqft'] = 0
        item['Baths'] = 0
        item['HalfBaths'] = 0
        item['Bedrooms'] = 0
        item['Garage'] = 0
        item['Description'] = ""
        item['ElevationImage'] = ""
        item['PlanWebsite'] = ""
        yield item

        try:
            link = response.xpath('//*[contains(text(),"Featured Listings")]/@href').extract_first()
            yield scrapy.Request(url='http://www.whitlockrealty.net/' + str(link),callback=self.home_list,meta={"PN": unique_number})
        except Exception as e:
            print(e)

    def home_list(self, response):
        PN = response.meta['PN']
        try:
            homeLinks = response.xpath('//*[@class="summary"]//tr[1]/th[contains(text(),"Bedrooms")]/../following-sibling::tr')
            for home in homeLinks:
                image = home.xpath('.//img/@src').extract_first()
                url = home.xpath('.//*[contains(text(),"View Property Details")]/@href').extract_first()
                yield scrapy.Request(url='http://www.whitlockrealty.net/'+url,callback=self.HomeDetails,meta={"PN": PN,"image":image})
        except Exception as e:
            print(e)

    def HomeDetails(self, response):
        try:
            PlanNumber = response.meta['PN']
        except Exception as e:
            print(e)

        address = response.xpath('normalize-space(//*[@id="contentinner"]/h1/text())').extract_first(default='').strip().split(',')
        SpecStreet1 = address[0]
        SpecCity = address[1].strip()
        SpecState = address[-1].strip().split(' ')[0]
        SpecZIP = address[-1].strip().split(' ')[1]

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
            SpecPrice = str(response.xpath('normalize-space(//*[contains(text(),"List Price:")]/text())').extract_first(default='0').strip()).replace(",", "")
            SpecPrice = re.findall(r"(\d+)", SpecPrice)[0]
        except Exception as e:
            print(e)

        try:
            SpecSqft = response.xpath('//*[contains(text(),"Apx Sq.Ft.:")]/../../td[2]/text()').extract_first(default='0').replace(',','')
            SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
        except Exception as e:
            print(e)

        try:
            SpecBaths = response.xpath('//*[contains(text(),"Bathrooms")]/../following-sibling::td/text()').extract_first(default='0')
            tmp = re.findall(r"(\d+)", SpecBaths)
            SpecBaths = tmp[0]
            if len(tmp) > 1:
                SpecHalfBaths = 1
            else:
                SpecHalfBaths = 0
        except Exception as e:
            print(e)

        try:
            SpecBedrooms = response.xpath('//*[contains(text(),"Bedrooms:")]/../../td[2]/text()').extract_first(default='0')
            SpecBedrooms = re.findall(r"(\d+)", SpecBedrooms)[0]
        except Exception as e:
            print(e)

        try:
            MasterBedLocation = "Down"
        except Exception as e:
            print(e)

        try:
            count = {'One':1,"Two":2,"Three":3,"Four":4,"Five":5,"Six":6,"Seven":7,"Eight":8,"Nine":9}
            SpecGarage = str(response.xpath('normalize-space(//*[contains(text(),"Garage:")]/../../td[2]/text())').extract_first(default='0').strip()).split(',')[-1].strip()
            SpecGarage = str(count[SpecGarage])
        except Exception as e:
            print(e)

        try:
            SpecDescription = response.xpath('normalize-space(//*[contains(text(),"LISTING DESCRIPTION:")]/following-sibling::text())').extract_first(default='').strip()
        except Exception as e:
            print(e)

        try:
            ElevationImage = response.meta['image'].replace('//','')
            if not ElevationImage.startswith('http'):
                SpecElevationImage = 'http://' + ElevationImage
            else:
                SpecElevationImage = ElevationImage
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
# execute("scrapy crawl whitelockrealityandcounstruction".split())