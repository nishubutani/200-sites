# -*- coding: utf-8 -*-
import json
import re
import os
import hashlib
import scrapy
from lxml import html
import requests
from scrapy.http import HtmlResponse
from scrapy.http import HtmlResponse
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision


class AshlarHomesSpider(scrapy.Spider):
    name = 'Ashlar_Homes'
    allowed_domains = ['']
    start_urls = ['https://www.ashlarhomeskc.com/communities']

    builderNumber = '529981498866376310866205893842'

    def parse(self, response):
        links = response.xpath('//*[@class="community-results-wrapper"]//li//a/@href').extract()
        for url in links:
            link = 'https://www.ashlarhomeskc.com'+url
            yield scrapy.FormRequest(url=link,dont_filter=True,callback=self.communities)

    def communities(self,response):
        # ------------------- Creating Communities ---------------------- #
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        try:
            sname = ''.join(response.xpath('//*[@class="col-lg-5 detail-header-content"]/h1/text()').extract())
            subdivisonNumber = int(hashlib.md5(bytes(sname, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            sname = ''
            subdivisonNumber = ''
            print("subdivisonNumber","sname",e)

        try:
            a = ''.join(response.xpath('//*[@class="col-lg-5 detail-header-content"]/h3[1]/text()').extract())
            z = a.split(' ')[0]+'1'
            zip = z[0:5]
            add = ' '.join(a.split(' ')[1:])

        except Exception as e:
            zip = ''
            add = ''
            print("add","add",e)

        try:
            dec = ''.join(response.xpath('//*[contains(text(),"Community Overview")]//following-sibling::p/text()').extract())[0:1999]
        except Exception as e:
            dec = ''
            print("dec",e)

        try:
            im = ''.join(response.xpath('//*[@class="col-lg-7 detail-header-media order-lg-2"]/@style').extract())
            img = im.replace("background-image:url('",'').replace("');",'')
        except Exception as e:
            img = ''
            print("img",e)



        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionName'] = sname
        item['SubdivisionNumber'] = subdivisonNumber
        item['BuilderNumber'] = self.builderNumber
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 1
        item['Street1'] = add
        item['City'] = 'Blue Springs'
        item['State'] ='MO'
        item['ZIP'] = zip
        item['AreaCode'] = '816'
        item['Prefix'] = '228'
        item['Suffix'] = '1188'
        item['Extension'] = ""
        item['Email'] = "info@ashlarhomeskc.com"
        item['SubDescription'] = dec #'WELCOME TO ASHLAR HOMES At Ashlar Homes we aim to build the strongest and most durable homes on the market so that we can deliver on a long lasting promise to our customers. Whether you choose to build your home in one of the select neighborhoods or on a lot of your choice, know when you chose Ashlar Homes you’re receiving the highest quality of construction and customer service, guaranteed. We go above and beyond for our customers, our Standard Ashlar Features are sure to impress any home buyer. We encourage you to visit a community or contact Shawn Woods for a tour of the product line.'
        item['SubImage'] = img #'https://images8.webydo.com/94/9403636/3958%2f0E79EB78-FC38-E881-E558-EC5FE325EDE5.png_400'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ""
        yield item

        hlink = response.xpath('//*[@class="css-t32728"]/div[2]//div[@class="HomeCard"]/a/@href').extract()
        links = response.xpath('//*[@class="row justify-content-center"]//div[@class="PlanCard"]')
        plandetails = {}
        for url in links:
            li = url.xpath('./div[@class="PlanCard_media"]/a/@href').extract_first()
            pri = ''.join(url.xpath('.//*[contains(text(),"Priced From: ")]//following-sibling::span/text()').extract())
            plan_link = 'https://www.ashlarhomeskc.com'+li
            yield scrapy.FormRequest(url=plan_link,dont_filter=True, callback=self.plan_details, meta={'sbdn':subdivisonNumber, 'hlink':hlink,'pri':pri, 'plandetails':plandetails}) #'hlink':hlink,

    # def plan_link_page(self, response):
    #     sbdn = response.meta['sbdn']
    #     hlink = response.meta['hlink']
    #     # plan_links = ['plan/mcqueen', 'plan/bronson', 'plan/redbud', 'plan/willow', 'plan/birch', 'plan/oakmont', '/plan/oakmont-ii', 'plan/linden']
    #     plinks = response.xpath('//*[@class="row justify-content-center"]//div[@class="PlanCard"]')
    #     for i in plinks:
    #         li = i.xpath('./a/@href').extract_first()
    #         link = 'https://www.ashlarhomeskc.com'+str(li)
    #         pri = ''.join(i.xpath('.//*[contains(text(),"Priced From: ")]//following-sibling::span/text()').extract())
    #         print("plan-------------->",link)
    #         yield scrapy.Request(url=link,dont_filter=True, callback=self.plan_details, meta={'sbdn': sbdn,'i':i,'pri':pri})

    def plan_details(self, response):
        plandetails = response.meta['plandetails']
        hlink = response.meta['hlink']
        Type = 'SingleFamily'
       
        Plan = response.url
        PlanName = Plan.split('/')[-1].replace('-','').strip()
        
        try:
            PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % PlanNumber, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
            print(e)

        SubdivisionNumber = response.meta['sbdn']
        
        PlanNotAvailable = 0
        
        PlanTypeName = 'Single Family'
       
        try:
            # price =response.xpath('//p/strong/text()').extract_first()
            pri = response.meta['pri'].replace('$','').replace(',','').strip()
            BasePrice = pri
            # print(BasePrice)
        except Exception as e:
            print(e)
            BasePrice=0

        
        PlanWebsite = response.url
        
        # a = response.xpath('//div[@class="innerText36_ContentDiv"]//text()').extract()
        # print(a)
        try:

            Bath = ''.join(response.xpath('//*[@class="detail-header-list2"]//*[contains(text(),"Baths")]/strong/text()').extract()).replace(' ','').strip()
            if Bath == '2.5':
                Baths = 2
                HalfBaths = 1
            elif Bath == '3.5':
                Baths = 3
                HalfBaths = 1
            else:
                Baths = Bath
                HalfBaths = 0
        except Exception as e:
            Baths = 0
            print(e)

        try:
            Bedrooms = ''.join(response.xpath('//*[@class="detail-header-list2"]//*[contains(text(),"  Beds")]/strong/text()').extract())
            # Bedrooms=Bedrooms.split(' ')[0]
            if Bedrooms == '':
                Bedrooms = 0
        except Exception as e:
            Bedrooms = 0
            print(e)

        try:
            Garage = ''.join(response.xpath('//*[@class="detail-header-list2"]//*[contains(text(),"Garages")]/strong/text()').extract()).replace(',','')
            # Garage = Garage.split(' ')[0]
        except Exception as e:
            print(e)
            Garage=0

        try:
            BaseSqft = ''.join(response.xpath('//*[@class="detail-header-list2"]//*[contains(text(),"SQ FT")]/strong/text()').extract()).replace(',','')
        except Exception as e:
            BaseSqft = ''
            print(e)

        try:
            # a='|'.join(response.xpath('//*[@class="innerText53_ContentDiv"]//text()').extract()).strip().replace('\\x8B','').replace('\\xE2','').replace('\\x80','')
            # b = '|'.join(response.xpath('//*[@class="innerText34_ContentDiv"]/p[1]/text()').extract()).strip().replace('\\x8B','').replace('\\xE2','').replace('\\x80','')
            dec = ''.join(response.xpath('//*[@class="wrapper col-md-8 ml-auto mr-auto"]//div[@class="content"]//p/text()').extract())
            Description = dec #(str(a)+str(b)).replace('\\x8B','').replace('\\xE2','').replace('\\x80','').encode('ascii','ignore').decode('utf8')
            # print(Description)
        except Exception as e:
            print(e)
            Description = ''

        try:
            img = response.xpath('//*[@class="AccordionToggle_contentInterior"]//ul[@class="PhotoList_list"]//li//div[@class="PhotoList_image"]/@style').extract()[-1]
            img = img.replace("background-image:url('",'').replace("');",'')
            ElevationImage = img
            # print(ElevationImage)
        except Exception as e:
            print(str(e))

        SubdivisionNumber = SubdivisionNumber  # if subdivision is there
        # SubdivisionNumber = self.builderNumber #if subdivision is not available
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        plandetails[PlanName] = unique_number
        item = BdxCrawlingItem_Plan()
        item['Type'] = Type
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = PlanNumber # < -------- Changes here
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
        # print(item)

        try:
            hmlink = hlink #response.xpath('//div[@class="HomeCard"]/a/@href').extract()
            for url in hmlink:
                link = 'https://www.ashlarhomeskc.com' + url
                yield scrapy.FormRequest(url=link, dont_filter=True, callback=self.home_details, meta={'PN': plandetails,'PlanNumber':PlanNumber})
        except:
            pass

    def home_details(self, response):

        PlanNumber = response.meta['PlanNumber']
        Spec = ''.join(response.xpath('//*[@class="col-lg-5 detail-header-content"]/h1/text()').extract()).strip()
        SpecStreet1 = ' '.join(Spec.split(' ')[1:])
        try:
            SpecPrice = ''.join(response.xpath('//*[@class="col-lg-5 detail-header-content"]/h2/strong/text()').extract()).replace(',','').replace('$','').strip()
        except Exception as e:
            print("SpecPrice---------->",e)

        try:
            ci = ''.join(response.xpath('//*[@class="col-lg-5 detail-header-content"]/h2/text()').extract())
            cty = ci.split(',')[0]
            city = cty
        except Exception as e:
            city = ''
            print(e)

        state = 'KS'
        try:
            zi = ''.join(response.xpath('//*[@class="col-lg-5 detail-header-content"]/h1/text()').extract()).strip()[0:5]
            zip =''.join(re.findall(r'\b\d{4,5}\b', zi))+'12427'
            zip = zip[0:5]
        except Exception as e:
            zip = ''
            print(e)
        unique = SpecStreet1 + city + state + zip
        # print(unique)
        SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        try:
            SpecSqft = ''.join(response.xpath('//*[@class="detail-header-list2"]//*[contains(text(),"SQ FT")]/strong/text()').extract()).replace(',','')
        except Exception as e:
            print("SpecSqft---------->",e)
        try:
            SpecBaths =''.join(response.xpath('//*[@class="detail-header-list2"]//*[contains(text(),"Baths")]/strong/text()').extract()).strip()
        except Exception as e:
            print("SpecBaths--------->",e)
        SpecBedrooms = ''.join(response.xpath('//*[@class="detail-header-list2"]//*[contains(text(),"Beds")]/strong/text()').extract()).strip()

        garage = ''.join(response.xpath('//*[@class="detail-header-list2"]//*[contains(text(),"Garages")]/strong/text()').extract()).strip()

        try:
            img = '|'.join(response.xpath('//*[@class="AccordionToggle_contentInterior"]//ul[@class="PhotoList_list"]//li//div[@class="PhotoList_image"]/@style').extract())
            img = img.replace("background-image:url('", '').replace("');", '')
            SpecElevationImage = img
        except Exception as e:
            SpecElevationImage = ''
            print(e)

        item = BdxCrawlingItem_Spec()
        item['SpecNumber'] = SpecNumber
        item['PlanNumber'] = PlanNumber
        item['SpecStreet1'] = SpecStreet1
        item['SpecCity'] = city
        item['SpecState'] = 'KS'
        item['SpecZIP'] = zip
        item['SpecCountry'] = 'USA'
        item['SpecPrice'] = SpecPrice
        item['SpecSqft'] = SpecSqft
        item['SpecBaths'] = SpecBaths
        item['SpecHalfBaths'] = 0
        item['SpecBedrooms'] = SpecBedrooms
        item['MasterBedLocation'] = 0
        item['SpecGarage'] = garage
        item['SpecDescription'] = 0
        item['SpecElevationImage'] = SpecElevationImage
        item['SpecWebsite'] = 'https://www.ashlarhomeskc.com/dayton-creek-available-homes-1.html'
        yield item
        # print('--------------->Homes', item)


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl Ashlar_Homes".split())
