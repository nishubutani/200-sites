import hashlib
import json
import re

import requests
import scrapy
from scrapy.selector import Selector
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class HardingHomesSpider(scrapy.Spider):
    name = 'Harding_Homes'
    allowed_domains = ['www.hardinghomes.net']
    start_urls = ['http://www.hardinghomes.net/']
    builderNumber = 49295

    def parse(self, response):
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
        item['Street1'] = 'P.O. Box 565'
        item['City'] = 'DeSoto'
        item['State'] = 'KS'
        item['ZIP'] = '66018'
        item['AreaCode'] = '913'
        item['Prefix'] = '583'
        item['Suffix'] = '3733'
        item['Extension'] = ""
        item['Email'] = 'info@hardinghomes.net'
        item['SubDescription'] = "Quality and reputation is what Harding Homes is all about. Harding Homes has been building custom homes in Johnson County Kansas for over 10 years and we pride ourselves in making your dream home a reality. We are a family owned “hands on” business that emphasizes integrity and honesty in every aspect of our work. Customer satisfaction is our #1 goal as we combine style with function to provide you with a quality home you love!"
        item['SubWebsite'] = response.url
        img_links = '|'.join(response.xpath('//img/@src').getall())
        item['SubImage'] = img_links

        yield item

        url = 'https://hardinghomes.net/properties-list/'
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.Plans)

    def Plans(self, response):
        links = response.xpath('//div[@class="listing-unit-img-wrapper"]/a/@href').getall()
        for link in links:
            url = link
            yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.Plan_data)

    def Plan_data(self, response):
        Type = 'SingleFamily'
        # try:
        PlanName = response.xpath('//div[@class="notice_area"]/h1/text()').get()
        PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        # except:
        #     PlanName = response.xpath('//div[@class="uk-width-1-2 uk-text-center"]/h2/text()').get()
        #     PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        SubdivisionNumber = self.builderNumber
        unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        PlanNotAvailable = 0
        PlanTypeName = 'Single Family'

        url = response.url

        # image = data1["items"][i]["image"]
        sbbg = response.xpath('//div[@class="single-content listing-content"]/p//text()').get()
        if sbbg != None:

            # sqft = str(sbbg.split('Total Sq. Ft')[0])
            if 'Aspen I' in PlanName:
                sqft = '1800'
            else:
                a = sbbg.replace(',', '')
                x = re.findall(r"(\d+)", a)
                print(x)
                p = []
                for i in x:
                    sq = int(i)
                    p.append(sq)
                sqft = max(p)



            try:
                if 'Aspen I' in PlanName:
                    Bedrooms = 3
                else:
                    Bedrooms = str(sbbg.split('Bedroom')[0]).strip().split()[-1]
            except:
                Bedrooms = 0
                print('error in bedrooms.........',response.url)

            try:
                if 'Aspen I' in PlanName:
                    Baths = '2'
                    HalfBaths = '1'
                else:
                    if 'Bath' in sbbg:
                        bathrooms = sbbg.split(' Bath')[0]
                        # print('1', bathrooms)
                        bathroom = bathrooms.split(" ")[-1]
                        # print('2', bathroom)
                        if '½' in bathroom:
                            bathrooms = bathrooms.split()[-2]
                            Bath = re.findall(r"(\d+)", bathrooms)
                            # print('3', Bath)
                            Baths = Bath[0]
                            # print('4 Baths = ', Baths)
                            tmp = bathrooms
                            # print('5', tmp)
                            HalfBaths = 1
                            # print('6 Halfbath = ', HalfBaths)

                        else:
                            Bath = re.findall(r"(\d+)", bathroom)
                            # print('3', Bath)
                            Baths = Bath[0]
                            # print('4 baths = ', Baths)
                            tmp = Bath
                            # print('5', tmp)
                            if len(tmp) > 1:
                                HalfBaths = 1
                                # print('6', HalfBaths)
                            else:
                                HalfBaths = 0
                                # print('6 halfbath = ', HalfBaths)
                    elif 'bath' in sbbg:
                        bathrooms = sbbg.split(' bath')[0]
                        # print('1', bathrooms)
                        bathroom = bathrooms.split(" ")[-1]
                        # print('2', bathroom)
                        if '½' in bathroom:
                            bathrooms = bathrooms.split()[-2]
                            Bath = re.findall(r"(\d+)", bathrooms)
                            # print('3', Bath)
                            Baths = Bath[0]
                            # print('4 Baths = ', Baths)
                            tmp = bathrooms
                            # print('5', tmp)
                            HalfBaths = 1
                            # print('6 Halfbath = ', HalfBaths)
                        else:
                            Bath = re.findall(r"(\d+)", bathroom)
                            # print('3', Bath)
                            Baths = Bath[0]
                            # print('4 baths = ', Baths)
                            tmp = Bath
                            # print('5', tmp)
                            if len(tmp) > 1:
                                HalfBaths = 1
                                # print('6', HalfBaths)
                            else:
                                HalfBaths = 0
                                # print('6 halfbath = ', HalfBaths)
            except:
                Baths = 0
                HalfBaths = 0
                print('error in baths and halfbaths.........')

            Garage = 0

        Description = str(response.xpath('//div[@class="single-content listing-content"]/p[1]//text()').get()).replace('\xa0','')
        BasePrice = 0

        imgs1 = '|'.join(response.xpath('//div[@class="floor_image"]/a/@href').getall())

        try:
            imgs2_1 = response.xpath('//div[@class="single-content listing-content"]/p/a/@href').get()
            if imgs2_1 == None:
                imgs2_2 = response.xpath('//div[@class="single-content listing-content"]/p//@src').get()
                if imgs2_2 == None:
                    # imgs2 = re.findall(r'<img src="//hardinghomes.net/wp-content/uploads/E.S.(.*?).jpg" width="1024"',response.text)#//rs-slides[@style="visibility: visible; display: block; max-height: none; height: 100%; width: 100%; overflow: hidden;"]/rs-slide//img/@src
                    # imgs2 = '|'.join(response.xpath('//rs-slides[@style="visibility: visible; display: block; max-height: none; height: 100%; width: 100%; overflow: hidden;"]/rs-slide//img/@src').getall())
                    img2 = response.xpath('//rs-layer[@data-frame_999="st:w;auto:true;"]/img/@src').getall()
                    imgs2 = []
                    for i in img2:
                        i = 'https:' +str(i)
                        imgs2.append(i)
                    imgs2 = '|'.join(imgs2)
                else:
                    imgs2 = imgs2_2
            else:
                imgs2 = imgs2_1
        except:
            imgs2 = 0
            print('problem in imgs2',response.url)

        Elevationimage = imgs1+'|'+imgs2

        # unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['Type'] = Type
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number  # < -------- Changes here
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = PlanName
        item['PlanNotAvailable'] = PlanNotAvailable
        item['PlanTypeName'] = PlanTypeName
        item['BasePrice'] = BasePrice
        item['BaseSqft'] = sqft
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = Description
        item['ElevationImage'] = Elevationimage
        item['PlanWebsite'] = url
        yield item

        unique1 = str("Plan Unknown") + str(self.builderNumber)
        unique_number1 = int(hashlib.md5(bytes(unique1, "utf8")).hexdigest(), 16) % (10 ** 30)
        item1 = BdxCrawlingItem_Plan()
        item1['unique_number'] = unique_number1
        item1['Type'] = "SingleFamily"
        item1['PlanNumber'] = "Plan Unknown"
        item1['SubdivisionNumber'] = self.builderNumber
        item1['PlanName'] = "Plan Unknown"
        item1['PlanNotAvailable'] = 1
        item1['PlanTypeName'] = "Single Family"
        item1['BasePrice'] = 0
        item1['BaseSqft'] = 0
        item1['Baths'] = 0
        item1['HalfBaths'] = 0
        item1['Bedrooms'] = 0
        item1['Garage'] = 0
        item1['Description'] = ""
        item1['ElevationImage'] = ""
        item1['PlanWebsite'] = ""
        yield item1
        url = 'https://hardinghomes.net/available-homes/'
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.home_links, meta={'PN': unique_number1})

    def home_links(self,response):
        # for link,img in links:
        for i in response.xpath('//div[@class="pt-cv-ifield"]/a'):
            url = i.xpath('./@href').get()
            img = i.xpath('./img/@src').get()
            PN = response.meta['PN']
            yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.home_data,meta={'PN':PN,'specimg':img})

    def home_data(self,response):
        add = response.xpath('//h1[@class="entry-title single-title"]/text()').get()
        SpecStreet1 = add.split(',')[0]
        SpecCity = add.split(',')[1]
        SpecState = add.split(',')[2].split(' ')[1]
        SpecZIP = add.split(',')[2].split(' ')[-1]

        unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
        # print(unique)
        SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

        f = open("html/%s.html" % SpecNumber, "wb")
        f.write(response.body)
        f.close()

        try:
            PlanNumber = response.meta['PN']
        except Exception as e:
            print(e)

        try:
            SpecCountry = "USA"
        except Exception as e:
            print(e)

        try:
            MasterBedLocation = "Down"
        except Exception as e:
            print(e)

        sbbg = response.xpath('//div[@class="single-content"]/p/text()').get()
        try:
            if 'sq. ft.' in sbbg:

                SpecSqft = str(sbbg.split(' sq. ft.')[0]).split()[-1]
                if 'total' in SpecSqft:
                    SpecSqft = str(sbbg.split(' sq. ft.')[1]).split()[-1]
                else:
                    SpecSqft = SpecSqft

            else:
                SpecSqft = 0
        except Exception as e:
            print(response.url,e)
            SpecSqft = 0
        try:
            if 'bath' in sbbg:
                bth = str(sbbg.split(' bath')[0]).split()[-1]
                if 'full' in bth:
                    ba = sbbg.split('full')[0].split()[-1]
                    if '1/2' in ba:
                        SpecBaths = sbbg.split('full')[0].split()[-2]
                        SpecHalfBaths = 1
                    else:
                        SpecBaths = ba
                        SpecHalfBaths=0
                else:
                    if '1/2' in bth:
                        SpecHalfBaths = 1
                        SpecBaths = str(sbbg.split(' bath')[0]).split()[-2]
                    else:
                        SpecHalfBaths = 0
                        SpecBaths = bth
            else:
                SpecBaths = 0
                SpecHalfBaths = 0
        except Exception as e:
            print(response.url, e)
            SpecBaths = 0
            SpecHalfBaths = 0

        try:
            if 'bedroom' in sbbg:
                bed = sbbg.split('bedroom')[0].split()[-1]
                SpecBedrooms = bed
            else:
                SpecBedrooms = 0
        except Exception as e:
            print(response.url, e)
            SpecBedrooms = 0
        try:
            if 'car garage' in sbbg:
                g = sbbg.split('car garage')[0].split()[-1]
                SpecGarage = g
            else:
                SpecGarage = 0
        except Exception as e:
            print(response.url, e)
            SpecGarage = 0

        try:
            if '$' in sbbg:
                price = sbbg.split('$')[-1].split(' ')[0]
                if price == '400,':
                    price = '400000'
                    SpecPrice = price
                else:
                    price = price.replace('.', '').replace('!', '').replace(',', '').replace(' ', '')
                    SpecPrice = price
            else:
                SpecPrice = 0
        except Exception as e:
            print(response.url, e)
            SpecPrice = 0

        try:
            des1 = response.xpath('//div[@class="single-content"]/p/text()').get()
        except Exception as e:
            print(response.url, e)
            des1 = ''

        try:
            spec_image = response.meta['specimg']
        except:
            spec_image = 0

        item = BdxCrawlingItem_Spec()
        item['SpecNumber'] = SpecNumber
        item['PlanNumber'] = PlanNumber
        item['SpecStreet1'] = SpecStreet1
        item['SpecCity'] = str(SpecCity).strip()
        item['SpecState'] = SpecState
        item['SpecZIP'] = SpecZIP
        item['SpecCountry'] = SpecCountry
        item['SpecPrice'] = SpecPrice
        item['SpecSqft'] = str(SpecSqft).replace(',','')
        item['SpecBaths'] = SpecBaths
        item['SpecHalfBaths'] = SpecHalfBaths
        item['SpecBedrooms'] = SpecBedrooms
        item['MasterBedLocation'] = MasterBedLocation
        item['SpecGarage'] = str(SpecGarage).replace('-','').strip()
        item['SpecDescription'] = des1
        item['SpecElevationImage'] = spec_image
        item['SpecWebsite'] = response.url
        yield item


# #
from scrapy.cmdline import execute
# execute("scrapy crawl Harding_Homes".split())

