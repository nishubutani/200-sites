# -*- coding: utf-8 -*-
import scrapy
import scrapy
import hashlib
import re
import scrapy
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class CasasdeleonSpider(scrapy.Spider):
    name = 'casasdeleon'
    allowed_domains = ['mycasasdeleon.com']
    start_urls = ['http://mycasasdeleon.com/find']
    builderNumber = '24080'

    def parse(self, response):
        community_links = response.xpath('//h5/a/@href').extract()
        statuss = response.xpath('//div[@class="gdlr-item gdlr-content-item"]//strong//text()').extract()
        print(statuss)
        for community,status in zip(community_links,statuss):
            if "Sold Out" not in status:
                if "Coming soon" not in status:
                    link = community
                    yield scrapy.FormRequest(url=link,
                                             callback=self.community_details)

    def community_details(self,response):
        global street, city, state, zipcode, SubdivisionNumber
        try:
            community_details = {}
            SubdivisionName = response.xpath('//div[@class="gdlr-page-title-wrapper"]//h1//text()').get()

            address = response.xpath('//div[@class="gdlr-item gdlr-content-item"]/p/strong[1]/following-sibling::text()[1]').get()
            if not address:
                address = response.xpath('//div[@class="directions-address"]/text()').get()
            address = address.replace('(Peyton Estates – Coming Soon)','').replace('(Coming soon)','')
            # address = '13606 Gatton St. TX 79928 (Coming soon)'

            if 'St.' not in address:
                if 'Ave.' not in address:
                    street = address.split(',')[0].strip()
                    city = address.split(',')[1].strip()
                    state = address.split(',')[-1].strip().split()[0].replace('Texas','TX')
                    zipcode = address.split(',')[-1].strip().split()[1]
            else:
                street = address.split('.')[0].strip()
                try:
                    city = address.split('.')[1].split(',')[0].strip()
                except Exception as e:
                    city = ''
                try:
                    state = address.split(',')[-1].strip().split()[0].replace('Texas','TX')
                except Exception as e:
                    state = address.split('.')[1].strip().split()[0].replace('Texas','TX')
                try:
                    zipcode = address.split(',')[-1].strip().split()[1]
                except Exception as e:
                    zipcode = address.split('.')[1].strip().split()[1]
            # if SubdivisionName =="El Paso County – Painted Desert 1":
            #     street = '13606 Gatton St.'
            #     city = ''
            #     state = 'TX'
            #     zipcode = '79928'

            item = BdxCrawlingItem_subdivision()

            f = open("html/%s.html" % self.builderNumber, "wb")
            f.write(response.body)
            f.close()

            item['sub_Status'] = "Active"
            SubdivisionNumber = int(
                hashlib.md5(bytes(str(SubdivisionName) + str(self.builderNumber), "utf8")).hexdigest(), 16) % (10 ** 30)
            print(SubdivisionNumber)
            community_details['subdivisionname'] = SubdivisionNumber
            item['SubdivisionNumber'] = SubdivisionNumber
            item['BuilderNumber'] = self.builderNumber
            item['SubdivisionName'] = SubdivisionName
            item['BuildOnYourLot'] = 0
            item['OutOfCommunity'] = 0
            item['Street1'] = street
            item['City'] = city
            item['State'] = state

            item['ZIP'] = zipcode
            item['AreaCode'] = "915"
            item['Prefix'] = "540"
            item['Suffix'] = "0101"
            item['Extension'] = ""
            item['Email'] = "info@mycasasdeleon.com"

            item[
                'SubDescription'] = "At Casas de Leon we can deliver to you the pursuit of the dream of American Home ownership and the happiness generations of families all over America have sought and attained."



            item['SubImage'] = "https://www.builtbywinterhomes.com/images/site/banner-communities-subdivisions.jpg"
            item['SubWebsite'] = response.url
            yield item

        except Exception as e:
            print(e)
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
            item['BuildOnYourLot'] = 0
            item['OutOfCommunity'] = 0
            item['Street1'] = "14271 Richard Wiles"
            item['City'] = "El Plso"
            item['State'] = "TX"

            item['ZIP'] = "79983"
            item['AreaCode'] = "915"
            item['Prefix'] = "540"
            item['Suffix'] = "0101"
            item['Extension'] = ""
            item['Email'] = "info@mycasasdeleon.com"

            item[
                'SubDescription'] = ""

            item['SubImage'] = ""
            item['SubWebsite'] = response.url
            yield item

        plan_links = response.xpath('//div[@class="gdlr-blog-thumbnail"]/a/@href').getall()
        for plan_link in plan_links:
            yield scrapy.Request(url=plan_link, callback=self.parse_planlink,
                                 dont_filter=True,meta={'SubdivisionNumber':SubdivisionNumber})

    def parse_planlink(self,response):



        # global bathroom
        global bathroom, garage, bedroom
        status = response.xpath('//p[contains(text(),"Sold Out")]//span/text()').get()
        sta = response.xpath('//div[@class="gdlr-blog-content"]//strong[contains(text(),"Sold Out")]/text()').get()
        s = response.xpath('////div[@class="gdlr-blog-content"]//span[contains(text(),"Sold Out")]/text()/text()').get()
        if status != "Sold Out":
            if sta != "Sold Out":
                if s != "Sold Out":
                    try:
                        subdivisionnumber = response.meta['SubdivisionNumber']
                        if "painted-sky" in response.url:
                            subdivisionnumber = '24080'
                    except Exception as e:
                        subdivisionnumber = self.builderNumber

                    planname = response.xpath('//h1[@class="gdlr-blog-title"]/text()').get()
                    # bedroom = response.xpath('//strong[contains(text(),"Bedroom:")]/following-sibling::text()[1]').get().encode('utf-8').decode('utf-8')
                    feet = response.xpath('//strong[contains(text(),"Square Feet:")]/following-sibling::text()[1]').get()
                    if response.url == "http://mycasasdeleon.com/the-paseos-at-mission-ridge-2-n-3-bilbao/":
                        feet = '1935'
                    description = response.xpath('//div[@class="gdlr-blog-content"]/p/text()').get().replace("one",'1').replace("two",'2').replace("three",'3').replace("four",'4').replace("One",'1').replace("Two",'2').replace("Three",'3').replace("Four",'4').replace(" ½",".5").replace("½",'.5')
                    if description:
                        if "bathrooms" in description:
                            # bathroom = re.findall(r"(\d) bathrooms",description)[0]
                            bathroom = description.split("bathrooms")[0].split()[-1]
                        else:
                            bathroom = 0
                        if "car garage" in description:
                            # garage = re.findall(r"(\d) car garage",description)[0]
                            garage = description.split("car garage")[0].split()[-1]
                        else:
                            garage = 0
                        if "bedrooms" in description:
                            bedroom = description.split("bedrooms")[0].split()[-1]
                        else:
                            bedroom = 0

                    elevation = response.xpath('//div[@class="with-sidebar-wrapper"]//img[contains(@src,"jpg")]/@src').getall()
                    elevation = "|".join(elevation)

                    PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % PlanNumber, "wb")
                    f.write(response.body)
                    f.close()

                    unique = str(PlanNumber) + str(SubdivisionNumber)
                    unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

                    item = BdxCrawlingItem_Plan()
                    item['Type'] = 'SingleFamily'
                    item['PlanNumber'] = PlanNumber
                    item['unique_number'] = unique_number
                    item['SubdivisionNumber'] = subdivisionnumber
                    # if not  item['SubdivisionNumber']:
                    #     item['SubdivisionNumber'] = self.builderNumber
                    item['PlanName'] = planname
                    item['PlanNotAvailable'] = 0
                    item['PlanTypeName'] = 'Single Family'
                    item['BasePrice'] = 0
                    item['BaseSqft'] = feet
                    item['Baths'] = bathroom
                    item['HalfBaths'] = 0
                    item['Bedrooms'] = bedroom
                    item['Garage'] = garage
                    item[
                        'Description'] = 'We are a custom home building company that has been building homes and developing communities in the Athens-Limestone area since 2002.'

                    item['ElevationImage'] = elevation
                    item['PlanWebsite'] = response.url
                    yield item


from scrapy.cmdline import execute
# execute("scrapy crawl casasdeleon".split())

