# -*- coding: utf-8 -*-
import hashlib
import re
import requests
import scrapy
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class CavinessCatesBuildingandDevelopmentSpider(scrapy.Spider):
    name = 'Caviness_Cates_Building_and_Development'
    allowed_domains = ['https://www.cavinessandcates.com/']
    start_urls = ['https://www.cavinessandcates.com/']

    builderNumber = "56939"


    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #
        # image1 = '|'.join(response.xpath('//*[@class="widget-gem-portfolio-item  "]/img/@src').extract())
        # image = '|'.join(response.xpath('//div[@id="details"]/div[2]//img/@src').extract())
        # images = f"{image1}|{image}"
        # item = BdxCrawlingItem_subdivision()
        # item['sub_Status'] = "Active"
        # item['SubdivisionNumber'] = ''
        # item['BuilderNumber'] = self.builderNumber
        # item['SubdivisionName'] = "No Sub Division"
        # item['BuildOnYourLot'] = 0
        # item['OutOfCommunity'] = 0
        # item['Street1'] = "6703 Greyson Dr"
        # item['City'] = "Papillion"
        # item['State'] = "NE"
        # item['ZIP'] = "68133"
        # item['AreaCode'] = "402"
        # item['Prefix'] = "250"
        # item['Suffix'] = "3431"
        # item['Extension'] = ""
        # item['Email'] = "petersabal1@aol.com"
        # item[
        #     'SubDescription'] = "At Castlebridge Homes, Inc. we strive to make your home building experience a pleasant one. Our goal is to provide you with an affordable quality custom home which will offer you years of enjoyment."
        # item['SubImage'] = images
        # item['SubWebsite'] = "https://castlebridgehomesomaha.com"
        # yield item
        # try:
        #     link1 = response.xpath('//a[contains(text(),"Home Designs")]/@href').extract_first()
        #     res = requests.get(url=link1)
        #     response1 = HtmlResponse(url=res.url, body=res.content)
        #     links = response1.xpath('//*[@class="portfolio-icons"]/a[1]/@href').extract()
        #     plandetains = {}
        #     for link in links:
        #         yield scrapy.Request(url=link, callback=self.plans_details,
        #                              meta={'sbdn': self.builderNumber, 'PlanDetails': plandetains}, dont_filter=True)
        # except Exception as e:
        #     print(e)

        # IF you have Communities
        links = response.xpath('//*[@aria-labelledby="ourHomesDropdown"]/a/@href').extract()
        for link in links:
            url = "https://www.cavinessandcates.com"+link
            yield scrapy.Request(url=str(url), callback=self.parse_communities, dont_filter=True)

    def parse_communities(self,response):
        links = response.xpath('//a[@class="oi-aspect sixteen-nine"]/@href').extract()
        for link in links:
            url = "https://www.cavinessandcates.com" + link
            yield scrapy.Request(url=str(url), callback=self.process_communities, dont_filter=True)

    def process_communities(self,response):
        try:
            address = response.xpath('//*[@class="container-fluid"]/div/div[2]//text()').extract()
            image = '|'.join(response.xpath('//img[@class="oi-aspect-img oi-image-click"]/@src').extract())
            images = image.strip('|')
            comm_id = response.url.split('/')[-3]
            SubdivisionName = response.xpath('//h1/text()').extract_first().strip()
            SubdivisionNumber = int(hashlib.md5(bytes(SubdivisionName + str(self.builderNumber) + str(comm_id), "utf8")).hexdigest(), 16) % (10 ** 30)
            if response.xpath('//*[@class="row"]/following-sibling::div/p/text()'):
                SubDescription = response.xpath('//*[@class="row"]/following-sibling::div/p/text()').extract_first().strip()
            elif response.xpath('//*[contains(@class,"wysiwyg")]/div/text()'):
                SubDescription = response.xpath('//*[contains(@class,"wysiwyg")]/div/text()').extract_first().strip()
            else:
                SubDescription = 'You’ll know you’re home when you explore an impeccably designed Caviness & Cates community. Every new home and customer is given our undivided attention throughout each phase of construction. It’s this attention to detail that creates exceptional results for homeowners in Fayetteville, Raleigh, Greenville, Wilmington, Jacksonville and Southern Pines areas. Find your new home in North Carolina and start making memories today!'
            item = BdxCrawlingItem_subdivision()
            item['sub_Status'] = "Active"
            item['SubdivisionNumber'] = SubdivisionNumber
            item['BuilderNumber'] = self.builderNumber
            item['SubdivisionName'] = SubdivisionName
            item['BuildOnYourLot'] = 0
            item['OutOfCommunity'] = 1
            item['Street1'] = address[0].strip()
            item['City'] = address[1].split(',')[0].strip()
            item['State'] = address[1].split(',')[1].split()[0].strip()
            item['ZIP'] = address[1].split(',')[1].split()[1].strip()
            item['AreaCode'] = "910"
            item['Prefix'] = "481"
            item['Suffix'] = "0503"
            item['Extension'] = ""
            item['Email'] = "jenn@cavinessandcates.com"
            item['SubDescription'] = SubDescription
            item['SubImage'] = images
            item['SubWebsite'] = response.url
            yield item

            plan_links = response.xpath('//*[contains(@class,"caviness-pane p-3") and contains(@id,"2")]/div/div/div/div/a[1]/@href').extract()
            for plan_link in plan_links:
                plandetails = {}
                yield scrapy.Request(url="https://www.cavinessandcates.com" + str(plan_link),callback=self.process_plan, dont_filter=True,
                                     meta={'SubdivisionNumber': SubdivisionNumber,'plandetails':plandetails,'comm_id':comm_id})

        except Exception as e:
            print(e)

    def process_plan(self,response):
        plandetails = response.meta['plandetails']
        comm_id = response.meta['comm_id']
        comm_id2 = response.xpath('//a[contains(text(),"VIEW COMMUNITY")]/@href').extract_first()
        comm_id2 = comm_id2.split('/')[-3]
        if comm_id == comm_id2:
            try:
                PlanName = response.xpath('//h1[contains(@class,"caviness-title")]/text()').extract_first(default='').strip()
                if '–' in PlanName:
                    PlanName = PlanName.split('–')[0].strip()
            except Exception as e:
                print(e)

            try:
                BasePrice = response.xpath('//span[contains(text(),"from $")]/text()').extract_first(default='0').strip()
                BasePrice = BasePrice.replace("from $",'').replace(",",'').strip()
            except Exception as e:
                print(e)

            try:
                PlanNumber = int(hashlib.md5(bytes(response.url + str(PlanName) + str(BasePrice) + str(comm_id), "utf8")).hexdigest(),16) % (10 ** 30)
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
                Baths = str(response.xpath('//span[contains(text(),"Bath")]/b/text()').extract_first(default='0').strip())
                tmp = re.findall(r"(\d+)", Baths)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                print(e)

            try:
                Bedrooms = str(response.xpath('//span[contains(text(),"Bed")]/b/text()').extract_first(default='0').strip())
                Bedrooms = re.findall(r'(\d+)',Bedrooms)[0]
            except Exception as e:
                print(e)

            try:
                Garage = response.xpath('//span[contains(text(),"Garage")]/b/text()').extract_first(default='0')
                if '-' in Garage:
                    Garage_list = Garage.split('-')
                    if int(Garage_list[0]) > int(Garage_list[1]):
                        Garage = Garage_list[0]
                    else:
                        Garage = Garage_list[1]
                BaseSqft = response.xpath('//span[contains(text(),"Sq. Ft.")]/b/text()').extract_first(default='0').replace(",", "")
            except Exception as e:
                print(e)

            try:
                Description = ''.join(response.xpath('//*[contains(@class,"wysiwyg")]/ul/li/text()').extract()).strip()
            except Exception as e:
                print(e)

            try:
                ElevationImage1 = '|'.join(response.xpath('//*[@data-fancybox="elevation-images"]/@href').extract())
                GallaryImage = '|'.join(response.xpath('//*[@data-fancybox="gallery-images"]/@href').extract())
                floorplanImage = '|'.join(response.xpath('//img[@class="d-none"]/@src').extract())
                ElevationImage = ElevationImage1.strip('|')+GallaryImage.strip('|')+floorplanImage.strip('|')
            except Exception as e:
                print(e)

            try:
                PlanWebsite = response.url
            except Exception as e:
                print(e)
            try:
                SubdivisionNumber = response.meta['SubdivisionNumber'] #if subdivision is there
                #SubdivisionNumber = self.builderNumber #if subdivision is not available
                unique = str(PlanNumber)+str(SubdivisionNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                plandetails[PlanName] = unique_number
                item = BdxCrawlingItem_Plan()
                item['Type'] = 'SingleFamily'
                item['PlanNumber'] = PlanNumber
                item['unique_number'] = unique_number
                item['SubdivisionNumber'] = SubdivisionNumber
                item['PlanName'] = PlanName
                item['PlanNotAvailable'] = PlanNotAvailable
                item['PlanTypeName'] = 'Single Family'
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

            home_links = response.xpath('//*[@class="oi-aspect sixteen-nine oi-image-click"]/@href').extract()
            for home_link in home_links:
                yield scrapy.Request(url="https://www.cavinessandcates.com" + str(home_link),callback=self.process_home, dont_filter=True,
                                     meta={'SubdivisionNumber': SubdivisionNumber,"PN": plandetails,"comm_id":comm_id,'unique_number':unique_number})
        else:
            print("Plan and subdivision does not match")

    def process_home(self, response):
        if response.xpath('//h1[contains(text(),"Under Construction!")]'):
            print("Under Construction!")
        else:
            unique_number = response.meta['unique_number']
            PN = response.meta['PN']
            address = response.xpath('//*[@class="text-tundora"]/text()').extract()
            try:
                SpecStreet1 = response.xpath('//h1/text()').extract_first()
            except Exception as e:
                print(str(e))

            try:
                SpecCity = address[1].split()[0].strip()
            except Exception as e:
                print(str(e))

            try:
                SpecState = address[1].split()[1].strip()
            except Exception as e:
               print(str(e))

            try:
                SpecZIP = address[1].split()[2].strip()
            except Exception as e:
                print(str(e))

            unique = SpecStreet1 + SpecCity + SpecState + SpecZIP + str(response.url)
            SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

            try:
                planName = re.findall(r'Floorplan:(.*?)</b>',response.text)
                if len(planName) == 1:
                    planName = re.findall(r'>(.*?)$',planName[0])[0].strip()
                    for key,value in PN.items():
                        if planName in key:
                            PlanNumber = PN[key]
            except Exception as e:
                PlanNumber = unique_number
                print(e)

            try:
                SpecCountry = "USA"
            except Exception as e:
                print(e)

            try:
                SpecPrice = response.xpath('//*[contains(text(),"priced $")]/text()').extract_first(default='0').strip().replace(",", "")
                SpecPrice = re.findall(r"(\d+)", SpecPrice)[0]
            except Exception as e:
                print(e)

            try:
                SpecSqft = response.xpath('//span[contains(text(),"Sq. Ft.")]/b/text()').extract_first(default='0').strip().replace(',','')
            except Exception as e:
                print(e)

            try:
                SpecBaths = response.xpath('//span[contains(text(),"Bath")]/b/text()').extract_first(default='0').strip()
                tmp = re.findall(r"(\d+)", SpecBaths)
                SpecBaths = tmp[0]
                if len(tmp) > 1:
                    SpecHalfBaths = 1
                else:
                    SpecHalfBaths = 0
            except Exception as e:
                print(e)

            try:
                SpecBedrooms = response.xpath('//span[contains(text(),"Bed")]/b/text()').extract_first(default='0').strip()
            except Exception as e:
                print(e)

            try:
                MasterBedLocation = response.xpath('//span[contains(text(),"Master Bed ")]/b/text()').extract_first(default='0').strip()
            except Exception as e:
                print(e)

            try:
                SpecGarage = response.xpath('//span[contains(text(),"Garage")]/b/text()').extract_first(default='0').strip()
            except Exception as e:
                print(e)

            try:
                SpecDescription = response.xpath('//div[@class="wysiwyg pr-lg-5 pr-0"]/ul/li/text()').extract_first(default='0').strip()
            except Exception as e:
                print(e)

            try:
                ElevationImage = response.xpath('//*[@data-fancybox="elevation-images"]/@href').extract()
                SpecElevationImage = '|'.join(ElevationImage)
            except Exception as e:
                print(e)

            try:
                SpecWebsite = response.url
            except Exception as e:
                print(e)

            try:
                comid = response.meta['comm_id']
                commid = response.url.split('/')[-5]
                if commid == comid:
                    item = BdxCrawlingItem_Spec()
                    item['SpecNumber'] = SpecNumber
                    item['PlanNumber'] = PlanNumber
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
            except:
                print("commm")



from scrapy.cmdline import execute
# execute("scrapy crawl Caviness_Cates_Building_and_Development".split())