# -*- coding: utf-8 -*-
import scrapy
import re
import hashlib
import os
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision
from BDX_Crawling.export_xml import genxml
from w3lib.html import remove_tags

class ShepardhomesllcSpider(scrapy.Spider):
    name = 'shepardhomesllc'
    allowed_domains = ['shepardhomesllc.com']
    #start_urls = ['http://www.shepardhomesllc.com/']
    start_urls = ['http://www.shepardhomesllc.com/available-homes/']

    BuilderNumber = '283635848478943545962237502906'

    def parse(self, response):

        # ----------------------------------------------------------------- #
        # subdivision == > Builders communities
        # Plans == > available plans in that communities
        # specs == > available Homes in plans

        # ----------------------- Don't change anything here -------------- #


        # In case you can't able to find any communities, then please use this line of code, and reference this SubdivisionNumber in All Plans

        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.BuilderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 1
        item2['Street1'] = "1101 Robinson Street"
        item2['City'] = "Ocean Springs"
        item2['State'] = "MS"
        item2['ZIP'] = "39564"
        item2['AreaCode'] = "228"
        item2['Prefix'] = "215"
        item2['Suffix'] = "0469"
        item2['Extension'] = ""
        item2['Email'] = "office@shepardhomesllc.com"
        item2['SubDescription'] = "Joey Shepard, owner of Shepard Homes, LLC  has been building new homes on the Mississippi Gulf Coast for over 15 years.  Joey moved to the Coast in 2002 after graduating from The University of Southern Mississippi to start his career in new home construction.  Joey’s degree in Architectural Engineering combined with his years of knowledge and experience in the industry make it possible to turn his clients’ dreams into a reality.  By treating every home that he builds as it was his own, Joey takes great pride in focusing on attention to detail, efficiency, and making the process enjoyable."
        item2['SubImage'] = ""
        item2['SubWebsite'] = ''
        yield item2

        # In case you have found the communities (subdivision) and Homes (Specs) but you are not able to find the plan details then,
        # please use this line of code, and reference this Plannumber  in All Home(Specs)

        item3 = BdxCrawlingItem_Plan()
        item3['Type'] = "SingleFamily"
        item3['PlanNumber'] = "Plan Unknown"

        unique = item3['PlanNumber'] + str(['BuilderNumber'])
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item3['unique_number'] = unique_number

        item3['SubdivisionNumber'] = item2['BuilderNumber']
        item3['PlanName'] = "Plan Unknown"
        item3['PlanNotAvailable'] = 1
        item3['PlanTypeName'] = 'Single Family'
        item3['BasePrice'] = 0
        item3['BaseSqft'] = 0
        item3['Baths'] = 0
        item3['HalfBaths'] = 0
        item3['Bedrooms'] = 0
        item3['Garage'] = 0
        item3['Description'] = ""
        item3['ElevationImage'] = ""
        item3['PlanWebsite'] = ""
        yield item3

        # -------------------------------------------------------------------- #

        # --------------------- TO the Communities page -------- #

        try:
            Homes = response.xpath('//div[@class="gw-gopf-post-title"]/h2/a')
            for Home in Homes:
                HomeLink = ''
                HomeLink = Home.xpath('@href').extract_first(default='').strip()
                HomeTitle = Home.xpath('text()').extract_first(default='').strip()
                #HomeLink = 'http://www.shepardhomesllc.com/available_listings/lot-19-florence-gardens/'
                # yield scrapy.Request(url=self.start_urls[0]+links, callback=self.communities_list, meta={'BN': item1['BuilderNumber']})
                yield scrapy.Request(url=self.start_urls[0] + HomeLink, callback=self.HomesDetails, meta={"PN": item3['PlanNumber'],'HomeTitle':HomeTitle,'unique_number':unique_number})
                #break
        except Exception as e:
            print(e)

    def HomesDetails(self, response):
        print (response.url)
        unique_number = response.meta['unique_number']
        # specs == > available Homes in plans

        # ------------------------------------------- Extract Homedetails ------------------------------ #
        try:
            PlanNumber = response.meta['PN']
            HomeTitle = response.meta['HomeTitle']
        except Exception as e:
            print(e)

        try:
            Address_1 = ''
            Address_2 = ''
            Address_1 = response.xpath('//div[@class="listing-address-1"]/strong/text()').extract_first(default='').strip()
            Address_2 = response.xpath('//div[@class="listing-address-2"]/strong/text()').extract_first(default='').strip()
        except Exception as e:
            print(e)

        try:
            if Address_1 == '':
                MainTag = response.xpath('//div[@id="content"]')
                MainTag_P = MainTag.xpath('//div[@class="wpb_wrapper"]')[1].xpath('//p').extract()
                # MainTag_1 = MainTag.xpath('//div[@class="wpb_wrapper"]')[1].extract()
                # MainTag_str = response.xpath('//div[@id="content"]').extract_first(default='').strip().replace(u'\xa0', u' ')
                # MainTag_str_encode = MainTag_str.encode('utf-8')
                for itemIndex,Tag_P in enumerate(MainTag_P):
                    if (re.match('<p>(.*.[a-zA-Z]{2} [0-9]{5}).*.',Tag_P)):
                    #if (re.match('[a-zA-Z]{2} [0-9]{5}', Tag_P)):
                        Address_2 = remove_tags(Tag_P)
                        if itemIndex > 0:Address_1 = remove_tags(MainTag_P[itemIndex - 1])
                        else:Address_1 = ''
                        break

        except Exception as e:
            print(e)

        try:
            SpecPrice = ''
            SpecBaths = ''
            SpecBedrooms = ''
            SpecSqft = ''
            if Address_1=='':
                Temp = response.xpath('//meta[@property="og:description"]/@content').extract_first().split('\r\n')
                for itemIndex, Tag in enumerate(Temp):
                    # if (re.match('<p>(.*.[a-zA-Z]{2} [0-9]{5}).*.',Tag_P)):
                    if (re.match('.*([a-zA-Z]{2} [0-9]{5}).*', Tag)) and Address_1 =='':
                    #if (re.match('[a-zA-Z]{2} [0-9]{5}', Tag)):
                        Address_2 = remove_tags(Tag)
                        if itemIndex > 0: Address_1 = remove_tags(Temp[itemIndex - 1])
                        else: Address_1 = ''
                        break
                    if (re.match('.*(\$.*)', Tag)) and SpecPrice=='':
                        SpecPrice = Tag
                    if (re.match('.*([0-9]+).*Bath.*', Tag)) and SpecBaths == '':
                        SpecBaths = re.findall('.*([0-9]+).*Bath.*', Tag)[0]
                    if (re.match('.*([0-9]+).*Bedroom.*', Tag)) and SpecBedrooms=='':
                        SpecBedrooms = re.findall('.*([0-9]+).*Bedroom.*', Tag)[0]
                    if (re.match('.*([0-9]+).*sq ft.*', Tag)) and SpecSqft == '':
                        #SpecSqft = re.findall('.*([0-9]+).*sq ft.*', Tag)[0]
                        SpecSqft = re.sub("\D", "", Tag)
        except Exception as e:
            print(e)

        try:
            SpecStreet1 = ''
            SpecStreet1 = Address_1.strip()
        except Exception as e:
            print(e)

        try:
            SpecCity = ''
            SpecCity = str(Address_2.split(',',1)[0]).strip()
        except Exception as e:
            print(e)

        try:
            SpecState = ''
            SpecState = str(Address_2.split(',',1)[1].strip()).split(' ',1)[0].strip()
        except Exception as e:
            print(e)

        try:
            SpecZIP = ''
            SpecZIP = str(Address_2.split(',',1)[1].strip()).split(' ',1)[1].strip()
        except Exception as e:
            print(e)

        try:
            SpecElevationImage = ''
            ElevationImage = MainTag.xpath('//div[@class="wpb_wrapper"]')[1].xpath("//p[a/img]/a/@href").extract()
            ElevationImage = "|".join(ElevationImage)
            SpecElevationImage = str(ElevationImage)
        except Exception as e:
            print(e)

        try:
            if not SpecElevationImage:
                SpecElevationImage = "|".join(response.xpath('//a[@class="prettyphoto"]/@href').extract())
                #SpecElevationImage = "|".join(SpecElevationImage)
                SpecElevationImage = str(SpecElevationImage)
        except Exception as e : print(e)

        try:
            if not SpecElevationImage:
                SpecElevationImage = response.xpath('//figure[@class="wpb_wrapper vc_figure"]/div/img/@src').extract()
                SpecElevationImage = "|".join(SpecElevationImage)
                SpecElevationImage = str(SpecElevationImage)
        except Exception as e : print(e)

        try:
            unique = HomeTitle +SpecStreet1+SpecCity+SpecState+SpecZIP
            SpecNumber = int(hashlib.md5(bytes(unique,"utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        try:
            SpecCountry = "USA"
        except Exception as e:
            print(e)

        try:
            if SpecPrice == '':
                SpecPrice = response.xpath('//div[@class="listing-price"]/strong/text()').extract_first(default='').strip()
            SpecPrice = SpecPrice.replace('$','').replace(',','')
            #SpecPrice = re.findall(r"(\d+)", SpecPrice)[0]
        except Exception as e:
            print(e)

        try:
            if SpecSqft=='':
                SpecSqft = str(response.xpath('//div[@class="listing-fields-wrapper"]/span[3]/text()').extract_first(default='').strip()).replace(",", "")
            SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
        except Exception as e:
            print(e)

        try:
            SpecHalfBaths = ''
            if SpecBaths == '':
                SpecBaths = str(response.xpath('//span[@class="listing-field listingBathrooms"]').extract_first(default='').strip()).replace(",", "")
            tmp = re.findall(r"(\d+)", SpecBaths)
            SpecBaths = tmp[0]
            if len(tmp) > 1:
                SpecHalfBaths = 1
            else:
                SpecHalfBaths = 0
        except Exception as e:
            print(e)

        try:
            if SpecBedrooms == '':
                SpecBedrooms = str(response.xpath('//span[@class="listing-field listingBedrooms"]').extract_first(default='').strip()).replace(",", "")
            SpecBedrooms = re.findall(r"(\d+)", SpecBedrooms)[0]
        except Exception as e:
            print(e)

        try:
            MasterBedLocation = "Down"
        except Exception as e:
            print(e)

        try:
            SpecGarage = response.xpath('normalize-space(//div[@class="homeDetailBox"]//*[contains(@class,"garage")]/text())').extract_first(default='0')
            SpecGarage = re.findall(r"(\d+)", SpecGarage)[0]
        except Exception as e:
            SpecGarage = '0'
            print(e)

        try:
            SpecDescription='Shepard Homes is a custom residential home builder along the Mississippi Gulf Coast. Your new home is an expression of yourself and we want to make sure you have every detail incorporated into the plans that you desire.'
            #SpecDescription = response.xpath('normalize-space(//div[@class="planDescription bdxRTEWrapper"]/text())').extract_first(default='').strip()
        except Exception as e:
            print(e)

        try:
            SpecWebsite = response.url
        except Exception as e:
            print(e)

        # ----------------------- Don't change anything here ---------------- #
        try:
            if SpecPrice=='' : SpecPrice = '0'
            if SpecSqft =='': SpecSqft = '0'
            if SpecBaths == '': SpecBaths = '0'
            if SpecHalfBaths == '': SpecHalfBaths = '0'
            if SpecBedrooms == '': SpecBedrooms = '0'

            item = BdxCrawlingItem_Spec()
            item['SpecNumber'] = SpecNumber
            item['PlanNumber'] = unique_number
            #item['PlanNumber'] = PlanNumber
            item['SpecStreet1'] = SpecStreet1
            item['SpecCity'] = SpecCity
            item['SpecState'] = SpecState
            item['SpecZIP'] = SpecZIP
            item['SpecCountry'] = SpecCountry
            item['SpecPrice'] = SpecPrice#
            item['SpecSqft'] = SpecSqft
            item['SpecBaths'] = SpecBaths
            item['SpecHalfBaths'] = SpecHalfBaths
            item['SpecBedrooms'] = SpecBedrooms
            item['MasterBedLocation'] = MasterBedLocation
            item['SpecGarage'] = SpecGarage
            item['SpecDescription'] = SpecDescription
            item['SpecElevationImage'] = SpecElevationImage[0:2000]
            item['SpecWebsite'] = SpecWebsite
            #print (item)
            yield item
        except Exception as e:
            print(e)
        # --------------------------------------------------------------------- #

#from scrapy.cmdline import execute
#execute("scrapy crawl shepardhomesllc".split())