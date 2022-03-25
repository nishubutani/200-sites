# -*- coding: utf-8 -*-
import hashlib
import re
# import json
import scrapy
# from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
# import requests
# from scrapy.http import HtmlResponse


class brookstonepropertySpider(scrapy.Spider):
    name = 'c3ci'
    # allowed_domains = []
    start_urls = ['https://c3ci.com/']

    builderNumber = 63705

    def parse(self,response):
        links= response.xpath("//a[contains(text(),'COMMUNITIES')]/following-sibling::ul/li/a/@href").extract()
        for link in links:
            yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)

    def parse2(self,response):


        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()


        try:
            add1 = response.xpath("//h2/span/text()").extract_first('')
            print(add1)

            city = add1.split(",")[0]
            state = add1.split(",")[1].strip()

        except Exception as E:
            print(E)
            city,state = '',''

        try:
            desc = response.xpath('//div[@class="et_pb_module et_pb_text et_pb_text_2  et_pb_text_align_left et_pb_bg_layout_light"]//div[@class="et_pb_text_inner"]//text()').extract()
            if desc != []:
                desc = "".join(desc)
            print(desc)
        except Exception as e:
            print(e)

        try:
            comm_name = response.xpath("//h1/text()").extract_first('')
            print(comm_name)
        except Exception as e:
            print(e)

        subdivisonNumber = int(hashlib.md5(bytes(comm_name, "utf8")).hexdigest(), 16) % (10 ** 30)


        try:
            image = response.xpath("//a[contains(@href,'Screen-Shot')]/@href").extract_first('')
            print(image)
            if image == '':
                image = 'https://c3ci.com/wp-content/uploads/2020/07/07-IMG_0493_4_5-scaled.jpg'
        except Exception as e:
            print(e)

        try:

            zzz = "".join(response.xpath('//*[@class="et_pb_section et_pb_section_2 et_pb_with_background et_section_regular"]//*[contains(@class,"et_pb_css_mix_blend_mode_passthrough")]//h3//text()').extract())
            zip_code  = re.findall(r'\d{5}',zzz)[0]
            print(zip_code)

            # zip_code = response.xpath("//h3/text()").extract_first('')
            # print(zip_code)
            # zip_code = zip_code.split(",")[-1]
            # print(zip_code)
            zip_code = zip_code.strip()
        except Exception as e:
            print(e)



        try:
            aminity = ''.join(response.xpath('//div[@class="et_pb_module et_pb_text et_pb_text_2  et_pb_text_align_left et_pb_bg_layout_light"]//div[@class="et_pb_text_inner"]//text()').getall())
            aminity = aminity.title()
        except Exception as e:
            print(e)
        a = []
        amenity_list = ["Pool", "Playground", "GolfCourse", "Tennis", "Soccer", "Volleyball", "Basketball",
                        "Baseball", "Views", "Lake", "Pond", "Marina", "Beach", "WaterfrontLots", "Park",
                        "Trails", "Greenbelt", "Clubhouse", "CommunityCenter"]
        for i in amenity_list:
            # print(i)
            if i in aminity:
                # print(i)
                a.append(i)
        ab = '|'.join(a)


        if comm_name != 'THE GROVES':
            item = BdxCrawlingItem_subdivision()
            item['sub_Status'] = "Active"
            item['SubdivisionNumber'] = subdivisonNumber
            item['BuilderNumber'] = self.builderNumber
            item['SubdivisionName'] = comm_name
            item['BuildOnYourLot'] = 0
            item['OutOfCommunity'] = 1
            item['Street1'] = ""
            item['City'] = city
            item['State'] = state
            item['ZIP'] = zip_code
            item['AreaCode'] = "479"
            item['Prefix'] = "717"
            item['Suffix'] = "2282"
            item['Extension'] = ""
            item['Email'] = 'kburks@c3ci.com'  # From Contact Us page
            item['SubDescription'] = desc
            item['SubImage'] = image
            item['SubWebsite'] = response.url
            item['AmenityType'] = ab
            yield item


            homes = response.xpath('//*[@class="et_pb_section et_pb_section_2 et_pb_with_background et_section_regular"]//*[contains(@class,"et_pb_css_mix_blend_mode_passthrough")]')

            for check in homes:
                check1 = check.xpath(".//h3//text()|//p/text()").extract_first('')

                if 'sold' in check1 or "UNDER CONTRACT" in check1:
                    if 'sold' in check1:
                        pass
                    # if  "sold" or "UNDER CONTRACT:" in " ".join(check.xpath('.//h3//text()').getall()).strip().lower() or "" == " ".join(check.xpath('.//h3//text()').getall()).strip().lower():
                    # pass
                else:
                    if 'sold' in check1:
                        pass
                    else:
                        unique = str("Plan Unknown") + str(subdivisonNumber)
                        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                        item = BdxCrawlingItem_Plan()
                        item['unique_number'] = unique_number
                        item['Type'] = "SingleFamily"
                        item['PlanNumber'] = self.builderNumber
                        item['SubdivisionNumber'] = subdivisonNumber
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

                        item = BdxCrawlingItem_Spec()
                        print(check.xpath('.//h3/text()').get())
                        print(check.xpath('.//p/text()').get())
                        item['PlanNumber'] = unique_number
                        item['SpecStreet1'] = " ".join(check.xpath('.//h3//text()').getall()).split(",")[0].strip()
                        if 'SOLD' not in item['SpecStreet1']:
                            if 'UNDER CONTRACT' not in item['SpecStreet1']:
                                item['SpecStreet1'] = item['SpecStreet1'].replace('UNDER CONTRACT:', '')
                                item['SpecCity'] = 'Bentonville' if "Bentonville" in item['SpecStreet1'] else " ".join(check.xpath('.//h3//text()').getall()).replace('UNDER CONTRACT:', '').split(",")[1].strip()
                                item['SpecStreet1'] = item['SpecStreet1'].replace("Bentonville", "").strip()
                                item['SpecState'] = " ".join(check.xpath('.//h3//text()').getall()).replace('UNDER CONTRACT:', '').split(",")[-1].strip().split()[0]
                                # item['SpecZIP'] = '00000' if "AR" == " ".join(check.xpath('.//h3//text()').getall()).replace('UNDER CONTRACT:', '').split()[-1].strip() else " ".join(check.xpath('.//h3//text()').getall()).replace('UNDER CONTRACT:', '').split()[-1].strip()
                                item['SpecZIP'] = zip_code
                                item['SpecNumber'] = int(hashlib.md5(bytes(item['SpecStreet1'], "utf8")).hexdigest(), 16) % (10 ** 30)
                                item['SpecCountry'] = "USA"
                                item['SpecPrice'] = re.findall(r'\$[ ]*(\d*[,]*\d+)', check.xpath('.//p/text()').get())[0].replace(",", "")
                                item['SpecSqft'] = int(re.findall(r'(\d*[,]*\d+)[ ]*[sS][qQ][ ]*[Ff][tT]', check.xpath('.//p/text()').get())[0].replace(",", ""))
                                item['SpecBaths'] = re.findall(r'(\d*[.]*\d+)[ ]*[bB][Aa][tT][Hh]', check.xpath('.//p/text()').get())[0]
                                if len(item['SpecBaths']) > 1:
                                    item['SpecHalfBaths'] = 1
                                    item['SpecBaths'] = item['SpecBaths'][0]
                                else:
                                    item['SpecHalfBaths'] = 0
                                    item['SpecBaths'] = item['SpecBaths'][0]
                                item['SpecBedrooms'] = re.findall(r'(\d+)[ ]*[bB][eE][dD]', check.xpath('.//p/text()').get())[0]
                                item['MasterBedLocation'] = 'Down'
                                item['SpecGarage'] = 0
                                item['SpecDescription'] = ''
                                item['SpecElevationImage'] = check.xpath('.//img/@src').get()
                                item['SpecWebsite'] = response.url
                                yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    # execute("scrapy crawl {}".format(brookstonepropertySpider.name).split())
    execute("scrapy crawl c3ci".split())
    # execute("scrapy crawl allamericandreamhomes".split())
