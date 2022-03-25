# -*- coding: utf-8 -*-
import copy
import re
import os
import json
import hashlib
from pprint import pprint

import requests
import scrapy
from lxml import html
from scrapy.http import HtmlResponse
from w3lib.html import remove_tags
from w3lib.http import basic_auth_header

from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class CovingtonHomescoSpider_bdx(scrapy.Spider):
    name = 'covingtonhomesco'
    allowed_domains = ['covingtonhomesco.com']
    start_urls = ['http://covingtonhomesco.com/index.html']

    builderNumber = '763403827167790767654963906668'


    def parse(self, response):
        # -------------------- fetch all the Communities ----- #
        try:
            link = response.xpath('//a[contains(text(),"Neighborhoods")]/following-sibling::ul/li/a/@href').getall()
            hdr = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Cookie":"_ga=GA1.2.1596343724.1586839501; _gid=GA1.2.899752743.1586839501; _gat_gtag_UA_150904305_1=1",
                    "If-Modified-Since":"Thu, 09 Apr 2020 20:28:46 GMT",
                    "Host":"www.covingtonhomesco.com",
                    "Sec-Fetch-Dest":"document",
                    "Sec-Fetch-Mode":"navigate",
                    "Sec-Fetch-Site":"same-origin",
                    "Sec-Fetch-User":"?1",
                    "Upgrade-Insecure-Requests":"1",
                    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36"}
            for li in link:
                li = 'http://covingtonhomesco.com/' + li
                print(li)
                yield scrapy.Request(url=li, callback=self.process_communities, meta={'BN': self.builderNumber}, headers=hdr)

            # yield scrapy.Request(url='https://www.covingtonhomesco.com/banninglewisranch-enclave.html', callback=self.process_communities, meta={'BN': self.builderNumber}, headers=hdr)
            # yield scrapy.Request(url='https://www.covingtonhomesco.com/banninglewisranch.html', callback=self.process_communities, meta={'BN': self.builderNumber}, headers=hdr)
            # yield scrapy.Request(url='https://www.covingtonhomesco.com/stonebridge-meridianranch.html', callback=self.process_communities, meta={'BN': self.builderNumber}, headers=hdr)
            # yield scrapy.Request(url='https://www.covingtonhomesco.com/stonebridge-meridianranch-enclave.html', callback=self.process_communities, meta={'BN': self.builderNumber}, headers=hdr)
            # yield scrapy.Request(url='https://www.covingtonhomesco.com/highline-wolfranch.html', callback=self.process_communities, meta={'BN': self.builderNumber}, headers=hdr)
            # yield scrapy.Request(url='https://www.covingtonhomesco.com/daybreak-wolfranch.html', callback=self.process_communities, meta={'BN': self.builderNumber}, headers=hdr)
            # yield scrapy.Request(url='https://www.covingtonhomesco.com/gardensatnorthcarefree.html', callback=self.process_communities, meta={'BN': self.builderNumber}, headers=hdr)

        except Exception as e:
            print(e)

    def process_communities(self, response):

        # ---------------------------Extracting Communities Details ------------------------------------ #
        url = response.url
        try:
            SubDescription = ''.join(response.xpath('//*[@class="post-classic-body"]/p/text()').getall())
            if not SubDescription:
                SubDescription = ''
        except Exception as e:
            print(e)

        try:
            if 'Coming Soon!' in SubDescription:
                sub_Status = 'ComingSoon'
            else:
                sub_Status = 'Active'

        except Exception as e:
            print(e)

        try:
            BuilderNumber = response.meta['BN']
        except Exception as e:
            print(e)

        try:
            SubdivisionName = response.xpath('//*[@class="heading-decorated"]/text()').extract_first('')
            if SubdivisionName == '':
                SubdivisionName = response.xpath('//h2/text()').extract_first()
            SubdivisionName = SubdivisionName.strip()
        except Exception as e:
            print(e)
            SubdivisionName = ''


        try:
            SubdivisionNumber = int(hashlib.md5(bytes(SubdivisionName+url, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            SubdivisionNumber = ''
            print(e)

        try:
            BuildOnYourLot = 1 if "build-on-your-lot" in str(response.url) else 0
        except Exception as e:
            print(e)

        try:
            OutOfCommunity = 1
        except Exception as e:
            print(e)

        try:
            addr = response.xpath('//h5//text()').get()
            City = addr.split(',')[1].strip()
            Street1 = addr.split(',')[0].strip()
            statezip = addr.split(',')[2].strip()
            if statezip == 'Colorado':
                State = 'CO'
                ZIP = addr.split(',')[3].strip()
            else:
                State = statezip.split()[0].replace('.','').strip()
                ZIP = statezip.split()[1]

        except Exception as e:
            print(e)

        try:
            Email = 'info@covingtonhomesco.com'
        except Exception as e:
            print(e)



        try:
            SubImage = response.xpath('//*[@class="post-classic"]/img/@src').get()
            SubImage = 'http://covingtonhomesco.com' + SubImage
        except Exception as e:
            SubImage = ""

        try:
            SubWebsite = response.url
        except Exception as e:
            print(e)

        a = []
        # aminity = ''.join(response.xpath('//*[@class="ll-features-content__half right col-md-1of2"]/ul[1]/li/text()').extract())
        try:
            aminity = ''.join(response.xpath('//*[@class="post-classic-body"]/p/text()').getall())
            aminity = aminity.title()
        except Exception as e:
            print(e)

        amenity_list = ["Pool", "Playground", "GolfCourse", "Tennis", "Soccer", "Volleyball", "Basketball",
                        "Baseball", "Views", "Lake", "Pond", "Marina", "Beach", "WaterfrontLots", "Park",
                        "Trails", "Greenbelt", "Clubhouse", "CommunityCenter"]
        for i in amenity_list:
            # print(i)
            if i in aminity:
                # print(i)
                a.append(i)
        ab = '|'.join(a)

        # ----------------------- Don't change anything here --------------
        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = sub_Status
        item2['SubdivisionNumber'] = SubdivisionNumber
        item2['BuilderNumber'] = BuilderNumber
        item2['SubdivisionName'] = SubdivisionName
        item2['BuildOnYourLot'] = BuildOnYourLot
        item2['OutOfCommunity'] = OutOfCommunity
        item2['Street1'] = Street1
        item2['City'] = City
        item2['State'] = State
        item2['ZIP'] = ZIP
        item2['AreaCode'] = "719"
        item2['Prefix'] = "205"
        item2['Suffix'] = "6110"
        item2['Extension'] = ''
        item2['Email'] = Email
        item2['SubDescription'] = SubDescription
        item2['SubImage'] = SubImage
        item2['SubWebsite'] = SubWebsite
        item2['AmenityType'] = ab
        yield item2

        # item = BdxCrawlingItem_subdivision()
        # item['sub_Status'] = "Active"
        # item['SubdivisionNumber'] = self.builderNumber
        # item['BuilderNumber'] = self.builderNumber
        # item['SubdivisionName'] = "No Sub Division"
        # item['BuildOnYourLot'] = 0
        # item['OutOfCommunity'] = 0
        # item['Street1'] = '13725 Struthers Road, Suite 201'
        # item['City'] = 'Colorado Springs'
        # item['State'] = 'CO'
        # item['ZIP'] = '80921'
        # item['AreaCode'] = '719'
        # item['Prefix'] = "205"
        # item['Suffix'] = "5248"
        # item['Extension'] = ""
        # item['Email'] = "info@covingtonhomesco.com"
        # item['SubDescription'] = 'Covington Homes has been bestowed with the honor of the Builder of the Year Award by the St Jude Children’s Research Hospital. Covington Homes has made a long-term commitment to partner with the St Jude Children’s Research Hospital as the St Jude Dream Home Builder in Southern Colorado. For the past two years, Covington Homes has built the Colorado Spring St Jude Dream Home at zero cost! This means that all of the proceeds from the ticket sales of the Dream Home go directly to St Jude Children’s Research Hospital. In fact, Covington Homes and our trade partners have done an amazing job in supporting St Jude’s lifesaving mission and have helped to raise over $2.7 million dollars in the past three years to fight childhood cancer and other life-threatening diseases. Service and compassion for others have always been the cornerstone of Covington Homes’ culture. Covington Homes is the Builder that Gives back. The entire Covington Homes Team is truly a group of people who care about the community and care deeply about giving to others.Covington Homes is celebrating a fantastic milestone this year- its 10th year anniversary. Since its founding in 2008, Covington Homes continues to be among the top builders in Colorado Springs and El Paso County.'
        # item['SubImage'] = 'http://covingtonhomesco.com/images/bg-image-1.jpg|http://covingtonhomesco.com/images/home-photo1.jpg|http://covingtonhomesco.com/images/home-photo2.jpg|http://covingtonhomesco.com/images/home-photo3.jpg|http://covingtonhomesco.com/images/home-photo4.jpg|http://covingtonhomesco.com/images/home-photo5.jpg|http://covingtonhomesco.com/images/home-photo6.jpg|http://covingtonhomesco.com/images/home-photo7.jpg|http://covingtonhomesco.com/images/home-photo8.jpg'
        # item['SubWebsite'] = 'covingtonhomesco.com'
        # item['AmenityType'] = ''
        # yield item
        # # process plans:
        # # ----------------
        # link = 'http://covingtonhomesco.com/collections.html'
        # hdr = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        #             "Cookie":"_ga=GA1.2.1596343724.1586839501; _gid=GA1.2.899752743.1586839501; _gat_gtag_UA_150904305_1=1",
        #             "Host":"www.covingtonhomesco.com",
        #             "Sec-Fetch-Dest":"document",
        #             "Sec-Fetch-Mode":"navigate",
        #             "Sec-Fetch-Site":"same-origin",
        #             "Sec-Fetch-User":"?1",
        #             "Upgrade-Insecure-Requests":"1",
        #             "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36"}
        # r = requests.get(url=link, headers=hdr)
        # res = HtmlResponse(url=r.url, body=r.content)
        #
        # plan_url = res.xpath('//h6[@class="padbot"]/following-sibling::ul/li/a/@href').getall()
        # for pu in plan_url:
        #     pu = 'http://covingtonhomesco.com/' + pu
        #     yield scrapy.Request(url=pu, callback=self.plans_details, meta={'sbdn': item['SubdivisionNumber']})

        #--------------- code modified ------------------------------------------------------------#

        plan_url = response.xpath('//ul[@class="list-xxs small"]/li/a/@href').getall()
        for pu in plan_url:
            pu = 'http://covingtonhomesco.com/' + pu
            yield scrapy.Request(url=pu, callback=self.plans_details, meta={'sbdn': SubdivisionNumber,'SubdivisionName':SubdivisionName})

    def plans_details(self, response):
        SubdivisionName = response.meta['SubdivisionName']
        url = response.url

        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//*[@class="row justify-content-center"]/h3/text()').get()
        except Exception as e:
            PlanName = ''
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName+SubdivisionName+response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            PlanNumber = ''
            print(e)

        try:
            SubdivisionNumber = response.meta['sbdn']
            print(SubdivisionNumber)
        except Exception as e:
            SubdivisionNumber = ''
            print(e)

        try:
            PlanNotAvailable = 0
        except Exception as e:
            print(e)

        try:
            PlanTypeName = 'Single Family'
        except Exception as e:
            print(e)

        try:
            BasePrice = 0
        except Exception as e:
            print(e)

        try:
            sqft = response.xpath('//td[contains(text(),"Total Square Feet:")]/following-sibling::td/text()').get()
            if '-' in sqft:
                sqft = sqft.split("-")[1]
            sqft = sqft.replace(',','').strip()
            BaseSqft = re.findall(r"(\d+)", sqft)[0]

        except Exception as e:
            print(e)

        try:
            bath = response.xpath('//td[contains(text(),"Bathrooms:")]/following-sibling::td/text()').get()
            if '-' in bath:
                bath = bath.split("-")[1]
            tmp = re.findall(r"(\d+)", bath)
            # tmp = re.findall(r"^(\d+) -", bath)[0]
            # if not tmp:
            #     tmp = re.findall(r"^(\d\.\d) -", bath)[0]
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            print(e)
            bath,HalfBaths = '',''

        try:
            Bedrooms = response.xpath('//td[contains(text(),"Bedrooms:")]/following-sibling::td/text()').get()
            if '-' in Bedrooms:
                Bedrooms = Bedrooms.split("-")[1]
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)

        try:
            Garage = response.xpath('//td[contains(text(),"Garage Spaces:")]/following-sibling::td/text()').get()
            if '-' in Garage:
                Garage = Garage.split("-")[1]
            Garage = re.findall(r"(\d+)", Garage)[0]
            if not Garage:
                Garage = 0
        except Exception as e:
            Garage = 0
            print(e)

        try:
            Description = ''.join(response.xpath('//h4[contains(text(),"Plan Description")]/following-sibling::p/text()').getall())
            if Description == '':
                Description = 'At Covington Homes we are focused on investing in our community, building quality homes at a practical price, and maintaining the highest level of customer service. Our homes are well thought out, fully planned, and exceptionally executed.'
        except Exception as e:
            print(e)

        try:
            images = []
            imagedata = response.xpath('//*[@class="row row-50"]/div/article/a/@href').getall()
            for id in imagedata:
                id = 'http://covingtonhomesco.com/' + id
                images.append(id)
            ElevationImage = "|".join(images)
        except Exception as e:
            print(e)

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

        # ----------------------- Don't change anything here --------------
        unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
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
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = Description
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl covingtonhomesco'.split())
