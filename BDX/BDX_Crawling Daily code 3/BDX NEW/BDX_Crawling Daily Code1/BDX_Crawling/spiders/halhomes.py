import requests
from scrapy.http import HtmlResponse

# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'halhomes'
    allowed_domains = ['halhomes.com']
    start_urls = ['http://www.halhomes.com/']
    builderNumber = 27592


    def parse(self, response):
        links = response.xpath('//div[@class="callout-button"]/a/@href').extract()
        for link in links:
            link = 'http://www.halhomes.com' + link
            yield scrapy.FormRequest(url=link,callback=self.community_detail,dont_filter=True)

    def community_detail(self,response):

        try:
            subdivisonName = response.xpath("//h1/text()").extract_first('')
            print(subdivisonName)
        except Exception as e:
            print(e)
            subdivisonName = ''

        try:
            sub_imagwe = []
            image = response.xpath('//div[@class="slide-image"]/img/@src').extract()

            if image != []:

                for ii in image:
                    ii = ii.replace("background-image: url(","").replace(");","")
                    sub_imagwe.append(ii)


                sub_imagwe = "|".join(sub_imagwe)
                print(sub_imagwe)
            else:
                sub_imagwe = ''

        except Exception as e:
            print(e)
            sub_imagwe = ""

        map_link = response.xpath("//span[contains(text(),'MAP & DIRECTIONS')]/../@href").extract_first("")
        if map_link != '':
            map_link = 'http://www.halhomes.com' + map_link
            print(map_link)

            yield scrapy.FormRequest(url=map_link,callback=self.comm,dont_filter=True,meta={'subdivisonName':subdivisonName,'sub_imagwe':sub_imagwe})

    def comm(self,response):
        subdivisonName = response.meta['subdivisonName']
        sub_imagwe = response.meta['sub_imagwe']

        try:
            if subdivisonName == 'Falling Brook':
                street ,city,state,zip = "5757 Falling Brook Dr",'Mason',"OH" , "45040"
            else:
                final_link = 'https://www.google.com/maps?ll=39.229611,-84.269133&z=16&t=m&hl=en-GB&gl=US&mapclient=embed&q=6408+Birch+Creek+Dr+Loveland,+OH+45140'
                street ,city,state,zip = '6408 Birch Creek Dr','Loveland','OH','45140'

            # final_link = response.xpath("//*[contains(text(),'View larger map')]/@href").extract_first('')
            # print(final_link)
        except Exception as e:
            print(e)

        # try:
        #     if subdivisonName == 'Falling Brook':
        #         final_link = 'https://www.google.com/maps?ll=39.354586,-84.279677&z=16&t=m&hl=en-GB&gl=US&mapclient=embed&q=5757+Falling+Brook+Dr+Mason,+OH+45040'
        #     else:
        #         final_link = 'https://www.google.com/maps?ll=39.229611,-84.269133&z=16&t=m&hl=en-GB&gl=US&mapclient=embed&q=6408+Birch+Creek+Dr+Loveland,+OH+45140'
        #
        #     # final_link = response.xpath("//*[contains(text(),'View larger map')]/@href").extract_first('')
        #     # print(final_link)
        # except Exception as e:
        #     print(e)
        #
        # url = final_link
        # try:
        #     res_d = requests.request("GET", url=url)
        #     response_d = HtmlResponse(url=url, body=res_d.content)
        #     # print(response_d.text)
        #     try:
        #         full = response_d.text.split(r'\"],null,null,null,null,null,1,null,')[-1].split(r'\",\"')[1].split(
        #             r'\",null,[null,null,')[0]
        #         if "null" in full:
        #             try:
        #                 full = response_d.text.split(r'[[[1,[[\"')[1].split(r'\"]]],')[0]
        #                 # print(full)
        #                 if "null" in full:
        #                     full = response_d.text.split.split('],null,0],[null,["')[-1](r'"Google Maps",')[0]
        #                     # print(full)
        #             except:
        #                 # full = response_d.text.split.split('],null,0],[null,["')[-1](r'"Google Maps",')[0]
        #                 full = \
        #                 response_d.text.split('],null,0],[null,["')[-1].split(r'"Google Maps",')[0].split('",null')[
        #                     0].strip()
        #                 # print(full)
        #         else:
        #             full = full
        #
        #     except:
        #         full = ''
        # except Exception as e:
        #     print(e)
        #
        #
        #
        # try:
        #     street = full.split(",")[0]
        #     print(street)
        # except Exception as e:
        #     print(e)
        #     street = ''
        #
        # try:
        #     add2 = full.split(",")[1].strip()
        #     print(add2)
        #     city = add2.split(",")[0]
        #     print(city)
        #
        #     state = add2.split(",")[1].strip().split(" ")[0]
        #     zip = add2.split(",")[1].strip().split(" ")[1]
        # except Exception as e:
        #     print(e)
        #     city,state,zip = '','',''
        #
        #
        # try:
        #     desc = ''
        # except Exception as e:
        #     print(e)
        #     desc = ''
        #


        subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = subdivisonNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = subdivisonName
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = street
        item['City'] = city
        item['State'] = state
        item['ZIP'] = zip
        item['AreaCode'] = ''
        item['Prefix'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = ''
        item['SubImage'] = sub_imagwe
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item


        unique = str("Plan Unknown") +str(self.builderNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['unique_number'] = unique_number
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = "Plan Unknown"
        item['SubdivisionNumber'] =  subdivisonNumber = int(hashlib.md5(bytes('Falling Brook', "utf8")).hexdigest(), 16) % (10 ** 30)
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

        spec_link = 'http://www.halhomes.com/listings/'
        yield scrapy.FormRequest(url=spec_link,callback=self.spec_links,dont_filter=True,meta={'unique_number':unique_number})

    def spec_links(self,response):
        unique_number = response.meta['unique_number']
        links = response.xpath('//h2/a/@href').extract()
        for spec in links:
            yield scrapy.FormRequest(url=spec, callback=self.spec_detail, dont_filter=True,meta={'unique_number':unique_number})

    def spec_detail(self,response):

        status = response.xpath('//div[@class="ptb_module ptb_text ptb_occupancy_date"]//text()[2]').get().replace("\n","").strip()
        if status != 'SOLD':
            unique_number = response.meta['unique_number']
            address = response.xpath('//div[@class="ptb_module ptb_text ptb_property_address"]/text()[2]').extract_first().strip()
            try:
                SpecStreet1 = address.split(",")[0]
                SpecCity = address.split(',')[1].strip()
                SpecCity = address.split(',')[0].strip()
            except Exception as e:
                print(e)
            try:
                SpecState = address.split(',')[2].strip()
                SpecState = SpecState.split(" ")[0].strip()
            except Exception as e:
                print(e)
            try:
                SpecZIP = address.split(',')[2].strip()
                SpecZIP = SpecZIP.split(' ')[1].strip()
            except Exception as e:
                print(e)

            try:
                unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()
            except Exception as e:
                print(e)

            try:
                SpecCountry = "USA"
            except Exception as e:
                print(e)

            try:
                SpecPrice = response.xpath('//div[@class="ptb_module ptb_number ptb_price"]/text()[2]').extract_first().replace('$', '').replace(',', '')
                SpecPrice = re.findall(r"(\d+)", SpecPrice)[0]
            except Exception as e:
                print(e)

            try:
                SpecSqft = str(
                    response.xpath('//div[@class="ptb_module ptb_number ptb_sq_ft"]/text()[2]').extract_first(default='0').strip()).replace(",",
                                                                                                                       "")
                SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
            except Exception as e:
                SpecSqft = '0'
                print(e)

            try:
                SpecBaths = str(response.xpath('//div[@class="ptb_module ptb_number ptb_bathrooms"]/text()[2]').extract_first(
                    default='0').strip()).replace(",", "")
                tmp = re.findall(r"(\d+)", SpecBaths)
                SpecBaths = tmp[0]
                if len(tmp) > 1:
                    SpecHalfBaths = 1
                else:
                    SpecHalfBaths = 0
            except Exception as e:
                print(e)

            try:
                SpecBedrooms = str(response.xpath('//div[@class="ptb_module ptb_number ptb_bedrooms"]/text()[2]').extract_first(
                    default='0').strip()).replace(",", "")
                SpecBedrooms = re.findall(r'(\d+)', SpecBedrooms)[0]
            except Exception as e:
                print(e)

            try:
                MasterBedLocation = "Down"
            except Exception as e:
                print(e)

            try:
                SpecGarage = response.xpath('//div[@class="ptb_module ptb_text ptb_garage_space"]/text()[2] ').extract_first(default='0')
                SpecGarage = re.findall(r"(\d+)", SpecGarage)[0]
            except Exception as e:
                SpecGarage = '0'
                print(e)

            try:

                SpecDescription = ''.join(
                        response.xpath('//div[@class="ptb_entry_content"]/p/text()').extract()).strip()
            except Exception as e:
                print(e)

            try:
                ElevationImage = '|'.join(response.xpath('//figure[@class="ptb_post_image clearfix"]/img/@src').extract())
            except Exception as e:
                print(e)

            try:
                SpecWebsite = response.url
            except Exception as e:
                print(e)

                # ----------------------- Don't change anything here ---------------- #
            item = BdxCrawlingItem_Spec()
            item['SpecNumber'] = SpecNumber
            item['PlanNumber'] = unique_number
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
            item['SpecDescription'] = SpecDescription
            item['SpecElevationImage'] = ElevationImage
            item['SpecWebsite'] = SpecWebsite
            yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl halhomes'.split())
