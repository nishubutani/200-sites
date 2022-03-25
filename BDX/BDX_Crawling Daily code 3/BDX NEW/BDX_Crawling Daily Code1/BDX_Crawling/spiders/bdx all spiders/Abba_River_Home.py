# -*- coding: utf-8 -*-
import hashlib
import re
import requests
from scrapy.http import HtmlResponse
import scrapy
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class AbbaRiverHomeSpider(scrapy.Spider):
    name = 'Abba_River_Home'
    allowed_domains = ['www.abbariverhomes.com']
    start_urls = ['http://abbariverhomes.com/']

    builderNumber = "53901"

    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

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
        item['Street1'] = '2601 Cleburne Hwy'
        item['City'] = 'Cresson'
        item['State'] = 'TX'
        item['ZIP'] = '76035'
        item['AreaCode'] = '817'
        item['Prefix'] = '300'
        item['Suffix'] = '4352'
        item['Extension'] = ""
        item['Email'] = 'ARHContactUs@gmail.com'
        SubDescription= ''.join(response.xpath('//div[@id="pp-texttop"]/div//text()').extract()).strip()
        item['SubDescription']=re.sub('[\t]|\n|\s\s+|\r', ' ', str(SubDescription))
        item['SubImage'] = '|'.join(response.xpath('//div[@class="nivoSlider"]/a/img/@src').extract())
        item['SubWebsite'] = response.url
        item['AmenityType'] = ""
        yield item

    ####plan found below
        res_p = requests.get('http://abbariverhomes.com/home-plans-designs/')
        response = HtmlResponse(url=res_p.url, body=res_p.content)
        all_plans = response.xpath('//div[@class="button-block"]/a/@href').extract()
        try:
            for i in all_plans:
                url = i
                # print(url)
                res_p = requests.get(url)
                response = HtmlResponse(url=res_p.url, body=res_p.content)
                item = BdxCrawlingItem_Plan()
                PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
                SubdivisionNumber = self.builderNumber  # if subdivision is there
                unique = str(PlanNumber) + str(SubdivisionNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                item['Type'] = "SingleFamily"
                item['PlanNumber'] = PlanNumber
                item['unique_number'] = unique_number
                item['SubdivisionNumber'] = SubdivisionNumber
                item['PlanName'] = response.xpath('//div[@class="title-block"]/h2/text()').extract_first()
                item['PlanNotAvailable'] = 0
                item['PlanTypeName'] = 'Single Family'
                item['BasePrice'] = 0
                try:
                    if "Sq_Ft</li>" in str(response.text):
                        BaseSqft = re.findall("<li class='parameter-block'>Sq_Ft</li>(.*?)</li>", response.text)[0]
                    else:
                        BaseSqft = re.findall("<li class='parameter-block'>Sq Ft</li>(.*?)</li>", response.text)[0]
                    BaseSqft=BaseSqft.replace(",","")
                    tmp = re.findall(r"(\d+)", BaseSqft)
                    BaseSqft = tmp[0]
                    item['BaseSqft'] = BaseSqft
                except Exception as e:
                    item['BaseSqft'] = 0

                try:
                    Bedrooms = re.findall("<li class='parameter-block'>Bedrooms</li>(.*?)</li>", response.text)[0]
                    tmp = re.findall(r"(\d+)", Bedrooms)[0]
                    Bedrooms = tmp[0]
                    item['Bedrooms'] = Bedrooms
                except Exception as e:
                    item['Bedrooms'] = 0
                try:
                    Baths = re.findall('Baths</li>(.*?)</li>', response.text)[0]
                    tmp = re.findall(r"(\d+)", Baths)
                    item['Baths'] = tmp[0]
                    if len(tmp) > 1:
                        item['HalfBaths'] = 1
                    else:
                        item['HalfBaths'] = 0
                except Exception as e:
                    item['Baths'] = 0
                    item['HalfBaths'] = 0
                try:
                    Garage = re.findall('Garage</li>(.*?)</li>', response.text)[0]
                    tmp = re.findall(r"(\d+)", Garage)
                    Garage = tmp[0]
                    item['Garage'] = Garage
                except Exception as e:
                    item['Garage'] = 0

                try:
                    item['Description'] = ''.join(response.xpath('//div[@class="entry-content"]/p[1]//text()').extract())
                except Exception as e:
                    item['Description']=""
                    print(str(e))
                try:
                    images = response.xpath('//ul[@class="thumbs-list"]/li/a/@href').extract()
                    item['ElevationImage'] = "|".join(images)
                except Exception as e:
                    print(str(e))
                item['PlanWebsite'] = response.url

                yield item
        except Exception as e:
            print(str(e))

        unique = str("Plan Unknown") + self.builderNumber  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['unique_number'] = unique_number
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = "Plan Unknown"
        item['SubdivisionNumber'] = self.builderNumber
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
        # ------------------------------------------- Extract Homedetails ------------------------------ #
        # url=['http://abbariverhomes.com/hills-of-aledo/']
        url = ['http://abbariverhomes.com/hills-of-aledo/', 'http://abbariverhomes.com/stanford-estates/']
        for i in (url):
            planurl_2=i
            res_p = requests.get(planurl_2)
            response = HtmlResponse(url=res_p.url, body=res_p.content)
            specs_links_all =response.xpath('//div[@class="button-block"]/a/@href').extract()
            try:
                for i in specs_links_all:
                    url =i
                    res_p = requests.get(url)
                    response = HtmlResponse(url=res_p.url, body=res_p.content)
                    item = BdxCrawlingItem_Spec()
                    try:
                        address = response.xpath('//div[@class="title-block"]/h2/text()').extract_first()
                        address =address.split("(")[0].strip()
                        addressRest=(address.split(','))
                        addressRestlen = len(address.split(','))

                        SpecStreet1 = addressRest[0].strip()

                        if addressRestlen==3:
                            SpecState = addressRest[2].split("(")[0].strip()
                            SpecCity = addressRest[1].strip()
                        elif addressRestlen == 4:
                            SpecState = addressRest[3].split("(")[0].strip()
                            SpecCity = addressRest[2].strip()
                        else:
                            SpecState = addressRest[1].split("(")[0].strip()
                            SpecCity = addressRest[1].strip()

                        SpecZIP = "00000"
                        if " " in str(SpecCity):
                            SpecCity1 = SpecCity
                            SpecCity = SpecCity1.split(' ')[0].strip()
                            SpecState1 = SpecCity1.split(' ')[1].strip()
                            SpecState = SpecState1.split("(")[0].strip()

                        unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
                        SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

                        f = open("html/%s.html" % SpecNumber, "wb")
                        f.write(response.body)
                        f.close()

                    except Exception as e:
                        print(e)

                    # try:
                    #     PlanNumber = response.meta['PN']
                    # except Exception as e:
                    #     print(e)

                    try:
                        SpecCountry = "USA"
                    except Exception as e:
                        print(e)
                    try:
                        if "Sq_Ft</li>" in str(response.text):
                            SpecSqft = re.findall("<li class='parameter-block'>Sq_Ft</li>(.*?)</li>", response.text)[0]
                        elif "Sq Ft</li>" in str(response.text):
                            SpecSqft = re.findall("<li class='parameter-block'>Sq Ft</li>(.*?)</li>", response.text)[0]
                        elif "Sqft</li>" in str(response.text):
                            SpecSqft = re.findall("<li class='parameter-block'>Sqft</li>(.*?)</li>", response.text)[0]
                        SpecSqft = SpecSqft.replace(",", "")
                        tmp = re.findall(r"(\d+)", SpecSqft)
                        SpecSqft = tmp[0]
                        item['SpecSqft'] = SpecSqft
                    except Exception as e:
                        item['SpecSqft'] = 0

                    try:
                        specBedrooms = re.findall("<li class='parameter-block'>Bedrooms</li>(.*?)</li>", response.text)[0]
                        tmp = re.findall(r"(\d+)", specBedrooms)[0]
                        specBedrooms = tmp[0]
                        item['SpecBedrooms'] = specBedrooms
                    except Exception as e:
                        item['SpecBedrooms'] = 0
                    try:
                        SpecBaths = re.findall('Bathrooms</li>(.*?)</li>', response.text)[0]
                        tmp = re.findall(r"(\d+)", SpecBaths)
                        item['SpecBaths'] = tmp[0]
                        if len(tmp) > 1:
                            item['SpecHalfBaths'] = 1
                        else:
                            item['SpecHalfBaths'] = 0
                    except Exception as e:
                        item['SpecBaths'] = 0
                        item['SpecHalfBaths'] = 0
                    try:
                        Garage = re.findall('Garage</li>(.*?)</li>', response.text)[0]
                        tmp = re.findall(r"(\d+)", Garage)
                        Garage = tmp[0]
                        item['SpecGarage'] = Garage
                    except Exception as e:
                        item['SpecGarage'] = 0

                    try:
                        item['SpecDescription'] = ''.join(
                            response.xpath('//div[@class="entry-content"]/p[1]//text()').extract())
                    except Exception as e:
                        item['SpecDescription'] = ""
                        print(str(e))

                    try:
                        SpecPrice = str(response.xpath('//*[@class="old-price"]/text()').extract_first()).replace(",", "").strip()
                        if SpecPrice=="SOLD":
                            continue
                        SpecPrice = re.findall(r"(\d+)", SpecPrice)[0]
                    except Exception as e:
                        SpecPrice=0
                        print(e)

                    try:
                        MasterBedLocation = "Down"
                    except Exception as e:
                        print(e)

                    try:
                        ElevationImage = response.xpath('//ul[@class="thumbs-list"]/li/a/@href').extract()
                        ElevationImage = "|".join(ElevationImage)
                        SpecElevationImage = ElevationImage
                    except Exception as e:
                        print(e)

                    try:
                        SpecWebsite = response.url
                    except Exception as e:
                        print(e)

                    # ----------------------- Don't change anything here ---------------- #

                    item['SpecNumber'] = SpecNumber
                    item['PlanNumber'] = unique_number
                    item['SpecStreet1'] = SpecStreet1
                    item['SpecCity'] = SpecCity
                    item['SpecState'] = SpecState
                    item['SpecZIP'] = SpecZIP
                    item['SpecCountry'] = SpecCountry
                    item['SpecPrice'] = SpecPrice
                    item['MasterBedLocation'] = MasterBedLocation
                    item['SpecElevationImage'] = SpecElevationImage
                    item['SpecWebsite'] = SpecWebsite
                    yield item
            except Exception as e:
                print(e)

if __name__=='__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl Abba_River_Home".split())
