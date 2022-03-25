# -*- coding: utf-8 -*-
import os
import hashlib
import re

import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Plan, BdxCrawlingItem_subdivision, BdxCrawlingItem_Spec


class StanfordHomesIdahoSpider(scrapy.Spider):
    name = 'stanfordhomesidaho'
    allowed_domains = []
    start_urls = ['http://www.stanfordhomesidaho.com/']

    builderNumber = '769010103839058446734136440338'

    def parse(self, response):

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ""
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 1
        item['Street1'] = "1500 W. Bannock"
        item['City'] = "Boise"
        item['State'] = "ID"
        item['ZIP'] = "83702"
        item['AreaCode'] = "208"
        item['Prefix'] = "794"
        item['Suffix'] = "7694"
        item['Extension'] = ""
        item['Email'] = "StanfordHomes@parkpointe.com"
        item['SubDescription'] = 'Stanford Homes has over 40 years experience in home building. We know flexibility and communication are key to building a quality home to suit any lifestyle.'
        item['SubImage'] = 'http://www.stanfordhomesidaho.com/System/Resources/Themes/79f56a7f-d6c1-4042-8f8f-c245eaaccdd1/images/photo%20montoge.jpg'
        item['SubWebsite'] = "http://www.stanfordhomesidaho.com"
        item['AmenityType'] = ''
        yield item

        yield scrapy.Request(url='http://www.stanfordhomesidaho.com/Home%20plans/', callback=self.plans)




    def plans(self, response):

        divs = response.xpath('//div[@class="row"][1]//tr/td/div[@style="position:relative"]')


        for div in divs:
            link = div.xpath('.//*[contains(text(),"More")]/@href').extract_first()

            try:
                BaseSqft = div.xpath('.//p[2]/text()[2]').extract_first()
                BaseSqft = BaseSqft.split("/")[1].replace(",",'')
                BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
                print(BaseSqft)
            except Exception as e:
                print(e)
                BaseSqft = ''


            try:
                Bedrooms = div.xpath('.//p[2]/text()[1]').extract_first()
                Bedrooms = Bedrooms.split("/")[0]
                Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
                print(Bedrooms)
            except Exception as e:
                print(e)
                Bedrooms = ''


            try:
                Baths = div.xpath('.//p[2]/text()[1]').extract_first()
                Baths = Baths.split("/")[1]
                tmp = re.findall(r"(\d+)", Baths)


                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0

                print(Baths)

            except Exception as e:
                print(e)
                Baths,HalfBaths = '',''

            try:
                Garage = div.xpath(
                    './/p[2]/text()[2]').extract_first()
                Garage = Garage.split("/")[0]
                Garage = re.findall(r"(\d+)", Garage)[0]
                print(Garage)
            except Exception as e:
                print(e)
                Garage = ''

            item = BdxCrawlingItem_Plan()
            item['BaseSqft'] = BaseSqft
            item['Baths'] = Baths
            item['HalfBaths'] = HalfBaths
            item['Bedrooms'] = Bedrooms
            item['Garage'] = Garage

            # links = response.xpath('//*[contains(text(),"More")]/@href').extract()
            # for link in links:
            yield scrapy.Request(url='http://www.stanfordhomesidaho.com'+link, callback=self.plan_data,meta={'item':item})
            # yield scrapy.Request(url='http://www.stanfordhomesidaho.com/home_plans/payette/', callback=self.plan_data,meta={'item':item})


    def plan_data(self, response):
        item = response.meta['item']
        PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)

        SubdivisionNumber = self.builderNumber

        PlanName = response.xpath('//td[@class="ModuleTitleText"]//text()').extract_first(default='').strip()

        site_text = ''.join(response.xpath('//td[@class="modulecontent"]/div//span/text()').extract())
        site_text = re.sub('\s+', ' ', re.sub('\r|\n|\t', ' ', site_text))

        # try:
        #     BaseSqft = re.findall(r'(\d,?\d+?) sq.', site_text, re.IGNORECASE)[0]
        #     if ',' in BaseSqft:
        #         BaseSqft = BaseSqft.replace(',','')
        # except:
        #     BaseSqft = 0
        #
        # try:
        #     Baths = re.findall(r'(\d.?\d?) bath', site_text, re.IGNORECASE)[0]
        #     tmp = re.findall(r"(\d+)", Baths)
        #     Baths = tmp[0]
        #     if len(tmp) > 1:
        #         HalfBaths = 1
        #     else:
        #         HalfBaths = 0
        # except:
        #     Baths = 0
        #     HalfBaths = 0
        #
        # try:
        #     Bedrooms = re.findall(r'(\d) bed', site_text, re.IGNORECASE)[0]
        # except:
        #     Bedrooms = 0
        #
        # try:
        #     Garage = re.findall(r'(\d)\+? car', site_text, re.IGNORECASE)[0]
        # except:
        #     Garage = 0

        try:
            Description = site_text
        except:
            Description = ''

        try:
            images = []
            images1 = response.xpath('//div[@class="sidePane"]/ul/li/a/@href').extract()
            for img in images1:
                imgs = 'http://www.stanfordhomesidaho.com' + str(img)
                images.append(imgs)
            images2 = response.xpath('//*[@class="panes"]//img/@src').extract()
            for img in images2:
                imgs = 'http://www.stanfordhomesidaho.com' + str(img)
                images.append(imgs)
            # images3 = response.xpath('//div[@class="sidePane"]/ul/li/a/@href').extract_first()
            # for img in images3:
            #     imgs = 'http://www.stanfordhomesidaho.com' + str(img)
            #     images.append(imgs)
        except Exception as e:
            print(e)

        unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here


        # item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number  # < -------- Changes here
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = PlanName
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0.00
        # item['BaseSqft'] = BaseSqft
        # item['Baths'] = Baths
        # item['HalfBaths'] = HalfBaths
        # item['Bedrooms'] = Bedrooms
        # item['Garage'] = Garage
        item['Description'] = Description
        item['ElevationImage'] = '|'.join(images)
        item['PlanWebsite'] = response.url
        yield item

        # SubdivisionNumber = SubdivisionNumber
        # unique = str("Plan Unknown") + str(self.builderNumber)
        # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        # item = BdxCrawlingItem_Plan()
        # item['unique_number'] = unique_number
        # item['Type'] = "SingleFamily"
        # item['PlanNumber'] = "Plan Unknown"
        # item['SubdivisionNumber'] = SubdivisionNumber
        # item['PlanName'] = "Plan Unknown"
        # item['PlanNotAvailable'] = 1
        # item['PlanTypeName'] = "Single Family"
        # item['BasePrice'] = 0
        # item['BaseSqft'] = 0
        # item['Baths'] = 0
        # item['HalfBaths'] = 0
        # item['Bedrooms'] = 0
        # item['Garage'] = 0
        # item['Description'] = ""
        # item['ElevationImage'] = ""
        # item['PlanWebsite'] = ""
        # yield item
    #
    #     yield scrapy.Request(url='http://www.stanfordhomesidaho.com/available_homes/', callback=self.homes, meta={'PN':unique_number})
    #
    #
    # def homes(self, response):
    #     PlanNumber = response.meta['PN']
    #     link = response.xpath('//a[@class="forecolor10 fontstyle4"]/@href').extract_first()
    #     yield scrapy.Request(url='http://www.stanfordhomesidaho.com'+link, callback=self.home_details, meta={'PN':PlanNumber})
    #
    #
    # def home_details(self, response):
    #     add = response.xpath('//h1[@itemprop="address"]/address/span/text()').extract_first()
    #     try:
    #         street = add.split(',')[0].strip()
    #         city = add.split(',')[1].strip()
    #         add1 = add.split(',')[-1].split(' ')
    #         state = add1[1].strip()
    #         zipcode = add1[-1].strip()
    #     except Exception as e:
    #         print(str(e))
    #
    #     try:
    #         unique = street + city + state + zipcode
    #         SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
    #         f = open("html/%s.html" % SpecNumber, "wb")
    #         f.write(response.body)
    #         f.close()
    #     except Exception as e:
    #         print(e)
    #
    #     PlanNumber = response.meta['PN']
    #
    #     try:
    #         bedrooms = response.xpath('//div[@class="n-v1-cols nospacing"]//div[@class="two-columns two-columns-tablet two-columns-mobile-landscape four-columns-mobile-portrait darkgrey item block"][1]//span/text()').extract_first()
    #     except Exception as e:
    #         bedrooms = 0
    #
    #     try:
    #         baths = response.xpath('//div[@class="n-v1-cols nospacing"]//div[@class="two-columns two-columns-tablet two-columns-mobile-landscape four-columns-mobile-portrait darkgrey item block"][2]//span/text()').extract_first()
    #         tmp = re.findall(r"(\d+)", baths)
    #         baths = tmp[0]
    #         if len(tmp) > 1:
    #             halfbaths = 1
    #         else:
    #             halfbaths = 0
    #     except Exception as e:
    #         baths = 0
    #         halfbaths = 0
    #
    #     try:
    #         garage = response.xpath('//div[@class="n-v1-cols nospacing"]//div[@class="two-columns two-columns-tablet two-columns-mobile-landscape four-columns-mobile-portrait darkgrey item block"][3]//span/text()').extract_first()
    #     except Exception as e:
    #         print(str(e))
    #
    #     try:
    #         price = response.xpath('//div[@class="price"]/span/text()').extract_first().replace(',', '').replace('$','')
    #     except Exception as e:
    #         print(str(e))
    #
    #     try:
    #         sqft = response.xpath('//div[@class="n-v1-cols nospacing"]//div[@class="two-columns two-columns-tablet two-columns-mobile-landscape four-columns-mobile-portrait darkgrey item block"][5]//span/text()').extract_first()
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         description = response.xpath('//div[@class="twelve-columns twelve-columns-tablet twelve-columns-mobile-landscape lightgrey block"]/span/text()').extract_first()
    #     except Exception as e:
    #         print(str(e))
    #
    #     try:
    #         Images = []
    #         images = response.xpath('//div[@class="banner"]/ul/li/img/@src').extract()
    #         for image in images:
    #             imgs = 'http://www.stanfordhomesidaho.com' + str(image)
    #             Images.append(imgs)
    #
    #     except Exception as e:
    #         print(str(e))
    #
    #     try:
    #         item = BdxCrawlingItem_Spec()
    #         item['SpecNumber'] = SpecNumber
    #         item['PlanNumber'] = PlanNumber
    #         item['SpecStreet1'] = street
    #         item['SpecCity'] = city
    #         item['SpecState'] = state
    #         item['SpecZIP'] = zipcode
    #         item['SpecCountry'] = "USA"
    #         item['SpecPrice'] = price
    #         item['SpecSqft'] = sqft
    #         item['SpecBaths'] = baths
    #         item['SpecHalfBaths'] = halfbaths
    #         item['SpecBedrooms'] = bedrooms
    #         item['MasterBedLocation'] = "Down"
    #         item['SpecGarage'] = garage
    #         item['SpecDescription'] = description
    #         item['SpecElevationImage'] = '|'.join(Images)
    #         item['SpecWebsite'] = response.url
    #
    #         yield item
    #     except Exception as e:
    #         print(str(e))



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl stanfordhomesidaho'.split())