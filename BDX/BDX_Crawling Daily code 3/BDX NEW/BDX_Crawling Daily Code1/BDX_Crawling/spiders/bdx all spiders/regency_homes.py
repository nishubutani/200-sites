# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from scrapy.utils.response import open_in_browser
from w3lib.http import basic_auth_header
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class RegencyHomesSpider(scrapy.Spider):
    name = 'regency_homes'
    # allowed_domains = ['regencyhomesomaha.com']
    # start_urls = ['https://regencyhomesomaha.com/communities/']

    builderNumber = "247023033297893430770769556238"

    def start_requests(self):
        try:
            self.header = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "max-age=0",
                # "cookie": "humans_21909=1; ubix_gen_session_id=1562825411148X3046625804967500; __utmz=265077516.1560324182.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _fbp=fb.1.1560324191210.670892201; __utma=265077516.1612233427.1560324182.1560765825.1562825411.5; __utmc=265077516; __utmb=265077516.1.10.1562825411",
                # "referer": "https://regencyhomesomaha.com/contact/",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36",
                # "Proxy-Authorization": basic_auth_header('lum-customer-xbyte-zone-zone_us-country-us', '0gi0pioy3oey')
                }
            link = 'https://regencyhomesomaha.com'
            yield scrapy.FormRequest(url=str(link), callback=self.communities_list, headers=self.header)  #
        except Exception as e:
            print(e)

    def communities_list(self,response):

        divs = response.xpath('//div[@class="footer-widget"]')

        for div in divs:
            subdivisonName = div.xpath('.//div/h4/text()').extract_first('')

            subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)

            street = div.xpath('.//div/p[2]/text()[1]').extract_first('')

            add = div.xpath('.//div/p[2]/text()[2]').extract_first('')
            if ',' not in add:
                add = div.xpath('.//div/p[2]/text()[3]').extract_first('')

            city = add.split(",")[0].replace("\n","")
            print(city)

            state = add.split(",")[1].strip().split(" ")[0]
            print(state)

            zip_code = add.split(",")[1].strip().split(" ")[1]
            print(zip_code)


            phone = div.xpath('.//div/div/p[3]/a/text()').extract_first('')
            phone = phone.split("-")


            subimages = ''
            item2 = BdxCrawlingItem_subdivision()
            item2['sub_Status'] = "Active"
            item2['SubdivisionName'] = subdivisonName
            item2['SubdivisionNumber'] = subdivisonNumber
            item2['BuilderNumber'] = self.builderNumber
            item2['BuildOnYourLot'] = 0
            item2['OutOfCommunity'] = 1
            item2['Street1'] = street
            item2['State'] = state
            item2['City'] = city
            item2['ZIP'] = zip_code
            item2['AreaCode'] = phone[0]
            item2['Prefix'] = phone[1]
            item2['Suffix'] = phone[2]
            item2['Extension'] = ""
            item2['Email'] = ""
            item2['SubDescription'] = ''
            item2['SubImage'] = subimages
            item2['SubWebsite'] = response.url
            item2['AmenityType'] = ''
            yield item2

        
        plan_link = 'https://regencyhomesomaha.com/models-and-plans/'
        yield scrapy.Request(url=str(plan_link),callback=self.parse_planlink ,headers=self.header,
                                     )

    def parse_planlink(self,response):
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = "13900 E. Harvard Avenue"
        item['City'] = "Aurora"
        item['State'] = "CO"
        item['ZIP'] = "80014"
        item['AreaCode'] = "303"
        item['Prefix'] = "306"
        item['Suffix'] = "2239"
        item['Extension'] = ""
        item['Email'] = "Regencyhomeswarranty@2-10.com"
        item['SubDescription'] = "To enhance our warranty service we contracted with 2-10 HBW. Your warranty includes 1-Year Workmanship, 2-Year Systems and 10-Year Structural coverage. This service also includes their Front Line Warranty Service Program to process all Regency homeowner warranty requests."
        item['SubImage'] = ""
        item['SubWebsite'] = ""
        item['AmenityType'] = ""
        yield item

        try:
            plan_links = response.xpath('//div[@class="et_pb_text_inner"]/p/a[contains(@href,"-plans")]/@href').extract()
            for link in plan_links:
                url = link
                print(url)
                yield scrapy.Request(url=str(url),callback=self.PlanDataLinks,headers=self.header,meta={'sbdn': item['BuilderNumber']})
        except Exception as e:
            print(e)

    def PlanDataLinks(self,response):
        try:
            plan_links = response.xpath('//div[@class="et_pb_image_container"]/a/@href').extract()
            for link in plan_links:
                yield scrapy.Request(url=str(link),callback=self.plans_details,meta=response.meta)
        except Exception as e:
            print(e)

    def plans_details(self,response):
        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = response.meta['sbdn']
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//h2/text()').extract_first(default='').strip()
        except Exception as e:
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % PlanNumber, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
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
            BasePrice = '0'
        except Exception as e:
            print(e)


        try:
            Baths = str(response.xpath("//strong[contains(text(),'Bathrooms')]/following-sibling::text()").extract_first(default='0').strip()).replace(",", "")
            tmp = re.findall(r"(\d+)", Baths)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            print(e)

        try:
            BaseSqft = response.xpath("//strong[contains(text(),'Square')]/following-sibling::text()").extract_first(default='0').replace(',','')
            BaseSqft = BaseSqft.replace(",","")
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]

        except Exception as e:
            print(e)
        try:
            Bedrooms = response.xpath("//strong[contains(text(),'Bedrooms:')]/following-sibling::text()").extract_first(default='0')
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)

        try:
            Garage = response.xpath("//strong[contains(text(),'Garage')]/following-sibling::text()").extract_first(default='0')
        except Exception as e:
            print(e)

        try:
            Description = ''
        except Exception as e:
            print(e)

        try:
            Image = '|'.join(response.xpath('//figure[@class="fg-item-inner"]/a/@href').extract())
            print(Image)
            ElevationImage = Image
        except Exception as e:
            print(e)

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

        SubdivisionNumber = SubdivisionNumber #if subdivision is there
        #SubdivisionNumber = self.builderNumber #if subdivision is not available
        unique = str(PlanNumber)+str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['Type'] = Type
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
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
    execute("scrapy crawl regency_homes".split())