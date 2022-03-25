# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'avtech_homes'
    allowed_domains = ['https://avtechomes.com/']
    start_urls = ['https://avtechomes.com/our-communities/']

    builderNumber = "62843"

    def __init__(self):
        self.temp_list = ["Citation 3 - Model Home","Citation 4 - Model Home","Constellation 4 - Model Home","Gulfstream - Model Home","GULFSTREAM 4/3 - Model Home","Gulfstream 4J - Model Home","Saratoga - Model Home","The Capri - Model Home","the Citation 4 Plus - Model Home","The Newport - Model Home","The Paradise - Model Home"]

    # ------------------- Creating Communities ---------------------- #

    def parse(self, response):
        links = response.xpath('//div[@class="community-title"]/a/@href').extract()
        for link in links:
            link = 'https://avtechomes.com' + link
            yield scrapy.FormRequest(url=link,callback=self.comm,dont_filter=True)

        link = 'https://avtechomes.com/home-plans/'
        yield scrapy.FormRequest(url=link,callback=self.new_plan,dont_filter=True)


    def comm(self,response):
        subdivisonName = response.xpath('//div[@class="model-box-title"]/text()').extract_first(default="")
        subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)

        f = open("html/%s.html" % subdivisonNumber, "wb")
        f.write(response.body)
        f.close()

        contactTmp = response.xpath('//div[@class="community-address"][1]/text()').extract_first()
        contactTmp2 = response.xpath('//div[@class="community-address"][1]/text()[2]').extract_first()


        street1 = contactTmp.split(",")[0]
        if 'Ave' in street1:
            city = street1.split("Ave ")[1]
        elif 'SE' in street1:
            city = street1.split("SE")[1]
        else:
            # city = contactTmp.split(",")[1].strip().split(" ")[1]
            city = 'palm cost'

        street1 = street1.replace(" Palm Bay","")
        state = contactTmp.split(",")[1].strip().split(" ")[0].strip()
        if len(state) != 2:
            state = contactTmp.split(" ")[-2]
            zip_code = contactTmp.split(" ")[-1]
        else:
            try:
                zip_code  = contactTmp.split(state)[1].strip()
            except:
                zip_code = '00000'

        if zip_code == '':
            zip_code = '00000'

        # zip_code = contactTmp.split(",")[1].strip().split(" ")[1].strip()

        area = contactTmp2.split("-")[0]
        Prefix = contactTmp2.split("-")[1].split("-")[0]
        Suffix = contactTmp2.split("-")[2]

        if subdivisonName == 'deltona':
            email = 'lpesce@avtechomes.com'
        elif subdivisonName == 'Palm Bay & South Brevard':
            email = 'breese@avtechomes.com'
        else:
            email = 'smeinke@avtechomes.com'

        try:
            aminity = ''.join(response.xpath("//*[contains(text(),'Details')]/following-sibling::div[@class='model-box-content']//text()").getall())
            aminity = aminity.title()
        except Exception as e:
            print(e)
        a = []
        amenity_list = ["Pool", "Playground", "GolfCourse", "Tennis", "Soccer", "Volleyball", "Basketball",
                        "Baseball", "Views", "Lake", "Pond", "Marina", "Beach", "WaterfrontLots", "Park",
                        "Trails", "Greenbelt", "Clubhouse", "CommunityCenter"]
        for i in amenity_list:
            # print(i)
            if i in aminity:
                # print(i)
                a.append(i)
        ab = '|'.join(a)


        if zip_code!= '00000':

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
            item2['ZIP'] = zip_code
            item2['AreaCode'] = area
            item2['Prefix'] = Prefix
            item2['Suffix'] = Suffix
            item2['Extension'] = ""
            item2['Email'] = email
            item2['SubDescription'] ="".join(response.xpath('//div[@class="model-box-content"]/p/text()').extract())
            item2['SubImage'] = response.xpath('//a[@id="first-in-tour"]/img/@src').extract_first()
            item2['SubWebsite'] = response.url
            item2['AmenityType'] = ab
            yield item2

            links = response.xpath('//div[@class="model-box-content"]/a/@href').extract()
            for link in links:
                print(link)
                yield scrapy.FormRequest(url=link,callback=self.parse3,dont_filter=True,meta={'subdivisonNumber':subdivisonNumber})
                # yield scrapy.FormRequest(url='https://avtechomes.com/home-model/gulfstream-4-3/',callback=self.parse3,dont_filter=True,meta={'subdivisonNumber':subdivisonNumber})

    def parse3(self,response):
        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//div[@class="model-box-title"]/text()').get()
        except Exception as e:
            PlanName = ''
            print(e)

        # self.temp_list.append(PlanName)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName + response.url, "utf8")).hexdigest(), 16) % (
                    10 ** 30)
        except Exception as e:
            PlanNumber = ''
            print(e)

        try:
            SubdivisionNumber = response.meta['subdivisonNumber']
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
            sqft = response.xpath('//*[@id="model-features"]/div[2]/text()[5]').extract_first('')
            # sqft = sqft.split("|")[0]
            sqft = sqft.replace(',', '').strip()
            BaseSqft = re.findall(r"(\d+)", sqft)[0]

        except Exception as e:
            print(e)
            BaseSqft = ''

        try:
            bath = response.xpath('//*[@id="model-features"]/div[2]/text()[3]').extract_first()
            # bath = bath.split("|")[2]
            # if '-' in bath:
            #     bath = bath.split("-")[1]
            tmp = re.findall(r"(\d+)", bath)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            print(e)

        try:
            Bedrooms = response.xpath('//*[@id="model-features"]/div[2]/text()[1]').extract_first()
            # Bedrooms = Bedrooms.split("|")[1].split("|")[0]
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)

        try:
            # Garage = response.xpath('//div[@itemprop="description"]/p/text()[3]').extract_first('')
            # Garage = re.findall(r"(\d*[three]*[four]*[two]*)[-]*[ ]*car garage", response.text.lower())[0]
            Garage = Garage = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*car garage", response.text.lower())[0]
            Garage = Garage.replace("three", "3").replace("four", "4").replace("two", "2")
            Garage = re.findall(r"(\d+)", Garage)[0]
        except Exception as e:
            print(e)
            Garage = 0

        # try:
        #     Garage = 0
        # except Exception as e:
        #     Garage = 0
        #     print(e)

        try:
            # temp = response.xpath('//div[@class="model-box-content"]/p/text()').extract_first('')

            Description = []
            Description_create = response.xpath('//div[@class="model-box-content"]/p/text()').extract()
            for desx in Description_create:
                print(desx)
                if desx != 'CLICK TO ENLARGE':
                    Description.append(desx)


            Description = "".join(Description)
            print(Description)


            #
            # if temp == 'CLICK TO ENLARGE':
            #     Description = response.xpath('//div[@class="model-box-content"]/p[2]//text()').extract_first('')
            # else:
            #     Description = response.xpath('//div[@class="model-box-content"]/p[2]//text()').extract_first('')
            # if Description == '':
            #     Description = response.xpath('//div[@class="model-box-content"]/p[1]/text()').extract_first()
        except Exception as e:
            print(e)

        try:
            images = []
            images1 = response.xpath('//a[@class="jackbox"]/@href').extract()
            for i in images1:
                images.append(i)


            imagedata = response.xpath("//img/@src").extract()[2:4]
            for id in imagedata:
                id = id
                images.append(id)
            ElevationImage = images
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
        item['ElevationImage'] = "|".join(ElevationImage)
        item['PlanWebsite'] = PlanWebsite
        yield item


    def new_plan(self,response):

        links = response.xpath('//div[@class="model-item-box"]/div/a/@href').extract()
        for link in links:
            print(link)
            yield scrapy.FormRequest(url=link,callback=self.new_plan1,dont_filter=True)


    def new_plan1(self,response):

        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionName'] = "No Sub Division"
        item2['SubdivisionNumber'] = self.builderNumber
        item2['BuilderNumber'] = self.builderNumber
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        item2['Street1'] = '2661 Keysville Ave'
        item2['City'] = 'Deltona'
        item2['State'] = 'FL'
        item2['ZIP'] = '32725'
        item2['AreaCode'] = '321'
        item2['Prefix'] = '676'
        item2['Suffix'] = '4688'
        item2['Extension'] = ""
        item2['Email'] = 'info@avtechomes.com'
        item2['SubDescription'] = "".join(response.xpath('//div[@class="model-box-content"]/p/text()').extract())
        item2['SubImage'] = "https://avtechomes.com/wp-content/uploads/2020/02/Desktop_Homepage_Graphic_Floor-Plan.png|https://avtechomes.com/wp-content/uploads/2020/02/Tablet_Graphic_House.png|https://avtechomes.com/wp-content/uploads/2020/02/Desktop_Homepage_Slider_3-scaled.jpg"
        item2['SubWebsite'] = response.url
        item2['AmenityType'] = ''
        yield item2


        # com1 = ['Palm Coast','Palm Bay & South Brevard','Deltona']
        # for subdivisonName in com1:
        subdivisonNumber = self.builderNumber

        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//div[@class="model-box-title"]/text()').get()
        except Exception as e:
            PlanName = ''
            print(e)

        print(self.temp_list)


        if PlanName not in self.temp_list:
            try:
                PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (
                        10 ** 30)
            except Exception as e:
                PlanNumber = ''
                print(e)

            try:
                SubdivisionNumber = subdivisonNumber
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
                sqft = response.xpath('//*[@id="model-features"]/div[2]/text()[5]').extract_first('')
                # sqft = sqft.split("|")[0]
                sqft = sqft.replace(',', '').strip()
                BaseSqft = re.findall(r"(\d+)", sqft)[0]

            except Exception as e:
                print(e)
                BaseSqft = ''

            try:
                bath = response.xpath('//*[@id="model-features"]/div[2]/text()[3]').extract_first()
                # bath = bath.split("|")[2]
                # if '-' in bath:
                #     bath = bath.split("-")[1]
                tmp = re.findall(r"(\d+)", bath)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                print(e)

            try:
                Bedrooms = response.xpath('//*[@id="model-features"]/div[2]/text()[1]').extract_first()
                # Bedrooms = Bedrooms.split("|")[1].split("|")[0]
                Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            except Exception as e:
                print(e)

            try:
                # Garage = response.xpath('//div[@itemprop="description"]/p/text()[3]').extract_first('')
                # Garage = re.findall(r"(\d*[three]*[four]*[two]*)[-]*[ ]*car garage", response.text.lower())[0]
                Garage = Garage = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*car garage", response.text.lower())[0]
                Garage = Garage.replace("three", "3").replace("four", "4").replace("two", "2")
                Garage = re.findall(r"(\d+)", Garage)[0]
            except Exception as e:
                print(e)
                Garage = 0

            try:
                # temp = response.xpath('//div[@class="model-box-content"]/p/text()').extract_first('')

                Description = []
                Description_create = response.xpath('//div[@class="model-box-content"]/p/text()').extract()
                for desx in Description_create:
                    print(desx)
                    if desx != 'CLICK TO ENLARGE':
                        Description.append(desx)

                Description = "".join(Description)
                print(Description)

                #
                # if temp == 'CLICK TO ENLARGE':
                #     Description = response.xpath('//div[@class="model-box-content"]/p[2]//text()').extract_first('')
                # else:
                #     Description = response.xpath('//div[@class="model-box-content"]/p[2]//text()').extract_first('')
                # if Description == '':
                #     Description = response.xpath('//div[@class="model-box-content"]/p[1]/text()').extract_first()
            except Exception as e:
                print(e)

            try:
                images = []
                images1 = response.xpath('//a[@class="jackbox"]/@href').extract()
                for i in images1:
                    images.append(i)

                imagedata = response.xpath("//img/@src").extract()[2:4]
                for id in imagedata:
                    id = id
                    images.append(id)
                ElevationImage = images
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
            item['ElevationImage'] = "|".join(ElevationImage)
            item['PlanWebsite'] = PlanWebsite
            yield item





    # --------------------------------------------------------------------- #

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl avtech_homes'.split())