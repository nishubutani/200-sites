# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class CalynhomesSpider(scrapy.Spider):
    name = 'calynhomes'
    allowed_domains = ['www.calynhomes.com']
    start_urls = ['http://www.calynhomes.com']
    builderNumber = '49267'

    def parse(self, response):

        community_links = response.xpath('//*[@class="dropdown"][4]/ul/li/a/@href').getall()
        del community_links[0]

        for community_link in community_links:
            community_link = 'http://www.calynhomes.com' + community_link
            yield scrapy.FormRequest(url=community_link,callback=self.community_detail)

    def community_detail(self,response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        SubdivisionName = response.xpath('//*[@class="comm-header-wrapper"]/div/h2/text()').get()
        SubdivisionNumber = int(hashlib.md5(bytes(str(SubdivisionName) + str(self.builderNumber), "utf8")).hexdigest(),
                                16) % (10 ** 30)
        item['SubdivisionNumber'] = SubdivisionNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = SubdivisionName
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        try:
            item['Street1'] = response.xpath('//*[@class="comm-header-wrapper"]//div[@class="comm_header_cols"][2]/p[1]/text()[1]').get()
            cityzip = response.xpath('//*[@class="comm-header-wrapper"]//div[@class="comm_header_cols"][2]/p[1]/text()[2]').get().strip()
        except:
            item['Street1'] = ''
            cityzip = response.xpath(
                '//*[@class="comm-header-wrapper"]//div[@class="comm_header_cols"][2]/p[1]/text()[1]').get().strip()

        item['City'] = cityzip.split(',')[0].strip()
        item['State'] = cityzip.split(',')[1].strip().split()[0].strip()
        item['ZIP'] = cityzip.split(',')[1].strip().split()[1].strip()
        phone = response.xpath('//div[@class="comm_header_cols"]//span[contains(text(),"PH:")]/following-sibling::text()[1]').get()
        try:
            item['AreaCode'] = phone.split()[0].replace('(', '').replace(')', '')
            item['Prefix'] = phone.split()[1].split('-')[0]
            item['Suffix'] = phone.split()[1].split('-')[1]
        except:
            item['AreaCode'] = ''
            item['Prefix'] = ''
            item['Suffix'] = ''

        item['Extension'] = ""
        item['Email'] = 'bigelow@bigelowhomes.net'
        item[
            'SubDescription'] = response.xpath('//*[@class="entry-content"]/p[2]//text()').get()
        image = response.xpath('//div[@class="comm_header_cols"]/img/@src').get()
        if image:
            item[
                'SubImage'] = 'http://www.calynhomes.com' + str(image)
        else:
            item[
                'SubImage'] = ''

        item['SubWebsite'] = response.url
        yield item

        planlink = "http://www.calynhomes.com" + str(response.xpath('//*[@class="plans"]/a/@href').get())
        yield scrapy.FormRequest(url=planlink, dont_filter=True, callback=self.Plans_urls,
                                 meta={'SubdivisionNumber': SubdivisionNumber,'SubdivisionName': SubdivisionName})

    def Plans_urls(self, response):
        SubdivisionName = response.meta['SubdivisionName']
        SubdivisionNumber = response.meta['SubdivisionNumber']
        divs = response.xpath('//*[@class="mod_infobox"]')
        if divs != []:
            for div in divs:
                url = 'http://www.calynhomes.com' + str(div.xpath('./a/@href').get())
                bedrooms = div.xpath('.//ul/li/span[contains(text(),"Bedrooms:")]/following-sibling::text()').get().strip()

                bathrooms = div.xpath('.//ul/li/span[contains(text(),"Bathrooms:")]/following-sibling::text()').get()
                if not bathrooms:

                    unique = str("Plan Unknown") + str(SubdivisionNumber)  # < -------- Changes here
                    unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
                            10 ** 30)  # < -------- Changes here
                    print(unique_number)
                    item = BdxCrawlingItem_Plan()
                    item['unique_number'] = unique_number
                    plandetail = {}
                    plandetail[SubdivisionName] = unique_number
                    item['Type'] = "SingleFamily"
                    item['PlanNumber'] = "Plan Unknown"
                    item['SubdivisionNumber'] = SubdivisionNumber
                    item['PlanName'] = "Plan Unknown"
                    item['PlanNotAvailable'] = 1
                    item['PlanTypeName'] = 'Single Family'
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

                    homelink = 'http://www.calynhomes.com' + str(response.xpath('//*[@class="homes"]/a/@href').get())

                    yield scrapy.FormRequest(url=homelink, dont_filter=True, callback=self.homeurl,
                                             meta={ 'PN': plandetail,
                                                   'homelink': homelink,
                                                   'bathrooms':0})
                else:
                    planname = div.xpath('.//h4/text()').get()
                    homelink = 'http://www.calynhomes.com' + str(response.xpath('//*[@class="homes"]/a/@href').get())

                    yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.Plans_details, meta={'SubdivisionNumber': SubdivisionNumber,'planname':planname,

                                                                                                       'bathrooms':bathrooms,'bedrooms':bedrooms,'homelink':homelink,'SubdivisionName': SubdivisionName})
        else:

            unique = str("Plan Unknown") + str(SubdivisionNumber)  # < -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
                        10 ** 30)  # < -------- Changes here
            print(unique_number)
            item = BdxCrawlingItem_Plan()
            item['unique_number'] = unique_number
            plandetail = {}
            plandetail[SubdivisionName] = unique_number
            item['Type'] = "SingleFamily"
            item['PlanNumber'] = "Plan Unknown"
            item['SubdivisionNumber'] = SubdivisionNumber
            item['PlanName'] = "Plan Unknown"
            item['PlanNotAvailable'] = 1
            item['PlanTypeName'] = 'Single Family'
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

            homelink = 'http://www.calynhomes.com' + str(response.xpath('//*[@class="homes"]/a/@href').get())

            yield scrapy.FormRequest(url=homelink, dont_filter=True, callback=self.homeurl,
                                     meta={'SubdivisionNumber': SubdivisionNumber, 'PN': plandetail ,'homelink':homelink,'bathrooms':0})

    def Plans_details(self,response):
        homelink = response.meta['homelink']
        garage = response.xpath('//span[contains(text(),"Garage")]/parent::li/text()').get()
        if garage != None:
            garage = re.findall(r'(\d)',garage)[0]
        else:
            garage = 0

        image = response.xpath('//img[contains(@src,"jpg")]/@src').getall()

        item = BdxCrawlingItem_Plan()

        PlanName = response.meta['planname']
        SubdivisionName = response.meta['SubdivisionName']

        PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        f = open("html/%s.html" % PlanNumber, "wb")
        f.write(response.body)
        f.close()

        bathrooms = response.meta['bathrooms']
        try:
            if '.' in bathrooms:
                bathrooms = bathrooms.split('.')[0]
                halfbaths = 1
            else:
                bathrooms = bathrooms
                halfbaths = 0
        except:
            bathrooms = 0
            halfbaths = 0


        plandetails = {}
        SubdivisionNumber = response.meta['SubdivisionNumber']
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        mapp1 = str(PlanName) + '_' + str(response.meta['SubdivisionName'])
        plandetails[mapp1] = unique_number
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = PlanName
        item['Baths'] = bathrooms
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0
        item['BaseSqft'] = 0
        item['HalfBaths'] = halfbaths
        item['Bedrooms'] = response.meta['bedrooms']
        item['Garage'] = garage
        item[
            'Description'] = "Calyn Homes is Johnson County's premier custom home builder. Founded on the principles of quality craftsmanship, hands-on service, and innovative design, Calyn Homes offers homebuyers a uniquely personal, one-on-one experience as they build their dream home in Olathe or Overland Park."
        images = []
        for i in image:
            image = 'http://www.calynhomes.com' + str(i)
            images.append(image)
        item['ElevationImage'] = "|".join(images)

        item['PlanWebsite'] = response.url
        yield item

        yield scrapy.FormRequest(url=response.url, dont_filter=True, callback=self.homeurl,
                                 meta={ 'PN': plandetails,
                                       'homelink':homelink,'bathrooms':bathrooms})

    def homeurl(self,response):

        PN = response.meta['PN']

        bathrooms = response.meta['bathrooms']


        homelink = response.meta['homelink']

        yield scrapy.FormRequest(url=homelink, dont_filter=True, callback=self.home,meta={'PN': PN,'bathrooms':bathrooms})

    def home(self,response):
        PN = response.meta['PN']

        bathrooms = response.meta['bathrooms']

        divs = response.xpath('//div[@class="mod_btns"]')
        for div in divs:
            link = 'http://www.calynhomes.com' + str(div.xpath('./a/@href').get())
            yield scrapy.FormRequest(url=link, dont_filter=True, callback=self.home_detail,meta={'PN':PN,'bathrooms':bathrooms})

    def home_detail(self, response):
        global PlanNumber, SpecStreet1, mappp, SubdivisionName
        try:
            PN = response.meta['PN']
            bathrooms = response.meta['bathrooms']

            try:
                details = response.xpath('//div[@class="detail-left"]/h3//text()').getall()

                add = details[-1].split(',')
                SpecStreet1 = details[0]
                SpecCity = add[0].strip()
                SpecState = add[-1].split()[0].strip()
                SpecZIP = add[-1].split()[1].strip()

                planName = response.xpath(
                    '//span[contains(text(),"Plan Name:")]/following-sibling::a/text()').extract_first()
                SubdivisionName = response.xpath(
                    '//span[contains(text(),"Community:")]/following-sibling::a/text()').extract_first()
                mappp = str(planName) + '_' + str(SubdivisionName)
                unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()

                try:
                    PlanNumber = PN[mappp]
                except:
                    PlanNumber = PN[SubdivisionName]

            except Exception as e:
                PlanNumber = PN

            try:
                SpecCountry = "USA"
            except Exception as e:
                print(e)

            try:
                SpecPrice = response.xpath('//span[contains(text(),"Price:")]/following-sibling::text()').extract_first().strip()
                SpecPrice = SpecPrice.replace('$', '')
                SpecPrice = re.sub(',', '', SpecPrice)
                SpecPrice = SpecPrice.strip()
                # print(SpecPrice)
            except Exception as e:
                print(str(e))

            try:
                SpecBedrooms = response.xpath('//span[contains(text(),"Bedrooms")]/parent::li/text()').extract_first()
                SpecBedrooms = re.findall(r"(\d+)", SpecBedrooms)
                SpecBedrooms = SpecBedrooms[0]
            except Exception as e:
                print(str(e))

            try:
                SpecBath = response.xpath('//span[contains(text(),"Bathrooms")]/parent::li/text()').extract_first().strip()
                SpecBaths = re.findall(r"(\d+)", SpecBath)
                SpecBaths = SpecBaths[0]
                tmp = SpecBath
                if len(tmp) > 1:
                    SpecHalfBaths = 1
                else:
                    SpecHalfBaths = 0
                # print(SpecBaths)
            except Exception as e:
                print(str(e))

            try:
                SpecGarage = response.xpath('//span[contains(text(),"Garage")]/parent::li/text()').extract_first()
                SpecGarage = re.findall(r"(\d+)", SpecGarage)
                SpecGarage = SpecGarage[0]
            except Exception as e:
                print(str(e))

            try:
                SpecSqft = 0
            except Exception as e:
                print(str(e))

            try:
                MasterBedLocation = "Down"
            except Exception as e:
                print(e)

            try:
                SpecDescription = ''

            except Exception as e:
                print(e)

            try:
                image = response.xpath('//*[@class="detail-right"]//a/img/@src').getall()
                images = []
                for i in image:
                    image = 'http://www.calynhomes.com' + str(i)
                    images.append(image)
                ElevationImage ='|'.join(images)

            except Exception as e:
                print(str(e))

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
            item['SpecPrice'] = SpecPrice
            item['SpecSqft'] = SpecSqft
            item['SpecBaths'] = SpecBaths
            item['SpecHalfBaths'] = SpecHalfBaths
            item['SpecBedrooms'] = SpecBedrooms
            item['MasterBedLocation'] = MasterBedLocation
            item['SpecGarage'] = SpecGarage
            item['SpecDescription'] = SpecDescription
            item['SpecElevationImage'] = ElevationImage
            item['SpecWebsite'] = SpecWebsite
            yield item

        except Exception as e:
            print(e)


from scrapy.cmdline import execute
# execute("scrapy crawl calynhomes".split())





