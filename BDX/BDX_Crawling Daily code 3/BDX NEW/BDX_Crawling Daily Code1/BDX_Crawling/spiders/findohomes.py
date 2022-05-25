
# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from scrapy.cmdline import execute
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class bellavistacustomehomesSpider(scrapy.Spider):
    name = 'findohomes'
    allowed_domains = ['findohomes.com']
    # start_urls = ['https://www.findohomes.com/']
    builderNumber = 53740

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,gu;q=0.7',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
    }

    def start_requests(self):
        ink = 'https://www.findohomes.com'
        yield scrapy.FormRequest(url=ink, callback=self.parse11, dont_filter=True, headers=self.headers)

    def parse11(self,response):

        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        item2['Street1'] = '500 W. Lanier AvenueBldg. 600, Unit 605'
        item2['City'] = 'Fayetteville'
        item2['State'] = 'GA'
        item2['ZIP'] = '30214'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "Findo Homes & Communities was founded over 15 years ago by Funmi Abiodun-Findo, with a promise to design and build new homes that blend ideal floor plans, quality construction and outstanding value. Today, families all across Metro Atlanta Cities are continuing to put their trust in Findo Homes & Communities and their team of talented building professionals, artisans, trade partners and sub contractors"
        item2['SubImage'] = "https://lirp.cdn-website.com/07727de3/dms3rep/multi/opt/findopix-6_orig-d6222d4b-720w.jpg|https://lirp.cdn-website.com/07727de3/dms3rep/multi/opt/walton-picture_2_orig-3c3649c6-720w.jpg|https://lirp.cdn-website.com/07727de3/dms3rep/multi/opt/pexels-mark-mccammon-1080719-1920w.jpg|https://lirp.cdn-website.com/07727de3/dms3rep/multi/opt/Belmonte-builders-002-1920w.jpg|https://lirp.cdn-website.com/md/dmtmpl/adf13b6a-699d-4fcf-82e8-b8210c4030b4/dms3rep/multi/opt/modern_villa_outdoor-1920w.jpg|https://lirp.cdn-website.com/07727de3/dms3rep/multi/opt/family+dinner-1920w.jpg"
        item2['SubWebsite'] = 'https://www.cchofwaunakee.com/'
        item2['AmenityType'] = ''
        yield item2

        link = 'https://www.findohomes.com/floor-plans'
        yield scrapy.FormRequest(url=link,callback=self.plans,dont_filter=True,headers=self.headers)

    def plans(self,response):

        divs = response.xpath("//div[@class='dmRespColsWrapper']/div/div//div[contains(@class,'u_')]/following-sibling::div[contains(@class,'u_')]//h2")
        for div in divs:

            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                PlanName = div.xpath('.//text()').extract_first(
                    default='').strip()
                print(PlanName)
            except Exception as e:
                print(e)

            try:
                PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
                print(PlanName)
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
                Baths = div.xpath("./../..//span[contains(text(),'Bed')]/text()").extract_first(default='0').strip().replace(",", "")
                Baths = re.findall(r'(.*?) Bathroo', Baths)[0]
                Baths = Baths.split("/")[-1]
                if '+' in Baths:
                    Baths = Baths.split("+")
                Baths = re.findall(r"(\d+)", Baths)
                Bath = Baths[0]
                print(Baths)
                if len(Baths) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                print(e)

            try:
                Bedrooms = div.xpath("./../..//span[contains(text(),'Bed')]/text()").extract_first(default='0').strip().replace(",", "")
                Bedrooms = re.findall(r'(.*?) Bedrooms', Bedrooms)[0]
                Bedrooms = Bedrooms.split("/")[-1]
                Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
                print(Bedrooms)
            except Exception as e:
                print(e)

            try:
                Garage = div.xpath("./../..//span[contains(text(),'Garage')]/text()").extract_first(default='0').strip().replace(",","")
                Garage = re.findall(r'(.*?) Garage', Garage)[0]
                Garage = Garage.split("/")[-1]
                Garage = re.findall(r"(\d+)", Garage)[0]
                print(Garage)
            except Exception as e:
                print(e)
                Garage = 0.0

            try:
                BaseSqft = div.xpath(".//../..//span[contains(text(),'Bed')]/text()").extract_first(default='0').strip().replace(",", "")
                BaseSqft = re.findall(r'(.*?) Sq', BaseSqft)[0]
                BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
                print(BaseSqft)

            except Exception as e:
                print(e)

            try:
                Description = "".join(response.xpath(".//../..//div[contains(@class,'dmNewParagraph')][2]/p/span/text()").extract()).strip().encode('ascii', 'ignore')
                # print(Description)
                Description = Description.encode('ascii', 'ignore')
            except Exception as e:
                Description = ''

            try:
                images = []
                image1 = div.xpath('.//../..//img/@src').extract()
                if image1 != []:
                    for im in image1:
                        images.append(im)

                ElevationImage = "|".join(images)
            except Exception as e:
                print(e)
                ElevationImage = ''

            try:
                PlanWebsite = response.url
            except Exception as e:
                print(e)

                # SubdivisionNumber = SubdivisionNumber #if subdivision is there
            SubdivisionNumber = self.builderNumber  # if subdivision is not available
            unique = str(PlanName) + str(SubdivisionNumber)
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

            ink = 'https://www.findohomes.com'
            yield scrapy.FormRequest(url=ink,callback=self.parse,dont_filter=True,headers=self.headers)

    def parse(self, response):
        links = response.xpath("//span[contains(text(),'Explore')]/../@href").extract()
        for link in links:
            link = 'https://www.findohomes.com'+ link
            print(link)

            yield scrapy.FormRequest(url=link, callback=self.communities,dont_filter="True" , headers=self.headers)

    def communities(self, response):

        # ------------------- Creating Communities ---------------------- #
        subdivisonName = response.xpath('//h2/span/text()').extract_first(default="")
        print(subdivisonName)
        subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)

        f = open("html/%s.html" % subdivisonNumber, "wb")
        f.write(response.body)
        f.close()

        contactTmp = response.xpath('//div[@class="dmNewParagraph"]/p[2]/span/text()').extract_first('')

        try:
            desc = "".join(response.xpath('//div[@class="dmNewParagraph"]/p/span/text()').extract())
            desc = desc.split(contactTmp)[1]
        except Exception as e:
            print(e)
            desc= ''

        try:
            image = response.xpath('//li[@animation="fadeInUp"]/img/@src').extract()
            image = "|".join(image)
        except Exception as e:
            print(e)
            image = ""

        a = []
        amenity_list = ["Pool", "Playground", "GolfCourse", "Tennis", "Soccer", "Volleyball", "Basketball",
                        "Baseball", "Views", "Lake", "Pond", "Marina", "Beach", "WaterfrontLots", "Park",
                        "Trails", "Greenbelt", "Clubhouse", "CommunityCenter"]
        for i in amenity_list:
            if i in desc:
                a.append(i)
        ab = '|'.join(a)


        street1 = ''
        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionName'] = subdivisonName
        item2['SubdivisionNumber'] = subdivisonNumber
        item2['BuilderNumber'] = self.builderNumber
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 1
        item2['Street1'] = street1
        item2['City'] = contactTmp.split(",")[0].strip()
        item2['State'] = contactTmp.split(",")[1].split(" ")[0].strip()
        item2['ZIP'] = contactTmp.split(",")[1].split(" ")[1].strip()
        item2['AreaCode'] = ''
        item2['Prefix'] = ''
        item2['Suffix'] = ''
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = desc
        item2['SubImage'] = image
        item2['SubWebsite'] = response.url
        item2['AmenityType'] = ab
        yield item2

        item = BdxCrawlingItem_Plan()
        unique = str("Plan Unknown") + str(self.builderNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
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

        spec_divs = response.xpath("//div[@class='dmRespColsWrapper']/div[contains(@class,'medium-12 large-12')]/div/h3[1]")
        for spec in spec_divs:

            try:
                SpecStreet1 =  spec.xpath(".//text()").extract_first('')
                contact =  "".join(spec.xpath(".//../h3[2]//span/text()").extract())
                spec_city = contact.split(",")[0]
                spec_state = contact.split(",")[1].strip().split(" ")[0]
                spec_zip = contact.split(",")[1].strip().split(" ")[1]
            except Exception as e:
                print(e)
                SpecStreet1,spec_city,spec_state,spec_zip = '','','',''


            try:
                SpecPrice = ''.join(spec.xpath(".//../..//span[contains(text(),'Price: ')]/text()").extract()).replace(',', '').replace('$', '').strip()
                SpecPrice = re.findall(r"(\d+)", SpecPrice)[0]
            except Exception as e:
                print("SpecPrice---------->", e)
                SpecPrice = '0'


            unique = SpecStreet1 + spec_city + spec_state + spec_zip
            SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            try:
                SpecSqft = ''
            except Exception as e:
                print("SpecSqft---------->", e)

            try:
                SpecBaths = ''.join(spec.xpath(".//../..//span[contains(text(),'Full Baths: ')]/text()").extract()).strip()
                SpecBaths = re.findall(r"(\d+)", SpecBaths)[0]
                SpecHalfBaths = ''.join(spec.xpath(".//../..//span[contains(text(),'Half Bath')]/text()").extract()).strip()
                SpecHalfBaths = re.findall(r"(\d+)", SpecHalfBaths)[0]
            except Exception as e:
                print("SpecBaths--------->", e)

            try:
                SpecBedrooms = ''.join(spec.xpath(".//../..//span[contains(text(),'Bedrooms: ')]/text()").extract()).strip()
                SpecBedrooms = re.findall(r"(\d+)", SpecBedrooms)[0]
            except Exception as e:
                print(e)
                SpecBedrooms = ''

            try:
               garage = '0'
            except Exception as e:
                print(e)
                garage = '0'

            try:
                img = spec.xpath('.//../../../../../..//ul[@class="slides"]/li/img/@src').extract()
                SpecElevationImage = "|".join(img)
            except Exception as e:
                SpecElevationImage = ''
                print(e)

            item = BdxCrawlingItem_Spec()
            item['SpecNumber'] = SpecNumber
            item['PlanNumber'] = unique_number
            item['SpecStreet1'] = SpecStreet1
            item['SpecCity'] = spec_city
            item['SpecState'] = spec_state
            item['SpecZIP'] = spec_zip
            item['SpecCountry'] = 'USA'
            item['SpecPrice'] = SpecPrice
            item['SpecSqft'] = SpecSqft
            item['SpecBaths'] = SpecBaths
            item['SpecHalfBaths'] = SpecHalfBaths
            item['SpecBedrooms'] = SpecBedrooms
            item['MasterBedLocation'] = 0
            item['SpecGarage'] = garage
            item['SpecDescription'] = ''
            item['SpecElevationImage'] = SpecElevationImage
            item['SpecWebsite'] = response.url
            yield item





if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl findohomes".split())

