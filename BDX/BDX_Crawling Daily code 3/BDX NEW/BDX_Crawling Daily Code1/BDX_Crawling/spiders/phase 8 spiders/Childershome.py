# -*- coding: utf-8 -*-
import hashlib
import re

import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class chdHomesSpider(scrapy.Spider):
    name = 'childershome'
    allowed_domains = []
    start_urls = ['http://www.childershomes.com/']

    builderNumber = 52305

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
        item['Street1'] = '13110 N. 144th Plaza Circle'
        item['City'] = 'Bennington'
        item['State'] = 'NE'
        item['ZIP'] = '68007'
        item['AreaCode'] = '402'
        item['Prefix'] = '238'
        item['Suffix'] = '3093'
        item['Extension'] = ""
        item['Email'] = 'info@cityline.us'
        item[
            'SubDescription'] = 'Welcome to Childers Custom Homes website!Whether you are looking to build your "dream home" or a quality "starter" home, Childers Custom Homes can provide you with committed customer service to help you through the process!Paul Childers has been building homes in and around Omaha for 15 years. He is a very "hands on" builder that you will see on your jobsite. His personal care to detail is above and beyond what you may experience with other builders! Many of our customers appreciate dealing directly with the builder to make their home everything they want it to be.Childers Custom homes is licensed and bonded.Our new model is located in Stratford Park located at 168th and State. Call us today to see this beautiful home!Thank you!'
        item['SubImage'] = ''
        item['SubWebsite'] = response.url
        yield item

        yield scrapy.Request(url=response.url, callback=self.plan_link_page)

    def plan_link_page(self, response):

        unique = str("Plan Unknown") + str(self.builderNumber)  # < -------- Changes here
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

        home_link = 'https://www.childershomes.com/search/featuredlistings.aspx'
        yield scrapy.Request(url=home_link, callback=self.homelink,dont_filter=True,meta={'PN':unique_number})


    def homelink(self,response):
        PN=response.meta['PN']
        link=response.xpath('//section[@class="listing listing__photo"]//a[@aria-label="listing photo link"]/@href').extract()
        for i in link:
            lk= 'https://www.childershomes.com'+i
            print(lk)
            yield scrapy.Request(url=lk, callback=self.home_data, dont_filter=True,meta={'PN':PN})

    def home_data(self, response):
                st=re.findall('Listing Status:</strong>(.*?)</li>',response.text,re.DOTALL)
                st=st[0].replace('\r','').replace('\n','').strip()
                if st!='Sold':
                    street1=re.findall('hmsitemprop="streetAddress">(.*?)</span>',response.text)[0].strip()
                    city=re.findall('hmsitemprop="addressLocality">(.*?)</span>',response.text)[0].strip().replace(',','')
                    sts=re.findall('hmsitemprop="addressRegion">(.*?)</span>',response.text)[0].strip()
                    zip=re.findall('hmsitemprop="postalCode">(.*?)</span>',response.text)[0].strip()

                    unique = street1 + city + sts + zip + str(response.url)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    try:
                        price=re.findall('hmsitemprop="Price">(.*?)</span>',response.text)[0].strip()

                    except:
                        price=0.00

                    sqft=re.findall('hmsitemprop="SearchableSqft">(.*?)</span>',response.text)[0].strip()
                    bed=re.findall('hmsitemprop="Bedrooms">(.*?)</span>',response.text)[0].strip()
                    bath=re.findall('hmsitemprop="Bathrooms">(.*?)</span>',response.text)[0].strip()

                    try:
                        garage= ''.join(re.findall('<strong class="details--label details--label__main">Garage:</strong>(.*?)</li>',response.text,re.DOTALL)).replace('\r','').replace('\n','').strip()
                        print(garage)
                        if garage=='':
                            garage=0.0
                    except:
                        garage= 0.0

                    eimg='|'.join(re.findall('data-slide-image data-src="(.*?)"',response.text,re.DOTALL))


                    desc = 'Welcome to Childers Custom Homes website!Whether you are looking to build your "dream home" or a quality "starter" home, Childers Custom Homes can provide you with committed customer service to help you through the process!Paul Childers has been building homes in and around Omaha for 15 years. He is a very "hands on" builder that you will see on your jobsite. His personal care to detail is above and beyond what you may experience with other builders! Many of our customers appreciate dealing directly with the builder to make their home everything they want it to be.Childers Custom homes is licensed and bonded.Our new model is located in Stratford Park located at 168th and State. Call us today to see this beautiful home!Thank you!'

                    item = BdxCrawlingItem_Spec()
                    item['SpecNumber'] = SpecNumber
                    item['PlanNumber'] = response.meta['PN']
                    item['SpecStreet1'] = street1
                    item['SpecCity'] = city
                    item['SpecState'] = sts
                    item['SpecZIP'] = zip
                    item['SpecCountry'] = 'USA'
                    item['SpecPrice'] = price
                    item['SpecSqft'] = sqft
                    item['SpecBaths'] = bath
                    item['SpecHalfBaths'] = 0
                    item['SpecBedrooms'] = bed
                    item['MasterBedLocation'] = "Down"
                    item['SpecGarage'] = garage
                    item['SpecDescription'] = desc
                    item['SpecElevationImage'] = eimg
                    item['SpecWebsite'] = response.url
                    yield item

#
# from scrapy.cmdline import execute
# execute("scrapy crawl childershome".split())