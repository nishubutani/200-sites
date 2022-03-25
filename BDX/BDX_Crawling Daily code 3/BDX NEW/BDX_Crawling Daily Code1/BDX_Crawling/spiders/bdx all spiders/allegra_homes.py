# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'allegra_homes'
    allowed_domains = ['https://allegra-homes.com/']
    start_urls = ['https://allegra-homes.com/']

    builderNumber = "62673"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()



        # images = ''
        # image = response.xpath('//span/img/@src').extract()
        # for i in image:
        #     images = images + i + '|'
        # images = images.strip('|')
        #

        images = "https://i1.wp.com/allegra-homes.com/wp-content/uploads/2021/06/Allegra_Homes_Lakeshore_hero.jpg?resize=1080%2C487&ssl=1|https://i0.wp.com/allegra-homes.com/wp-content/uploads/2021/02/Allegra_Homes_Dominic.jpg?resize=1080%2C491&ssl=1|https://i0.wp.com/allegra-homes.com/wp-content/uploads/2020/10/Allegra-Homes-Gloria-22.jpg?fit=1600%2C1066&ssl=1|https://i2.wp.com/allegra-homes.com/wp-content/uploads/2020/10/Allegra-Homes-Gloria-41.jpg?fit=1600%2C1066&ssl=1|https://i1.wp.com/allegra-homes.com/wp-content/uploads/2021/02/Allegra_Homes_Hibiscus-10.jpg|https://i2.wp.com/allegra-homes.com/wp-content/uploads/2021/01/Allegra_Homes_Westward-2.jpg"

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '2344 Bee Ridge Road'
        item['City'] = 'Sarasota'
        item['State'] = 'FL'
        item['ZIP'] = '34239'
        item['AreaCode'] = '941'
        item['Prefix'] ='915'
        item['Suffix'] = '5000'
        item['Extension'] = ""
        item['Email'] = 'Rob.Allegra@comcast.net'
        item['SubDescription'] = 'Award-winning Allegra Homes has been a leader in Sarasota’s competitive real estate market since 2008. Allegra Homes sets the bar when it comes to luxury custom homes in Sarasota. Its owner, Rob Allegra, loves working with his clients to ensure that they end up in the home of their dreams.'
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'https://allegra-homes.com/featured-homes/'
        yield scrapy.FormRequest(url=link, callback=self.parse2, dont_filter=True)

    def parse2(self, response):
        links = response.xpath('//h2[@class="et_pb_module_header"]/a/@href').extract()
        for link in links:
            yield scrapy.FormRequest(url=link, callback=self.parse3, dont_filter=True)
        # yield scrapy.FormRequest(url='https://allegra-homes.com/project/lois-paul/', callback=self.parse3, dont_filter=True)

    def parse3(self, response):

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
            if '–' in PlanName or '-' in PlanName:
                ab = 5
                for i in range(1,ab+1,1):
                    # i=5
                    try:
                        PlanName = response.xpath('//div[@class="et_pb_text_inner"]/p/text()').extract()[i-1]
                        print(PlanName)
                    except Exception as e:
                        PlanName = ''
                        print(e)

                    try:
                        PlanNumber = int(hashlib.md5(bytes(PlanName + response.url, "utf8")).hexdigest(), 16) % (
                                10 ** 30)
                    except Exception as e:
                        PlanNumber = ''
                        print(e)

                    try:
                        sqft = response.xpath("//div[@class='et_pb_text_inner']/text()[2]").extract_first('')
                        if sqft == '' or sqft == '\n':
                            sqft = response.xpath('//div[@class="et_pb_text_inner"]/p/text()').extract()[i]
                            sqft = sqft.split('Bath')[1]
                            print(sqft)
                            sqft = sqft.split("/")[-2].strip()
                            print(sqft)
                        else:
                            sqft = sqft.split('Bath')[1].strip()
                        BaseSqft = re.findall(r"(\d+)", sqft)[0]

                    except Exception as e:
                        print(e)
                        BaseSqft = ''

                    try:
                        bath = response.xpath("//div[@class='et_pb_text_inner']/text()[2]").extract_first('')
                        if bath == '' or bath == '\n':
                            bath = response.xpath('//div[@class="et_pb_text_inner"]/p/text()').extract()[i]
                            bath = bath.split("/")[1].split("/")[0].strip()
                        else:
                            bath = bath.split("/")[1].split("/")[0].strip()
                        tmp = re.findall(r"(\d+)", bath)
                        Baths = tmp[0]
                        if len(tmp) > 1:
                            HalfBaths = 1
                        else:
                            HalfBaths = 0
                    except Exception as e:
                        print(e)

                    try:
                        Bedrooms = response.xpath("//div[@class='et_pb_text_inner']/text()[2]").extract_first('')
                        if Bedrooms == '' or Bedrooms == '\n':
                            Bedrooms = response.xpath('//div[@class="et_pb_text_inner"]/p/text()').extract()[i]
                            Bedrooms = Bedrooms.split("/")[0]
                        else:
                            Bedrooms = Bedrooms.split("/")[0]
                        Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
                    except Exception as e:
                        print(e)

                    try:
                        Garage = response.xpath('//div[@class="et_pb_text_inner"]/p/text()').extract()[i]
                        Garage = Garage.split('Sq Ft')[1].strip()
                        Garage = re.findall(r"(\d+)", Garage)[0]

                    except Exception as e:
                        print(e)
                        Garage = '0'

                    try:

                        desc = response.xpath(
                            '//div[@class="et_pb_row et_pb_row_1"]/div[2]//div[@class="et_pb_text_inner"]/p/text()').extract_first(
                            '')
                        if desc == '':
                            desc = ''
                            # desc = '/Allegra Homes got its start West of the Trail, in the area south of Downtown Sarasota where Rob and his family have lived for over 20 years. The company has since expanded having completed homes on Siesta and Bird keys. Starting in 2016, Allegra Homes began building homes East of the Trail'
                        Description = desc
                    except Exception as e:
                        print(e)

                    if PlanName == 'St Joseph':
                        Description = 'Relax in solitude soaking up the peaceful serenity of the 2-story St. Joseph I offering plenty of room to entertain: 4 bedrooms · 3 baths · 3657 sq. ft. (total 4605 sq. ft.) · 2 living levels · great room with 19 ft. ceiling · laundry room off the 3-car garage · den/office · bonus/game room · 2 covered lanais (1 with summer kitchen) · 2nd en suite bedroom · master wing with double walk-in closets, private access to lanai, separate tub and shower, dual vanities and water closet. Upper level: 2 bedrooms · 1 bath · loft/media room with vaulted ceiling and Juliette balcony overlooking the great room below'
                    # elif PlanName == 'St. Joseph II':
                    elif PlanName == 'St Joseph II':
                        Description = 'Featuring some truly remarkable amenities, the 2-story St. Joseph II offers great livability to live the life you love: 4 bedrooms · 3 baths · 3693 sq. ft. (total 4672 sq. ft.) · 2 living levels · living room with 19 ft. ceiling · laundry room off the 3-car garage · den · game room · 2 covered lanais (1 with summer kitchen) · guest suite with shared bath · double door entry · master wing with walk-in closet, private access to lanai, separate tub and shower, dual vanities and water closet · elevator shaft. Upper level: 2 bedrooms · 1 bath · loft media room with Juliette balcony overlooking the living room below'
                    # elif PlanName == 'St. Joseph III':
                    elif PlanName == 'St. Joseph III':
                        Description = 'The St. Joseph III offers an exceptional lifestyle where you just may never want to leave: 4 bedrooms · 3.5 baths · 3775 sq. ft. (total 5111 sq. ft.) · 2 living levels · great room with 19 ft. ceiling · laundry room off the 3-car garage · double door entry · den · bonus room with pool bath · huge lanai with summer kitchen · guest suite with shared bath · master wing with huge walk-in closet, private access to lanai, separate tub and shower, dual vanities and water closet · elevator shaft · optional pool and spa. Upper level: 2 bedrooms · 1 bath · loft/media room with Juliette balcony overlooking the great room below'

                    try:
                        img1 = response.xpath('//span[@class="et_pb_image_wrap "]/img/@src').extract_first('')
                        images = []
                        imagedata = response.xpath('//div[@class="et_pb_gallery_image landscape"]/a/@href').getall()
                        if imagedata != []:
                            for id in imagedata:
                                id = id
                                images.append(id)
                            ElevationImage = "|".join(images)
                        else:
                            ElevationImage = ''
                        if img1 != '':
                            if ElevationImage == '':
                                ElevationImage = img1
                            else:
                                ElevationImage = ElevationImage + '|' + img1
                        else:
                            ElevationImage = ElevationImage
                    except Exception as e:
                        print(e)

                    try:
                        PlanWebsite = response.url
                    except Exception as e:
                        print(e)

                    # ----------------------- Don't change anything here --------------
                    unique = str(PlanNumber) + str(SubdivisionNumber) + str(PlanName)  # < -------- Changes here
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
            elif '&' in PlanName:
                ab = 2
                for i in range(1, ab+2 , 2):
                    try:
                        print(i)
                        PlanName = response.xpath('//div[@class="et_pb_text_inner"]/p/text()').extract()[i-1]
                    except Exception as e:
                        PlanName = ''
                        print(e)

                    try:
                        PlanNumber = int(hashlib.md5(bytes(PlanName + response.url, "utf8")).hexdigest(), 16) % (
                                10 ** 30)
                    except Exception as e:
                        PlanNumber = ''
                        print(e)

                    try:
                        sqft = response.xpath("//div[@class='et_pb_text_inner']/text()[12]").extract_first('')
                        if sqft == '':
                            sqft = response.xpath('//div[@class="et_pb_text_inner"]/p/text()').extract()[i]
                            sqft = sqft.split('Bath')[1]
                            print(sqft)
                            sqft = sqft.split("/")[-2].strip()
                            print(sqft)
                        else:
                            sqft = sqft.split('Bath')[1].strip()
                        BaseSqft = re.findall(r"(\d+)", sqft)[0]

                    except Exception as e:
                        print(e)
                        BaseSqft = ''

                    try:
                        bath = response.xpath("//div[@class='et_pb_text_inner']/text()[12]").extract_first('')
                        if bath == '':
                            bath = response.xpath('//div[@class="et_pb_text_inner"]/p/text()').extract()[i]
                            bath = bath.split("/")[1].split("/")[0].strip()
                        else:
                            bath = bath.split("/")[1].split("/")[0].strip()
                        tmp = re.findall(r"(\d+)", bath)
                        Baths = tmp[0]
                        if len(tmp) > 1:
                            HalfBaths = 1
                        else:
                            HalfBaths = 0
                    except Exception as e:
                        print(e)

                    try:
                        Bedrooms = response.xpath("//div[@class='et_pb_text_inner']/text()[12]").extract_first('')
                        if Bedrooms == '':
                            Bedrooms = response.xpath('//div[@class="et_pb_text_inner"]/p/text()').extract()[i]
                            Bedrooms = Bedrooms.split("/")[0]
                        else:
                            Bedrooms = Bedrooms.split("/")[0]
                        Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
                    except Exception as e:
                        print(e)

                    try:
                        Garage = response.xpath('//div[@class="et_pb_text_inner"]/p/text()').extract()[i]
                        Garage = Garage.split('Sq Ft')[1].strip()
                        Garage = re.findall(r"(\d+)", Garage)[0]

                    except Exception as e:
                        print(e)
                        Garage = '0'

                    try:

                        desc = response.xpath(
                            '//div[@class="et_pb_row et_pb_row_1"]/div[2]//div[@class="et_pb_text_inner"]/p/text()').extract_first(
                            '')
                        if desc == '':
                            desc =''
                            # desc = 'Allegra Homes got its start West of the Trail, in the area south of Downtown Sarasota where Rob and his family have lived for over 20 years. The company has since expanded having completed homes on Siesta and Bird keys. Starting in 2016, Allegra Homes began building homes East of the Trail'
                        Description = desc
                    except Exception as e:
                        print(e)

                    try:
                        img1 = response.xpath('//span[@class="et_pb_image_wrap "]/img/@src').extract_first('')
                        images = []
                        imagedata = response.xpath('//div[@class="et_pb_gallery_image landscape"]/a/@href').getall()
                        if imagedata != []:
                            for id in imagedata:
                                id = id
                                images.append(id)
                            ElevationImage = "|".join(images)
                        else:
                            ElevationImage = ''
                        if img1 != '':
                            if ElevationImage == '':
                                ElevationImage  = img1
                            else:
                                ElevationImage = ElevationImage + '|' + img1
                        else:
                            ElevationImage = ElevationImage
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

            else:
                try:
                    sqft = response.xpath("//div[@class='et_pb_text_inner']/text()[2]").extract_first('')
                    if sqft == '' or sqft== '\n':
                        sqft = response.xpath('//div[@class="et_pb_text_inner"]/p/text()[2]').extract_first('')
                        sqft = sqft.split('Bath')[1]
                        print(sqft)
                        sqft = sqft.split("/")[-2].strip()
                        print(sqft)
                    else:
                        sqft = sqft.split('Bath')[1].strip()
                    BaseSqft = re.findall(r"(\d+)", sqft)[0]

                except Exception as e:
                    print(e)
                    BaseSqft=''

                try:
                    bath = response.xpath("//div[@class='et_pb_text_inner']/text()[2]").extract_first('')
                    if bath == '' or bath == '\n':
                        bath = response.xpath('//div[@class="et_pb_text_inner"]/p/text()[2]').extract_first('')
                        bath = bath.split("/")[1].split("/")[0].strip()
                    else:
                        bath = bath.split("/")[1].split("/")[0].strip()
                    tmp = re.findall(r"(\d+)", bath)
                    Baths = tmp[0]
                    if len(tmp) > 1:
                        HalfBaths = 1
                    else:
                        HalfBaths = 0
                except Exception as e:
                    print(e)

                if PlanName == 'Lakeshore':
                    HalfBaths = 2
                elif PlanName == 'Dominic':
                    HalfBaths = 2

                try:
                    Bedrooms = response.xpath("//div[@class='et_pb_text_inner']/text()[2]").extract_first('')
                    if Bedrooms == '' or Bedrooms == '\n':
                        Bedrooms = response.xpath('//div[@class="et_pb_text_inner"]/p/text()[2]').extract_first('')
                        Bedrooms = Bedrooms.split("/")[0]
                    else:
                        Bedrooms = Bedrooms.split("/")[0]
                    Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
                except Exception as e:
                    print(e)

                try:
                    Garage = response.xpath('//div[@class="et_pb_text_inner"]/p/text()[2]').extract_first('')
                    Garage = Garage.split('Sq Ft')[1].strip()
                    Garage = re.findall(r"(\d+)", Garage)[0]

                except Exception as e:
                    print(e)
                    Garage = '0'


                try:

                    desc = response.xpath('//div[@class="et_pb_row et_pb_row_1"]/div[2]//div[@class="et_pb_text_inner"]/p/text()').extract_first('')
                    if desc == '' or desc == '\n':
                        desc = ''

                        # desc = 'Allegra Homes got its start West of the Trail, in the area south of Downtown Sarasota where Rob and his family have lived for over 20 years. The company has since expanded having completed homes on Siesta and Bird keys. Starting in 2016, Allegra Homes began building homes East of the Trail'

                    Description = desc
                except Exception as e:
                    print(e)

                try:
                    img1 = response.xpath('//span[@class="et_pb_image_wrap "]/img/@src').extract_first('')
                    images = []
                    imagedata = response.xpath('//div[@class="et_pb_gallery_image landscape"]/a/@href').getall()
                    if imagedata != []:
                        for id in imagedata:
                            id = id
                            images.append(id)
                        ElevationImage = "|".join(images)
                    else:
                        ElevationImage = ''

                    if img1 != '':
                        if ElevationImage == '':
                            ElevationImage = img1
                        else:
                            ElevationImage = ElevationImage  + '|' + img1
                    else:
                        ElevationImage = ElevationImage
                except Exception as e:
                    print(e)
                    ''

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
        except Exception as e:
            print(e)


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl allegra_homes'.split())