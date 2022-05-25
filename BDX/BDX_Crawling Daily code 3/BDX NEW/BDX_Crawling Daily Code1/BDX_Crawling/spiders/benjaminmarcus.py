import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header


class BenjaminMarcusHomesSpider(scrapy.Spider):
    name = 'benjaminmarcus'
    allowed_domains = []
    start_urls = ['https://www.benjaminmarcushomes.com/our-homes/locations/']
    builderNumber = 56818

    def parse(self, response):
        clink = []
        communitylinks1 = response.xpath('//ul//li//span//a/@href').getall()
        for i in communitylinks1:
            if 'https://www.benjaminmarcushomes.com/our-homes/locations/' not in i:
                url = 'https://www.benjaminmarcushomes.com/our-homes/locations/' + str(i)
                clink.append(url)
        del communitylinks1[0]
        d = clink + communitylinks1
        communitylinks2 = response.xpath('//div[@class="fl-rich-text"]//ul//li/a/@href').getall()
        communitylinks = d + communitylinks2
        print(len(communitylinks))
        for l1 in communitylinks:
            print(l1)
            yield scrapy.FormRequest(url=l1, callback=self.communityDetail)

    def communityDetail(self, response):
        print(response.url)
        if response.url == 'https://www.benjaminmarcushomes.com/our-homes/locations/summerbrooke/':
            subdivisonName = 'SUMMERBROOKE'
            subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % subdivisonNumber, "wb")
            f.write(response.body)
            f.close()
            item2 = BdxCrawlingItem_subdivision()
            item2['sub_Status'] = "Active"
            item2['SubdivisionName'] = subdivisonName
            item2['SubdivisionNumber'] = subdivisonNumber
            item2['BuilderNumber'] = self.builderNumber
            item2['BuildOnYourLot'] = 0
            item2['OutOfCommunity'] = 1
            item2['Street1'] = 'Spindle Court, Canonsburg'
            item2['City'] = 'North Strabane Township'
            item2['State'] = 'PA'
            item2['ZIP'] = '15317'
            item2['AreaCode'] = ''
            item2['Prefix'] = ''
            item2['Suffix'] = ''
            item2['Extension'] = ""
            item2['Email'] = ""
            item2[
                'SubDescription'] = 'Introducing 14 fabulous home sites in Summerbrooke at Spindle Court in North Strabane, PA. With various home plans designed for your style of living, including two-story four-bedroom homes, as well as first-floor masters, and a one-level ranch with first-floor master. BMH quality craftsmanship with access to shopping, schools, and community activities, all while having direct access to Route 19, and Interstate 79.'
            item2['SubImage'] = "|".join(response.xpath('//ul[@class="slides"]/li/img/@src').extract())
            item2['SubWebsite'] = response.url
            yield item2

        elif response.url == 'https://www.benjaminmarcushomes.com/our-homes/locations/hamlet-of-springdale/':
            subdivisonName = 'HAMLET OF SPRINGDALE'
            subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % subdivisonNumber, "wb")
            f.write(response.body)
            f.close()
            item2 = BdxCrawlingItem_subdivision()
            item2['sub_Status'] = "Active"
            item2['SubdivisionName'] = subdivisonName
            item2['SubdivisionNumber'] = subdivisonNumber
            item2['BuilderNumber'] = self.builderNumber
            item2['BuildOnYourLot'] = 0
            item2['OutOfCommunity'] = 1
            item2['Street1'] = 'Buckingham Dr, Venetia'
            item2['City'] = 'Peters Township'
            item2['State'] = 'PA'
            item2['ZIP'] = '15367'
            item2['AreaCode'] = ''
            item2['Prefix'] = ''
            item2['Suffix'] = ''
            item2['Extension'] = ""
            item2['Email'] = ""
            item2[
                'SubDescription'] = 'An enchanting European-style retreat, the Hamlet of Springdale is a beautiful neighborhood setting, offering lots from 0.5 to 0.9 acres. A flagship development for BMH, the Hamlet of Springdale is entering Phase VII with the additional of Regents Park, which we are now taking lot deposits and reservations. These beautiful lots feature 50 ft. building setbacks and a minimum width of 110 ft. at the building line which allows all lots to accommodate both an attached garage and a first-floor master (if desired).'
            item2['SubImage'] = "|".join(response.xpath('//ul[@class="slides"]/li/img/@src').extract())
            item2['SubWebsite'] = response.url
            yield item2

        elif response.url == 'https://www.benjaminmarcushomes.com/our-homes/locations/kensington-trace/':
            subdivisonName = 'KENSINGTON TRACE'
            subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % subdivisonNumber, "wb")
            f.write(response.body)
            f.close()
            item2 = BdxCrawlingItem_subdivision()
            item2['sub_Status'] = "Active"
            item2['SubdivisionName'] = subdivisonName
            item2['SubdivisionNumber'] = subdivisonNumber
            item2['BuilderNumber'] = self.builderNumber
            item2['BuildOnYourLot'] = 0
            item2['OutOfCommunity'] = 1
            item2['Street1'] = 'Buckingham Dr, Venetia'
            item2['City'] = 'Peters Township'
            item2['State'] = 'PA'
            item2['ZIP'] = '15367'
            item2['AreaCode'] = ''
            item2['Prefix'] = ''
            item2['Suffix'] = ''
            item2['Extension'] = ""
            item2['Email'] = ""
            item2[
                'SubDescription'] = 'We are excited to announce the Kensington Trace development located in Peters Township. Only eight lots are available in this Benjamin Marcus Homes Keystone and Cornerstone Series development. Lots are .23 – .27 acres and are located directly across from 1.67 acres of open space. We are now taking deposits on this unique neighborhood located within The Hamlet of Springdale.'
            item2['SubImage'] = "|".join(response.xpath('//ul[@class="slides"]/li/img/@src').extract())
            item2['SubWebsite'] = response.url
            yield item2

        elif response.url == 'https://www.benjaminmarcushomes.com/our-homes/locations/regents-park/':
            subdivisonName = 'REGENTS PARK'
            subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % subdivisonNumber, "wb")
            f.write(response.body)
            f.close()
            item2 = BdxCrawlingItem_subdivision()
            item2['sub_Status'] = "Active"
            item2['SubdivisionName'] = subdivisonName
            item2['SubdivisionNumber'] = subdivisonNumber
            item2['BuilderNumber'] = self.builderNumber
            item2['BuildOnYourLot'] = 0
            item2['OutOfCommunity'] = 1
            item2['Street1'] = 'Buckingham Dr, Venetia'
            item2['City'] = 'Peters Township'
            item2['State'] = 'PA'
            item2['ZIP'] = '15367'
            item2['AreaCode'] = ''
            item2['Prefix'] = ''
            item2['Suffix'] = ''
            item2['Extension'] = ""
            item2['Email'] = ""
            item2[
                'SubDescription'] = 'We are now accepting lot reservations for Regent’s Park, Phase VII of The Hamlet of Springdale in Peters Township. The low-maintenance development will continue to build upon the beauty and serenity that customers have come to know and expect with Benjamin Marcus Homes and The Hamlet of Springdale community, our flagship development in the South Hills of Pittsburgh.Regent’s Park is located just minutes away from Bower Hill Elementary, Peterswood Park & Reese Park, convenient access to prime shopping and entertainment areas, and is easily accessible from I-79.'
            item2['SubImage'] = "|".join(response.xpath('//div[@class="nivoSlider"]/img/@src').extract())
            item2['SubWebsite'] = response.url
            yield item2

        elif response.url == 'https://www.benjaminmarcushomes.com/our-homes/locations/ironwood/':
            subdivisonName = 'IRONWOOD'
            subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % subdivisonNumber, "wb")
            f.write(response.body)
            f.close()
            item2 = BdxCrawlingItem_subdivision()
            item2['sub_Status'] = "Active"
            item2['SubdivisionName'] = subdivisonName
            item2['SubdivisionNumber'] = subdivisonNumber
            item2['BuilderNumber'] = self.builderNumber
            item2['BuildOnYourLot'] = 0
            item2['OutOfCommunity'] = 1
            item2['Street1'] = 'Lelak Ln, Venetia'
            item2['City'] = 'Peters Township'
            item2['State'] = 'PA'
            item2['ZIP'] = '15367'
            item2['AreaCode'] = ''
            item2['Prefix'] = ''
            item2['Suffix'] = ''
            item2['Extension'] = ""
            item2['Email'] = ""
            item2[
                'SubDescription'] = 'Ironwood is located in the heart of Peters Township and consists of 21 beautiful single-family homes. These Cornerstone Series homes boast .5+ acre plots. This development is located near Peterswood Park and Scenic Valley Golf Course with easy access to Route 19 and Interstate 79. '
            item2['SubImage'] = "|".join(response.xpath('//ul[@class="slides"]/li/img/@src').extract())
            item2['SubWebsite'] = response.url
            yield item2

        elif response.url == 'https://www.benjaminmarcushomes.com/our-homes/locations/tuscany/':
            subdivisonName = 'TUSCANY'
            subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % subdivisonNumber, "wb")
            f.write(response.body)
            f.close()
            item2 = BdxCrawlingItem_subdivision()
            item2['sub_Status'] = "Active"
            item2['SubdivisionName'] = subdivisonName
            item2['SubdivisionNumber'] = subdivisonNumber
            item2['BuilderNumber'] = self.builderNumber
            item2['BuildOnYourLot'] = 0
            item2['OutOfCommunity'] = 1
            item2['Street1'] = 'Villa Dr'
            item2['City'] = 'Venetia'
            item2['State'] = 'PA'
            item2['ZIP'] = '15367'
            item2['AreaCode'] = ''
            item2['Prefix'] = ''
            item2['Suffix'] = ''
            item2['Extension'] = ""
            item2['Email'] = ""
            item2[
                'SubDescription'] = 'If a large estate setting is in your future, BMH has the perfect location to create your custom home paradise. This development offers acres of land with limitless possibilities. Lots in this development range from 1.1 to 7.4 acres with a tranquil 1.3 acre springfed pond. Treat yourself to breathtaking views, in an area tucked away from high-traffic areas, yet still convenient to all of Peters Township’s amenities. Additionally, Its location is only one mile from the Peters Township Recreation Center and Peterswood Park. Tuscany represents the prestigious upper level offering in the BMH portfolio.'
            item2['SubImage'] = "|".join(response.xpath('//ul[@class="slides"]/li/img/@src').extract())
            item2['SubWebsite'] = response.url
            yield item2

        elif response.url == 'https://www.benjaminmarcushomes.com/our-homes/locations/newbury/':
            subdivisonName = 'NEWBURY'
            subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % subdivisonNumber, "wb")
            f.write(response.body)
            f.close()
            item2 = BdxCrawlingItem_subdivision()
            item2['sub_Status'] = "Active"
            item2['SubdivisionName'] = subdivisonName
            item2['SubdivisionNumber'] = subdivisonNumber
            item2['BuilderNumber'] = self.builderNumber
            item2['BuildOnYourLot'] = 0
            item2['OutOfCommunity'] = 1
            item2['Street1'] = 'Celebration Circle'
            item2['City'] = 'Bridgeville'
            item2['State'] = 'PA'
            item2['ZIP'] = '15017'
            item2['AreaCode'] = ''
            item2['Prefix'] = ''
            item2['Suffix'] = ''
            item2['Extension'] = ""
            item2['Email'] = ""
            item2[
                'SubDescription'] = 'Benjamin Marcus Homes is excited to announce Newbury in South Fayette.  As part of our Keystone and Cornerstone Series, Newbury offers townhomes, attached units, ranch-style and single family homes. In addition, Newbury is located within the prestigious South Fayette School District. Therefore, this development is located within one mile of The Club at Nevillewood and only minutes from Interstate 79.'
            item2['SubImage'] = "|".join(response.xpath('//ul[@class="slides"]/li/img/@src').extract())
            item2['SubWebsite'] = response.url
            yield item2

        elif response.url == 'https://www.benjaminmarcushomes.com/our-homes/locations/siena-at-st-clair/':
            subdivisonName = 'SIENA AT ST. CLAIR'
            subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % subdivisonNumber, "wb")
            f.write(response.body)
            f.close()
            item2 = BdxCrawlingItem_subdivision()
            item2['sub_Status'] = "Active"
            item2['SubdivisionName'] = subdivisonName
            item2['SubdivisionNumber'] = subdivisonNumber
            item2['BuilderNumber'] = self.builderNumber
            item2['BuildOnYourLot'] = 0
            item2['OutOfCommunity'] = 1
            item2['Street1'] = 'Lucca Lane'
            item2['City'] = 'Upper St. Clair'
            item2['State'] = 'PA'
            item2['ZIP'] = '15241'
            item2['AreaCode'] = ''
            item2['Prefix'] = ''
            item2['Suffix'] = ''
            item2['Extension'] = ""
            item2['Email'] = ""
            item2[
                'SubDescription'] = 'Siena at St. Clair is the latest premiere neighborhood in the South Hills.  With shopping and retail within walking distance to beautiful residential homes, homeowners can experience all the conveniences of a mixed-use community, while having direct access to restaurants, Whole Foods, Route 19, and the South Hills Village Mall.We are pleased to announce that Benjamin Marcus Homes will be the exclusive builder of these highly desired residential units.  Siena at St. Clair will feature 21 patio home units and 12 townhouse units. The patio homes will be available in two basic styles— ranch and 1.5 story units—with options for further customization. The townhouses are built in 3 buildings of 4 units, also with customizable features. All homes come complete with granite countertops, beautiful hardwood floors, maple cabinetry and designer lighting packages.'
            item2['SubImage'] = "|".join(response.xpath('//ul[@class="slides"]/li/img/@src').extract())
            item2['SubWebsite'] = response.url
            yield item2

        elif response.url == 'https://www.benjaminmarcushomes.com/our-homes/locations/fair-acres/':
            subdivisonName = 'FAIR ACRES'
            subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % subdivisonNumber, "wb")
            f.write(response.body)
            f.close()
            item2 = BdxCrawlingItem_subdivision()
            item2['sub_Status'] = "Active"
            item2['SubdivisionName'] = subdivisonName
            item2['SubdivisionNumber'] = subdivisonNumber
            item2['BuilderNumber'] = self.builderNumber
            item2['BuildOnYourLot'] = 0
            item2['OutOfCommunity'] = 1
            item2['Street1'] = 'Fair Acres Dr.'
            item2['City'] = 'Upper St. Clair'
            item2['State'] = 'PA'
            item2['ZIP'] = '15241'
            item2['AreaCode'] = ''
            item2['Prefix'] = ''
            item2['Suffix'] = ''
            item2['Extension'] = ""
            item2['Email'] = ""
            item2[
                'SubDescription'] = 'The beautiful Fair Acres development, off of Hays Road in Upper St. Clair, offers custom single family home on .35 – .76 acre homesites. The Fair Acres neighborhood combines luxury and convenience, minutes from Route 19 and close to Interstate 79. Boyce Elementary and Upper St. Clair High School fall within the Blue Ribbon School District and are minutes away. This Cornerstone Series development is within walking distance to Hays Park, and a few miles to Boyce Park and the Upper St. Clair Recreation Center.'
            item2['SubImage'] = "|".join(response.xpath('//ul[@class="slides"]/li/img/@src').extract())
            item2['SubWebsite'] = response.url
            yield item2

        elif response.url == 'https://www.benjaminmarcushomes.com/our-homes/locations/fair-acres/':
            subdivisonName = 'FAIR ACRES'
            subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % subdivisonNumber, "wb")
            f.write(response.body)
            f.close()
            item2 = BdxCrawlingItem_subdivision()
            item2['sub_Status'] = "Active"
            item2['SubdivisionName'] = subdivisonName
            item2['SubdivisionNumber'] = subdivisonNumber
            item2['BuilderNumber'] = self.builderNumber
            item2['BuildOnYourLot'] = 0
            item2['OutOfCommunity'] = 1
            item2['Street1'] = 'Fair Acres Dr.'
            item2['City'] = 'Upper St. Clair'
            item2['State'] = 'PA'
            item2['ZIP'] = '15241'
            item2['AreaCode'] = ''
            item2['Prefix'] = ''
            item2['Suffix'] = ''
            item2['Extension'] = ""
            item2['Email'] = ""
            item2[
                'SubDescription'] = 'The beautiful Fair Acres development, off of Hays Road in Upper St. Clair, offers custom single family home on .35 – .76 acre homesites. The Fair Acres neighborhood combines luxury and convenience, minutes from Route 19 and close to Interstate 79. Boyce Elementary and Upper St. Clair High School fall within the Blue Ribbon School District and are minutes away. This Cornerstone Series development is within walking distance to Hays Park, and a few miles to Boyce Park and the Upper St. Clair Recreation Center.'
            item2['SubImage'] = "|".join(response.xpath('//ul[@class="slides"]/li/img/@src').extract())
            item2['SubWebsite'] = response.url
            yield item2

        elif response.url == 'https://www.benjaminmarcushomes.com/our-homes/locations/venango-trails/':
            subdivisonName = 'VENANGO TRAILS'
            subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % subdivisonNumber, "wb")
            f.write(response.body)
            f.close()
            item2 = BdxCrawlingItem_subdivision()
            item2['sub_Status'] = "Active"
            item2['SubdivisionName'] = subdivisonName
            item2['SubdivisionNumber'] = subdivisonNumber
            item2['BuilderNumber'] = self.builderNumber
            item2['BuildOnYourLot'] = 0
            item2['OutOfCommunity'] = 1
            item2['Street1'] = 'Venango Trail, Mars'
            item2['City'] = 'Marshall Township'
            item2['State'] = 'PA'
            item2['ZIP'] = '16046'
            item2['AreaCode'] = ''
            item2['Prefix'] = ''
            item2['Suffix'] = ''
            item2['Extension'] = ""
            item2['Email'] = ""
            item2[
                'SubDescription'] = 'Benjamin Marcus Homes is pleased to be an approved home builder for Venango Trails, in Marshall Township, one of the fastest selling communities in Pittsburgh. While the majority of our developments are located in the South Hills, we’re pleased to now offer our custom home building experience in the Northern part of the Pittsburgh region for the first time.'
            item2['SubImage'] = "|".join(response.xpath('//ul[@class="slides"]/li/img/@src').extract())
            item2['SubWebsite'] = response.url
            yield item2

        elif response.url == 'https://www.benjaminmarcushomes.com/our-homes/locations/mallard-pond/':
            subdivisonName = 'MALLARD POND'
            subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % subdivisonNumber, "wb")
            f.write(response.body)
            f.close()
            item2 = BdxCrawlingItem_subdivision()
            item2['sub_Status'] = "Active"
            item2['SubdivisionName'] = subdivisonName
            item2['SubdivisionNumber'] = subdivisonNumber
            item2['BuilderNumber'] = self.builderNumber
            item2['BuildOnYourLot'] = 0
            item2['OutOfCommunity'] = 1
            item2['Street1'] = '785 Spang Rd'
            item2['City'] = 'Baden'
            item2['State'] = 'PA'
            item2['ZIP'] = '15005'
            item2['AreaCode'] = ''
            item2['Prefix'] = ''
            item2['Suffix'] = ''
            item2['Extension'] = ""
            item2['Email'] = ""
            item2[
                'SubDescription'] = 'Benjamin Marcus Homes is proud to announce Mallard Pond, our third building location in Pittsburgh’s northern suburbs.In addition, Mallard Pond is located in Marshall Twp in the  North Allegheny School District.After that, Mallard Pond has easy access to major highways (Interstate 79, Interstate 76 and Route 19), shopping, dining, healthcare and professional services in both Allegheny and Butler Counties. For instance, the development is two minutes from Knob Hill Park and 6 minutes from Marshall Campus/North Allegheny Schools.'
            item2['SubImage'] = "|".join(response.xpath('//ul[@class="slides"]/li/img/@src').extract())
            item2['SubWebsite'] = response.url
            yield item2

        elif response.url == 'https://www.benjaminmarcushomes.com/our-homes/locations/emerald-fields/':
            subdivisonName = 'EMERALD FIELDS'
            subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % subdivisonNumber, "wb")
            f.write(response.body)
            f.close()
            item2 = BdxCrawlingItem_subdivision()
            item2['sub_Status'] = "Active"
            item2['SubdivisionName'] = subdivisonName
            item2['SubdivisionNumber'] = subdivisonNumber
            item2['BuilderNumber'] = self.builderNumber
            item2['BuildOnYourLot'] = 0
            item2['OutOfCommunity'] = 1
            item2['Street1'] = 'Emerald Fields Drive'
            item2['City'] = 'Mars'
            item2['State'] = 'PA'
            item2['ZIP'] = '00000'
            item2['AreaCode'] = ''
            item2['Prefix'] = ''
            item2['Suffix'] = ''
            item2['Extension'] = ""
            item2['Email'] = ""
            item2[
                'SubDescription'] = 'Benjamin Marcus Homes is delighted to introduce Emerald Fields in Pine Township. It represents our second building development in the northern suburbs of Pittsburgh.This addition to our portfolio offers lots ranging from .5 to 2 acres in a picturesque setting, rich in natural beauty. In addition, Emerald Fields is part of the award-winning Pine-Richland School District.Additionally, Emerald Fields is located on 276 acres along Mt. Pleasant Road in Pine Township. Therefore, the location is one of the best in Pine Township as it allows easy access to major highways (Interstate 79, Interstate 76 and Route 19), shopping, dining, healthcare and professional services in both Allegheny and Butler Counties.'
            item2['SubImage'] = "|".join(response.xpath('//div[@class="nivoSlider"]/img/@src').extract())
            item2['SubWebsite'] = response.url
            yield item2

        # elif response.url == 'https://www.benjaminmarcushomes.com/our-homes/locations/eagle-ridge/':
        #     subdivisonName = 'EAGLE RIDGE'
        #     subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
        #     f = open("html/%s.html" % subdivisonNumber, "wb")
        #     f.write(response.body)
        #     f.close()
        #     item2 = BdxCrawlingItem_subdivision()
        #     item2['sub_Status'] = "Active"
        #     item2['SubdivisionName'] = subdivisonName
        #     item2['SubdivisionNumber'] = subdivisonNumber
        #     item2['BuilderNumber'] = self.builderNumber
        #     item2['BuildOnYourLot'] = 0
        #     item2['OutOfCommunity'] = 1
        #     item2['Street1'] = 'Emerald Fields Drive'
        #     item2['City'] = 'Mars'
        #     item2['State'] = 'PA'
        #     item2['ZIP'] = '00000'
        #     item2['AreaCode'] = ''
        #     item2['Prefix'] = ''
        #     item2['Suffix'] = ''
        #     item2['Extension'] = ""
        #     item2['Email'] = ""
        #     item2[
        #         'SubDescription'] = 'Benjamin Marcus Homes has officially begun new home construction in Eagle Ridge, our fourth building location in Pittsburgh’s northern suburbs.This Benjamin Marcus Homes exclusive development features 22 single family estate lots ranging from around one half acre to more than a full acre. The development's picturesque location and its unique design means that every lot will be on a cul de sac.In addition, Eagle Ridge is located in Cranberry Township in the Seneca Valley School District in Butler County.Eagle Ridge has easy access to major highways (Interstate 79, Interstate 76 and Route 19), shopping, dining, healthcare, and professional services in both Allegheny and Butler Counties. '
        #     item2['SubImage'] = "|".join(response.xpath('//div[@class="nivoSlider"]/img/@src').extract())
        #     item2['SubWebsite'] = response.url
        #     yield item2


