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
    name = 'infinityhomes'
    allowed_domains = []
    start_urls = ['https://infinitybuilthomes.com/communities/']
    builderNumber = 33906

    def parse(self, response):
        community_links = response.xpath('//*[@class="tileWrap neighborhood"]/div/a/@href').extract()
        for community_link in community_links:
            print(community_link)
            yield scrapy.FormRequest(url=community_link, callback=self.communityDetail, dont_filter=True)

    def communityDetail(self, response):
        subdivisonName = response.xpath('//div[@class="elementor-widget-container"]/h1/text()').extract_first(default="")
        subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)

        f = open("html/%s.html" % subdivisonNumber, "wb")
        f.write(response.body)
        f.close()

        contactTmp = response.xpath('//*[contains(text(),"Model Address:")]/../text()').extract_first()
        print(contactTmp)
        phoneNumber = response.xpath('//*[@class="content-column three_fourth"]/strong[2]/a/text()').extract_first()
        print(phoneNumber)
        street1 = contactTmp.split(',')[0].strip()
        city = contactTmp.split(',')[-2]
        zipcode = contactTmp.split(',')[-1].split(' ')[-1]
        state = contactTmp.split(',')[-1].split(' ')[-2]
        Email = response.xpath('//*[@class="content-column three_fourth"]/strong[1]/a/text()').extract_first()
        Subdscr = "".join(response.xpath('//div[@class="content-column one_half image"]/div/p/text()').extract())
        Subimg = "|".join(response.xpath('//div[@class="gallery gallery-size-thumbnail"]/figure/a/@href').extract())
        AreaCode = phoneNumber.split("-")[0]
        Suffix = phoneNumber.split("-")[-1]
        Prefix = phoneNumber.split("-")[-2]
        print(AreaCode,Prefix)

        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionName'] = subdivisonName
        item2['SubdivisionNumber'] = subdivisonNumber
        item2['BuilderNumber'] = self.builderNumber
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 1
        item2['Street1'] = street1
        item2['City'] = city
        item2['State'] = state
        item2['ZIP'] = zipcode
        item2['AreaCode'] = AreaCode
        item2['Prefix'] = Prefix
        item2['Suffix'] = Suffix
        item2['Extension'] = ""
        item2['Email'] = Email
        item2['SubDescription'] = Subdscr
        item2['SubImage'] = Subimg
        item2['SubWebsite'] = response.url
        yield item2

        plan_link = 'https://infinitybuilthomes.com/home-plans/'
        yield scrapy.FormRequest(url=plan_link,callback=self.planurls,dont_filter=True,meta={'sbdn':subdivisonNumber})

    def planurls(self,response):
        SubdivisionNumber = response.meta['sbdn']
        links = response.xpath('//*[@class="inner"]/a/@href').extract()
        print(len(links))
        for link in links:
            print(link)
            yield scrapy.FormRequest(url=link,callback=self.planDetail,dont_filter=True,meta={'sbdn':SubdivisionNumber})

    def planDetail(self,response):
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
        item['Street1'] = ' 1736 E Main St'
        item['City'] = 'New Albany'
        item['State'] = 'IN'
        item['ZIP'] = '47150'
        item['AreaCode'] = ''
        item['Prefix'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] = 'info@infinitybuilthomes.com'
        item[
            'SubDescription'] = 'With over a decade of home building experience, Infinity Homes builds new homes in Southern Indiana and the greater Louisville, Kentucky area.  Known throughout the area as “The Neighborhood Builder,” Infinity Homes builds award-winning homes for award-winning lifestyles.  Offering a wide variety of home styles, price ranges, and communities, Infinity Homes is pleased to have been selected as the 2018,  2019, and 2020 home builder for the Louisville St. Jude Dream Home Giveaway. '
        item[
            'SubImage'] = 'http://dannysullivanconstruction.com/wp-content/uploads/2018/01/custom-homes-1.jpg|http://dannysullivanconstruction.com/wp-content/uploads/2018/01/kitchen2.jpg'
        item['SubWebsite'] = response.url
        yield item

        try:
            Type = 'SingleFamily'
        except Exception as e:
            Type = 'SingleFamily'
            print(e)
        try:
            PlanName = response.xpath('//*[@class="elementor-widget-container"]/h1/text()').extract_first()
            print(PlanName)
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
            BasePrice = 0.00
        except Exception as e:
            print(e)
        try:
            plansquare = response.xpath('//div[@class="stats"]/div[4]/span/text()').get()
            plansquare = re.sub('<[^<]+?>', '', str(plansquare))
            if '-' in plansquare:
                plansquare = plansquare.split('-')[-1]
            BaseSqft = plansquare
            print(BaseSqft)
        except Exception as e:
            print("BaseSqft: ", e)
        try:
            planbeds = response.xpath('//div[@class="stats"]/div[1]/span/text()').get()
            planbeds = re.sub('<[^<]+?>', '', str(planbeds))
            if '-' in planbeds:
                planbeds = planbeds.split('-')[-1]
            print(planbeds)
        except Exception as e:
            print("planbeds: ", e)
        try:
            planbath = response.xpath('//div[@class="stats"]/div[2]/span/text()').get()
            planbath = re.sub('<[^<]+?>', '', str(planbath))
            if '-' in planbath:
                planbath = planbath.split('-')[-1]
            tmp = re.findall(r"(\d+)", planbath)
            planbath = tmp[0]
            print(planbath)
            if len(tmp) > 1:
                planHalfBaths = 1
                print(planHalfBaths)
            else:
                planHalfBaths = 0
                print(planHalfBaths)
        except Exception as e:
            print("planbath: ", e)
        try:
            cargarage = response.xpath('//div[@class="stats"]/div[3]/span/text()').get()
            cargarage = re.sub('<[^<]+?>', '', str(cargarage))
            if '-' in cargarage:
                cargarage = cargarage.split('-')[-1]
            print(cargarage)
        except Exception as e:
            print("cargarage: ", e)
        try:
            Description = " ".join(response.xpath('//div[@class="content-column one_half"]/p/text()').extract())
            print(Description)
        except Exception as e:
            Description = ' '
            print('Description:',e)
        try:
            PlanImage = []
            PlanImages = response.xpath('//div[@class="imgWrap"]/img/@src').extract()
            for PlanImag in PlanImages:
                PlanImage.append(PlanImag)
            PlanImage = '|'.join(PlanImage)
            print(PlanImage)
        except Exception as e:
            print("SpecElevationImage: ", e)
        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)
        try:
            unique = str(PlanName) + str(self.builderNumber)  # < -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
                    10 ** 30)  # < -------- Changes here
            item = BdxCrawlingItem_Plan()
            item['Type'] = Type
            item['PlanNumber'] = PlanNumber
            item['unique_number'] = unique_number  # < -------- Changes here
            item['SubdivisionNumber'] = self.builderNumber
            item['PlanName'] = PlanName
            item['PlanNotAvailable'] = PlanNotAvailable
            item['PlanTypeName'] = 'Single Family'
            item['BasePrice'] = BasePrice
            item['BaseSqft'] = BaseSqft
            item['Baths'] = planbath
            print(item['Baths'])
            item['HalfBaths'] = planHalfBaths
            print(item['HalfBaths'])
            item['Bedrooms'] = planbeds
            item['Garage'] = cargarage
            item['Description'] = Description
            item['ElevationImage'] = PlanImage
            item['PlanWebsite'] = PlanWebsite
            yield item
        except Exception as e:
            print(e)

        homelinks = 'https://infinitybuilthomes.com/available-homes/'
        yield scrapy.FormRequest(url=homelinks,callback=self.homelink,dont_filter=True)

    def homelink(self,response):
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
        links = response.xpath('//*[@class="tileWrap homes"]/div/a/@href').extract()
        for link in links:
            print(link)
            yield scrapy.FormRequest(url=link,callback=self.homeDetail,meta={'plannumber':unique_number},dont_filter=True)


    # def homeDetail(self,response):
    #
    #     # solds = response.xpath('//div[@class="topNav"]/div/text()').extract_first()
    #     # if 'SOLD' not in solds:
    #         try:
    #             SpecStreet1 = response.xpath('//div[@class="elementor-widget-container"]/h1/text()').extract_first()
    #             # SpecStreet1=SpecStreet1.replace(",","")
    #             SpecCity ='New Albany'
    #             SpecState = 'IN'
    #             SpecZIP = '47150'
    #             unique = str(SpecStreet1) + str(SpecCity) + str(SpecState) + str(SpecZIP)
    #             SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
    #             f = open("html/%s.html" % SpecNumber, "wb")
    #             f.write(response.body)
    #             f.close()
    #         except Exception as e:
    #             print(e)
    #
    #
    #         try:
    #             SpecCountry = "USA"
    #         except Exception as e:
    #             print(e)
    #
    #         try:
    #             SpecPrice = str(response.xpath('normalize-space(//*[contains(text(),"$")]/text())').extract_first(default='0').strip()).replace(",", "")
    #             SpecPrice = re.findall(r"(\d+)", SpecPrice)[0]
    #         except Exception as e:
    #             SpecPrice = 0
    #             print(e)
    #
    #         try:
    #             SpecSqft = str(response.xpath('normalize-space(//div[@class="stats"]/div[4]/span/text())').extract_first(default='0').strip()).replace(",", "")
    #             SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
    #         except Exception as e:
    #             SpecSqft = 0
    #
    #         try:
    #             SpecBaths = str(response.xpath(
    #                 'normalize-space(//div[@class="stats"]/div[2]/span/text())').extract_first(
    #                 default='0').strip()).replace(",", "")
    #             tmp = re.findall(r"(\d+)", SpecBaths)
    #             SpecBaths = tmp[0]
    #             if len(tmp) > 1:
    #                 SpecHalfBaths = 1
    #             else:
    #                 SpecHalfBaths = 0
    #         except Exception as e:
    #             SpecBaths = 0
    #             SpecHalfBaths = 0
    #
    #         try:
    #             SpecBedrooms = str(response.xpath(
    #                 'normalize-space(//div[@class="stats"]/div[1]/span/text())').extract_first(
    #                 default='0').strip()).replace(",", "")
    #             SpecBedrooms = re.findall(r"(\d+)", SpecBedrooms)[0]
    #         except Exception as e:
    #             SpecBedrooms = 0
    #
    #         try:
    #             MasterBedLocation = "Down"
    #         except Exception as e:
    #             print(e)
    #
    #         try:
    #             SpecGarage = response.xpath('//div[@class="stats"]/div[3]/span/text()').get()
    #             SpecGarage = re.findall(r"(\d+)", SpecGarage)[0]
    #         except Exception as e:
    #             SpecGarage = 0
    #
    #         try:
    #             SpecDescription = response.xpath('//div[@class="content-column one_half last_column"]/p/text()').extract()
    #             SpecDescription = str(''.join(SpecDescription)).strip()
    #             SpecDescription = SpecDescription.replace("\n", "").replace("  ", "")
    #         except Exception as e:
    #             print(e)
    #
    #         try:
    #             ElevationImage = response.xpath('//div[@class="gallery"]/div/div/a/@href').extract()
    #             ElevationImage = "|".join(ElevationImage)
    #             SpecElevationImage = ElevationImage
    #         except Exception as e:
    #             print(e)
    #
    #         try:
    #             SpecWebsite = response.url
    #         except Exception as e:
    #             print(e)
    #
    #         # ----------------------- Don't change anything here ---------------- #
    #         item = BdxCrawlingItem_Spec()
    #         item['SpecNumber'] = SpecNumber
    #         item['PlanNumber'] = response.meta['plannumber']
    #         item['SpecStreet1'] = SpecStreet1
    #         item['SpecCity'] = SpecCity
    #         item['SpecState'] = SpecState
    #         item['SpecZIP'] = SpecZIP
    #         item['SpecCountry'] = SpecCountry
    #         item['SpecPrice'] = SpecPrice
    #         item['SpecSqft'] = SpecSqft
    #         item['SpecBaths'] = SpecBaths
    #         item['SpecHalfBaths'] = SpecHalfBaths
    #         item['SpecBedrooms'] = SpecBedrooms
    #         item['MasterBedLocation'] = MasterBedLocation
    #         item['SpecGarage'] = SpecGarage
    #         item['SpecDescription'] = SpecDescription
    #         item['SpecElevationImage'] = SpecElevationImage
    #         item['SpecWebsite'] = SpecWebsite
    #         yield item

if __name__ == '__main__':
    execute("scrapy crawl infinityhomes".split())