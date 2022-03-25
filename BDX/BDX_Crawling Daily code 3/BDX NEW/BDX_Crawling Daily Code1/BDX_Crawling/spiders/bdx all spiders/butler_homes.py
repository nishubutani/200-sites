# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from scrapy.cmdline import execute
from scrapy.utils.response import open_in_browser

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class butlerhomesSpider(scrapy.Spider):
    name = 'butler_homes'
    allowed_domains = ['www.butlerhomesllc.com/']
    start_urls = ['http://butlerhomesllc.com/']

    builderNumber = "23470"


    def parse(self, response):
        yield scrapy.FormRequest(url='https://www.butlerhomesllc.com/communities',callback=self.parse2,dont_filter=True)

    def parse2(self,response):
        links = response.xpath('//a[@class="CommunityCard_detailButton"]/@href').extract()
        for link in links:
            link = 'https://www.butlerhomesllc.com' + link
            yield scrapy.FormRequest(url=link, callback=self.parse3,dont_filter=True)


    def parse3(self,response):

        # ---------------------------Extracting Communities Details ------------------------------------ #
        url = response.url
        try:
            SubDescription = ''.join(response.xpath('//p[@class="text-lg-center"]/text()').getall())
            if not SubDescription:
                SubDescription = ''
        except Exception as e:
            print(e)

        # try:
        #     if 'Coming Soon!' in SubDescription:
        #         sub_Status = 'ComingSoon'
        #     else:
        #         sub_Status = 'Active'
        #
        # except Exception as e:
        #     print(e)
        try:
            sub_Status = response.xpath("//*[contains(text(),'Status:')]/../text()").extract_first()
        except Exception as e:
            print(e)
            sub_Status = ''

        if sub_Status != 'Sold Out' and sub_Status != 'Coming Soon':

            try:
                BuilderNumber = self.builderNumber
            except Exception as e:
                print(e)

            try:
                SubdivisionName = response.xpath('//h1[@class="DetailHeader_heading"]/text()').get().strip()
            except Exception as e:
                SubdivisionName = ''
                print(e)

            try:
                SubdivisionNumber = int(hashlib.md5(bytes(SubdivisionName + url, "utf8")).hexdigest(), 16) % (10 ** 30)
            except Exception as e:
                SubdivisionNumber = ''
                print(e)

            try:
                BuildOnYourLot = 1 if "build-on-your-lot" in str(response.url) else 0
            except Exception as e:
                print(e)

            try:
                OutOfCommunity = 1
            except Exception as e:
                print(e)

            try:

                City = response.xpath('//li[@class="DetailHeader_detailsListItem"][1]/text()[2]').extract_first()
                Street1 = response.xpath('//li[@class="DetailHeader_detailsListItem"][1]/text()[1]').extract_first()
                State = response.xpath('//li[@class="DetailHeader_detailsListItem"][1]/text()[4]').extract_first()
                ZIP = response.xpath('//li[@class="DetailHeader_detailsListItem"][1]/text()[6]').extract_first()

            except Exception as e:
                print(e)

            try:
                Email = "ContactUs@butlerhomesllc.com"
            except Exception as e:
                print(e)


            try:
                images = []
                SubImage = response.xpath('//li[@class="PhotoList_item"]/span/div/@style').extract()
                if SubImage == []:
                    SubImage = response.xpath('//div[@class="PhotoList_image"]/@style').extract()
                for image in SubImage:
                    # print(image)
                    image = image.split("background-image:url('")[1]
                    # print(image)
                    image = image.split("');")[0]
                    # print(image)
                    images.append(image)
                # print(images)
                images = "|".join(images)
                print(images)
            except Exception as e:
                SubImage = ""

            try:
                SubWebsite = response.url
            except Exception as e:
                print(e)

            a = []
            # aminity = ''.join(response.xpath('//*[@class="ll-features-content__half right col-md-1of2"]/ul[1]/li/text()').extract())
            try:
                aminity = ''.join(response.xpath(
                    '//p[@class="text-lg-center"]/text()').extract())
            except Exception as e:
                print(e)

            amenity_list = ["Pool", "Playground", "GolfCourse", "Tennis", "Soccer", "Volleyball", "Basketball",
                            "Baseball", "Views", "Lake", "Pond", "Marina", "Beach", "WaterfrontLots", "Park",
                            "Trails", "Greenbelt", "Clubhouse", "CommunityCenter"]
            for i in amenity_list:
                if i in aminity:
                    a.append(i)
            ab = '|'.join(a)


            # ----------------------- Don't change anything here --------------
            item2 = BdxCrawlingItem_subdivision()
            item2['sub_Status'] = sub_Status
            item2['SubdivisionNumber'] = SubdivisionNumber
            item2['BuilderNumber'] = BuilderNumber
            item2['SubdivisionName'] = SubdivisionName
            item2['BuildOnYourLot'] = BuildOnYourLot
            item2['OutOfCommunity'] = OutOfCommunity
            item2['Street1'] = Street1
            item2['City'] = City
            item2['State'] = State
            item2['ZIP'] = ZIP
            item2['AreaCode'] = "918"
            item2['Prefix'] = "824"
            item2['Suffix'] = "2700"
            item2['Extension'] = ''
            item2['Email'] = Email
            item2['SubDescription'] = SubDescription
            item2['SubImage'] = images
            item2['SubWebsite'] = SubWebsite
            item2['AmenityType'] = ab
            yield item2
            print(response.url)
            #---------------------- for plan -----------------#

            links = response.xpath('//h4[@class="Extra_Padding"]/a/@href').extract()
            for link in links:
                link = 'https://www.butlerhomesllc.com' + link
                # link = 'https://www.butlerhomesllc.com/plan/vale-at-redbud/breckenridge'
                yield scrapy.FormRequest(url=link,callback=self.parse4,dont_filter=True,meta={'sbdn':SubdivisionNumber,"SubdivisionName":SubdivisionName})


    def parse4(self,response):

        SubdivisionName = response.meta['SubdivisionName']

        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//h1[@class="DetailHeader_heading"]/text()[1]').get()
        except Exception as e:
            PlanName = ''
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName+SubdivisionName+response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            PlanNumber = ''
            print(e)

        try:
            SubdivisionNumber = response.meta['sbdn']
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
            sqft = response.xpath('//img[@alt="Icon Sqft"]/../span/b/text()').get()
            sqft = sqft.replace(',','').strip()
            BaseSqft = re.findall(r"(\d+)", sqft)[0]

        except Exception as e:
            print(e)

        try:
            bath = "".join(response.xpath('//img[@alt="Icon Baths"]/../span//b/text()').extract()).replace(" ","")
            print(bath)

            Baths = re.findall(r"(\d+)", bath)[0]
            tmp = re.findall(r"(\d+)", bath)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            print(e)

        try:
            Bedrooms = "".join(response.xpath('//img[@alt="Icon Beds"]/../span//b/text()').extract())
            if '-' in Bedrooms:
                Bedrooms = Bedrooms.split("-")[1]

            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)

        try:
            Garage = response.xpath('//img[@alt="Icon Garage"]/../span//b/text()').get()
            Garage = re.findall(r"(\d+)", Garage)[0]
            if not Garage:
                Garage = 0
        except Exception as e:
            Garage = 0
            print(e)

        try:
            Description = ''.join(response.xpath('//p[@class="Testimonial_body"]/text()').getall())
            if not Description:
                Description = ''
        except Exception as e:
            print(e)

        try:

            image1 = response.xpath('//div[@class="PhotoList_image"]/@style').extract_first('')
            if image1 != '':
                image1 = image1.split("background-image:url('")[1]
                image1 = image1.split("');")[0]


            image2 = response.xpath('//div[@class="PhotoList_image-vertical"]/@style').extract_first('')
            if image2 !='':
                image2 = image2.split("background-image:url('")[1]
                image2 = image2.split("');")[0]
                print(image2)

            if image1 != '':
                if image2 != '':
                    images = image2 + '|' + image1
                    ElevationImage = images
                else:
                    ElevationImage = image1
        except Exception as e:
            print(e)
            ElevationImage = ''

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



        #---- home code starts here ------------------#


        lik = 'https://www.butlerhomesllc.com/homes'
        yield scrapy.FormRequest(url=lik,callback=self.parse5,dont_filter=True,meta={'pn':unique_number,'PlanName':PlanName})


    def parse5(self,response):

        pn = response.meta['pn']
        PlanName = response.meta['PlanName']
        # links = response.xpath('//a[@class="ViewHomeBtn"]/@href').extract()
        links = response.xpath('//span[@class="HomecardStatus-overlayModel"]/../@href').extract()
        for link in links:
            link = 'https://www.butlerhomesllc.com' + link
            yield scrapy.FormRequest(url=link,callback=self.parse6,dont_filter=True,meta={'pn':pn,'PlanName':PlanName})

    def parse6(self,response):

        pn = response.meta['pn']
        PlanName_old = response.meta['PlanName']

        planName = response.xpath('//li[@class="DetailHeader_detailsListItem"]/a/text()').extract_first(default='').strip()
        print(planName)

        if planName == PlanName_old:

            address = response.xpath('//h1[@class="DetailHeader_heading"]/text()[1]').extract_first(default='').strip()
            print(address)

            SpecCity = response.xpath('//h1[@class="DetailHeader_heading"]/span/text()[1]').extract_first('').strip()
            print(SpecCity)

            SpecState = response.xpath('//h1[@class="DetailHeader_heading"]/span/text()[3]').extract_first('').strip()
            print(SpecState)


            SpecZIP = response.xpath('//h1[@class="DetailHeader_heading"]/span/text()[5]').extract_first('').strip()
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
                SpecPrice = response.xpath('//h3[@class="DetailHeader_price"]/text()').extract_first().replace(",", "")
                SpecPrice = re.findall(r"(\d+)", SpecPrice)[0]
            except Exception as e:
                print(e)

            try:
                SpecSqft = response.xpath('//img[@alt="Icon Sqft"]/../span/b/text()').extract_first().replace(",", "")
                SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
                print(SpecSqft)
            except Exception as e:
                print(e)

            try:
                SpecBaths = "".join(response.xpath('//ul[@class="DetailHeader_iconList"]//img[@alt="Icon Baths"]/../span/b//text()').extract()).strip().replace(",", "").replace(" ","")
                tmp = re.findall(r"(\d+)", SpecBaths)
                SpecBaths = tmp[0]
                if len(tmp) > 1:
                    SpecHalfBaths = 1
                else:
                    SpecHalfBaths = 0
            except Exception as e:
                print(e)

            try:
                SpecBedrooms = response.xpath('//ul[@class="DetailHeader_iconList"]//img[@alt="Icon Beds"]/../span/b//text()').extract_first()
                SpecBedrooms = re.findall(r'(\d+)', SpecBedrooms)[0]
            except Exception as e:
                print(e)

            try:
                MasterBedLocation = "Down"
            except Exception as e:
                print(e)

            try:
                SpecGarage = response.xpath('//img[@alt="Icon Garage"]/../span/b/text()').extract_first(
                    default='0')
                SpecGarage = re.findall(r"(\d+)", SpecGarage)[0]
            except Exception as e:
                print(e)

            try:
                SpecDescription = "Love the people that helped make my dream home! Becky and Rick are amazing!"
            except Exception as e:
                print(e)

            try:

                images = []
                SubImage = response.xpath('//li[@class="PhotoList_item"]/span/div/@style').extract()
                for image in SubImage:
                    image = image.split("background-image:url('")[1]
                    image = image.split("');")[0]
                    images.append(image)
                ElevationImage = "|".join(images)
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
            item['PlanNumber'] = pn
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
    execute('scrapy crawl butler_homes'.split())