# def communityDetail(self, response):
#     print(response.url)
#     Address = re.findall(r'"address":"(.*?)"', response.text)[0]
#     print(Address)
#     subdivisonName = response.xpath('//div[@class="fl-module-content fl-node-content"]/h1/span/text()').extract_first()
#     subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
#
#     f = open("html/%s.html" % subdivisonNumber, "wb")
#     f.write(response.body)
#     f.close()
#     street1 = Address.split(',')
#     s = street1[-2].strip()
#     state = s.split(' ')[0]
#     zipcode = s.split(' ')[-1]
#     city = street1[2].strip()
#     a = street1[0] + street1[1]
#     print(a)
#     print(state,zipcode,city)
#     SubImage = "|".join(response.xpath('//ul[@class="slides"]/li/img/@src').extract())
#
#     item2 = BdxCrawlingItem_subdivision()
#     item2['sub_Status'] = "Active"
#     item2['SubdivisionName'] = subdivisonName
#     item2['SubdivisionNumber'] = subdivisonNumber
#     item2['BuilderNumber'] = self.builderNumber
#     item2['BuildOnYourLot'] = 0
#     item2['OutOfCommunity'] = 1
#     item2['Street1'] = a
#     item2['City'] = city
#     item2['State'] = state
#     item2['ZIP'] = zipcode
#     item2['AreaCode'] = ''
#     item2['Prefix'] = ''
#     item2['Suffix'] = ''
#     item2['Extension'] = ""
#     item2['Email'] = "lindsay@lecontecompanies.com"
#     item2['SubDescription'] = response.xpath('//div[@class="fl-rich-text"]/p/span/text()').extract_first(default="")
#     item2['SubImage'] = SubImage
#     item2['SubWebsite'] = response.url
#     yield item2


if __name__ == '__main__':
    execute("scrapy crawl benjaminmarcus".split())
