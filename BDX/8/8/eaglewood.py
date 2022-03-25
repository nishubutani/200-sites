import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header


class DannysullivanconstructionComSpider(scrapy.Spider):
    name = 'eaglewood'
    allowed_domains = []
    start_urls = ['https://www.eaglewood.com/']
    builderNumber = 31366

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
        item['Street1'] = '2490 E. GALA ST.'
        item['City'] = 'MERIDIAN'
        item['State'] = 'ID'
        item['ZIP'] = '83642'
        item['AreaCode'] = '208'
        item['Prefix'] = '855'
        item['Suffix'] = '0502'
        item['Extension'] = ""
        item['Email'] = 'info@eaglewood.com'
        item[
            'SubDescription'] = 'With decades of experience and hundreds of homes under our belt, no one is more qualified to bring your dreams into reality than the experienced professionals at Eaglewood. Over the years we have assembled a team of skilled craftsmen and construction experts Ventura Kitchenthat take great pride in our reputation, building every component and detail of the home with precision. These professionals have proven themselves by consistently delivering the best product, so you can rest assured your new home meets the highest quality standards.'
        item[
            'SubImage'] = 'https://www.eaglewood.com/images/banners/slider/monterey-master-meridian-idaho.jpg|https://www.eaglewood.com/images/banners/slider/clearwater-bath-boise.jpg|https://www.eaglewood.com/images/banners/slider/clearwater-exterior-boise.jpg'
        item['SubWebsite'] = response.url
        yield item
        l = ['0', '10', '20', '30', '40']
        for i in l:
            link = f'https://www.eaglewood.com/floor-plans/ep?action=list&plan_id=&result_offset={i}'
            print(link)
            yield scrapy.FormRequest(url=link, callback=self.d17, dont_filter=True)

    def d17(self, response):
        planlinks = response.xpath('//div[@class="sr_result_row"]/../@href').extract()
        for plink in planlinks:
            print(plink)
            yield scrapy.FormRequest(url=plink, callback=self.pDetail, dont_filter=True)

    def pDetail(self, response):
        try:
            PlanName = response.xpath('//div[@class="h_title"]/h1/text()').extract_first()
            print(PlanName)
        except Exception as e:
            print("PlanName: ", e)
        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
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
            Bedroo = response.xpath(
                '//*[contains(text(),"BED")]/../p[2]/text()').extract_first().strip()
            # Bedroom = Bedroo.split('|')[1]
            Bedrooms = re.findall(r"(\d+)", Bedroo)[0]
            Bedrooms = Bedrooms.strip()

        except Exception as e:
            Bedrooms = 0
            print("Bedrooms: ", e)

        try:
            Bathroo = response.xpath(
                '//*[contains(text(),"BATH")]/../p[2]/text()').extract_first().strip()
            # Bathroom = Bathroo.split('|')[2]
            # Baths = Bathroom.split(' bath,')
            tmp = re.findall(r"(\d+)", Bathroo)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0

        except Exception as e:
            Baths = 0
            print("Baths: ", e)

        Garage = response.xpath('//*[contains(text(),"Garage")]/../p[2]/text()').extract_first()
        try:
            BaseSqft = response.xpath(
                '//*[contains(text(),"SQFT")]/../p[2]/text()').extract_first().strip().replace(',', '')
            BaseSqft = ''.join(re.findall(r"(\d+)", BaseSqft))
            BaseSqft = BaseSqft.strip()
            print(BaseSqft)
        except Exception as e:
            print("BaseSQFT: ", e)

        try:
            images=''.join(re.findall('<div class="sr_small_images"><div>(.*?)id="sr_shadow"/>',response.text,re.DOTALL))
            img=re.findall('<img src="(.*?)"',images,re.DOTALL)
            # Elevationimag = response.xpath('//div[@class="slick-slide"]/img/@src').extract()
            Elevationimage='https://www.eaglewood.com'+'|https://www.eaglewood.com/f'.join(img)
            print(Elevationimage)
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
        item[
            'Description'] = 'We have access to building sites, in nearly every development in the area! Bring us your custom home plans or choose from one of the many popular plans in our library. Click one of the thumbnails below for a PDF sheet with full details.'
        item['ElevationImage'] = Elevationimage
        item['PlanWebsite'] = PlanWebsite
        yield item

        hlink = 'https://www.eaglewood.com/new-homes-for-sale/'
        yield scrapy.FormRequest(url=hlink, callback=self.HomeUrls, dont_filter=True)


    def HomeUrls(self, response):
        urls = response.xpath('//div[@class="sr_search_results"]/a/@href').extract_first()
        yield scrapy.FormRequest(url=urls, callback=self.hDetail, dont_filter=True)


    def hDetail(self, response):
        unique = str("Plan Unknown") + str(self.builderNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['unique_number'] = unique_number
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = "Plan Unknown"
        item['SubdivisionNumber'] = self.builderNumber
        item['PlanName'] = "Plan Unknown"
        item['PlanNotAvailable'] = 1
        item['PlanTypeName'] = "Single Family"
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
            SpecStreet1 = response.xpath('//div[@class="sr_listing_container"]/h1/text()').extract()
            Address = SpecStreet1[0].replace(',', '')
            print(Address)
            city = SpecStreet1[1]
            state = 'ID'
            ZIP = '83686'
            unique = str(Address) + str(city) + str(state) + str(ZIP)
            SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % SpecNumber, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
            print(e)

        # try:
        #     PlanNumber = response.meta['PN']
        # except Exception as e:
        #     print(e)

        try:
            SpecCountry = "USA"
        except Exception as e:
            print(e)

        try:
            SpecPrice = str(response.xpath('normalize-space(//*[contains(text(),"$")]/text())').extract_first(
                default='0').strip()).replace(",", "").replace('$', '')
            SpecPrice = re.findall(r"(\d+)", SpecPrice)[0]
        except Exception as e:
            print(e)

        try:
            SpecSqft = str(response.xpath('normalize-space(//*[contains(text(),"SQFT")]/../p[2]/text())').extract_first(
                default='0').strip()).replace(",", "")
            SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
        except Exception as e:
            SpecSqft = 0

        try:
            SpecBaths = str(response.xpath(
                'normalize-space(//*[contains(text(),"BATHS")]/../p[2]/text())').extract_first(
                default='0').strip()).replace(",", "")
            tmp = re.findall(r"(\d+)", SpecBaths)
            SpecBaths = tmp[0]
            if len(tmp) > 1:
                SpecHalfBaths = 1
            else:
                SpecHalfBaths = 0
        except Exception as e:
            SpecBaths = 0
            SpecHalfBaths = 0

        try:
            SpecBedrooms = str(response.xpath(
                'normalize-space(//*[contains(text(),"BEDS")]/../p[2]/text())').extract_first(
                default='0').strip()).replace(",", "")
            SpecBedrooms = re.findall(r"(\d+)", SpecBedrooms)[0]
        except Exception as e:
            SpecBedrooms = 0

        try:
            MasterBedLocation = "Down"
        except Exception as e:
            print(e)

        try:
            SpecGarage =response.xpath('//*[contains(text(),"Garage")]/../p//text()').extract_first()
            SpecGarage=''.join(re.findall('\d+',SpecGarage,re.DOTALL))
            print(SpecGarage)
        except Exception as e:
            SpecGarage = 0

        # try:
        #     SpecDescription = response.xpath('//*[@id="ldp-detail-romance"]//text()').extract()
        #     SpecDescription = str(''.join(SpecDescription)).strip()
        #     SpecDescription = SpecDescription.replace("\n", "").replace("  ", "")
        # except Exception as e:
        #     print(e)

        # try:
        #     ElevationImage = response.xpath(
        #         '//*[@class="fsgallery-main owl-carousel ldp-photos "]//div[@class=""]//img//@data-src').extract()
        #     ElevationImage = "|".join(ElevationImage)
        #     SpecElevationImage = ElevationImage
        # except Exception as e:
        #     print(e)
        # if ElevationImage == "":
        #     try:
        #         ElevationImage = response.xpath(
        #             '//div[@class="sr_floor_plan"]//div/div/img/@src').extract()
        #         ElevationImage = "|".join(ElevationImage)
        #         SpecElevationImage = ElevationImage
        #     except Exception as e:
        #         print(e)

        try:
            SpecWebsite = response.url
        except Exception as e:
            print(e)

        # ----------------------- Don't change anything here ---------------- #
        item = BdxCrawlingItem_Spec()
        item['SpecNumber'] = SpecNumber
        item['PlanNumber'] = unique_number
        item['SpecStreet1'] = Address
        item['SpecCity'] = city
        item['SpecState'] = state
        item['SpecZIP'] = ZIP
        item['SpecCountry'] = SpecCountry
        item['SpecPrice'] = SpecPrice
        item['SpecSqft'] = SpecSqft
        item['SpecBaths'] = SpecBaths
        item['SpecHalfBaths'] = SpecHalfBaths
        item['SpecBedrooms'] = SpecBedrooms
        item['MasterBedLocation'] = MasterBedLocation
        item['SpecGarage'] = SpecGarage
        item['SpecDescription'] ='The Albany is a beautifully designed single level home by Eaglewood. It features large open spaces including a kitchen with 20 ceilings, custom cabinetry, and stone counter tops. The Albany has received recognition for "Best Master Suite" in the Parade of Homes. The master suite boasts huge windows and recessed ceilings in the bedroom and a luxurious bathroom with a soaker tub, large tiled shower, and stone top dual vanity. As always, the home is filled with all the spectacular details and high-quality finishes that Eaglewood is known for.'
        item['SpecElevationImage'] = "https://www.eaglewood.com/files/floor-plans/first-floors/FILE_5a4bd1c694869336354232.png"
        item['SpecWebsite'] = SpecWebsite
        yield item


# if __name__ == '__main__':
#         execute("scrapy crawl eaglewood".split())