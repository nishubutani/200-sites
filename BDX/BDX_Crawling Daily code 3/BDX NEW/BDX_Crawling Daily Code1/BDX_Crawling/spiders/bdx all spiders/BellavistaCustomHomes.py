

# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from scrapy.cmdline import execute
from scrapy.utils.response import open_in_browser

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class bellavistacustomehomesSpider(scrapy.Spider):
    name = 'bellavista_customhomes'
    allowed_domains = ['']
    # start_urls = ['https://bellavistacustomhomes.com/']
    start_urls = ['https://bellavistacustomhomes.com/communities/']
    builderNumber = 222316573167120933732921392763

    # def start_requests(self):
    #     link = 'https://bellavistacustomhomes.com/'
    #     yield scrapy.FormRequest(url=link,dont_filter=True,callback=self.parse)

    def parse(self, response):
        links = response.xpath('//div[@class="card"]/a/@href').extract()
        print(links)
        for link in links:
            yield scrapy.FormRequest(url=link, callback=self.communities,dont_filter="True")

    def communities(self, response):
      # ------------------- Creating Communities ---------------------- #
      #   subdivisonName = response.xpath('//div[@class="card-content-communities"]/h5[2]/text()').extract_first(default="")
        subdivisonName = response.xpath('//div[@class="col-sm-12 no-gutters"]/h1/text()').extract_first(default="")
        print(subdivisonName)


        subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)

        f = open("html/%s.html" % subdivisonNumber, "wb")
        f.write(response.body)
        f.close()

        contactTmp =  " ".join(response.xpath('//div[@class="margin-b-md"]/h4[@class="margin-b-none margin-t-md"]/text()').extract())
        # contactTmp = re.findall(r'(\d{1,}) [a-zA-Z0-9\s]+(\,)? [a-zA-Z]+(\,)? [a-zA-Z]+(\,)? [A-Z]{2} [0-9]{5,6}',contactTmp)
        print(contactTmp)
        # phoneNumber = '915-491-2056'
        # street1 = contactTmp[1]
        street1 = contactTmp.split(",")[0]
        print(street1)

        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionName'] = subdivisonName
        item2['SubdivisionNumber'] = subdivisonNumber
        item2['BuilderNumber'] = self.builderNumber
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 1
        item2['Street1'] = street1
        item2['City'] = contactTmp.split(",")[1]
        item2['State'] = contactTmp.split(",")[2].split(" ")[-2]
        item2['ZIP'] = contactTmp.split(",")[2].split(" ")[-1]
        item2['AreaCode'] = ''
        item2['Prefix'] = ''
        item2['Suffix'] = ''
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = response.xpath('//*[@id="tab1"]/div/ul/li[1]/p/text()').extract_first(default="")
        item2['SubImage'] = "https://bellavistacustomhomes.com/wp-content/uploads/2020/02/coming-soon.png"
        item2['SubWebsite'] = response.url
        item2['AmenityType'] = ''


        if item2['ZIP'] != "":
            yield item2

        url = 'https://bellavistacustomhomes.com/plans/'
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.parse_planlink)
                                 # meta={'sbdn': subdivisonNumber})

    def parse_planlink(self, response):
        # subdivisonNumber = response.meta['sbdn']
        try:
            links = response.xpath('//div[@class="card"]/a/@href').extract()
            print(links)
            # plandetains = {}
            for link in links:
              yield scrapy.Request(url=link,
                                   callback=self.plans_details,dont_filter=True)
        except Exception as e:
            print(e)


    def plans_details(self, response):
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = "1404 North Zaragoza Roa"
        item['City'] = "El Paso"
        item['State'] = "TX"
        item['ZIP'] = "79936"
        item['AreaCode'] = "915"
        item['Prefix'] = "491"
        item['Suffix'] = "2056"
        item['Extension'] = ""
        item['Email'] = "egarcia@bellavistaep.com"
        item['SubDescription'] = "Bella Vista Custom Homes was founded by Edgar Garcia in 2001. Edgar is a second generation builder of homes inspired by his father. A team of professionals at Bella Vista Custom Homes, Inc. is committed to design and construct distinguished custom homes that exceedingly satisfy your lifestyle and expectations for the best craftsmanship possible. We care deeply about your satisfaction throughout the entire planning and building process even after completion."
        item['SubImage'] = 'https://bellavistacustomhomes.com/wp-content/uploads/2020/02/bella-vista-custom-homes.png'
        item['SubWebsite'] = 'https://bellavistacustomhomes.com/'
        item['AmenityType'] =''
        yield item

        item = BdxCrawlingItem_Plan()
        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        # try:
        #     SubdivisionNumber = response.meta['sbdn']
        # except Exception as e:
        #     print(e)

        try:
            PlanName = response.xpath('//div[@class="col-sm-12 no-gutters"]/h1/text()').extract_first(default='').strip()
            print(PlanName)
        except Exception as e:
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
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
            Baths = response.xpath(
                '//div[@class="col-md-7 col-sm-12 col-xs-12 no-gutters margin-t-sm margin-b-sm"]/div[2]/h5[@class="info-icon-text text-center margin-t-lg"]/text()').extract_first(
                default='0').strip().replace(",", "")
            Baths = Baths.split(" ")[0]
            Baths = re.findall(r"(\d+)", Baths)
            Bath = Baths[0]
            print(Baths)
            if len(Baths) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
            item['HalfBaths'] = HalfBaths
        except Exception as e:
            print(e)

        try:

            Bedrooms = response.xpath('//div[@class="col-md-7 col-sm-12 col-xs-12 no-gutters margin-t-sm margin-b-sm"]/div[1]/h5[@class="info-icon-text text-center margin-t-lg"]/text()').extract_first(
                default='0').strip().replace(",", "")
            Bedrooms = Bedrooms.split(" ")[0]
            print(Bedrooms)
        except Exception as e:
            print(e)

        try:

            Garage = 0.0
            BaseSqft = response.xpath('//div[@class="col-md-7 col-sm-12 col-xs-12 no-gutters margin-t-sm margin-b-sm"]/div[4]/h5[@class="info-icon-text text-center margin-t-lg"]/text()').extract_first(default='0').strip().replace(",", "")
            BaseSqft = BaseSqft.split(" ")[0]
            print(BaseSqft)

        except Exception as e:
            print(e)

        try:
            Description="Bella Vista Custom Homes was founded by Edgar Garcia in 2001. Edgar is a second generation builder of homes inspired by his father. A team of professionals at Bella Vista Custom Homes, Inc. is committed to design and construct distinguished custom homes that exceedingly satisfy your lifestyle and expectations for the best craftsmanship possible. We care deeply about your satisfaction throughout the entire planning and building process even after completion."
            # Description="".join(response.xpath('//div[@class="row"]/div/div/div[1]/ul[@class="feature-table margin-t-sm"]/li/h6/text()').extract_first(default='').strip())
            print(Description)
        except Exception as e:
            Description=''

        try:
            images = ''
            image = "|".join(response.xpath('//div[@class="image-background image-large hide-medium"]/@style').extract())
            images = image.replace('background-image: url(', "").replace(')', "")
            ElevationImage = images
            print(ElevationImage)
        except Exception as e:
            ElevationImage = ''

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

        # SubdivisionNumber = SubdivisionNumber #if subdivision is there
        SubdivisionNumber = self.builderNumber #if subdivision is not available
        unique = str(PlanNumber)+str(SubdivisionNumber)
        print(unique)
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
        item['Baths'] = Bath
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = Description
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item

        url = "https://bellavistacustomhomes.com/homes/"
        yield scrapy.Request(url=url, callback=self.home_link, dont_filter=True)

    def home_link(self, response):

        try:
            links = response.xpath('//div[@class="card"]/a/@href').extract()
            # plandetains = {}
            for link in links:
                yield scrapy.Request(url=link,callback=self.HomesDetails,dont_filter=True)
        except Exception as e:
            print(e)

    def HomesDetails(self,response):

        unique = str("Plan Unknown") + str(self.builderNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        item2 = BdxCrawlingItem_Plan()
        item2['unique_number'] = unique_number
        item2['Type'] = "SingleFamily"
        item2['PlanNumber'] = "Plan Unknown"
        item2['SubdivisionNumber'] = self.builderNumber
        item2['PlanName'] = "Plan Unknown"
        item2['PlanNotAvailable'] = 1
        item2['PlanTypeName'] = 'Single Family'
        item2['BasePrice'] = 0
        item2['BaseSqft'] = 0
        item2['Baths'] = 0
        item2['HalfBaths'] = 0
        item2['Bedrooms'] = 0
        item2['Garage'] = 0
        item2['Description'] = ""
        item2['ElevationImage'] = ""
        item2['PlanWebsite'] = ""
        yield item2

        # PN = response.meta['PN']
        planName = response.xpath('//div[@class="col-sm-12 no-gutters"]/h2/text()').extract_first(default='').strip()
        print(planName)
        #
        # try:
        #     PlanNumber = PN[planName]
        # except Exception as e:
        #     print(e)

        # SpecStreet1 = response.meta['street']
        address = planName.split(",")[0]
        print(address)

        SpecCity = planName.split(",")[1]
        print(SpecCity)

        SpecState = planName.split(",")[2].strip()
        SpecState = SpecState.split(" ")[0].replace("Texas","TX")
        print(SpecState)

        SpecZIP = planName.split(",")[2].strip()
        SpecZIP = SpecZIP.split(" ")[1].strip()
        print(SpecZIP)

        SpecStreet1 = address

        try:
            unique1 = SpecStreet1 + SpecCity + SpecState + SpecZIP
            SpecNumber = int(hashlib.md5(bytes(unique1, "utf8")).hexdigest(), 16) % (10 ** 30)
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
            SpecPrice = response.xpath('//*[contains(text(),"Price")]/text()').extract_first().replace(",","")
            SpecPrice = re.findall(r"(\d+)", SpecPrice)[0]
        except Exception as e:
            print(e)

        try:
            SpecSqft =  response.xpath('//*[contains(text()," ft")]/text()').extract_first().replace(",","")
            SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
            print(SpecSqft)
        except Exception as e:
            print(e)

        try:
            SpecBaths = str(response.xpath('normalize-space(//*[contains(text(),"Bath")]/text())').extract_first(default='0').strip()).replace(",", "")
            tmp = re.findall(r"(\d+)", SpecBaths) [2]
            SpecBaths = tmp[0]
            if len(tmp) > 1:
                SpecHalfBaths = 1
            else:
                SpecHalfBaths = 0
        except Exception as e:
            print(e)

        try:
            SpecBedrooms = response.xpath('normalize-space(//*[contains(text(),"Bed")]/text())').extract_first()
            SpecBedrooms = re.findall(r'(\d+)',SpecBedrooms)[0]
        except Exception as e:
            print(e)

        try:
            MasterBedLocation = "Down"
        except Exception as e:
            print(e)

        try:
            SpecGarage = response.xpath('normalize-space(//*[contains(text(),"Garag")]/text())').extract_first(default='0')
            SpecGarage = re.findall(r"(\d+)", SpecGarage)[0]
        except Exception as e:
            print(e)
            SpecGarage = 0

        try:
            SpecDescription = "Bella Vista Custom Homes was founded by Edgar Garcia in 2001. Edgar is a second generation builder of homes inspired by his father. A team of professionals at Bella Vista Custom Homes, Inc. is committed to design and construct distinguished custom homes that exceedingly satisfy your lifestyle and expectations for the best craftsmanship possible. We care deeply about your satisfaction throughout the entire planning and building process even after completion."
        except Exception as e:
            print(e)

        try:
            ElevationImage = "|".join(response.xpath('//div[@class="image-background image-large carousel-img show-medium"]/@style').extract())
            ElevationImage = ElevationImage.replace("background-image: url(","").replace(");","")
            print(ElevationImage)
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
        item['PlanNumber'] = unique_number
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


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl bellavista_customhomes".split())


# Homes

        # url = "https://bellavistacustomhomes.com/homes/"
        # yield scrapy.Request(url=url, callback=self.home_link, meta={"PN": plandetails}, dont_filter=True)

    # def home_link(self, response):
    #
    #     try:
    #         links = response.xpath('//div[@class="card"]/a/@href').extract()
    #         plandetains = {}
    #         for link in links:
    #             yield scrapy.Request(url=self.start_urls[0]+ str(link),
    #                                  callback=self.HomesDetails,
    #                                  meta={'sbdn': self.builderNumber, 'PlanDetails': plandetains}, dont_filter=True)
    #     except Exception as e:
    #         print(e)

    # def HomesDetails(self,response):
    #     PN = response.meta['PN']
    #     planName = response.xpath('//div[@class="col-sm-12 no-gutters"]/h2/text()').extract_first(default='').strip()
    #     print(planName)
    #
    #     try:
    #         PlanNumber = PN[planName]
    #     except Exception as e:
    #         print(e)
    #
    #     SpecStreet1 = response.meta['street']
    #     address = response.meta['address'].split(',')
    #     SpecCity = address[0].strip()
    #     SpecState = address[-1].strip().split(' ')[0]
    #     SpecZIP = address[-1].strip().split(' ')[1]
    #
    #     try:
    #         unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
    #         SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
    #         f = open("html/%s.html" % SpecNumber, "wb")
    #         f.write(response.body)
    #         f.close()
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         SpecCountry = "USA"
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         SpecPrice = response.meta['price']
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         SpecSqft = ""
    #         # SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         SpecBaths = str(response.xpath('normalize-space(//*[contains(text(),"Bathrooms")]/following-sibling::text())').extract_first(default='0').strip()).replace(",", "")
    #         tmp = re.findall(r"(\d+)", SpecBaths)
    #         SpecBaths = tmp[0]
    #         if len(tmp) > 1:
    #             SpecHalfBaths = 1
    #         else:
    #             SpecHalfBaths = 0
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         SpecBedrooms = str(response.xpath('normalize-space(//*[contains(text(),"Bedrooms")]/following-sibling::text())').extract_first(default='0').strip()).replace(",", "")
    #         SpecBedrooms = re.findall(r'(\d+)',SpecBedrooms)[0]
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         MasterBedLocation = "Down"
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         SpecGarage = response.xpath('normalize-space(//*[contains(text(),"Garage")]/following-sibling::text())').extract_first(default='0')
    #         SpecGarage = re.findall(r"(\d+)", SpecGarage)[0]
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         SpecDescription = response.xpath('normalize-space(//*[@class="sn-133"]/div/p/text())').extract_first(default='').strip()
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         ElevationImage = '|'.join(response.urljoin(self.start_urls[0] + i) for i in response.xpath('//*[@class="sn-144"]/img/@src').extract())
    #         ElevationImage = ElevationImage + '|' + '|'.join(response.urljoin(self.start_urls[0] + i) for i in response.xpath('//*[@class="sn-156"]//a/@href').extract())
    #         SpecElevationImage = ElevationImage + '|' + '|'.join(response.urljoin(self.start_urls[0] + i) for i in response.xpath('//*[@class="zoomImg"]/@src').extract())
    #         SpecElevationImage = SpecElevationImage.strip('|')
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         SpecWebsite = response.url
    #     except Exception as e:
    #         print(e)
    #
    #         # ----------------------- Don't change anything here ---------------- #
    #     item = BdxCrawlingItem_Spec()
    #     item['SpecNumber'] = SpecNumber
    #     item['PlanNumber'] = PlanNumber
    #     item['SpecStreet1'] = SpecStreet1
    #     item['SpecCity'] = SpecCity
    #     item['SpecState'] = SpecState
    #     item['SpecZIP'] = SpecZIP
    #     item['SpecCountry'] = SpecCountry
    #     item['SpecPrice'] = SpecPrice
    #     item['SpecSqft'] = SpecSqft
    #     item['SpecBaths'] = SpecBaths
    #     item['SpecHalfBaths'] = SpecHalfBaths
    #     item['SpecBedrooms'] = SpecBedrooms
    #     item['MasterBedLocation'] = MasterBedLocation
    #     item['SpecGarage'] = SpecGarage
    #     item['SpecDescription'] = SpecDescription
    #     item['SpecElevationImage'] = SpecElevationImage
    #     item['SpecWebsite'] = SpecWebsite
    #     yield item
    #













# # -*- coding: utf-8 -*-
# import hashlib
# import re
# import scrapy
# from scrapy.utils.response import open_in_browser
# from scrapy.http import HtmlResponse
# import requests
# from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
#
#
# class blueribbonokSpider(scrapy.Spider):
#     name = 'BellavistaCustomHomes'
#     # allowed_domains = ['bellavistacustomhomes.com']
#     start_urls = ['http://www.bellavistacustomhomes.com/bella-vista-real-estate.html']
#     builderNumber = "222316573167120933732921392763"
#
#
#     def parse(self, response):
#
#         # IF you do not have Communities and you are creating the one
#         # --------------------------------------------------------------------------- If No communities found ------------------------------------------------------------------------------------------------ #
#
#         f = open("html/%s.html" % self.builderNumber, "wb")
#         f.write(response.body)
#         f.close()
#         try:
#             SubDescription = []
#             tmp_dscr = response.xpath('//div[@class="medium-18 large-centered columns"]//text()').extract()
#             for t in tmp_dscr:
#                 t = t.strip()
#                 pattern = re.compile(r'\r+\n+\s+')
#                 t = re.sub(pattern, '', t)
#                 if t:
#                     SubDescription.append(t)
#             SubDescription = ''.join(SubDescription)
#
#             item = BdxCrawlingItem_subdivision()
#             item['sub_Status'] = "Active"
#             item['SubdivisionNumber'] = ''
#             item['BuilderNumber'] = self.builderNumber
#             item['SubdivisionName'] = "No Sub Division"
#             item['BuildOnYourLot'] = 0
#             item['OutOfCommunity'] = 0
#             item['Street1'] = "1404 N. Zaragoza Ste. B"
#             item['City'] = " El Paso"
#             item['State'] = "TX"
#             item['ZIP'] = "79936"
#             item['AreaCode'] = '915'
#             item['Prefix'] = '491'
#             item['Suffix'] = '2056'
#             item['Extension'] = ""
#             item['Email'] = "griselortega.bellavista@yahoo.com"
#             item['SubDescription'] = SubDescription
#
#             res = requests.get('http://www.bellavistacustomhomes.com/index.html')
#             response = HtmlResponse(url='xyz.com',body=res.content)
#             print(response)
#             images = re.findall(r'<div><img alt="custom houses,custom home designs,custom homes for sale" src="(.*?)" /></div>',response.text)
#             a = []
#             for i in images:
#                 image = 'http://www.bellavistacustomhomes.com' + i.replace('.','').replace('jpg','.jpg')
#                 a.append(image)
#             b = '|'.join(a)
#
#             item['SubImage'] = b
#             item['SubWebsite'] = response.url
#             yield item
#
#         except Exception as e:
#             print("Problem in Community :",e)
#
#
#         try:
#             item = BdxCrawlingItem_Plan()
#             unique = str("Plan Unknown") + str(self.builderNumber)
#             unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
#             item['unique_number'] = unique_number
#             item['Type'] = "SingleFamily"
#             item['PlanNumber'] = "Plan Unknown"
#             item['SubdivisionNumber'] = self.builderNumber
#             item['PlanName'] = "Plan Unknown"
#             item['PlanNotAvailable'] = 1
#             item['PlanTypeName'] = "Single Family"
#             item['BasePrice'] = 0
#             item['BaseSqft'] = 0
#             item['Baths'] = 0
#             item['HalfBaths'] = 0
#             item['Bedrooms'] = 0
#             item['Garage'] = 0
#             item['Description'] = ""
#             item['ElevationImage'] = ""
#             item['PlanWebsite'] = ""
#             yield item
#
#         except Exception as e:
#             print("Problem in Unknown Plan creation:", e)
#
# from scrapy.cmdline import execute
# execute("scrapy crawl BellavistaCustomHomes".split())