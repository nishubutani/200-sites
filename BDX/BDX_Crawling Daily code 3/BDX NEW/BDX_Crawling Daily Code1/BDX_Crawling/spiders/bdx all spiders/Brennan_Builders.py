# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from lxml import html
from scrapy.utils.response import open_in_browser
import requests

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class BrennanBuildersSpider(scrapy.Spider):
    name = 'Brennan_Builders'
    allowed_domains = []
    start_urls = ['https://www.brennanhomes.com/new-homes/']
    builderNumber = 56819

    def parse(self, response):
        community_links = response.xpath('//*[@class="card home-card location-card h-100 white-bg trans oi-map-item location-map-item"]/a/@href').extract()
        for i in community_links:
            links = 'https://www.brennanhomes.com'+str(i)
            print("Communities------------->",links)
            yield scrapy.FormRequest(url=links, callback=self.property_details)

    def property_details(self, response):
        # ------------------- Creating Communities --------------------- #
        try:
            subdivisonName = response.xpath('//*[@class="col-12 col-sm-6 text-primary text-center text-sm-left"]/h3/text()').extract_first()
            subdivisonNumber = int(hashlib.md5(bytes(str(subdivisonName) + str(self.builderNumber), "utf8")).hexdigest(), 16) % (10 ** 30)
            # print(subdivisonNumber)
        except Exception as e:
            print(e)

        f = open("html/%s.html" % subdivisonNumber, "wb")
        f.write(response.body)
        f.close()
        try:
            ElevationImage = '|'.join(response.xpath('//*[@data-fancybox="photos"]//@href').extract()) #//*[@class="oi-aspect-img"]/@src
        except Exception as e:
            print(str(e))
        Street1 = response.xpath('//*[@id="lsp-details"]/div/div/div[1]/p[1]/text()').extract_first()
        a = response.xpath('//*[@class="col-12 col-sm-6 text-primary text-center text-sm-left"]/h6/text()').extract_first()
        City = a.split(',')[0]
        if response.url == 'https://www.brennanhomes.com/new-homes/pa/harmony/harmony-place/5514/':
            SubDescription = ''.join(response.xpath('//div[@class="wysiwyg pb-3"]//span//text()').extract())
        else:
            SubDescription = ''.join(response.xpath('//*[@class="wysiwyg pb-3"]//text()').extract())


        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionName'] = subdivisonName
        item['SubdivisionNumber'] = subdivisonNumber
        item['BuilderNumber'] = self.builderNumber
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 1
        item['Street1'] = Street1
        item['City'] = City
        item['State'] = 'PA'
        item['ZIP'] = '16001'
        item['AreaCode'] = '724'
        item['Prefix'] = '908'
        item['Suffix'] = '4140'
        item['Extension'] = ""
        item['Email'] = "sales@brennanhomes.com"
        item['SubDescription'] = SubDescription
        item['SubImage'] = ElevationImage
        item['SubWebsite'] = response.url
        a = []
        aminity = ''.join(response.xpath('//h5//..//ul//li//text()').extract()).replace('Walking trails','Trails').replace('Swimming Pool','Pool')
        # print(aminity)
        # if aminity == '':
        #     aminity = ''.join(response.xpath('//*[@class="fusion-li-item"]//div//p//text()').extract()[5:])

        # aminity = ''.join(response.xpath('//*[@class="ll-features-content__half right col-md-1of2"]/ul[1]/li/text()').extract())
        # try:
        #     aminity = ''.join(response.xpath(
        #         '//*[@class="heading icon-left"]//text()|//*[@class="fusion-li-item"]//div//p//text()[5:]').extract())
        # except Exception as e:
        #     print(e)

        amenity_list = ["Pool", "Playground", "GolfCourse", "Tennis", "Soccer", "Volleyball", "Basketball",
                        "Baseball", "Views", "Lake", "Pond", "Marina", "Beach", "WaterfrontLots", "Park",
                        "Trails", "Greenbelt", "Clubhouse", "CommunityCenter"]
        for i in amenity_list:
            if i in aminity:
                a.append(i)
        ab = '|'.join(a)
        item['AmenityType'] = ab
        yield item

        urls = response.xpath('//*[@aria-labelledby="plans-tab"]//a[@class="btn btn-sm btn-highlight my-3"]/@href').extract()
        for i in urls:
            url = 'https://www.brennanhomes.com'+str(i)
            print("Plans----------------------->",url)
            yield scrapy.FormRequest(url=url,dont_filter=True,callback=self.Plans_Details, meta={'sbdn': subdivisonNumber,'sname':subdivisonName})

    def Plans_Details(self,response):

        if response.meta['sname'] == 'Duffy Highlands':

            try:
                PlanNumber = int(hashlib.md5(bytes('Unknown Plan', "utf8")).hexdigest(), 16) % (10 ** 30)
            except Exception as e:
                PlanNumber = ''
                print(e)
            try:
                UniqNumber = int(hashlib.md5(bytes(str(PlanNumber), "utf8")).hexdigest(), 16) % (10 ** 30)
            except Exception as e:
                UniqNumber = ''
                print(e)

            # '713476943738426116626858005105'

            unique = str("Plan Unknown") + str(self.builderNumber)  # < -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
                        10 ** 30)  # < -------- Changes here
            item2 = BdxCrawlingItem_Plan()
            item2['unique_number'] = unique_number
            item2['Type'] = "SingleFamily"
            item2['PlanNumber'] = "Plan Unknown"
            item2['SubdivisionNumber'] = '713476943738426116626858005105'
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


    #
    #     print(response.meta['sname'])
    #     try:
    #         Type = 'SingleFamily'
    #     except Exception as e:
    #         print(e)
    #     try:
    #         PlanName = response.xpath('//*[@class="m-md-0"]/text()').extract_first().strip()
    #     except Exception as e:
    #         print(e)
    #     try:
    #         PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         SubdivisionNumber = response.meta['sbdn']
    #         # print(SubdivisionNumber)
    #     except Exception as e:
    #         print(str(e))
    #
    #     try:
    #         PlanNotAvailable = 0
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         PlanTypeName = response.xpath('//*[@class="col-12 col-md-5 text-md-right"]/p[1]/text()').extract_first()
    #     except:
    #         PlanTypeName = 'Single Family'
    #
    #
    #     try:
    #         BasePrice = response.xpath('//*[@class="h5 bold m-0"]/text()').extract_first().replace('From','')
    #         BasePrice = BasePrice.replace('$', '')
    #         BasePrice = re.sub(',', '', BasePrice)
    #         BasePrice = BasePrice.strip()
    #         # print(BasePrice)
    #     except Exception as e:
    #         print(str(e))
    #
    #
    #     try:
    #         PlanWebsite = response.url
    #     except Exception as e:
    #         print(e)
    #
    #
    #     a=response.xpath('//span[@class="bold"]//text()').extract()
    #     Bedrooms = a[0]
    #
    #     Baths = a[3]
    #     Bath = re.findall(r"(\d+)", Baths)
    #     Baths = Bath[0]
    #     tmp = Bath
    #     if len(tmp) > 1:
    #         HalfBaths = 1
    #     else:
    #         HalfBaths = 0
    #
    #     Garage = a[-1]
    #     Garage = re.findall(r"(\d+)", Garage)
    #     Garage = Garage[0]
    #     # print(Garage)
    #     BaseSqft = ''.join(a[1]).replace(',','')
    #     # print(BaseSqft)
    #
    #     try:
    #         Description = ''.join(response.xpath('//*[@class="wysiwyg pb-3"]//text()').extract()).strip().replace('\\x80','').replace('\\xE2','').replace('\\xB2','')
    #     except:
    #         Description = ''
    #
    #     try:
    #         # Image = []
    #         img = response.xpath('//*[@data-fancybox="photos"]//@href').extract()
    #         img1 = response.xpath('//*[@class="d-none"]//@src').extract()
    #         for i in img1:
    #             img.append(i)
    #         Images = '|'.join(img)
    #
    #
    #         ElevationImage = Images
    #         # print(ElevationImage)
    #     except Exception as e:
    #         print(str(e))
    #
    #     unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
    #     unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
    #     item = BdxCrawlingItem_Plan()
    #     item['Type'] = Type
    #     item['PlanNumber'] = PlanNumber
    #     item['unique_number'] = unique_number  # < -------- Changes here
    #     item['SubdivisionNumber'] = SubdivisionNumber
    #     item['PlanName'] = PlanName
    #     item['PlanNotAvailable'] = PlanNotAvailable
    #     item['PlanTypeName'] = PlanTypeName
    #     item['BasePrice'] = BasePrice
    #     item['BaseSqft'] = BaseSqft
    #     item['Baths'] = Baths
    #     item['HalfBaths'] = HalfBaths
    #     item['Bedrooms'] = Bedrooms
    #     item['Garage'] = Garage
    #     item['Description'] = Description
    #     item['ElevationImage'] = ElevationImage
    #     item['PlanWebsite'] = PlanWebsite
    #     yield item
    #
    #     #---------------------fake plan for homes------------------------
    #
    #
    #
    #
    #     links= response.xpath('//*[@class="row justify-content-center"]//a[@class="btn btn-sm btn-highlight my-3"]/@href').extract()
    #     for i in links:
    #         link = 'https://www.brennanhomes.com/'+str(i)
    #         print("Homes------------------------>",link)
    #         yield scrapy.Request(url=link, callback=self.home_details, meta={'PN': unique_number})
    #
    # def home_details(self, response):
    #
    #     try:
    #         address = response.xpath('//*[@class="sans-header bold"]/text()').extract_first()
    #         add = address.split(',')
    #         SpecStreet1 = add[0]
    #         SpecCity = add[1]
    #         # print(SpecCity)
    #
    #         SpecState = 'PA'
    #         zip=add[-1]
    #         SpecZIP = ''.join(re.findall(r"(\d+)", zip))
    #         # print(SpecZIP)
    #
    #         unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
    #         # print(unique)
    #         SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
    #
    #         f = open("html/%s.html" % SpecNumber, "wb")
    #         f.write(response.body)
    #         f.close()
    #
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         PlanNumber = response.meta['PN']
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         SpecCountry = "USA"
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         SpecPrice = response.xpath('//*[@class="h5 bold m-0"]/text()').extract_first().replace('From','')
    #         SpecPrice = SpecPrice.replace('$', '')
    #         SpecPrice = re.sub(',', '', SpecPrice)
    #         SpecPrice = SpecPrice.strip()
    #         # print(SpecPrice)
    #     except Exception as e:
    #         print(str(e))
    #     a = response.xpath('//span[@class="bold"]//text()').extract()
    #     try:
    #         SpecBedrooms = a[0]
    #         # print(SpecBedrooms)
    #     except Exception as e:
    #         print(str(e))
    #
    #     try:
    #         SpecBath = a[3]
    #         SpecBaths = re.findall(r"(\d+)", SpecBath)
    #         SpecBaths = SpecBaths[0]
    #         tmp = SpecBath
    #         if len(tmp) > 1:
    #             SpecHalfBaths = 1
    #         else:
    #             SpecHalfBaths = 0
    #         # print(SpecBaths)
    #     except Exception as e:
    #         print(str(e))
    #
    #     try:
    #         SpecGarage = a[5]
    #         SpecGarage = re.findall(r"(\d+)", SpecGarage)
    #     except Exception as e:
    #         print(str(e))
    #
    #     try:
    #
    #         SpecSqft =  a[1]
    #
    #     except Exception as e:
    #         print(str(e))
    #
    #     try:
    #         MasterBedLocation = "Down"
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         SpecDescription = ''.join(response.xpath('//*[@class="wysiwyg pb-3"]//text()').extract_first()).strip()
    #
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         # img = '|'.join(response.xpath('//*[@data-fancybox="photos"]//@href').extract())
    #         # img1 = '|'.join(response.xpath('//*[@class="d-none"]//@src').extract())
    #         # Image = img + img1
    #         # ElevationImage = '|'.join(Image)
    #         ElevationImage = '|'.join(response.xpath('//*[@class="row no-gutters"]//img/@src').extract())
    #
    #     except Exception as e:
    #         print(str(e))
    #
    #     try:
    #         SpecWebsite = response.url
    #     except Exception as e:
    #         print(e)
    #
    #     # ----------------------- Don't change anything here --------------------- #
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
    #     item['SpecElevationImage'] =ElevationImage
    #     item['SpecWebsite'] = SpecWebsite
    #     yield item
    #

if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute('scrapy crawl Brennan_Builders'.split())