# -*- coding: utf-8 -*-
import hashlib
import re
import time

import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class canopybuilders(scrapy.Spider):
    name = 'canopybuilders'
    allowed_domains = ['https://canopybuilders.com']
    start_urls = ['https://canopybuilders.com/communities/']

    builderNumber = "63729"

    def __init__(self):
        self.temp_list = []


    def parse(self,response):
        links = response.xpath('//div[@class="card"]/a/@href').extract()
        for link in links:
            yield scrapy.FormRequest(url=link,callback=self.communites,dont_filter=True)

    def communites(self,response):

        subdivisonName = response.xpath('//h1/text()').extract_first()

        subdivisonNumber = int(hashlib.md5(bytes(subdivisonName+response.url,"utf8")).hexdigest(), 16) % (10 ** 30)
        f = open("html/%s.html" % subdivisonNumber, "wb")
        f.write(response.body)
        f.close()

        try:
            add = response.xpath('//h3/text()').extract_first('')
            print(add)
        except Exception as e:
            print(e)
            add = ''

        try:
            street = add.split(".")[0]
            print(street)
        except Exception as e:
            print(e)
            street = ''

        try:
            city = add.split(",")[0]
            city = city.split(street)[1].split(".")[1].strip()
            print(city)
        except Exception as e:
            print(e)
            city = ''

        try:
            state = add.split(",")[1].strip()
            state = state.split(" ")[0].strip()
            state = state.replace("Florida","FL")
        except Exception as e:
            print(e)
            state = ''

        try:
            zip_code = add.split(",")[1].strip()
            zip_code = zip_code.split(" ")[1].strip()
            print(zip_code)
        except Exception as e:
            print(e)
            zip_code = ''

        try:
            desc = response.xpath('//div[@class="margin-b-md"]/p/text()').extract_first('').replace("\r","").replace("\n","").strip()
            print(desc)
        except Exception as e:
            print(e)
            desc = ''

        a = []
        try:
            aminity = "".join(response.xpath('//div[@class="col-sm-12 show-small"]//text()').extract()).replace("Play Ground","Playground")
        except Exception as e:
            print(e)

        amenity_list = ["Pool", "Playground", "GolfCourse", "Tennis", "Soccer", "Volleyball", "Basketball",
                        "Baseball", "Views", "Lake", "Pond", "Marina", "Beach", "WaterfrontLots", "Park",
                        "Trails", "Greenbelt", "Clubhouse", "CommunityCenter"]
        for i in amenity_list:
            print(i)
            if i in aminity:
                a.append(i)
        ab = '|'.join(a)

        image = []
        img = response.xpath('//div[@class="image-background image-large carousel-img show-medium"]/@style').getall()
        for im in img:
            im = im.split("background-image: url(")[1].split(");")[0]
            image.append(im)
        image = '|'.join(image)

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
        item2['AreaCode'] = '727'
        item2['Prefix'] = '560'
        item2['Suffix'] = '0737'
        item2['Extension'] = ""
        item2['Email'] = 'info@canopybuilders.com'
        item2['SubDescription'] = desc
        item2['AmenityType'] = ab
        item2['SubImage'] = image
        item2['SubWebsite'] =response.url
        yield item2

        temp_dict = {
            'subdivisonNumber': subdivisonNumber,
            'zip_code': zip_code
        }
        self.temp_list.append(temp_dict)


        # #------------- creating fake community --------------------------------------------#
        #
        # item = BdxCrawlingItem_subdivision()
        # item['sub_Status'] = "Active"
        # item['SubdivisionNumber'] = ''
        # item['BuilderNumber'] = self.builderNumber
        # item['SubdivisionName'] = "No Sub Division"
        # item['BuildOnYourLot'] = 0
        # item['OutOfCommunity'] = 0
        # item['Street1'] = '200 Mirror Lake Drive North'
        # item['City'] = 'Petersburg'
        # item['State'] = 'FL'
        # item['ZIP'] = '33701'
        # item['AreaCode'] = '727'
        # item['Prefix'] = '560'
        # item['Suffix'] = '0737'
        # item['Extension'] = ""
        # item['Email'] = 'info@canopybuilders.com'
        # item['SubDescription'] = 'Canopy Builders is a premier custom home builder in St Petersburg, specializing in new construction of the highest quality homes. Our homes combine the timeless elements of traditional architecture and design with modern day conveniences and construction technology. We aim to continue and expand upon the craft and legacy of the neighborhoods in which we build, while providing a personalized service to all of our clients.'
        # item['SubImage'] = 'https://canopybuilders.com/wp-content/uploads/2020/07/1818-11th-st-n20.jpg|https://canopybuilders.com/wp-content/uploads/2020/07/IMG_1078.jpg|https://canopybuilders.com/wp-content/uploads/2020/07/catherinewalkerhome-54.jpg'
        # item['SubWebsite'] = response.url
        # item['AmenityType'] = ''
        # yield item


        link = 'https://canopybuilders.com/plans/'
        yield scrapy.FormRequest(url=link, callback=self.parse2, dont_filter=True,meta={'subdivisonNumber':subdivisonNumber})

    def parse2(self, response):
        subdivisonNumber = response.meta['subdivisonNumber']
        links = response.xpath('//div[@class="card"]/a/@href').extract()
        for link in links:
            yield scrapy.FormRequest(url=link, callback=self.parse3, dont_filter=True,meta={'subdivisonNumber':subdivisonNumber})

    def parse3(self, response):
        SubdivisionNumber = response.meta['subdivisonNumber']

        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//h1/text()').get()
        except Exception as e:
            PlanName = ''
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName + response.url, "utf8")).hexdigest(), 16) % (
                    10 ** 30)
        except Exception as e:
            PlanNumber = ''
            print(e)

        # try:
        #     SubdivisionNumber = self.builderNumber
        #     print(SubdivisionNumber)
        # except Exception as e:
        #     SubdivisionNumber = ''
        #     print(e)

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

            sqft = response.xpath("//h5[contains(text(),' ft')]/text()").extract_first('')
            # sqft = sqft.split("|")[0]
            sqft = sqft.replace(',', '').strip()
            if '.' in sqft:
                sqft = sqft.split(".")[0]
            BaseSqft = re.findall(r"(\d+)", sqft)[0]

        except Exception as e:
            print(e)
            BaseSqft = ''

        try:
            bath = response.xpath("//h5[contains(text(),' Bath')]/text()").extract_first()
            if 'or' in bath:
                bath = bath.split("or")[1]
            tmp = re.findall(r"(\d+)", bath)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            print(e)

        try:

            Bedrooms = response.xpath("//h5[contains(text(),' Bed')]/text()").extract_first('')
            if 'or' in Bedrooms:
                Bedrooms = Bedrooms.split("or")[1]
            # Bedrooms = Bedrooms.split("|")[1].split("|")[0]
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)

        try:
            Garage = response.xpath("//h5[contains(text(),' Garage')]/text()").extract_first('')
            # Garage = re.findall(r"(\d*[three]*[four]*[two]*)[-]*[ ]*car garage", response.text.lower())[0]
            # Garage = Garage = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*car garage", response.text.lower())[0]
            # Garage = Garage.replace("three", "3").replace("four", "4").replace("two", "2")
            Garage = re.findall(r"(\d+)", Garage)[0]
        except Exception as e:
            print(e)
            Garage = 0

        try:
            Description = "".join(response.xpath('//div[@class="col-sm-12 margin-b- no-gutters"]/../p/text()').extract())
            Description = Description.encode('ascii','ignore').decode('utf8')
            # if Description == '':
            #     Description = 'Canopy Builders is a premier custom home builder in St Petersburg, specializing in new construction of the highest quality homes. Our homes combine the timeless elements of traditional architecture and design with modern day conveniences and construction technology. We aim to continue and expand upon the craft and legacy of the neighborhoods in which we build, while providing a personalized service to all of our clients.'
        except Exception as e:
            print(e)
            Description = ''


        price = 0

        try:

            images1 = response.xpath('//div[@class="image-background image-large carousel-img show-medium container-border"]/@style').extract()

            images2 = response.xpath('//div[@class="entry-image relative"]/a/img/@data-src').extract_first('')
            if ',' in images2:
                images2 = images2.split(",")[0]
                print(images2)

            images = []
            for id in images1:
                id = id.split("background-image: url(")[1].split(");")[0]
                images.append(id)
            ElevationImage = images

            if images2 != '':
                ElevationImage.append(images2)

            print(ElevationImage)
        except Exception as e:
            print(e)

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

            # ----------------------- Don't change anything here --------------
        unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
                10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['Type'] = Type
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number  # < -------- Changes here
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = PlanName
        item['PlanNotAvailable'] = PlanNotAvailable
        item['PlanTypeName'] = PlanTypeName
        item['BasePrice'] = price
        item['BaseSqft'] = BaseSqft
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = Description
        item['ElevationImage'] = "|".join(ElevationImage)
        item['PlanWebsite'] = PlanWebsite
        yield item

        link = 'https://canopybuilders.com/homes/'
        yield scrapy.FormRequest(url=link,callback=self.home_links,dont_filter=True)

    def home_links(self,response):
        links = response.xpath('//div[@class="col-sm-6 col-lg-4 margin-b-md"]/div/a/@href').extract()
        for link in links:
            yield scrapy.FormRequest(url=link,callback=self.home,dont_filter=True)


    def home(self,response):


        temp2 = response.xpath("//h4[contains(text(),'Status:')]/text()[2]").extract_first('')
        if temp2 == ' For Sale':
            print("thanks bro")
        elif temp2 == ' Featured':
            print("yes bro")

            if 'Under Construction' not in response.text:

                # if 'Coming Soon! ' and 'Coming Soon!' not in response.text:

                Spec = ''.join(response.xpath('//h2/text()').extract()).strip()

                try:
                    SpecStreet1 = Spec.split(".")[0]
                    print(SpecStreet1)
                except Exception as e:
                    print(e)
                    SpecStreet1 = ''

                try:
                    ci = Spec.split(".")[1].split(",")[0]
                    print(ci)
                    cty = ci.strip()
                    city = cty
                except Exception as e:
                    print(e)
                    city = ''

                state = 'FL'

                try:
                    zi = Spec.split(",")[2].strip().split(" ")[1]
                    zip = zi
                except Exception as e:
                    print(e)
                    zip = ''

                unique = SpecStreet1 + city + state + zip

                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

                try:
                    SpecSqft = response.xpath("//h5[contains(text(),' ft')]/text()").extract_first('')
                    # sqft = sqft.split("|")[0]
                    sqft = SpecSqft.replace(',', '').strip()
                    if '.' in sqft:
                        sqft = sqft.split(".")[0]
                    SpecSqft = re.findall(r"(\d+)", sqft)[0]

                except Exception as e:
                    print("SpecSqft---------->", e)


                try:
                    SpecBaths =  response.xpath("//h5[contains(text(),' Bath')]/text()").extract_first('')
                    SpecBaths = re.findall(r"(\d+)", SpecBaths)[0]
                    print(SpecBaths)

                    tmp = re.findall(r"(\d+)", SpecBaths)
                    SpecBaths = tmp[0]
                    if len(tmp) > 1:
                        SpecHalfBaths = 1
                    else:
                        SpecHalfBaths = 0
                except Exception as e:
                    SpecBaths = ''
                    print("SpecBaths--------->", e)


                try:
                    SpecBedrooms = response.xpath("//h5[contains(text(),' Bed')]/text()").extract_first()
                    SpecBedrooms = re.findall(r"(\d+)", SpecBedrooms)[0]
                except Exception as e:
                    print(e)
                    SpecBedrooms = ''


                try:
                    garage = response.xpath("//h5[contains(text(),' Garage')]/text()").extract_first('')
                    print(garage)
                    garage = re.findall(r"(\d+)", garage)[0]
                except Exception as e:
                    print(e)
                    garage = 0

                try:
                    spec_desc = "".join(response.xpath('//div[@class="col-sm-12 margin-b- no-gutters"]/../p/text()').extract())
                    spec_desc = spec_desc.encode('ascii','ignore').decode('utf8')
                    if spec_desc == '':
                        spec_desc = 'Canopy Builders is a premier custom home builder in St Petersburg, specializing in new construction of the highest quality homes. Our homes combine the timeless elements of traditional architecture and design with modern day conveniences and construction technology. We aim to continue and expand upon the craft and legacy of the neighborhoods in which we build, while providing a personalized service to all of our clients.'
                except Exception as e:
                    print(e)
                    spec_desc = ''



                try:
                    image = response.xpath('//div[@class="image-background image-large carousel-img show-medium"]/@style').extract_first('')
                    if image != '':
                        img = image.split("background-image: url(")[1].split(");")[0]
                    SpecElevationImage = img
                except Exception as e:
                    print(e)
                    SpecElevationImage = ''

                for i in self.temp_list:
                    subdivisionnumber = i['subdivisonNumber']
                    zip_code = i['zip_code']

                    if zip == zip_code:
                        item = BdxCrawlingItem_Plan()
                        unique = str("Plan Unknown") + str(self.builderNumber)
                        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                        item['unique_number'] = unique_number
                        item['Type'] = "SingleFamily"
                        item['PlanNumber'] = "Plan Unknown"
                        item['SubdivisionNumber'] = subdivisionnumber
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



                        item = BdxCrawlingItem_Spec()
                        item['SpecNumber'] = SpecNumber
                        # item['PlanNumber'] = PlanNumber
                        item['PlanNumber'] = unique_number
                        item['SpecStreet1'] = SpecStreet1
                        item['SpecCity'] = city
                        item['SpecState'] = state
                        item['SpecZIP'] = zip
                        item['SpecCountry'] = 'USA'
                        item['SpecPrice'] = '0'
                        item['SpecSqft'] = SpecSqft
                        item['SpecBaths'] = SpecBaths
                        item['SpecHalfBaths'] = SpecHalfBaths
                        item['SpecBedrooms'] = SpecBedrooms
                        item['MasterBedLocation'] = 0
                        item['SpecGarage'] = garage
                        item['SpecDescription'] = spec_desc
                        item['SpecElevationImage'] = SpecElevationImage
                        item['SpecWebsite'] = response.url
                        yield item

                    # print('--------------->Homes', item)


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl canopybuilders'.split())