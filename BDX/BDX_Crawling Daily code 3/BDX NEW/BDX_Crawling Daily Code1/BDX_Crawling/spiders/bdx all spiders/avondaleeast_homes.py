# -*- coding: utf-8 -*-
import hashlib
import json
import os
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'avondaleeast_homes'
    # allowed_domains = ['https://avondaleeast.com/']
    # start_urls = ['https://www.avondaleeast.com']

    builderNumber = "62842"


    def start_requests(self):
        link = 'https://avondaleeast.com/gallery/'
        yield scrapy.FormRequest(url=link,callback=self.parse,dont_filter=True)

    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()


        images = ''
        image = response.xpath('//div[@class="et_pb_gallery_image landscape"]/a/@href').extract()
        for i in image:
            images = images + i + '|'
        images = images.strip('|')

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '219 GROVE MILL LANE'
        item['City'] = 'AVONDALE ESTATES'
        item['State'] = 'GA'
        item['ZIP'] = '30002'
        item['AreaCode'] = '678'
        item['Prefix'] ='561'
        item['Suffix'] = '0466'
        item['Extension'] = ""
        item['Email'] = 'AVONDALEEAST@EVATLANTA.COM'
        item['SubDescription'] = 'Welcome home to a space you can call your own, woven into the fabrics of the Avondale Estates neighborhood. From local green spaces and craft food and beverage junctions to the close-knit community and means of connectivity, Avondale East represents an exclusive opportunity to live your now and craft your forever in a neighborhood specially designed to accommodate your lifestyle.'
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'https://avondaleeast.com/floorplans/'
        yield scrapy.FormRequest(url=link, callback=self.parse2, dont_filter=True)

    def parse2(self, response):
        divs = response.xpath('//div[@class="et_pb_section et_pb_section_1 et_section_regular"]/div/div')
        for div in divs:

            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                PlanName = div.xpath('.//h1/text()').get()
            except Exception as e:
                print(e)
                PlanName = ''


            try:
                PlanNumber = int(hashlib.md5(bytes(PlanName + response.url, "utf8")).hexdigest(), 16) % (
                        10 ** 30)
            except Exception as e:
                print(e)
                PlanNumber = ''


            try:
                SubdivisionNumber = self.builderNumber
                print(SubdivisionNumber)
            except Exception as e:
                SubdivisionNumber = ''
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
                BasePrice = 0
            except Exception as e:
                print(e)

            try:
                sqft = div.xpath(".//h1/../div/p/text()[1]").extract_first('')
                sqft = sqft.split("|")[0]
                sqft = sqft.replace(',', '').strip()
                BaseSqft = re.findall(r"(\d+)", sqft)[0]

            except Exception as e:
                print(e)
                BaseSqft = 0

            try:
                bath = div.xpath(".//h1/../div/p/text()[1]").extract_first()
                bath = bath.split("|")[2]
                if '-' in bath:
                    bath = bath.split("-")[1]
                tmp = re.findall(r"(\d+)", bath)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                print(e)

            try:
                Bedrooms = div.xpath(".//h1/../div/p/text()[1]").extract_first()
                Bedrooms = Bedrooms.split("|")[1].split("|")[0]
                if '-' in Bedrooms:
                    Bedrooms = Bedrooms.split("-")[1]
                Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            except Exception as e:
                print(e)

            try:
                Garage = 0
            except Exception as e:
                Garage = 0
                print(e)

            try:
                # Description ='Welcome home to a space you can call your own, woven into the fabrics of the Avondale Estates neighborhood. From local green spaces and craft food and beverage junctions to the close-knit community and means of connectivity, Avondale East represents an exclusive opportunity to live your now and craft your forever in a neighborhood specially designed to accommodate your lifestyle.'
                Description =''
            except Exception as e:
                print(e)

            try:
                images = []
                imagedata = div.xpath(".//span/img/@src").extract_first()
                # for id in imagedata:
                #     id = id
                # images.append(id)
                ElevationImage = imagedata
            except Exception as e:
                print(e)

            try:
                PlanWebsite = response.url
            except Exception as e:
                print(e)

                # ----------------------- Don't change anything here --------------
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
            item['Description'] = Description
            item['ElevationImage'] = ElevationImage
            item['PlanWebsite'] = PlanWebsite
            yield item

        item2 = BdxCrawlingItem_Plan()
        unique = str("Plan Unknown") + str(self.builderNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item2['unique_number'] = unique_number
        item2['Type'] = "SingleFamily"
        item2['PlanNumber'] = "Plan Unknown"
        item2['SubdivisionNumber'] = self.builderNumber
        item2['PlanName'] = "Plan Unknown"
        item2['PlanNotAvailable'] = 1
        item2['PlanTypeName'] = "Single Family"
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

        filename = 'D:\\nishant\\bdx\\april\\'
        files = os.walk(filename)
        for file in files:
            temp = file[2]
            for t in temp:
                print(t)
                with open(filename + t, "rb") as f:
                    text = f.read()
                    response = HtmlResponse(url='a.com', body=text)


                    #
                    #         yield scrapy.FormRequest(url=link,callback=self.home_link,dont_filter=True,meta={'PlanNumber':item2['unique_number']})
                    #
                    # def home_link(self,response):
                    #
                    #     PlanNumber = response.meta['PlanNumber']
                    links = response.xpath('//a[@class="sidx-content-overlay"]/@href').extract()
                    for link in links:
                        link =  link
                        yield scrapy.FormRequest(url=link,callback=self.home,dont_filter=True,meta={'PlanNumber':unique_number})
                        # yield scrapy.FormRequest(url='https://avondaleeast.com/properties/listing/fmls/6834769/Avondale-Estates/241-3rd-Avenue',callback=self.home,dont_filter=True,meta={'PlanNumber':unique_number})
#
    #
    def home(self,response):
        PlanNumber = response.meta['PlanNumber']
        Spec = ''.join(response.xpath('//div[@class="sidx-listing-heading"]/h1/div[1]/text()[1]').extract()).strip()
        SpecStreet1 = Spec
        try:
            SpecPrice = ''.join(
                response.xpath('//div[@class="sidx-price"]/text()').extract()).replace(',',
                                                                                                                   '').replace(
                '$', '').strip()
        except Exception as e:
            print("SpecPrice---------->", e)

        try:
            ci = ''.join(response.xpath('//div[@class="sidx-listing-heading"]/h1/div[@class="sidx-address-2"]/text()[1]').extract())
            cty = ci.strip()
            city = cty
        except Exception as e:
            city = ''
            print(e)



        state = response.xpath('//div[@class="sidx-listing-heading"]/h1/div[@class="sidx-address-2"]/text()[3]').extract_first()

        try:
            zi = ''.join(response.xpath('//div[@class="sidx-listing-heading"]/h1/div[@class="sidx-address-2"]/text()[5]').extract()).strip()
            zip = zi
        except Exception as e:
            zip = ''
            print(e)
        unique = SpecStreet1 + city + state + zip
        # print(unique)
        SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

        try:
            SpecSqft = response.xpath(
                '//div[contains(text(),"SqFt")]/../text()').extract_first().replace(',','')
        except Exception as e:
            print("SpecSqft---------->", e)


        try:
            SpecBaths = response.xpath('//div[contains(text(),"Full Baths")]/../text()|//div[contains(text(),"Total Baths")]/../div[@class="sidx-val"]/span/text()').extract_first().strip()

        except Exception as e:
            print("SpecBaths--------->", e)

        try:
            SpecHalfBaths = response.xpath('//div[contains(text(),"Partial Bath")]/../text()|//div[contains(text(),"Partial Bath")]/../div[@class="sidx-val"]/span/text()').extract_first('').strip()
            SpecHalfBaths = re.findall(r"(\d+)", SpecHalfBaths)[0]


        except Exception as e:
            print("SSpecHalfBaths--------->", e)
            SpecHalfBaths = ''


        SpecBedrooms = ''.join(response.xpath(
            '//div[contains(text(),"Beds")]/../text()').extract()).strip()


        try:
            garage = response.xpath('//p[contains(text(),"car garage")]/text()').extract_first('')
            if garage != '':
                garage = garage.split("car garage")[0]
                print(garage)
                garage = garage.split()[-1]
                print(garage)
                garage = garage.replace("three","3").replace("two","2").strip()
                garage = re.findall(r"(\d+)", garage)[0]
                if garage == '':
                    garage = 0


            else:
                garage = response.xpath('//p[contains(text(),"car rear-entry garage")]/text()').extract_first('')
                if garage != '':
                    garage = garage.split("car rear-entry garage")[0]
                    print(garage)
                    garage = garage.split()[-1]
                    print(garage)
                    garage = garage.replace("three", "3").replace("two", "2").strip()
                    garage = re.findall(r"(\d+)", garage)[0]

                    if garage == '':
                        garage = 0
                else:
                    garage = 0

            # garage = 0
        except Exception as e:
            print(e)
            garage = 0

        try:
            spec_desc = response.xpath('//p[@class="sidx-listing-description"]/text()').extract_first('')
        except Exception as e:
            print(e)
            spec_desc = ''

        try:
            specid = response.url.split("https://avondaleeast.com/properties/listing/fmls/")[1]
            specid = specid.split("/")[0]
            img = response.text.split("window.SIDX.initialState = ")[1]
            img = img.split("</script>")[0]

            temp = json.loads(img)

            # imgs = temp['listings']['fmls/6929231']['images']
            imgs = temp['listings'][f'fmls/{specid}']['images']
            print(imgs)
            SpecElevationImage = "|".join(imgs)

        except Exception as e:
            print(e)


        # try:
        #     img = '|'.join(response.xpath(
        #         '//div[@class="sidx-photo-array"]/img/@src').extract())
        #     # img = img.replace("background-image:url('", '').replace("');", '')
        #     SpecElevationImage = img
        # except Exception as e:
        #     SpecElevationImage = ''
        #     print(e)

        item = BdxCrawlingItem_Spec()
        item['SpecNumber'] = SpecNumber
        item['PlanNumber'] = PlanNumber
        # item['PlanNumber'] = unique_number
        item['SpecStreet1'] = SpecStreet1
        item['SpecCity'] = city
        item['SpecState'] = state
        item['SpecZIP'] = zip
        item['SpecCountry'] = 'USA'
        item['SpecPrice'] = SpecPrice
        item['SpecSqft'] = SpecSqft
        item['SpecBaths'] = SpecBaths
        item['SpecHalfBaths'] = SpecHalfBaths
        item['SpecBedrooms'] = SpecBedrooms
        item['MasterBedLocation'] = 0
        item['SpecGarage'] = garage
        item['SpecDescription'] = spec_desc
        item['SpecElevationImage'] = SpecElevationImage
        # item['SpecElevationImage'] = 'https://avondaleeast.com/wp-content/uploads/2020/03/home-1-1.jpg'
        item['SpecWebsite'] = response.url
        yield item

        # print('--------------->Homes', item)

    # --------------------------------------------------------------------- #

    # --------------------------------------------------------------------- #

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl avondaleeast_homes'.split())