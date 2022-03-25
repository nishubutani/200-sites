# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from scrapy.cmdline import execute
from scrapy.utils.response import open_in_browser

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class byrdhomebuildersSpider(scrapy.Spider):
    name = 'cewurzer_builders'
    allowed_domains = ['www.cewurzerbuilders.com/']
    start_urls = ['https://www.cewurzerbuilders.com/']
    builderNumber = "53164"

    def parse(self, response):
        images = ''
        # image = response.xpath('//*[contains(@src,"/images")]/@src').extract()
        image = response.xpath('//a[@title="View Gallery"]/@href').extract()
        for i in image:
            images = images + self.start_urls[0] + i + '|'
        images = images.strip('|')
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '1750 US-53 BUS'
        item['City'] = 'Chippewa Falls '
        item['State'] = 'WI '
        item['ZIP'] = '54729'
        item['AreaCode'] = '715'
        item['Prefix'] = '839'
        item['Suffix'] = '8806'
        item['Extension'] = ""
        item['Email'] = 'craig@cewurzerbuilders.com'
        item['SubDescription'] = 'We are more than happy to answer any questions you may have about our company, building process, experience, or general questions about building your custom home or general contracting in Eau Claire, WI. You can use the contact form below and well receive your request via email. Or, you can use the contact information at the right and reach us by phone or mail. We look forward to hearing from you soon!'
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        item['AmenityType'] = ""
        yield item

        # url = 'https://www.cewurzerbuilders.com/lookbook'
        url = 'https://www.cewurzerbuilders.com/homes/pre-packaged-plans/'
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.parse_planlink,
            meta={'sbdn': self.builderNumber})

    def parse_planlink(self, response):

        try:
            # links = response.xpath('//article[@class="lookbook highlight"]/a/@href').extract()
            links = response.xpath('//ul[@class="flexbox"]/li/a/@href').extract()
            plandetains = {}
            for link in links:
                yield scrapy.Request(url=self.start_urls[0]+ str(link),
                                     callback=self.plans_details,
                                     meta={'sbdn': self.builderNumber, 'PlanDetails': plandetains}, dont_filter=True)
        except Exception as e:
            print(e)

    def plans_details(self, response):
        global HalfBaths, PlanName
        plandetails = response.meta['PlanDetails']
        item = BdxCrawlingItem_Plan()

        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = response.meta['sbdn']
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath(
                '//div[@class="home-details-header"]//div/text()').extract_first(
                default='').strip()
            print(PlanName)

        except Exception as e:
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
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
            BasePrice = response.xpath('//div[@class="home-share"]/h1/text()').extract_first().replace(",", "")
            BasePrice = re.findall(r"(\d+)", BasePrice)[0]
        except Exception as e:
            print(e)
            BasePrice = '0'

        try:
            Baths1 = response.xpath('//span[@class="home-icon bath-icon"]/../strong/text()').extract_first('').strip().replace(",", "")
            Baths = re.findall(r"(\d+)", Baths1)
            # Baths = re.findall(r"(\d+)", Baths)[0]
            tmp = re.findall(r"(\d+)", Baths1)
            print(Baths)
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0


        except Exception as e:
            print(e)

        try:

            Bedrooms = response.xpath('//span[@class="home-icon bed-icon"]/../strong/text()').extract_first(
                default='0').strip().replace(",", "")
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            print(Bedrooms)

        except Exception as e:
            print(e)

        try:

            Garage = response.xpath("//*[contains(text(),'Car Garage')]").extract_first()
            Garage = Garage.split(" Car Garage")[0].split()[-1]
            Garage = re.findall(r"(\d+)", Garage)[0]

        except Exception as e:
            print(e)
            Garage = ''

        try:

            BaseSqft = str(response.xpath(
                '//span[@class="home-icon sq-icon"]/../strong/text()').extract_first(
                default='0').strip()).replace(",", "")
            # BaseSqft = BaseSqft.split(":")[1]
            # BaseSqft = BaseSqft.split(" ")[-2]
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
            print(BaseSqft)

        except Exception as e:
            print(e)

        try:

            Description = response.xpath('//div[@class="prop-details"]/div/p/text()').extract_first(
            default='').strip()
            print(Description)

        except Exception as e:
            print(e)

        try:
            images = ''
            image = response.xpath('//ul[@class="project-gallery"]/li/a/@href').extract()
            for i in image:
                images = images + 'https://www.cewurzerbuilders.com/' + str(i).replace("..","") + '|'
            images = images.strip('|')
            ElevationImage = images
            print(ElevationImage)

        except Exception as e:
            ElevationImage = ''
            print(e)

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

        SubdivisionNumber = SubdivisionNumber  # if subdivision is there
        # SubdivisionNumber = self.builderNumber #if subdivision is not available
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        plandetails[PlanName] = unique_number

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
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = Description
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item

        # link = 'https://www.cewurzerbuilders.com/homes/homes-for-sale/'
        link = 'https://www.cewurzerbuilders.com/homes/homes-for-sale/?pg=1'
        yield scrapy.FormRequest(url=link,callback=self.homelinks,dont_filter=True)

    def homelinks(self,response):
        links = response.xpath('//ul[@class="flexbox"]/li/a/@href').extract()
        for link in links:
            link = 'https://www.cewurzerbuilders.com' + link
            yield scrapy.FormRequest(url=link,callback=self.home,dont_filter=True)
            # yield scrapy.FormRequest(url='https://www.cewurzerbuilders.com/homes/homes-for-sale/14/',callback=self.home,dont_filter=True)

    def home(self,response):
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


        # ------------------- home code stats here ---------------------#


        try:
            address = response.xpath('//h1/div/text()').extract_first(default='').strip()
            print(address)

            add = response.xpath('//h1/div/span/text()').extract_first('').strip().replace("\t","")
            print(add)

            SpecCity = add.split(" ")[0].strip()
            SpecState = add.split(" ")[2].strip().replace("Wisconsin","WI").replace("Minnesota","MN")
            SpecZIP = add.split(" ")[4].strip()

            if SpecState == '':
                SpecCity1 = add.split(" ")[0].strip()
                SpecCity2 = add.split(" ")[1].strip()
                SpecCity = SpecCity1 + ''+ SpecCity2
                SpecState = add.split(" ")[3].strip().replace("Wisconsin", "WI").replace("Minnesota","MN")
                SpecZIP = add.split(" ")[5].strip()

            SpecStreet1 = address
        except Exception as e:
            print(e)
            SpecStreet1,SpecCity,SpecState,SpecZIP = '','','',''

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
            SpecPrice = response.xpath('//div[@class="home-share"]/h1/text()').extract_first().replace(",", "")
            SpecPrice = re.findall(r"(\d+)", SpecPrice)[0]
        except Exception as e:
            print(e)
            SpecPrice = 0

        try:
            SpecSqft = response.xpath('//span[@class="home-icon sq-icon"]/../strong/text()').extract_first().replace(",", "")
            SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
            print(SpecSqft)
        except Exception as e:
            print(e)

        try:
            SpecBaths = "".join(
                response.xpath('//span[@class="home-icon bath-icon"]/../strong/text()').extract()).strip().replace(",",
                                                                                                        "").replace(
                " ", "")
            tmp = re.findall(r"(\d+)", SpecBaths)
            SpecBaths = tmp[0]
            if len(tmp) > 1:
                SpecHalfBaths = 1
            else:
                SpecHalfBaths = 0
        except Exception as e:
            print(e)
            SpecBaths,SpecHalfBaths = 0,0

        try:
            SpecBedrooms = response.xpath('//span[@class="home-icon bed-icon"]/../strong/text()').extract_first()
            SpecBedrooms = re.findall(r'(\d+)', SpecBedrooms)[0]
        except Exception as e:
            print(e)

        try:
            MasterBedLocation = "Down"
        except Exception as e:
            print(e)


        SpecGarage = '0.0'

        try:
            SpecDescription = response.xpath('//div[@class="prop-details"]/div/p/text()').extract_first('')
            if SpecDescription == '':
                SpecDescription = response.xpath('//div[@class="prop-details"]/div/span/text()').extract_first('')
                if SpecDescription == '':
                    SpecDescription = "".join(response.xpath('//div[@class="prop-details"]/div//text()').extract())
        except Exception as e:
            print(e)
            SpecDescription=''

        try:

            images = []
            SubImage = response.xpath('//ul[@class="project-gallery"]/li/a/@href').extract()
            for image in SubImage:
                image = 'https://www.cewurzerbuilders.com' + image
                images.append(image)
            ElevationImage = "|".join(images)
            SpecElevationImage = ElevationImage
            if SpecElevationImage == 'https://www.cewurzerbuilders.com':
                SpecElevationImage =''
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
        if item['SpecElevationImage'] == '':
            item['SpecElevationImage'] = 'https://www.cewurzerbuilders.com/assets/images/2020/11/large/lot-41-keanan-lane-front.jpg'
        item['SpecWebsite'] = SpecWebsite
        yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl cewurzer_builders'.split())