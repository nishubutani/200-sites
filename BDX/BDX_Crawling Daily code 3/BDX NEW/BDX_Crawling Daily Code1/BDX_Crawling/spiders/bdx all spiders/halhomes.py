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
            final_link = response.xpath("//*[contains(text(),'View larger map')]/@href").extract_first('')
            print(final_link)
        except Exception as e:
            print(e)

        url = final_link
        try:
            res_d = requests.request("GET", url=url)
            response_d = HtmlResponse(url=url, body=res_d.content)
            # print(response_d.text)
            try:
                full = response_d.text.split(r'\"],null,null,null,null,null,1,null,')[-1].split(r'\",\"')[1].split(
                    r'\",null,[null,null,')[0]
                if "null" in full:
                    try:
                        full = response_d.text.split(r'[[[1,[[\"')[1].split(r'\"]]],')[0]
                        # print(full)
                        if "null" in full:
                            full = response_d.text.split.split('],null,0],[null,["')[-1](r'"Google Maps",')[0]
                            # print(full)
                    except:
                        # full = response_d.text.split.split('],null,0],[null,["')[-1](r'"Google Maps",')[0]
                        full = \
                        response_d.text.split('],null,0],[null,["')[-1].split(r'"Google Maps",')[0].split('",null')[
                            0].strip()
                        # print(full)
                else:
                    full = full

            except:
                full = ''
        except Exception as e:
            print(e)



        try:
            street = full.split(",")[0]
            print(street)
        except Exception as e:
            print(e)
            street = ''

        try:
            add2 = full.split(",")[1].strip()
            print(add2)
            city = add2.split(",")[0]
            print(city)

            state = add2.split(",")[1].strip().split(" ")[0]
            zip = add2.split(",")[1].strip().split(" ")[1]
        except Exception as e:
            print(e)
            city,state,zip = '','',''


        try:
            desc = ''
        except Exception as e:
            print(e)
            desc = ''



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
        item['SubDescription'] = desc
        item['SubImage'] = sub_imagwe
        item['SubWebsite'] = response.url
        # item['AmenityType'] = ''
        yield item



        i
if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl halhomes'.split())
