# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import json
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'brim_buildersinc'
    allowed_domains = ['https://brimbuildersinc.com/']
    start_urls = ['https://brimbuildersinc.com/communities/']

    builderNumber = "63673"

    def __init__(self):
        self.temp_list = []

    # ------------------- Creating Communities ---------------------- #


    def parse(self, response):

        links = response.xpath('//div[@class="card"]/a/@href').extract()
        for link in links:
            yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)
            # yield scrapy.FormRequest(url='https://brimbuildersinc.com/communities/leeway-estates/',callback=self.parse2,dont_filter=True)


    def parse2(self,response):

        subdivisonName = response.xpath('//h1/text()').extract_first(default="")
        subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)

        f = open("html/%s.html" % subdivisonNumber, "wb")
        f.write(response.body)
        f.close()

        street = response.xpath('//div[@class="col-md-9"]/div/h3/text()').extract_first()
        print(street)

        add = response.xpath('//div[@class="col-md-9"]/div/h3/following-sibling::h3/text()').extract_first('')
        print(add)

        try:
            city = add.split(",")[0].strip()
            print(city)
        except Exception as e:
            print(e)
            city = ''

        try:
            state = add.split(",")[1].strip().split(" ")[0]
            print(state)
            zip_code = add.split(",")[1].strip().split(" ")[1]
            print(zip_code)

        except Exception as e:
            print(e)
            state,zip_code = '',''

        a = []
        # aminity = ''.join(response.xpath('//*[@class="ll-features-content__half right col-md-1of2"]/ul[1]/li/text()').extract())
        try:
            aminity = ''.join(response.xpath('//div[@class="w70 columns"]//text()|//div[@class="container-text"]/p/text()').getall())
            aminity = aminity.title()
        except Exception as e:
            print(e)

        amenity_list = ["Pool", "Playground", "GolfCourse", "Tennis", "Soccer", "Volleyball", "Basketball",
                        "Baseball", "Views", "Lake", "Pond", "Marina", "Beach", "WaterfrontLots", "Park",
                        "Trails", "Greenbelt", "Clubhouse", "CommunityCenter",'Golf Course']
        for i in amenity_list:
            # print(i)
            if i in aminity:
                if i == 'Golf Course':
                    i= 'GolfCourse'
                # print(i)
                a.append(i)
        ab = '|'.join(a)


        try:
            desc = "".join(response.xpath('//div[@class="container-text"]/p/text()').extract())
            print(desc)
        except Exception as e:
            print(e)
            desc = ''

        try:
            images = []
            image = response.xpath('//div[@class="image-background image-large carousel-img show-medium"]/@style').extract()
            for i in image:
                i = i.split("background-image: url(")[1].split(");")[0]
                print(i)
                images.append(i)
            # images = "|".join([ "https://static.wixstatic.com/media/" + str(json.loads(x)['imageData']['uri']) for x in div.xpath('.//*[@data-image-info]/@data-image-info').extract()])
            # print(images.split("|"))


            images = "|".join(images)

        except Exception as e:
            print(e)
            images = ''


        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionName'] = subdivisonName
        item2['SubdivisionNumber'] = subdivisonNumber
        item2['BuilderNumber'] = self.builderNumber
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 1
        item2['Street1'] = street
        item2['City'] = city
        item2['State'] = state
        item2['ZIP'] = zip_code
        item2['AreaCode'] = "717"
        item2['Prefix'] = "264"
        item2['Suffix'] = "4838"
        item2['Extension'] = ""
        item2['Email'] = 'info@brimbuildersinc.com'
        item2['SubDescription'] = desc
        item2['SubImage'] = images
        item2['SubWebsite'] = response.url
        item2['AmenityType'] = ab
        yield item2



        link = response.xpath("//span[contains(text(),'Homes In This Community')]/../@href").extract_first('')
        print(link)

        link = 'https://brimbuildersinc.com/' + link
        print(link)

        link = link.replace("/../../","/")
        print(link)





        temp_dict = {
            'subdivisonNumber':subdivisonNumber,
            'zip_code':zip_code
        }
        self.temp_list.append(temp_dict)


        # link = 'https://brimbuildersinc.com/homes/'
        yield scrapy.FormRequest(url=link,callback=self.parse3,dont_filter=True,meta={'subdivisonNumber':subdivisonNumber})


    def parse3(self,response):
        subdivisonNumber = response.meta['subdivisonNumber']


        links = response.xpath('//div[@class="card"]/a/@href').extract()
        if links != []:
            for link in links:

                # link = 'https://brimbuildersinc.com/homes/heritage-estates-west-lot-68/'
                yield scrapy.FormRequest(url=link,callback=self.parse4,dont_filter=True,meta={'subdivisonNumber':subdivisonNumber})
    #
    def parse4(self,response):

        subdivisonNumber = response.meta['subdivisonNumber']

        item = BdxCrawlingItem_Plan()
        unique = str("Plan Unknown") + str(subdivisonNumber)
        # unique = str("Plan Unknown") + str(self.builderNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item['unique_number'] = unique_number
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = "Plan Unknown"
        item['SubdivisionNumber'] = subdivisonNumber
        # item['SubdivisionNumber'] = "29181167148119071041172338507"
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


        temp = "".join(response.xpath('//i[@class="fa fa-circle text-green"]/@aria-hidden|//i[@class="fa fa-star text-yellow"]/@aria-hidden').extract())
        print(temp)

        if temp != '':

            try:
                try:
                    SpecStreet1 = response.xpath('//div[@class="col-md-9"]/h2/text()').extract_first('')
                except Exception as e:
                    print(e)

                try:
                    add = response.xpath('//div[@class="col-md-9"]/h2/following-sibling::h2/text()').extract_first('')
                    print(add)
                except Exception as e:
                    print(e)

                try:
                    SpecC =add.split(",")[0].strip()
                    SpecCity = SpecC
                except Exception as e:
                    print(e)

                try:
                    SpecState = add.split(",")[1]
                    SpecState = SpecState.strip()
                    SpecState = SpecState.split(" ")[0]
                except Exception as e:
                    print(e)

                try:
                    SpecZIP = add.split(",")[1].strip()
                    SpecZIP = SpecZIP.strip()
                    SpecZIP = SpecZIP.split(" ")[1]
                except Exception as e:
                    SpecZIP = '00000'

                unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
                print(unique)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()

                try:
                    PlanNumber = self.builderNumber
                except Exception as e:
                    print(e)

                try:
                    SpecCountry = "USA"
                except Exception as e:
                    print(e)


                price = '0'

                try:
                    SpecBedrooms = response.xpath('//h4/text()').extract_first('').strip().replace("\n","").replace("\t","")
                    SpecBedrooms = SpecBedrooms.split("•")[0]
                    print(SpecBedrooms)
                    SpecBedrooms = re.findall(r'(\d{1})', SpecBedrooms)[0]
                except Exception as e:
                    print(str(e))

                try:
                    SpecBaths = response.xpath('//h4/text()').extract_first('').strip().replace("\n","").replace("\t","")
                    SpecBaths = SpecBaths.split("•")[1].split("•")[0]
                    tmp = re.findall(r"(\d+)", SpecBaths)
                    SpecBaths = tmp[0]
                    if len(tmp) > 1:
                        halfbath = 1
                    else:
                        halfbath = 0
                except Exception as e:
                    print(str(e))

                try:
                    SpecGarage = response.xpath('//h4/text()').extract_first('').strip().replace("\n","").replace("\t","")
                    SpecGarage = SpecGarage.split("•")[2].split("•")[0]
                    SpecGarage = re.findall(r'(\d{1})', SpecGarage)[0]
                except Exception as e:
                    print(str(e))

                try:
                    SpecSqft = response.xpath('//h4/text()').extract_first('').strip().replace("\n","").replace("\t","")
                    SpecSqft = SpecSqft.split("•")[-1].replace(",","")
                    SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
                except Exception as e:
                    print(str(e))

                try:
                    MasterBedLocation = "Down"
                except Exception as e:
                    print(e)

                try:
                    SpecDescription = "".join(response.xpath('//div[@class="container-text"]/p/text()').extract())
                    if '-' in SpecDescription:
                        SpecDescription = ''
                except Exception as e:
                    print(e)

                try:
                    specElevation = []
                    image = response.xpath('//div[@class="image-background image-large carousel-img show-medium"]/@style').extract()
                    for i in image:
                        i = i.split("background-image: url(")[1].split(");")[0]
                        print(i)
                        specElevation.append(i)
                    ElevationImage = "|".join(specElevation)
                except Exception as e:
                    print(e)

                try:
                    SpecWebsite = response.url
                except Exception as e:
                    print(e)

                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = unique_number
                item['SpecStreet1'] = SpecStreet1
                item['SpecCity'] = SpecCity
                item['SpecState'] = SpecState
                item['SpecZIP'] = SpecZIP
                item['SpecCountry'] = SpecCountry
                item['SpecPrice'] = price
                item['SpecSqft'] = SpecSqft
                item['SpecBaths'] = SpecBaths
                item['SpecHalfBaths'] = halfbath
                item['SpecBedrooms'] = SpecBedrooms
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = SpecGarage
                item['SpecDescription'] = SpecDescription
                item['SpecElevationImage'] = ElevationImage
                item['SpecWebsite'] = SpecWebsite
                yield item


                # for i in self.temp_list:
                #     subdivisionnumber = i['subdivisonNumber']
                #     zip_code = i['zip_code']
                #
                #     if SpecZIP == zip_code:
                #         item = BdxCrawlingItem_Plan()
                #         unique = str("Plan Unknown") + str(self.builderNumber)
                #         unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                #         item['unique_number'] = unique_number
                #         item['Type'] = "SingleFamily"
                #         item['PlanNumber'] = "Plan Unknown"
                #         item['SubdivisionNumber'] = subdivisionnumber
                #         item['PlanName'] = "Plan Unknown"
                #         item['PlanNotAvailable'] = 1
                #         item['PlanTypeName'] = "Single Family"
                #         item['BasePrice'] = 0
                #         item['BaseSqft'] = 0
                #         item['Baths'] = 0
                #         item['HalfBaths'] = 0
                #         item['Bedrooms'] = 0
                #         item['Garage'] = 0
                #         item['Description'] = ""
                #         item['ElevationImage'] = ""
                #         item['PlanWebsite'] = ""
                #         yield item
                #
                #         # ----------------------- Don't change anything here --------------------- #
                #         item = BdxCrawlingItem_Spec()
                #         item['SpecNumber'] = SpecNumber
                #         item['PlanNumber'] = unique_number
                #         item['SpecStreet1'] = SpecStreet1
                #         item['SpecCity'] = SpecCity
                #         item['SpecState'] = SpecState
                #         item['SpecZIP'] = SpecZIP
                #         item['SpecCountry'] = SpecCountry
                #         item['SpecPrice'] = price
                #         item['SpecSqft'] = SpecSqft
                #         item['SpecBaths'] = SpecBaths
                #         item['SpecHalfBaths'] = halfbath
                #         item['SpecBedrooms'] = SpecBedrooms
                #         item['MasterBedLocation'] = MasterBedLocation
                #         item['SpecGarage'] = SpecGarage
                #         item['SpecDescription'] = SpecDescription
                #         item['SpecElevationImage'] = ElevationImage
                #         item['SpecWebsite'] = SpecWebsite
                #         yield item

            except Exception as e:
                print(e)


    # --------------------------------------------------------------------- #

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl brim_buildersinc'.split())