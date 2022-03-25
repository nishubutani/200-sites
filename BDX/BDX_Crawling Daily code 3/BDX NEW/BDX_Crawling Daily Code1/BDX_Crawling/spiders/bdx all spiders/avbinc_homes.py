# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'avbinc_homes'
    allowed_domains = ['https://www.avbinc.com/']
    # start_urls = ['https://www.avbinc.com/homes-and-communities/build-a-home/#gallery']
    start_urls = ['https://www.avbinc.com/homes-and-communities/communities/']

    builderNumber = "62834"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        # f = open("html/%s.html" % self.builderNumber, "wb")
        # f.write(response.body)
        # f.close()
        #
        #
        #
        # images = ''
        # image = response.xpath('//img//@data-src').extract()[0:10]
        # for i in image:
        #     images = images + i + '|'
        # images = images.strip('|')
        #
        # item = BdxCrawlingItem_subdivision()
        # item['sub_Status'] = "Active"
        # item['SubdivisionNumber'] = ''
        # item['BuilderNumber'] = self.builderNumber
        # item['SubdivisionName'] = "No Sub Division"
        # item['BuildOnYourLot'] = 0
        # item['OutOfCommunity'] = 0
        # item['Street1'] = '4200 W. Centre Av'
        # item['City'] = 'Portage'
        # item['State'] = 'MI'
        # item['ZIP'] = '49024'
        # item['AreaCode'] = '269'
        # item['Prefix'] ='323'
        # item['Suffix'] = '2022'
        # item['Extension'] = ""
        # item['Email'] = 'erininger@avbinc.com'
        # item['SubDescription'] = 'AVB was formed in 1981 by Joe Gesmundo and Daryl Rynd, who shared a passion for creating great places to live and work. Together, AVB’s founding principals collaborated on the Kalamazoo area’s premier master-planned community, Woodbridge Hills. This visionary mixed-use community includes a retail center, medical and surgical buildings, office buildings, luxury condominiums, upscale private residences, and a private golf course. Today, AVB is a leading regional construction and development firm, dedicated to building great homes, buildings, and developments.'
        # item['SubImage'] = images
        # item['SubWebsite'] = response.url
        # item['AmenityType'] = ''
        # yield item
        #
        # link = 'https://www.avbinc.com/homes-and-communities/available-homes/'

        links = response.xpath("//span/following-sibling::a[contains(@href,'/homes-and-communities/communities')]/@href").extract()
        for link in links:
            link = 'https://www.avbinc.com' + link
            print(link)
            yield scrapy.FormRequest(url=link, callback=self.communitu, dont_filter=True)

    def communitu(self,response):

        subdivisonName = response.xpath('//h1/text()').extract_first(default="")
        subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)

        f = open("html/%s.html" % subdivisonNumber, "wb")
        f.write(response.body)
        f.close()

        try:
            aminity = ''.join(response.xpath(
                '//div[@class="sqs-block-content"]/h3/..//p[@style="white-space:pre-wrap;"]/text()').getall())
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

        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionName'] = subdivisonName
        item2['SubdivisionNumber'] = subdivisonNumber
        item2['BuilderNumber'] = self.builderNumber
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 1
        item2['AreaCode'] = ''
        item2['Prefix'] = ''
        item2['Suffix'] = ''
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = response.xpath('//div[@class="sqs-block-content"]/h3/..//p[@style="white-space:pre-wrap;"]/text()').extract_first('')
        item2['SubImage'] = response.xpath('//a[@id="first-in-tour"]/img/@src').extract_first('')
        item2['SubWebsite'] = response.url
        item2['AmenityType'] = ab


        link = response.xpath("//a[contains(text(),'Map & Directions')]/@href").extract_first('')
        # yield scrapy.FormRequest(url=link,callback=self.add_detail,dont_filter=True,meta={'item2',item2})

        response = requests.request("GET", url=link)
        response = HtmlResponse(url=link, body=response.content)


        try:
            full = response.text.split(r'\"],null,null,null,null,null,1,null,')[-1].split(r'\",\"')[1].split(
                r'\",null,[null,null,')[0].split(r'\",[[', 1)[0].split(r'\",[\"')[-1]
            print(full)
            if "null" in full:
                try:
                    full = response.text.split(r'[[[1,[[\"')[1].split(r'\"]]],')[0]
                    # print(full)
                    if "null" in full:
                        full = response.text.split.split('],null,0],[null,["')[-1](r'"Google Maps",')[0]
                        print(full)
                    if "null" in full:
                        full = response.text.split(r'\n,null,null,0]\n,[[\"')[-1]
                        print(full)
                except:
                    # full = response.text.split.split('],null,0],[null,["')[-1](r'"Google Maps",')[0]
                    full = response.text.split('],null,0],[null,["')[-1].split(r'"Google Maps",')[0].split('",null')[
                        0].strip()
                    # print(full)
            else:
                full = full

        except:
            full = ','.join(
                response.text.split(',null,null,null,null,null,null,null,null,null,null,null,null,null,1]],["', )[
                    1].split('",null,[null,null,')[0].split(",")[1:])
            print(full)
            # print(response.text)

        if "null" in full:
            full = ''
            print("hardik might be there is no address on given link or code requir.... few changes please check",)
        else:
            full = full
            print(full)


        try:
            street1 = full.split(",")[0].strip()
            print(street1)
        except Exception as e:
            print(e)
            street1 =''

        try:
            city = full.split(",")[1].strip()
            print(city)
        except Exception as e:
            print(e)
            city = ''

        try:
            state = full.split(",")[2].strip()
            print(state)
            state = state.split(" ")[0]
            print(state)
        except Exception as e:
            print(e)
            state = ''

        try:
            zip_code = full.split(",")[2].strip()
            print(zip_code)
            zip_code = zip_code.split(" ")[1]
            print(zip_code)
        except Exception as e:
            print(e)
            zip_code = ''

        if zip_code != '':
            item2['Street1'] = street1
            item2['City'] = city
            item2['State'] = state
            item2['ZIP'] = zip_code
            yield item2


        link = 'https://www.avbinc.com/homes-and-communities/available-homes/'
        yield scrapy.FormRequest(url=link, callback=self.parse2, dont_filter=True,meta={'subdivisonNumber':subdivisonNumber})


    def parse2(self, response):
        subdivisonNumber = response.meta['subdivisonNumber']
        links = response.xpath('//div[@class="collectionList_itemList_item_text"]/a/@href').extract()
        for link in links:
            link = 'https://www.avbinc.com' + link
            yield scrapy.FormRequest(url=link, callback=self.parse3, dont_filter=True,meta={'subdivisonNumber':subdivisonNumber})
            # yield scrapy.FormRequest(url='https://www.avbinc.com/homes-and-communities/available-homes/constructionnewhomes8094turningstonetrail/', callback=self.parse3, dont_filter=True,meta={'subdivisonNumber':subdivisonNumber})

    def parse3(self, response):
        subdivisonNumber = response.meta['subdivisonNumber']
        ab = response.xpath("//*[contains(text(),'Under Construction')]").extract_first('')
        if ab == '':

            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                PlanName = response.xpath('//h1/text()').get()
            except Exception as e:
                PlanName = ''
                print(e)

            try:
                PlanNumber = int(hashlib.md5(bytes(PlanName + response.url, "utf8")).hexdigest(), 16) % (
                        10 ** 30)
            except Exception as e:
                PlanNumber = ''
                print(e)

            # try:
            #     SubdivisionNumber = self.builderNumber
            #     print(SubdivisionNumber)
            # except Exception as e:
            #     SubdivisionNumber = ''
            #     print(e)

            try:
                PlanNotAvailable = 0
            except Exception as e:
                print(e)

            try:
                PlanTypeName = 'Single Family'
            except Exception as e:
                print(e)


            try:
                sqft = response.xpath("//*[contains(text(),'sq. ft')]/text()").extract_first('')
                sqft = sqft.replace(",","")
                BaseSqft = re.findall(r"(\d+)", sqft)[0]

            except Exception as e:
                print(e)
                BaseSqft=''

            try:

                bath = response.xpath("//*[contains(text(),' Bath')]/text()").extract_first('')
                # bath = bath.split("/")[1].split("/")[0].strip()
                tmp = re.findall(r"(\d+)", bath)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                print(e)

            try:
                Bedrooms = response.xpath("//*[contains(text(),' Bedroom')]/text()").extract_first('')
                Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            except Exception as e:
                print(e)

            try:
                price = response.xpath('//span[contains(text(),"$")]/text()').extract_first('')
                price = price.replace(",","")
                price = re.findall(r"(\d+)", price)[0]

            except Exception as e:
                print(e)
                price = '0'

            try:
                BasePrice = price
            except Exception as e:
                print(e)

            try:
                # Garage = response.xpath('//div[@itemprop="description"]/p/text()[3]').extract_first('')
                # Garage = re.findall(r"(\d*[three]*[four]*[two]*)[-]*[ ]*car garage", response.text.lower())[0]
                Garage = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*car garage", response.text.lower())[0]
                Garage = Garage.replace("three", "3").replace("four", "4").replace("two", "2").replace("double","2").replace("triple","3")
                Garage = re.findall(r"(\d+)", Garage)[0]
            except Exception as e:
                print(e)
                Garage = 0

            try:

                desc = "".join(response.xpath('//p/strong/../text()').extract()[0:2])
                if desc == [] or desc == '\n':
                    desc = 'AVB was formed in 1981 by Joe Gesmundo and Daryl Rynd, who shared a passion for creating great places to live and work. Together, AVB’s founding principals collaborated on the Kalamazoo area’s premier master-planned community, Woodbridge Hills. This visionary mixed-use community includes a retail center, medical and surgical buildings, office buildings, luxury condominiums, upscale private residences, and a private golf course. Today, AVB is a leading regional construction and development firm, dedicated to building great homes, buildings, and developments.'

                Description = desc
            except Exception as e:
                print(e)

            try:
                # img1 = response.xpath('//span[@class="et_pb_image_wrap "]/img/@src').extract_first('')
                images = []
                imagedata = response.xpath('//img//@data-src').getall()
                for id in imagedata:
                    id = id
                    images.append(id)
                ElevationImage = "|".join(images)
                ElevationImage = ElevationImage
            except Exception as e:
                print(e)


            try:
                PlanWebsite = response.url
            except Exception as e:
                print(e)

                # ----------------------- Don't change anything here --------------
            unique = str(PlanNumber) + str(subdivisonNumber)  # < -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
            item = BdxCrawlingItem_Plan()
            item['Type'] = Type
            item['PlanNumber'] = PlanNumber
            item['unique_number'] = unique_number  # < -------- Changes here
            item['SubdivisionNumber'] = subdivisonNumber
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
        else:
            pass



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl avbinc_homes'.split())