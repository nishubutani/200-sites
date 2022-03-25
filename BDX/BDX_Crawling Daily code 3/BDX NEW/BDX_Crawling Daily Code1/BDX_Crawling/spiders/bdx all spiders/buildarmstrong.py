# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class BuildArmstrongSpider(scrapy.Spider):
    name = 'buildarmstrong'
    allowed_domains = []
    start_urls = ['https://buildarmstrong.com/live/subdivisions']

    builderNumber = "344647556980929903684328997446"

    def parse(self, response):

        item1 = BdxCrawlingItem_subdivision()
        item1['sub_Status'] = "Active"
        item1['SubdivisionNumber'] = ''
        item1['BuilderNumber'] = self.builderNumber
        item1['SubdivisionName'] = "No Sub Division"
        item1['BuildOnYourLot'] = 0
        item1['OutOfCommunity'] = 1
        item1['Street1'] = '1701 Tullamore Ave. Ste. A'
        item1['City'] = 'Bloomington'
        item1['State'] = 'IL'
        item1['ZIP'] = '61704'
        item1['AreaCode'] = '309'
        item1['Prefix'] = '661'
        item1['Suffix'] = '1950'
        item1['Extension'] = ''
        item1['Email'] = 'info@buildarmstrong.com'
        item1[
            'SubDescription'] = 'Vic Armstrong, Jr. has been a leader in the Bloomington-Normal real estate industry for over 45 years. Vic began working with his father, Vic Armstrong, Sr., in 1967. After his father retired, Vic continued to successfully expand Armstrong Builders into two new markets: Champaign and Peoria. During his career, Vic has built over 4,500 homes and 1,000 apartments in Peoria and Bloomington. Vic Armstrong is a licensed real estate agent in the state of Illinois.Tom Armstrong is a Bloomington native. After graduating from Illinois Wesleyan in 1989, Tom owned a construction company for 15 years, building and remodeling homes in the Wrigley Field area of Chicago. In 2005, he returned home to Bloomington to be the owner and manager of Armstrong Builders of Peoria. In 2010, Tom stepped into the role of owner and manager of Armstrong Builders in Bloomington as well. Tom Armstrong is a licensed real estate agent in the state of Illinois.Paul Phillips has been involved in the building industry of Central and east Central Illinois for over 30 years. Having first provided services for other builders, he then became partner and owner of Armstrong Construction of Champaign twenty years ago. Since that time, Paul has focused on quality-built homes, specifically custom home building and remodeling.'
        item1[
            'SubImage'] = 'https://buildarmstrong.com/image/3501/1200|https://buildarmstrong.com/image/4299/1800|https://buildarmstrong.com/image/4283/1800|https://buildarmstrong.com/image/3461/1800|https://buildarmstrong.com/image/4275/1800'
        item1['AmenityType'] = ''
        item1['SubWebsite'] = response.url
        yield item1


        links = response.xpath('//*[@class="subdivisions__link"]/@href').extract()
        for link in links:
            yield scrapy.Request(url='https://buildarmstrong.com'+link, callback=self.communities)


    def communities(self, response):
        subdivisonName = response.xpath('//h1[@class="title__title"]/text()').extract_first(default="").strip()
        subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)

        f = open("html/%s.html" % subdivisonNumber, "wb")
        f.write(response.body)
        f.close()

        try:
            add = response.xpath('//h2[contains(text(),"Site Address")]/../following-sibling::td/strong/text()').extract_first(default='').strip()
            if add != '':
                state = re.findall(r'[A-Z]{2}',add)[0]
                zip =  re.findall(r'(\d{5})', add)[0].strip()


                images = 'https://buildarmstrong.com' + response.xpath('//img[@class="listings__image listings__profileImage"]/@src').extract_first()

                item = BdxCrawlingItem_subdivision()
                item['sub_Status'] = "Active"
                item['SubdivisionName'] = subdivisonName
                item['SubdivisionNumber'] = subdivisonNumber
                item['BuilderNumber'] = self.builderNumber
                item['BuildOnYourLot'] = 0
                item['OutOfCommunity'] = 0
                item['State'] = state
                item['ZIP'] = zip
                item['City'] = add.replace(item['ZIP'],'').replace(item['State'],'').strip().split()[-1]
                item['Street1'] = add.replace(item['ZIP'],'').replace(item['State'],'').replace(item['City'],'').strip()
                item['AreaCode'] = '309'
                item['Prefix'] = '661'
                item['Suffix'] = '1950'
                item['Extension'] = ""
                item['Email'] = "info@buildarmstrong.com"
                item['SubDescription'] = 'Vic Armstrong, Jr. has been a leader in the Bloomington-Normal real estate industry for over 45 years. Vic began working with his father, Vic Armstrong, Sr., in 1967. After his father retired, Vic continued to successfully expand Armstrong Builders into two new markets: Champaign and Peoria. During his career, Vic has built over 4,500 homes and 1,000 apartments in Peoria and Bloomington. Vic Armstrong is a licensed real estate agent in the state of Illinois.Tom Armstrong is a Bloomington native. After graduating from Illinois Wesleyan in 1989, Tom owned a construction company for 15 years, building and remodeling homes in the Wrigley Field area of Chicago. In 2005, he returned home to Bloomington to be the owner and manager of Armstrong Builders of Peoria. In 2010, Tom stepped into the role of owner and manager of Armstrong Builders in Bloomington as well. Tom Armstrong is a licensed real estate agent in the state of Illinois.Paul Phillips has been involved in the building industry of Central and east Central Illinois for over 30 years. Having first provided services for other builders, he then became partner and owner of Armstrong Construction of Champaign twenty years ago. Since that time, Paul has focused on quality-built homes, specifically custom home building and remodeling.'
                item['SubImage'] = images
                item['AmenityType'] = ''
                item['SubWebsite'] = response.url
                yield item


                yield scrapy.Request(url='https://buildarmstrong.com/live/listings/for-sale', dont_filter=True,
                                     callback=self.all_homes,
                                     meta={ 'fpn': self.builderNumber, 'name':subdivisonName,
                                           'sbdn': subdivisonNumber})
        except Exception as e:
            print(e)



    def all_homes(self, response):
        sbdn = response.meta['sbdn']
        sName = response.meta['name']
        fpn = response.meta['fpn']
        links = response.xpath('//*[@class="listings__link"]/@href').extract()
        for link in links:
            link = 'https://buildarmstrong.com'+str(link)
            yield scrapy.Request(url=link, callback=self.HomesDetails,meta={'sbdn':sbdn,'name':sName,'fpn':fpn}, dont_filter=True)

    def HomesDetails(self, response):
        sbdn = response.meta['sbdn']
        name = response.meta['name']
        sname = response.xpath('//*[@class="listings__profileContent"]/div/p[2]/span/text()').extract_first().strip()
        SpecStreet1 = response.xpath('//*[@class="listings__profileTitle"]/span/text()').extract_first()

        if sname == name:
            # unique = str(sbdn)  # < -------- Changes here
            unique = str("Plan Unknown")   # < -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
            item1 = BdxCrawlingItem_Plan()
            item1['unique_number'] = unique_number
            item1['Type'] = "SingleFamily"
            item1['PlanNumber'] = "Plan Unknown"
            item1['SubdivisionNumber'] = sbdn
            item1['PlanName'] = "Plan Unknown"
            item1['PlanNotAvailable'] = 1
            item1['PlanTypeName'] = 'Single Family'
            item1['BasePrice'] = 0
            item1['BaseSqft'] = 0
            item1['Baths'] = 1
            item1['HalfBaths'] = 0
            item1['Bedrooms'] = 0
            item1['Garage'] = 0
            item1['Description'] = "Armstrong Builders strives to satisfy customers, one home at a time, by constructing the markets best custom homes. Building homes in Bloomington, Champaign, Peoria and surrounding communities. Founded in 1963, Armstrong Builders is a company deeply committed to providing quality homes at affordable prices. Personal service is a key to our success. We involve the customer in every step, from the design phase, through construction, to a final walk-through. The Armstrong team cares about its products, its industry and its customer. All Armstrong homes are 2009 Illinois Energy Conservation Code compliant."
            item1['ElevationImage'] = "https://buildarmstrong.com/image/3501/1200|https://buildarmstrong.com/image/4299/1800|https://buildarmstrong.com/image/4283/1800|https://buildarmstrong.com/image/3461/1800|https://buildarmstrong.com/image/4275/1800"
            item1['PlanWebsite'] = "http://www.buildarmstrong.com"
            yield item1

            try:
                try:
                    SpecStreet1 = response.xpath('//*[@class="listings__profileTitle"]/span/text()').extract_first()
                except Exception as e:
                    print(e)

                try:
                    SpecC = re.findall('"city":"(.*?)",',response.text)
                    SpecCity = SpecC[0]
                except Exception as e:
                    SpecCity = "Chicago"
                    print(e)

                try:
                    state = re.findall('"state":"(.*?)",',response.text)
                    SpecState = state[0]
                except Exception as e:
                    SpecState = 'FL'
                    print(e)

                try:
                    zip = re.findall('"zip":"(.*?)",', response.text)
                    if  zip ==['']:
                        SpecZIP='00000'
                    else:
                        SpecZIP = zip[0]
                        print(SpecZIP)
                except Exception as e:
                    SpecZIP = '00000'


                unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
                print(unique)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()


                try:
                    PlanNumber = unique_number
                except Exception as e:
                    print(e)

                try:
                    SpecCountry = "USA"
                except Exception as e:
                    print(e)

                try:
                    price = response.xpath('//*[@class="listings__profileTitle"]/span[2]/text()').extract_first()
                    if price == None:
                        price = '0'
                    else:
                        price = price.replace('$','').replace(',','').strip()
                except Exception as e:
                    print(e)

                try:
                    SpecBedrooms = response.xpath('//p[contains(text(),"Bedrooms")]/text()').extract_first().strip()
                    SpecBedrooms =  re.findall(r'(\d{1})', SpecBedrooms)[0]
                except Exception as e:
                    print(str(e))

                try:
                    SpecBaths = response.xpath('//p[contains(text(),"Toilet")]/text()').extract_first().strip().split()[0]
                    if ".5" in SpecBaths:
                        SpecBaths = SpecBaths.split('.')[0].sstrip()
                        halfbath = 1
                    else:
                        SpecBaths = SpecBaths
                        halfbath = 0
                except Exception as e:
                    print(str(e))

                try:
                    SpecGarage = response.xpath('//p[contains(text(),"Garage")]/text()').extract_first().strip()
                    SpecGarage = re.findall(r'(\d{1})', SpecGarage)[0]
                except Exception as e:
                    print(str(e))

                try:
                    SpecSqft = response.xpath('//*[@class="listings__row listings__numbers"]/p[1]/text()').extract_first().strip()
                except Exception as e:
                    print(str(e))

                try:
                    MasterBedLocation = "Down"
                except Exception as e:
                    print(e)

                try:
                    SpecDescription = "Armstrong Builders strives to satisfy customers, one home at a time, by constructing the markets best custom homes. Building homes in Bloomington, Champaign, Peoria and surrounding communities. Founded in 1963, Armstrong Builders is a company deeply committed to providing quality homes at affordable prices. Personal service is a key to our success. We involve the customer in every step, from the design phase, through construction, to a final walk-through. The Armstrong team cares about its products, its industry and its customer. All Armstrong homes are 2009 Illinois Energy Conservation Code compliant"
                except Exception as e:
                    print(e)

                try:
                    image = response.xpath('//*[@class="listings__image listings__profileImage"]/@src').extract_first()
                    ElevationImage = "https://buildarmstrong.com"+image
                except Exception as e:
                    print(e)

                try:
                    SpecWebsite = response.url
                except Exception as e:
                    print(e)

                # ----------------------- Don't change anything here --------------------- #
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = PlanNumber
                item['SpecStreet1'] = SpecStreet1
                item['SpecCity'] = SpecCity
                item['SpecState'] = SpecState
                item['SpecZIP'] = SpecZIP
                item['SpecCountry'] = SpecCountry
                item['SpecPrice'] = price
                item['SpecSqft'] = SpecSqft
                item['SpecBaths'] = SpecBaths
                item['SpecHalfBaths'] = halfbath
                item['SpecBedrooms'] = SpecBedrooms
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = SpecGarage
                item['SpecDescription'] = SpecDescription
                item['SpecElevationImage'] = ElevationImage
                item['SpecWebsite'] = SpecWebsite
                yield item

            except Exception as e:
                print(e)
        else:
            # unique = str(sbdn)  # < -------- Changes here
            unique = str("Plan Unknown")  # < -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
                        10 ** 30)  # < -------- Changes here
            item1 = BdxCrawlingItem_Plan()
            item1['unique_number'] = unique_number
            item1['Type'] = "SingleFamily"
            item1['PlanNumber'] = "Plan Unknown"
            item1['SubdivisionNumber'] = self.builderNumber
            item1['PlanName'] = "Plan Unknown"
            item1['PlanNotAvailable'] = 1
            item1['PlanTypeName'] = 'Single Family'
            item1['BasePrice'] = 0
            item1['BaseSqft'] = 0
            item1['Baths'] = 1
            item1['HalfBaths'] = 0
            item1['Bedrooms'] = 0
            item1['Garage'] = 0
            item1[
                'Description'] = "Armstrong Builders strives to satisfy customers, one home at a time, by constructing the markets best custom homes. Building homes in Bloomington, Champaign, Peoria and surrounding communities. Founded in 1963, Armstrong Builders is a company deeply committed to providing quality homes at affordable prices. Personal service is a key to our success. We involve the customer in every step, from the design phase, through construction, to a final walk-through. The Armstrong team cares about its products, its industry and its customer. All Armstrong homes are 2009 Illinois Energy Conservation Code compliant."
            item1[
                'ElevationImage'] = "https://buildarmstrong.com/image/3501/1200|https://buildarmstrong.com/image/4299/1800|https://buildarmstrong.com/image/4283/1800|https://buildarmstrong.com/image/3461/1800|https://buildarmstrong.com/image/4275/1800"
            item1['PlanWebsite'] = "http://www.buildarmstrong.com"
            yield item1
            try:
                SpecStreet1 = response.xpath('//*[@class="listings__profileTitle"]/span/text()').extract_first()
            except Exception as e:
                print(e)

            try:
                SpecC = re.findall('"city":"(.*?)",', response.text)
                SpecCity = SpecC[0]
            except Exception as e:
                SpecCity = "Chicago"
                print(e)

            try:
                state = re.findall('"state":"(.*?)",', response.text)
                SpecState = state[0]
            except Exception as e:
                SpecState = 'FL'
                print(e)

            try:
                zip = re.findall('"zip":"(.*?)",', response.text)
                if zip == ['']:
                    SpecZIP = '00000'
                else:
                    SpecZIP = zip[0]
                    print(SpecZIP)
            except Exception as e:
                SpecZIP = '00000'

            unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
            print(unique)
            SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

            f = open("html/%s.html" % SpecNumber, "wb")
            f.write(response.body)
            f.close()

            # try:
            #     PlanNumber = response.meta['pn']
            # except Exception as e:
            #     print(e)
            #

            try:
                PlanNumber = response.meta['fpn']
            except Exception as e:
                print(e)

            try:
                price = response.xpath('//*[@class="listings__profileTitle"]/span[2]/text()').extract_first()
                if price == None:
                    price = '0'
                else:
                    price = price.replace('$', '').replace(',', '').strip()
            except Exception as e:
                print(e)

            try:
                SpecCountry = "USA"
            except Exception as e:
                print(e)

            try:
                SpecBedrooms = response.xpath('//p[contains(text(),"Bedrooms")]/text()').extract_first().strip()
                SpecBedrooms = re.findall(r'(\d{1})', SpecBedrooms)[0]
            except Exception as e:
                print(str(e))

            try:
                SpecBaths = response.xpath('//p[contains(text(),"Toilet")]/text()').extract_first().strip().split()[0]
                if ".5" in SpecBaths:
                    SpecBaths = SpecBaths.replace('.5', '').strip()
                    halfbath = 1
                else:
                    SpecBaths = SpecBaths
                    halfbath = 0
            except Exception as e:
                print(str(e))

            try:
                SpecGarage = response.xpath('//p[contains(text(),"Garage")]/text()').extract_first().strip()
                SpecGarage = re.findall(r'(\d{1})', SpecGarage)[0]
            except Exception as e:
                print(str(e))

            try:
                SpecSqft = response.xpath(
                    '//*[@class="listings__row listings__numbers"]/p[1]/text()').extract_first().strip()
            except Exception as e:
                print(str(e))

            try:
                MasterBedLocation = "Down"
            except Exception as e:
                print(e)

            try:
                SpecDescription = "Armstrong Builders strives to satisfy customers, one home at a time, by constructing the markets best custom homes. Building homes in Bloomington, Champaign, Peoria and surrounding communities. Founded in 1963, Armstrong Builders is a company deeply committed to providing quality homes at affordable prices. Personal service is a key to our success. We involve the customer in every step, from the design phase, through construction, to a final walk-through. The Armstrong team cares about its products, its industry and its customer. All Armstrong homes are 2009 Illinois Energy Conservation Code compliant"
            except Exception as e:
                print(e)

            try:
                image = response.xpath('//*[@class="listings__image listings__profileImage"]/@src').extract_first()
                ElevationImage = "https://buildarmstrong.com" + image
            except Exception as e:
                print(e)

            try:
                SpecWebsite = response.url
            except Exception as e:
                print(e)

            # ----------------------- Don't change anything here --------------------- #
            item = BdxCrawlingItem_Spec()
            item['SpecNumber'] = SpecNumber
            item['PlanNumber'] = PlanNumber
            item['SpecStreet1'] = SpecStreet1
            item['SpecCity'] = SpecCity
            item['SpecState'] = SpecState
            item['SpecZIP'] = SpecZIP
            item['SpecCountry'] = SpecCountry
            item['SpecPrice'] = price
            item['SpecSqft'] = SpecSqft
            item['SpecBaths'] = SpecBaths
            item['SpecHalfBaths'] = halfbath
            item['SpecBedrooms'] = SpecBedrooms
            item['MasterBedLocation'] = MasterBedLocation
            item['SpecGarage'] = SpecGarage
            item['SpecDescription'] = SpecDescription
            item['SpecElevationImage'] = ElevationImage
            item['SpecWebsite'] = SpecWebsite
            yield item

if __name__=='__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl buildarmstrong'.split())

