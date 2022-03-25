# -*- coding: utf-8 -*-
import hashlib
import requests
from scrapy.http import HtmlResponse
import re
import scrapy
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class MontehewetthomesSpider(scrapy.Spider):
    name = 'montehewetthomes'
    allowed_domains = []
    start_urls = ['https://montehewett.com/']

    builderNumber = "30056889955013300393106601211"

    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        images = ''
        image = response.xpath('//img/@src').extract()
        for i in image:
            images = images + i + '|'
        images = images.strip('|')

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '5775 Glenridge Drive Building B'
        item['City'] = 'Atlanta'
        item['State'] = 'GA'
        item['ZIP'] = '30328'
        item['AreaCode'] = '404'
        item['Prefix'] = '459'
        item['Suffix'] = '6080'
        item['Extension'] = ""
        item['Email'] = 'info@montehewett.com'
        item['SubDescription'] = 'Monte brings 25 years of industry experience to the table. He first came to Atlanta in 1998 to establish a local division of Texas-based Highland Homes. After several years, he went out on his own and established Monte Hewett Homes in 2002. Monte has since watched his business grow and what you see today is a great team driven by a natural born leader whos built successful relationships with employees, vendors and partners alike.'
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        # def parse(self, response):
    #
    #     try:
    #         contact_dict = {'206358154775741536316238455299':'404 940 0048','445490171844071602678551151562':'678 558 0361','815355120878095380817894181244':'678 460 0707','819425149110319258071119607073':'678 558 0361','947408792391465911836776096266':'678 460 0709','183972060404348752609509338172':'678 558 0361','380506142068696064486505080775':'678 460 0706','616931104084960314009098440625':'678 460 0628','609789267426749641003137489161':'678 460 0682'}
    #         mail_dict = {'206358154775741536316238455299':'rahwatassaw@atlantafinehomes.com','445490171844071602678551151562':'terry.fogarty@mhhomes.com','815355120878095380817894181244':'jason.jones@mhhomes.com','819425149110319258071119607073':'info@mhhomes.com','947408792391465911836776096266':'paula.burr@mhhomes.com','183972060404348752609509338172':'info@mhhomes.com','380506142068696064486505080775':'paula.burr@mhhomes.com','616931104084960314009098440625':'jason.jones@mhhomes.com','609789267426749641003137489161':'jason.jones@mhhomes.com'}
    #         com_links = response.xpath('//ul[@id="map"]/li/@id').extract()
    #         for link in com_links:
    #             # link = 'https://montehewetthomes.com/locations/madison-yards'
    #             print(self.start_urls[0]+'/'+str(link))
    #             head = {'Host': 'montehewetthomes.com','User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language': 'en-US,en;q=0.5','Accept-Encoding': 'gzip, deflate, br'}
    #             res_c = requests.get(self.start_urls[0]+'/'+str(link),verify=False,headers=head, allow_redirects=True)#'http://192.168.1.106:8050/render.html?url='+
    #             response_c = HtmlResponse(url=res_c.url,body=res_c.content)
    #
    #             # ------------------- If communities found ---------------------- #
    #             # ------------------- Creating Communities ---------------------- #
    #             subdivisonName = response_c.xpath('//h2[contains(@class,"cname")]/text()').extract_first(default="").strip()
    #             subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
    #
    #             f = open("html/%s.html" % subdivisonNumber, "wb")
    #             f.write(response_c.body)
    #             f.close()
    #
    #             add_raw = response_c.xpath('//a[@class="address-update"]/text()').extract_first(default='').strip()
    #             if '|' in add_raw:
    #                 add_raw = add_raw.split('|')
    #                 if ',' not in add_raw[0]:
    #                     street1 = add_raw[0].strip()
    #                     city = add_raw[-1].strip().split(',')[0].strip()
    #                     if link == 'the-wesley':
    #                         state = 'GA'
    #                     else:
    #                         state = add_raw[-1].strip().split(',')[-1].strip().split(' ')[0].strip()
    #                     zip = add_raw[-1].strip().split(',')[-1].strip().split(' ')[-1].strip()
    #                 else:
    #                     street1 = add_raw[0].strip().split(',')[0].strip()
    #                     state = add_raw[0].strip().split(',')[-1].strip()
    #                     city = add_raw[-1].strip().split(' ')[0].strip()
    #                     zip = add_raw[-1].strip().split(' ')[-1].strip()
    #             else:
    #                 add_raw = add_raw.split(',')
    #                 street1 = add_raw[0].strip()
    #                 try:
    #                     city = add_raw[-1].strip().split(' ')[0].strip()
    #                     if link == 'https://montehewetthomes.com/locations/the-wesley':
    #                         state = 'GA'
    #                     else:
    #                         state = add_raw[-1].strip().split(' ')[1].strip()
    #                     zip = add_raw[-1].strip().split(' ')[2].strip()
    #                 except:
    #                     city = add_raw[1].strip()
    #                     state = add_raw[-1].strip().split(' ')[0].strip()
    #                     zip = add_raw[-1].strip().split(' ')[1].strip()
    #
    #             email = mail_dict.get(str(subdivisonNumber))
    #             phoneNumber = contact_dict.get(str(subdivisonNumber)).split(' ')
    #
    #             image = []
    #             img1= response_c.xpath('//h2[@class="headline"]/following-sibling::img/@src').extract_first(default='').strip()
    #             if img1!='':
    #                 image.append(img1)
    #             img2 = response_c.xpath('//*[@id="overview"]//img[contains(@src,"s3.ama")]/@src').extract_first(default='').strip()
    #             if img2!='':
    #                 image.append(img2)
    #             img3 = response_c.xpath('//*[@id="siteplan"]//img[contains(@src,"s3.ama")]/@src').extract_first(default='').strip()
    #             if img3 != '':
    #                 image.append(img3)
    #             if image!=[]:
    #                 Image = '|'.join(image)
    #             else:
    #                 Image=''
    #
    #             #------------------process for another set of image
    #             try:
    #                 res_i = requests.get(response_c.url+'?tab=modelhome')
    #                 response_i = HtmlResponse(url=res_i.url,body=res_i.content)
    #                 try:images = 'https://'+'|https://'.join(response_i.xpath('//*[@class="dynamic-image"]/@data-image-src').extract())
    #                 except:images=''
    #
    #                 if images!='' and Image!='':
    #                     Image = Image+'|'+images
    #                 else:
    #                     Image= images
    #             except Exception as e:
    #                 print(e)
    #
    #             item2 = BdxCrawlingItem_subdivision()
    #             item2['sub_Status'] = "Active"
    #             item2['SubdivisionName'] = subdivisonName
    #             item2['SubdivisionNumber'] = subdivisonNumber
    #             item2['BuilderNumber'] = self.builderNumber
    #             item2['BuildOnYourLot'] = 0
    #             item2['OutOfCommunity'] = 1
    #             item2['Street1'] = street1
    #             item2['City'] = city
    #             item2['State'] = state
    #             if item2['State']=='NW':
    #                 item2['State'] ='GA'
    #             item2['ZIP'] = zip
    #             item2['AreaCode'] = phoneNumber[0]
    #             item2['Prefix'] = phoneNumber[1]
    #             item2['Suffix'] = phoneNumber[2]
    #             item2['Extension'] = ""
    #             item2['Email'] = email
    #             item2['SubDescription'] = response_c.xpath('//h3[contains(text(),"The Community")]/ancestor::div[1]/p[1]/text()').extract_first(default="").encode('ascii','ignore').decode('utf8').strip()
    #             item2['SubImage'] = Image
    #             item2['SubWebsite'] = response_c.url
    #             item2['AmenityType'] = ''
    #             yield item2
    #
    #             res_s = requests.get(response_c.url+'?tab=availability')
    #             response_s = HtmlResponse(url=res_s.url,body=res_s.content)
    #
    #             plan_links = response_s.xpath('//a[contains(text(),"VIEW HOME DETAILS")]/@href').extract()
    #             for slink in plan_links:
    #                 res_p = requests.get('https://montehewetthomes.com'+slink)
    #                 response_p = HtmlResponse(url=res_p.url,body=res_p.content)
    #
    #                 try:
    #                     Type = 'SingleFamily'
    #                 except Exception as e:
    #                     print(e)
    #
    #                 try:
    #                     PlanNumber = int(hashlib.md5(bytes(response_p.url, "utf8")).hexdigest(), 16) % (10 ** 30)
    #                 except Exception as e:
    #                     print(e)
    #
    #                 try:
    #                     PlanName = response_p.xpath('//h3/text()').extract_first(default='').strip()
    #                 except Exception as e:
    #                     print(e)
    #
    #                 try:
    #                     PlanNotAvailable = 0
    #                 except Exception as e:
    #                     print(e)
    #
    #                 try:
    #                     PlanTypeName = 'Single Family'
    #                 except Exception as e:
    #                     print(e)
    #
    #                 try:
    #                     BasePrice = response_p.xpath('//h5[@class="price"]/text()').extract_first(default=0).strip().replace('$','').replace(',','')
    #                     BasePrice = 0 if BasePrice=='' else BasePrice
    #                 except Exception as e:
    #                     BasePrice = 0
    #                     print(e)
    #
    #                 try:
    #                     Description = response_p.xpath('//h5[contains(text(),"ADDITIONAL")]/following-sibling::p/text()').extract_first(default='').strip()
    #                 except Exception as e:
    #                     print(e)
    #
    #                 try:
    #                     data = ' • '.join(response_p.xpath('//h5[@class="size"]/text()').extract())
    #                     try:Bedrooms = re.findall('(\d+)\sBed',data)[0].strip()
    #                     except:Bedrooms = 0
    #
    #                     try:Baths = re.findall('(\d+)\sFull Baths',data)[0].strip()
    #                     except:Baths = 0
    #
    #                     try:HalfBaths = re.findall('(\d+)\sHalf Baths',data)[0].strip()
    #                     except:HalfBaths = 0
    #
    #                     try:BaseSqft = re.findall('(\d+)\sSQFT',data)[0].strip()
    #                     except:BaseSqft = 0
    #                 except Exception as e:
    #                     print(e)
    #
    #                 try:
    #                     ElevationImage = '|'.join(response_p.xpath('//*[@class="clip"]/img/@src').extract())
    #                 except Exception as e:
    #                     print(e)
    #
    #                 try:
    #                     PlanWebsite = str(response_p.url)
    #                     # print(PlanWebsite)
    #                 except Exception as e:
    #                     print(e)
    #
    #                 # ----------------------- Don't change anything here --------------
    #                 try:
    #                     unique = str(PlanName) + str(response.url) + str(self.builderNumber)  # < -------- Changes here
    #                     unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
    #                                 10 ** 30)  # < -------- Changes here
    #                     item = BdxCrawlingItem_Plan()
    #                     item['Type'] = Type
    #                     item['PlanNumber'] = PlanNumber
    #                     item['unique_number'] = unique_number  # < -------- Changes here
    #                     item['SubdivisionNumber'] = subdivisonNumber
    #                     item['PlanName'] = PlanName
    #                     item['PlanNotAvailable'] = PlanNotAvailable
    #                     item['PlanTypeName'] = PlanTypeName
    #                     item['BasePrice'] = BasePrice
    #                     item['BaseSqft'] = BaseSqft
    #                     item['Baths'] = Baths
    #                     item['HalfBaths'] = HalfBaths
    #                     item['Bedrooms'] = Bedrooms
    #                     item['Garage'] = 0
    #                     item['Description'] = Description
    #                     item['ElevationImage'] = ElevationImage
    #                     item['PlanWebsite'] = PlanWebsite
    #                     yield item
    #                 except Exception as e:
    #                     print(e)
    #     except Exception as e:
    #         print(e)








if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl montehewetthomes'.split())