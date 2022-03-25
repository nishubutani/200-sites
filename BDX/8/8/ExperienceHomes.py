# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header

class DannysullivanconstructionComSpider(scrapy.Spider):
    name = 'ExperienceHomes'
    allowed_domains = []
    start_urls = ['https://amarillobuilder.com/']
    builderNumber = 52481

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
        item['Street1'] = 'P.O. Box 7344'
        item['City'] = 'Amarillo'
        item['State'] = 'TX'
        item['ZIP'] = '79114'
        item['AreaCode'] = '806'
        item['Prefix'] ='318'
        item['Suffix'] = '8686'
        item['Extension'] = ""
        item['Email'] ='bid@amarillobuilder.com'
        item['SubDescription'] ='Whether you are looking to buy your first home or are ready to design the custom home of your dreams, Experience Homes are the Amarillo home builders for you. Our new construction homes offer energy efficiency, quality craftsmanship, and most importantly – a home that is uniquely yours!'
        item['SubImage']= 'https://amarillobuilder.com/wp-content/uploads/2019/06/collagepic1-768x702.jpg|https://amarillobuilder.com/wp-content/uploads/2019/06/stove-e1591715549258.jpg|https://amarillobuilder.com/wp-content/uploads/2019/06/75258574_2701799283211656_2185144167519223808_o.jpg|https://amarillobuilder.com/wp-content/uploads/2020/02/4corners.jpg'
        item['SubWebsite'] = response.url
        yield item

        links = 'https://amarillobuilder.com/listings/?tab=pre-owned-homes'
        yield scrapy.FormRequest(url=links,callback=self.hlinks,dont_filter=True)

    def hlinks(self,resonse):
        unique = str("Plan Unknown") + str(self.builderNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
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
        # home_links = resonse.xpath('//a[@class="entire-meta-link"]/@href').extract()
        home_links =['https://amarillobuilder.com/4806-se-28th/']
        for home_link in home_links:
            # home_link ='https://amarillobuilder.com/13710-lobelia-place/'
            print(home_link)
            yield scrapy.FormRequest(url=home_link,callback=self.homeDetail,dont_filter=True,meta={'unique_number':unique_number})

    def homeDetail(self,response):

        print(response.url)
        try:
            SpecStreet1 = response.xpath('//*[@class="wpb_text_column wpb_content_element "]/div/h2/text()').extract_first()
            # SpecStreet1=SpecStreet1.replace(",","")
            s = response.xpath('//*[@class="wpb_text_column wpb_content_element "]/div/p/text()').get()
            print(s)
            SpecCity = s.split(',')[0]
            SpecState = s.split(',')[-1].split(' ')[1]
            SpecZIP = re.findall(r"(\d+)", s)[0]
            SpecZIP = SpecZIP
            unique = str(SpecStreet1) + str(SpecCity) + str(SpecState) + str(SpecZIP)
            SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % SpecNumber, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
            print(e)

        try:
            PlanNumber = response.meta['unique_number']
        except Exception as e:
            print(e)

        try:
            SpecCountry = "USA"
        except Exception as e:
            print(e)

        try:
            SpecPrice = str(response.xpath('normalize-space(//*[contains(text(),"$")]/text())').extract_first(default='0').strip()).replace(",", "")
            SpecPrice = re.findall(r"(\d+)", SpecPrice)[0]
        except Exception as e:
            SpecPrice = 0
            print(e)

        try:
            SpecSqft = str(response.xpath('normalize-space(//*[contains(text(),"Square Feet:")]/../..//div/text())').extract_first(
                default='0').strip()).replace(",", "")
            SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
        except Exception as e:
            SpecSqft = 0

        try:
            SpecBaths = str(response.xpath(
                'normalize-space(//*[contains(text(),"Bathrooms:")]/../..//div/text())').extract_first(
                default='0').strip()).replace(",", "")
            tmp = re.findall(r"(\d+)", SpecBaths)
            SpecBaths = tmp[0]
            if len(tmp) > 1:
                SpecHalfBaths = 1
            else:
                SpecHalfBaths = 0
        except Exception as e:
            SpecBaths = 0
            SpecHalfBaths = 0

        try:
            SpecBedrooms = str(response.xpath(
                'normalize-space(//*[contains(text(),"Bedrooms:")]/../..//div/text())').extract_first(
                default='0').strip()).replace(",", "")
            SpecBedrooms = re.findall(r"(\d+)", SpecBedrooms)[0]
        except Exception as e:
            SpecBedrooms = 0

        try:
            MasterBedLocation = "Down"
        except Exception as e:
            print(e)

        try:
            SpecGarage = response.xpath('//*[contains(text(),"Garage Space:")]/../..//div/text()').get()
            SpecGarage = re.findall(r"(\d+)", SpecGarage)[0]
        except Exception as e:
            SpecGarage = 0

        # try:
        #     SpecDescription = response.xpath('//*[@id="ldp-detail-romance"]//text()').extract()
        #     SpecDescription = str(''.join(SpecDescription)).strip()
        #     SpecDescription = SpecDescription.replace("\n", "").replace("  ", "")
        # except Exception as e:
        #     SpecDescription = ''
        #     print(e)

        try:
            ElevationImage = response.xpath('//img[@class="skip-lazy "]/@src').extract()
            ElevationImage = "|".join(ElevationImage)
            SpecElevationImage = ElevationImage
        except Exception as e:
            print(e)
        try:
            SpecWebsite = response.url
        except Exception as e:
            print(e)

        # ----------------------- Don't change anything here ---------------- #
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
        item['SpecDescription'] = 'Home isn’t just where you lay your head, it’s where life is lived and memories are made. Dreams are fulfilled, big milestones are reached, and community is knitted together. Home is where the heart is. As a locally owned and operated family business, Experience Homes isn’t just another run-of-the-mill building company – your home is where our heart is. We are the creators of custom dream homes, designed to house all of your family’s wants and needs, down to the very last details'
        item['SpecElevationImage'] = SpecElevationImage
        item['SpecWebsite'] = SpecWebsite
        yield item

if __name__ == '__main__':
    execute("scrapy crawl ExperienceHomes".split())