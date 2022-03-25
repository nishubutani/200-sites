import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class Hilmann_Home_BuildingSpider(scrapy.Spider):
    name = 'Hilmann_Home_Building'
    allowed_domains = []
    start_urls = ['http://www.hilmannhomebuilding.com/subdivisions/default.aspx']
    builderNumber = 49298

    def parse(self, response):
        community_links = response.xpath('//*[@class="capsule col-sm-6 col-md-4 subdivisions-clear"]/div[2]/h3/a/@href').extract()
        for community_link in community_links:
            link = 'http://www.hilmannhomebuilding.com/subdivisions/'+str(community_link)
            print(link)
            yield scrapy.FormRequest(url=link,callback=self.communityDetail)

    def communityDetail(self,response):
        subdivisonName = response.xpath('//*[@class="col-sm-6"]/h2/span/text()').extract_first(default="")
        subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)

        f = open("html/%s.html" % subdivisonNumber, "wb")
        f.write(response.body)
        f.close()

        contactTmp = response.xpath('//*[@class="entry-content"]//address//text()').extract()
        street = response.xpath('//*[@class="col-sm-6"]/h4/text()').extract_first()
        street1 = street.split(',')[0]
        city = street.split(',')[1]
        add2 = street.split(',')[2]
        state = add2.split(' ')[-2]
        zip = add2.split(' ')[-1]

        try:
            Image = []
            Images = response.xpath('//*[@class="col-sm-6"][2]//a/img/@src').getall()
            for i in Images:
                Imag = 'http://www.hilmannhomebuilding.com'+str(i)
                Image.append(Imag)
            Image = '|'.join(Image)
        except Exception as e:
            Image = ""


        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionName'] = subdivisonName
        item2['SubdivisionNumber'] = subdivisonNumber
        item2['BuilderNumber'] = self.builderNumber
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 1
        item2['Street1'] = street1
        item2['City'] = city
        item2['State'] = state
        item2['ZIP'] = zip
        item2['AreaCode'] = '913'
        item2['Prefix'] = '940'
        item2['Suffix'] = '2220'
        item2['Extension'] = ""
        item2['Email'] = "lindsay@lecontecompanies.com"
        item2['SubDescription'] = ''.join(response.xpath('//*[@class="col-sm-6"]/p/text()').extract_first(default=""))
        item2['SubImage'] = Image
        item2['SubWebsite'] = response.url
        item2['AmenityType'] = ""
        yield item2

        plan_link ='http://www.hilmannhomebuilding.com/floorplans/default.aspx'
        yield scrapy.FormRequest(url=plan_link,callback=self.PlanDetail,meta={'SubdivisionNumber':subdivisonNumber})

    def PlanDetail(self,response):
        SubdivisionNumber = response.meta['SubdivisionNumber']
        links = response.xpath('//*[@class="thumbnail"]/@href').extract()
        for l1 in links:
            link = 'http://www.hilmannhomebuilding.com/floorplans/'+str(l1)
            yield scrapy.FormRequest(url=str(link),callback=self.plan_detail,meta={'SubdivisionNumber':SubdivisionNumber})

    def plan_detail(self,response):

        try:
            Image = []
            Images = response.xpath('//*[@class="col-sm-6"][2]//a/img/@src').getall()
            for i in Images:
                Imag = 'http://www.hilmannhomebuilding.com' + str(i)
                Image.append(Imag)
            Image = '|'.join(Image)
        except Exception as e:
            Image = ""

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = self.builderNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = 'PO Box 860526'
        item['City'] = 'Shawnee'
        item['State'] = 'KS'
        item['ZIP'] = '66286'
        item['AreaCode'] = '913'
        item['Prefix'] = '940'
        item['Suffix'] = '2220'
        item['Extension'] = ""
        item['Email'] = 'lindsay@lecontecompanies.com'
        item['SubDescription'] = "For the discriminating client, Hilmann is the answer to your search for a homebuilder that is dedicated to nurturing every aspect of the construction of your home. We provide direct personal involvement and commitment on each and every project. Furthermore, you can feel confident that your new home has been personally supervised by us to insure quality throughout. Supported by a team of experienced professionals, we are committed to making your homebuilding experience a pleasant and rewarding one. After all, not only is it a financial investment, but a personal one as well and we're determined to making it one you can be very proud of."
        item['SubImage'] = Image
        item['SubWebsite'] = response.url
        item['AmenityType'] = ""
        yield item

        SubdivisionNumber = self.builderNumber
        try:
            PlanName = response.xpath('//div[@class="col-sm-6"]/h2/text()').extract_first()
            print(PlanName)
        except Exception as e:
            print("PlanName ",e)

        try:
            PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % PlanNumber, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
            print(e)

        try:
            BasePrice = 0
        except Exception as e:
            BasePrice = 0
        try:
            BaseSqft = response.xpath('//div[@class="col-sm-6"]/h4[2]/text()').extract_first()
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
            print(BaseSqft)
        except Exception as e:
            BaseSqft = 0

        try:
            Bedrooms = response.xpath('//*[contains(text(),"Bedrooms:")]/../../td[2]/text()').extract_first()
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            print(Bedrooms)
        except Exception as e:
            Bedrooms = 0

        try:
            Baths = response.xpath('//*[contains(text(),"Bathrooms:")]/../../td[2]/text()').extract_first()
            tmp = re.findall(r"(\d+)", Baths)
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
            Garage = response.xpath('//*[contains(text(),"Garages:")]/../../td[2]/text()').extract_first()
            Garage = re.findall(r"(\d+)", Garage)[0]
            print(Garage)
        except Exception as e:
            Garage = 0



        try:
            ElevationImage = []
            ElevationImages = response.xpath('//*[@class="col-sm-6"][2]//a/img/@src').getall()
            for i in ElevationImages:
                ElevationImag = 'http://www.hilmannhomebuilding.com'+str(i)
                ElevationImage.append(ElevationImag)
            ElevationImage = '|'.join(ElevationImage)
        except Exception as e:
            ElevationImage = ""

        # PlanNumber = int(hashlib.md5(bytes(str(PlanName), "utf8")).hexdigest(), 16) % (10 ** 30)
        # unique = str(PlanNumber) + str(SubdivisionNumber)
        # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

        SubdivisionNumber = SubdivisionNumber
        unique = str(PlanNumber)+str(SubdivisionNumber)
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
        item['Description'] = ''.join(response.xpath('//div[@class="col-sm-6"]/p/text()').getall())#"Our goal is simple; to get you into a home that is well built, reliable and affordable.A home you will love and want to show off to your friends and family. There is a big difference between a house and your home. Allow us to show you that difference. At Better Built Homes, we do just what our name implies, and we do it with honesty, integrity and an old-fashioned sense of pride in what we do. With 20 years’ experience in the homebuilding industry, you can count on owner Chuck Burt to build the house of your dreams."
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = response.url
        yield item

    #     home_link = 'http://www.hilmannhomebuilding.com/homesforsale/default.aspx'
    #     yield scrapy.FormRequest(url=home_link,callback=self.all_home,meta={'PlanNumber':unique_number})
    #
    #
    # def all_home(self,response):
    #     PlanNumber = response.meta['PlanNumber']
    #     links = response.xpath('//div[@class="home-loop"]').getall()
    #     for link in links:
    #         if '<h3 class="sold">SOLD</h3>' not in link:
    #             url1 = "http://www.hilmannhomebuilding.com/homesforsale/"
    #             url = str(url1) + re.findall(' <a class="thumbnail" href="(.*?)"',link)[0]
    #             # url = "http://www.hilmannhomebuilding.com/homesforsale/listingDetails.aspx?homeID=260&"
    #             yield scrapy.FormRequest(url=url,dont_filter=True,callback=self.home_detail,meta={'PlanNumber':PlanNumber})
    #
    # def home_detail(self, response):
    #     unique = str("Plan Unknown") + str(self.builderNumber)
    #     unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
    #     item = BdxCrawlingItem_Plan()
    #     item['unique_number'] = unique_number
    #     item['Type'] = "SingleFamily"
    #     item['PlanNumber'] = "Plan_Unknown"
    #     item['SubdivisionNumber'] = self.builderNumber
    #     item['PlanName'] = "Plan Unknown"
    #     item['PlanNotAvailable'] = 1
    #     item['PlanTypeName'] = "Single Family"
    #     item['BasePrice'] = 0
    #     item['BaseSqft'] = 0
    #     item['Baths'] = 0
    #     item['HalfBaths'] = 0
    #     item['Bedrooms'] = 0
    #     item['Garage'] = 0
    #     item['Description'] = ""
    #     item['ElevationImage'] = ""
    #     item['PlanWebsite'] = ""
    #     item['AmenityType'] = ''
    #     yield item
    #
    #     PlanNumber = unique_number
    #
    #     SpecStreet1 = response.xpath('//div[@class="col-sm-6"]/h2/text()').get()
    #     if '*Price To Be Determined*' in SpecStreet1:
    #         pass
    #     else:
    #         add = response.xpath('//div[@class="col-sm-6"]/h4[1]/text()').get()
    #         add2 = add.split(',')[1]
    #
    #         try:
    #             SpecCity = add.split(',')[0]
    #         except Exception as e:
    #             print(str(e))
    #         try:
    #             SpecState = add2.split(' ')[-2]
    #         except Exception as e:
    #             print(str(e))
    #
    #         try:
    #             SpecZIP = add2.split(' ')[-1]
    #         except Exception as e:
    #             print(str(e))
    #
    #         unique = SpecStreet1 + SpecCity + SpecState + SpecZIP + str(response.url)
    #         SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
    #
    #
    #         try:
    #             SpecPrice = response.xpath('//div[@class="col-sm-6"]/h4[2]/text()').get().replace('$','').replace(',','').split('.')[0]
    #         except Exception as e:
    #             print(e)
    #             SpecPrice = 0
    #
    #         try:
    #             SpecSqft = response.xpath('//div[@class="col-sm-6"]/h4[3]/text()').get().replace('ft','').strip()
    #         except Exception as e:
    #             SpecSqft = 0
    #
    #         try:
    #             SpecBaths = response.xpath('//strong[contains(text(),"Bathrooms:")]/../following-sibling::td[1]/text()').get()
    #             Bath = re.findall(r"(\d+)", SpecBaths)
    #             SpecBaths = Bath[0]
    #             tmp = Bath
    #             if len(tmp) > 1:
    #                 SpecHalfBaths = 1
    #             else:
    #                 SpecHalfBaths = 0
    #
    #         except Exception as e:
    #             print(e)
    #
    #
    #         try:
    #             SpecBedrooms = response.xpath('//strong[contains(text(),"Bedrooms:")]/../following-sibling::td[1]/text()').get()
    #         except Exception as e:
    #             SpecBedrooms = 0
    #
    #
    #
    #         try:
    #             SpecGarage = response.xpath('//strong[contains(text(),"Garages:")]/../following-sibling::td[1]/text()').get()
    #         except Exception as e:
    #             SpecGarage = 0
    #
    #         try:
    #             SpecDescription = response.xpath('//div[@class="col-sm-6"]/p/text()').get()
    #         except Exception as e:
    #             SpecDescription = ''
    #
    #         try:
    #             image=[]
    #             SpecElevationImage1 = response.xpath('//div[@class="col-sm-6"][2]//img/@src').getall()
    #             for im in SpecElevationImage1:
    #                 image.append("http://www.hilmannhomebuilding.com"+im)
    #             # SpecElevationImage2 = "http://www.hilmannhomebuilding.com"
    #             SpecElevationImage = '|'.join(image)
    #         except Exception as e:
    #             SpecElevationImage = ""
    #
    #         try:
    #             SpecWebsite = response.url
    #         except Exception as e:
    #             print(e)
    #
    #         try:
    #
    #             item = BdxCrawlingItem_Spec()
    #             item['SpecNumber'] = SpecNumber
    #             item['PlanNumber'] = PlanNumber
    #             item['SpecStreet1'] = SpecStreet1
    #             item['SpecCity'] = SpecCity
    #             item['SpecState'] = SpecState
    #             item['SpecZIP'] = SpecZIP
    #             item['SpecCountry'] = "USA"
    #             item['SpecPrice'] = SpecPrice
    #             item['SpecSqft'] = SpecSqft
    #             item['SpecBaths'] = SpecBaths
    #             item['SpecHalfBaths'] = SpecHalfBaths
    #             item['SpecBedrooms'] = SpecBedrooms
    #             item['MasterBedLocation'] = "Down"
    #             item['SpecGarage'] = SpecGarage
    #             item['SpecDescription'] = SpecDescription
    #             item['SpecElevationImage'] =  SpecElevationImage
    #             item['SpecWebsite'] = SpecWebsite
    #             yield item
    #         except:
    #             print("Home")

# execute("scrapy crawl Hilmann_Home_Building".split())


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl Hilmann_Home_Building".split())