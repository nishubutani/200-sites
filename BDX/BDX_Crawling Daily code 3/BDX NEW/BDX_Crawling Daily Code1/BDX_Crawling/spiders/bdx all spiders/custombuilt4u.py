# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision



class Custombuilt4uSpider(scrapy.Spider):
    name = 'custombuilt4u'
    allowed_domains = ['custombuilt4u.com']
    start_urls = ['http://custombuilt4u.com/about.htm']
    builderNumber = 746236072880224758061704626503

    def parse(self, response):
        # item2 = BdxCrawlingItem_Corporation()
        # item2['CorporateBuilderNumber'] = inp.CorporateBuilderNumber
        # item2['CorporateName'] = inp.CorporateName
        # item2['CorporateState'] = inp.CorporateState
        # yield item2
        #
        # item1 = BdxCrawlingItem_Builder()
        # item1['BuilderNumber'] = int(hashlib.md5(bytes(inp.BuilderWebsite, "utf8")).hexdigest(), 16) % (10 ** 30)
        # item1['BrandName'] = inp.BrandName
        # item1['BrandLogo_Med'] = 'http://custombuilt4u.com/'+response.xpath('//img[@alt="Elite Development Custom Home Builders"]/@src').extract_first(default="")
        # item1['ReportingName'] = inp.ReportingName
        # item1['DefaultLeadsEmail'] = inp.DefaultLeadsEmail
        # item1['BuilderWebsite'] = inp.BuilderWebsite
        # item1['CorporateBuilderNumber'] = inp.CorporateBuilderNumber
        # yield item1

        item3 = BdxCrawlingItem_subdivision()
        item3['sub_Status'] = "Active"
        item3['BuilderNumber'] = self.builderNumber
        item3['SubdivisionName'] = "Elite Development, LLC"
        item3['SubdivisionNumber'] = int(hashlib.md5(bytes(item3['SubdivisionName'], "utf8")).hexdigest(), 16) % (10 ** 30)
        item3['BuildOnYourLot'] = 0
        item3['OutOfCommunity'] = 1
        # enter any address you fond on the website.
        item3['Street1'] = '4012 Parliament Dr. Suite D'
        item3['City'] = 'Alexandria'
        item3['State'] = 'LA'
        item3['ZIP'] = '71303'
        item3['AreaCode'] = '318'
        item3['Prefix'] = "623"
        item3['Suffix'] = "2046"
        item3['Extension'] = "2047"
        item3['Email'] = ""
        item3['SubDescription'] = response.xpath('//img/parent::font/text()').extract_first(default='')
        item3['SubImage'] = ""
        item3['SubWebsite'] = "http://custombuilt4u.com"
        yield item3

        try:
            unique = str("Plan Unknown") + str(item3['SubdivisionNumber'])  # < -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
            item = BdxCrawlingItem_Plan()
            item['Type'] = "SingleFamily"
            item['unique_number'] = unique_number
            item['PlanNumber'] = int(hashlib.md5(bytes("Plan Unknown", "utf8")).hexdigest(), 16) % (10 ** 30)
            item['SubdivisionNumber'] = item3['SubdivisionNumber']
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
            url = 'http://custombuilt4u.com/'+response.xpath('//a[contains(text(),"View Homes")]/@href').extract_first(default='')
            yield scrapy.FormRequest(url,callback=self.get_homes,meta={'PlanNumber':item['unique_number']})
        except Exception as e:
            print(e)
    def get_homes(self,response):
        home_urls = response.xpath('//a[contains(@href,"Account_Reference") and child::img]/@href').extract()
        PlanNumber = response.meta['PlanNumber']
        for home_url in home_urls:
            home_url = 'http://custombuilt4u.com'+home_url
            yield scrapy.FormRequest(home_url, callback=self.get_home_details,meta={'PlanNumber':PlanNumber})

    def get_home_details(self,response):
        try:
            SpecBedrooms = SpecBaths = SpecHalfBaths = SpecSqft = 0
            td1 = response.xpath('//b[contains(text(),"$")]/ancestor::table[1]/..')
            SpecPrice = re.sub('\D','',td1.xpath('normalize-space(.//table[1]//b/text())').extract_first(default=''))
            if SpecPrice != '':
                SpecCountry = 'USA'
                SpecStreet1 = td1.xpath('.//table[2]//b/text()').extract()[0]
                address = td1.xpath('.//table[2]//b/text()').extract()[-1]
                address = address.split(',')
                if len(address) > 2:
                    SpecCity = address[0]
                    SpecState = address[1]
                    SpecZIP = address[2]
                else:
                    SpecCity = SpecState = SpecZIP = ''
                MasterBedLocation = "Down"

                # SpecBedrooms = td1.xpath('normalize-space(//b[contains(text(),"Bedrooms")]/../text())').extract_first(default='')
                SpecBedrooms = re.sub('\D','',td1.xpath('normalize-space(//b[contains(text(),"Bedrooms")]/../text())').extract_first(default='0'))
                if len(SpecBedrooms) > 0:SpecBedrooms = SpecBedrooms[0]
                else:SpecBedrooms = 0
                SpecBaths = re.sub('\D','',td1.xpath('normalize-space(//b[contains(text(),"Baths")]/../text())').extract_first(default='0'))
                if len(SpecBaths) > 1:
                    SpecHalfBaths = 1
                    SpecBaths = SpecBaths[0]
                elif len(SpecBaths) == 1:
                    SpecBaths = SpecBaths[0]
                else:
                    SpecBaths = 0

                SpecSqft = re.sub('\D','',td1.xpath('normalize-space(//b[contains(text(),"Square")]/../text())').extract_first(default='0.00'))
                if SpecSqft == '': SpecSqft = '0.00'

                SpecElevationImage = '|'.join(response.xpath('//td[@nowrap]/a/img/@src').extract())
                if len(SpecElevationImage) == 0:
                    SpecElevationImage = response.xpath('//td[@valign="top"]/img[@name="picture"]/@src').extract_first(default='')
                    pass
                SpecDescription = re.sub('\s+',' ',re.sub('\n|\t','',''.join(response.xpath('//*[contains(text(),"FEATURES")]/../../../following-sibling::tr//text()').extract()))).strip()
                SpecWebsite = str(response.url)
                try:
                    unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                except Exception as e:
                    print(e)
                SpecGarage = 0
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = response.meta['PlanNumber']
                item['SpecStreet1'] = re.sub('\s+',' ',re.sub(r'\n|\t',' ',SpecStreet1)).strip()
                item['SpecCity'] = re.sub('\s+',' ',re.sub(r'\n|\t',' ',SpecCity)).strip()
                item['SpecState'] = re.sub('\s+',' ',re.sub(r'\n|\t',' ',SpecState)).strip()
                item['SpecZIP'] = re.sub('\s+',' ',re.sub(r'\n|\t',' ',SpecZIP)).strip()
                item['SpecCountry'] = re.sub('\s+',' ',re.sub(r'\n|\t',' ',SpecCountry)).strip()
                item['SpecPrice'] = re.sub('\s+',' ',re.sub(r'\n|\t',' ',SpecPrice)).strip()
                item['SpecSqft'] = SpecSqft
                item['SpecBaths'] = SpecBaths
                item['SpecHalfBaths'] = SpecHalfBaths
                item['SpecBedrooms'] = SpecBedrooms
                item['MasterBedLocation'] = re.sub('\s+',' ',re.sub(r'\n|\t',' ',MasterBedLocation))
                item['SpecGarage'] = SpecGarage
                item['SpecDescription'] = re.sub('\s+',' ',re.sub(r'\n|\t',' ',SpecDescription))
                item['SpecElevationImage'] = SpecElevationImage
                item['SpecWebsite'] = SpecWebsite
                yield item
        except Exception as e:
            print(e)

from scrapy.cmdline import execute
# execute('scrapy crawl custombuilt4u'.split())




