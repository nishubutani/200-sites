# -*- coding: utf-8 -*-
import hashlib
import re
import requests
from scrapy.http import HtmlResponse
import scrapy
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class MastonpropertiesSpider(scrapy.Spider):
    name = 'mastonproperties'
    allowed_domains = []
    start_urls = ['http://www.mastonproperties.com']

    builderNumber = "593169448898710666081737038589"

    def parse(self, response):

        compage_link = response.xpath('//a[contains(text(),"New Communities")]/@href').extract_first(default='').strip()
        res__c = requests.get(self.start_urls[0]+compage_link[1:])
        response_c = HtmlResponse(url=res__c.url,body=res__c.content)

        com_links = response_c.xpath('//a[@class="MPC_TanToWhiteNoUnderline"]/@href').extract()
        com_cities = response_c.xpath('//a[@class="MPC_TanToWhiteNoUnderline"]/ancestor::font[1]/following-sibling::font/text()').extract()
        com_street = response_c.xpath('//a[@class="MPC_TanToWhiteNoUnderline"]/text()').extract()
        for ct in com_cities:
            if 'Coming' in ct:
                com_cities.remove(ct)

        for link in range(len(com_links)):
            if 'http' in com_links[link]:
                continue
            else:
                n = com_links.index(com_links[link])
                Street1 = com_street[n]
                City = str(com_cities[n]).replace('(','').replace(')','').strip()
                if City =='Lake Forest Park':
                    ZIP = '98155'
                elif City =='West Seattle':
                    ZIP = '98116'
                elif City =='Redmond':
                    ZIP = '98008'
                sbdn_link = com_links[link]
                res_cl = requests.get(self.start_urls[0]+str(sbdn_link[1:]))
                response_cl = HtmlResponse(url=res_cl.url,body=res_cl.content)

                image = response_cl.xpath('//img[contains(@border,"2")]/@src').extract()

                # ------------------- If communities found ---------------------- #
                # ------------------- Creating Communities ---------------------- #
                subdivisonName = Street1+' '+ZIP
                subdivisonNumber = int(hashlib.md5(bytes(subdivisonName,"utf8")).hexdigest(), 16) % (10 ** 30)

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
                item2['Street1'] = Street1
                item2['City'] = City
                item2['State'] = "WA"
                item2['ZIP'] = ZIP
                item2['AreaCode'] = "425"
                item2['Prefix'] = "787"
                item2['Suffix'] = "2137"
                item2['Extension'] = ""
                item2['Email'] = "inforamtion@MastonProperties.com"
                item2['SubDescription'] = ''.join(response.xpath('//*[@face="Times New Roman"][contains(@color,"#FFFFFF")]//text()').extract())
                item2['SubImage'] = str('|'.join(["http://www.mastonproperties.com" + img for img in image]))
                item2['SubWebsite'] = response.url
                yield item2

                # ------------------- If NO Plan Found found ---------------------- #

                # In case you have found the communities (subdivision) and Homes (Specs) but you are not able to find the plan details then,
                # please use this line of code, and reference this unique_number  in All Home(Specs)

                unique = str("Plan Unknown") + str(subdivisonNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                item = BdxCrawlingItem_Plan()
                item['unique_number'] = unique_number
                item['Type'] = "SingleFamily"
                item['PlanNumber'] = PlanNumber="Plan Unknown"
                item['SubdivisionNumber'] = subdivisonNumber
                item['PlanName'] = "Plan Unknown"
                item['PlanNotAvailable'] = 1
                item['PlanTypeName'] = "Single Family"
                item['BasePrice'] = 0
                item['BaseSqft'] = 0
                item['Baths'] = 1
                item['HalfBaths'] = 0
                item['Bedrooms'] = 1
                item['Garage'] = 0
                item['Description'] = ""
                item['ElevationImage'] = ""
                item['PlanWebsite'] = ""
                yield item

                specs_page = response_cl.xpath('//a[contains(text(),"Homes For Sale")]/@href').extract_first(default='').strip()
                res_s = requests.get(self.start_urls[0]+specs_page[1:])
                response_s = HtmlResponse(url=res_s.url,body = res_s.content)

                specs_text = response_s.xpath('//font[@face="Times New Roman"][contains(@color,"#FFFFFF")]')
                for s in range(len(specs_text)):
                    print('# ------------------------- '+str(response_s.url))

                    specs_data = specs_text[s].xpath('./text()').extract()
                    # ------------------------------------------- Extract Homedetails ------------------------------ #

                    try:
                        address = specs_text[s].xpath('./b/text()').extract()
                        if '\n' in address:
                            address.remove('\n')
                        if '\r\n' in address:
                            address.remove('\r\n')

                        SpecStreet1 = address[0].strip()
                        if len(address)==2:
                            city_state_zip = address[1].split(',')
                            SpecCity = str(city_state_zip[0]).strip()
                            SpecState = str(re.findall('(\D+)',city_state_zip[1])[0]).strip()
                            SpecZIP = str(re.findall('(\d+)', city_state_zip[1])[0]).strip()
                        elif len(address)<2:
                            address=  specs_text[s].xpath('.//text()').extract()[:3]
                            if address[2]=='\r\n':
                                if '\n' in address:
                                    address.remove('\n')
                                if '\r\n' in address:
                                    address.remove('\r\n')

                                SpecStreet1 = address[0].strip()
                                if len(address) == 2:
                                    city_state_zip = address[1].split(',')
                                    SpecCity = str(city_state_zip[0]).strip()
                                    SpecState = str(re.findall('(\D+)', city_state_zip[1])[0]).strip()
                                    SpecZIP = str(re.findall('(\d+)', city_state_zip[1])[0]).strip()
                            else:
                                SpecCity='Bothell'
                                SpecState='WA'
                                SpecZIP='98021'
                        else:
                            SpecCity = 'Bothell'
                            SpecState = 'WA'
                            SpecZIP = '98021'

                        unique = SpecStreet1 + str(response_s.url)
                        SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

                        f = open("html/%s.html" % SpecNumber, "wb")
                        f.write(response.body)
                        f.close()

                    except Exception as e:
                        print(e)

                    try:
                        PlanNumber = "Plan Unknown"
                    except Exception as e:
                        print(e)

                    try:
                        SpecCountry = "USA"
                    except Exception as e:
                        print(e)

                    try:
                        SpecPrice = 0
                    except Exception as e:
                        print(e)

                    try:
                        if specs_data !='':
                            # --------------- sqft
                            for d in specs_data:
                                if 'Sq. Ft.' in d:
                                    sqft = d.replace(',','')
                                    SpecSqft = re.findall('(\d+)',str(sqft))[0]
                                    break
                                else:
                                    SpecSqft=0

                            # --------------- bath
                            for d in specs_data:
                                if 'Bath' in d:
                                    tmp = re.findall(r"(\d+)", d)
                                    SpecBaths = tmp[0]
                                    if len(tmp) > 1:
                                        SpecHalfBaths = 1
                                    else:
                                        SpecHalfBaths = 0
                                    break
                                else:
                                    SpecBaths=0
                                    SpecHalfBaths = 0

                            # --------------- garage
                            for d in specs_data:
                                if 'Car Garage' in d:
                                    SpecGarage = re.findall('(\d+)',str(d))[0]
                                    break
                                else:
                                    SpecGarage=0

                            # --------------- garage
                            for d in specs_data:
                                if 'Bedrooms' in d:
                                    SpecBedrooms = re.findall('(\d+)', str(d))[0]
                                    break
                                else:
                                    SpecBedrooms = 0

                    except Exception as e:
                        print(e)

                    try:
                        MasterBedLocation = "Down"
                    except Exception as e:
                        print(e)

                    try:
                        SpecDescription = ''
                    except Exception as e:
                        print(e)

                    try:
                        SpecElevationImage = self.start_urls[0]+str(response_s.xpath('//img[@border="2"]/@src').extract_first(default='').strip())
                    except Exception as e:
                        print(e)

                    try:
                        SpecWebsite = response_s.url
                    except Exception as e:
                        print(e)

                    # ----------------------- Don't change anything here ---------------- #
                    try:
                        item = BdxCrawlingItem_Spec()
                        item['SpecNumber'] = SpecNumber
                        item['PlanNumber'] = unique_number
                        item['SpecStreet1'] = SpecStreet1
                        item['SpecCity'] = SpecCity
                        item['SpecState'] = str(SpecState).strip()
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
                    except Exception as e:
                        print(e)
                    # --------------------------------------------------------------------- #



# from scrapy.cmdline import execute
# execute("scrapy crawl mastonproperties --nolog".split())