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
    name = 'fairwayhomes'
    allowed_domains = []
    start_urls = ['https://www.fairwayhomeswest.com/']

    builderNumber = 24556

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
        item['Street1'] = '21725 North 20th Avenue Unit 104'
        item['City'] = 'Phoenix'
        item['State'] = 'AZ'
        item['ZIP'] = '85027'
        item['AreaCode'] = ''
        item['Prefix'] =''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] =''
        item['SubDescription'] ='We pride ourselves on offering over 60 fully customizable house floor plans ranging from 480sf to 3720sf and are affordably priced from $80,900 to $321,900 “Built on Your Land”. Our passion and focus is on creating new homes that deliver a lifetime of enjoyment and long-term value, with a spot-light on energy-efficiency. You’re one step closer to finding the perfect home for you and your family. Enjoy our site, thanks for stopping by!'
        item['SubImage']= 'https://www.fairwayhomeswest.com/wp-content/uploads/2019/06/custom-home-builder-washington-oregon-idaho.jpg|https://www.fairwayhomeswest.com/wp-content/uploads/2020/06/mom-dad-baby-desert-walk-faded-opt.jpg'
        item['SubWebsite'] = response.url
        yield item

        for i in range(1,7):
            planlink = 'https://www.fairwayhomeswest.com/floor-plans/?fwp_paged='+str(i)
            yield scrapy.FormRequest(url=planlink,callback=self.planLink,dont_filter=True)

    def planLink(self,response):
        planlinks = response.xpath('//div[@class="floor-plan"]/a/@href').extract()
        print(len(planlinks))
        for planlinks in planlinks:
            print(planlinks)
            yield scrapy.FormRequest(url=planlinks,callback=self.finalplan,dont_filter=True)

    def finalplan(self,response):
        try:
            Type = 'SingleFamily'
        except Exception as e:
            Type = 'SingleFamily'
            print(e)

        try:
            PlanName = response.xpath('//div[@class="hero-text"]/h1/text()').get()
            PlanName = re.sub('<[^<]+?>', '', str(PlanName))
            # print(PlanName)
        except Exception as e:
            PlanName = ''
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % PlanNumber, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = self.builderNumber
        except Exception as e:
            print(e)

        try:
            PlanNotAvailable = 0
        except Exception as e:
            print(e)

        try:
            BasePrice = response.xpath('//*[contains(text(),"Price")]/../ul/li/strong/text()[2]').extract_first().replace('$','').replace(",","").replace("*","")
        except Exception as e:
            print(e)
            BasePrice=0

        try:
            PlanTypeName = 'Single Family'
        except Exception as e:
            print(e)

        try:
            plansquare = response.xpath('//*[contains(text(),"sq. ft.")]/text()').get().strip()
            plansquare = re.sub('<[^<]+?>', '', str(plansquare))
            BaseSqft = plansquare.split('sq. ft.')[0]
            BaseSqft = re.findall(r"(\d+)",BaseSqft)[0].strip()
            # print(BaseSqft)
        except Exception as e:
            BaseSqft = 0
            print("BaseSqft: ", e)
        try:
            planbeds = response.xpath('//*[contains(text(),"Beds")]/text()').get()
            planbeds = re.sub('<[^<]+?>', '', str(planbeds))
            planbeds = re.findall(r"(\d+)",planbeds)[0].strip()
            # print(planbeds)
        except Exception as e:
            planbeds = 0
            print("planbeds: ", e)
        try:
            planbath = response.xpath('//*[contains(text(),"Baths")]/text()').get()
            planbath = re.sub('<[^<]+?>', '', str(planbath))
            tmp = re.findall(r"(\d+)", planbath)
            planbath = tmp[0]
            # print(planbath)
            if len(tmp) > 1:
                planHalfBaths = 1
                # print(planHalfBaths)
            else:
                planHalfBaths = 0
                # print(planHalfBaths)
            # print(planbath)
        except Exception as e:
            planbath = 0
            planHalfBaths = 0
            print("planbath: ", e)
        try:
            cargarage = response.xpath('//*[contains(text(),"Car Garage")]/text()').get()
            cargarage = re.sub('<[^<]+?>', '', str(cargarage))
            cargarage = re.findall(r"(\d+)",cargarage)[0]
            # print(cargarage)
        except Exception as e:
            cargarage = 0
            print("cargarage: ", e)
        # try:
        #     Description = "".join(re.findall(r"<p>(.*?)</p>",response.text)).strip().replace('&nbsp;','')
        #     # if Description == '':
        #     #     Description = re.findall(r"<br />(.*?)</p>",re.DOTALL)
        #     if Description == '':
        #         Description = ''.join(response.xpath('//div[@class="tabcontent"]/div/p/text()[6]').extract()).strip().replace('&nbsp;','')
        #     print(Description)
        # except Exception as e:
        #     Description = ' '
        #     print('Description:',e)
        try:
            PlanImage = "|".join(response.xpath('//*[@class="floor-plans-single-wrap"]//*[contains(@src,"i")]/@src').extract())
            # print(PlanImage)
        except Exception as e:
            PlanImage = ''
            print("SpecElevationImage: ", e)
        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)
        try:
            unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
                    10 ** 30)  # < -------- Changes here
            item = BdxCrawlingItem_Plan()
            item['Type'] = Type
            item['PlanNumber'] = PlanNumber
            item['unique_number'] = unique_number  # < -------- Changes here
            item['SubdivisionNumber'] = SubdivisionNumber
            item['PlanName'] = PlanName
            item['PlanNotAvailable'] = PlanNotAvailable
            item['PlanTypeName'] = PlanTypeName
            item['BasePrice'] = BasePrice
            item['BaseSqft'] = BaseSqft
            item['Baths'] = planbath
            # print(item['Baths'])
            item['HalfBaths'] = planHalfBaths
            # print(item['HalfBaths'])
            item['Bedrooms'] = planbeds
            item['Garage'] = cargarage
            item['Description'] = "Fairway Homes West has been delivering beautiful custom homes to satisfied customers for over a decade. The family partnership began in 2002 when brothers, Lowell and Jamie Hankel, along with Tom Fancher (Jamie’s father in-law) founded our parent company Reality Homes Inc. with a vision to build high quality homes with lasting value and energy efficiency in the Pacific Northwest."
            item['ElevationImage'] = PlanImage
            item['PlanWebsite'] = PlanWebsite
            print(item)
            yield item
        except Exception as e:
            print(e)

if __name__ == '__main__':
    execute("scrapy crawl fairwayhomes".split())