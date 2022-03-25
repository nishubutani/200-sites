# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import json
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'brannon_built'
    allowed_domains = ['https://www.brannonbuilt.com/']
    start_urls = ['https://www.brannonbuilt.com/communities']

    builderNumber = "63666"

    # ------------------- Creating Communities ---------------------- #

    def parse(self, response):

        divs = response.xpath('//*[@data-testid="mesh-container-content"]/section')
        for div in divs:

            subdivisonName = div.xpath('.//h4[@class="font_4"]//span[@style="letter-spacing:0em"]/text()').extract_first(default="")
            subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)

            f = open("html/%s.html" % subdivisonNumber, "wb")
            f.write(response.body)
            f.close()

            street = div.xpath(".//span[contains(text(),'Location')]/../../../../following-sibling::p/span/span/span/span/text()[1]").extract_first()
            print(street)

            add = div.xpath(".//span[contains(text(),'Location')]/../../../../following-sibling::p/span/span/span/span/text()[2]").extract_first()
            print(add)

            try:
                city = add.split(",")[0].strip()
                print(city)
            except Exception as e:
                print(e)
                city = ''

            try:
                state = add.split(",")[1].strip().split(" ")[0]
                print(state)
                zip_code = add.split(",")[1].strip().split(" ")[1]
                print(zip_code)

            except Exception as e:
                print(e)
                state,zip_code = '',''

            try:
                phon_no = div.xpath(".//span[contains(text(),'Phone Numbe')]/../../../../following-sibling::p/span/span/span/span/text()[1]").extract_first()
                print(phon_no)
            except Exception as e:
                print(e)
                phon_no = ''

            try:
                area = phon_no.split(")")[0].replace("(","").strip()
                print(area)

                Prefix = phon_no.split("-")[0].strip().split(")")[1].strip()
                print(Prefix)

                Suffix = phon_no.split("-")[1].strip()
                print(Suffix)

            except Exception as e:
                print(e)
                area,Prefix,Suffix = '','',''


            try:
                amenities_list = []
                amenities = div.xpath(".//span[contains(text(),'Amenities')]/../../../../following-sibling::ul/li/p/span/span/span//text()[1]").extract()
                for abcd in amenities:
                    abcd = abcd.split(" ")[0].strip()
                    if abcd not in amenities_list:
                        amenities_list.append(abcd)
                print(amenities)

                amenities = "|".join(amenities_list)
            except Exception as e:
                print(e)
                amenities = ''

            try:
                desc = "".join(div.xpath('.//span[@style="letter-spacing:0em"]/text()').extract())
                print(desc)
            except Exception as e:
                print(e)
                desc = ''

            try:
                images = "|".join([ "https://static.wixstatic.com/media/" + str(json.loads(x)['imageData']['uri']) for x in div.xpath('.//*[@data-image-info]/@data-image-info').extract()])
                print(images.split("|"))

            except Exception as e:
                print(e)
                images = ''

            temp = "".join(div.xpath('.//span[@style="letter-spacing:0em"]/text()').extract())
            if 'Sold Out' not in temp:

                item2 = BdxCrawlingItem_subdivision()
                item2['sub_Status'] = "Active"
                item2['SubdivisionName'] = subdivisonName
                item2['SubdivisionNumber'] = subdivisonNumber
                item2['BuilderNumber'] = self.builderNumber
                item2['BuildOnYourLot'] = 0
                item2['OutOfCommunity'] = 1
                item2['Street1'] = street
                item2['City'] = city
                item2['State'] = state
                item2['ZIP'] = zip_code
                item2['AreaCode'] = area
                item2['Prefix'] = Prefix
                item2['Suffix'] = Suffix
                item2['Extension'] = ""
                item2['Email'] = ''
                item2['SubDescription'] = desc
                item2['SubImage'] = images
                item2['SubWebsite'] = response.url
                item2['AmenityType'] = amenities
                yield item2

                link = 'https://www.brannonbuilt.com/models-plans'
                yield scrapy.FormRequest(url=link, callback=self.parse3, dont_filter=True,
                                         meta={'subdivisonNumber': subdivisonNumber})

            else:
                pass


            # #----------------------- creating fake community ------------------------------------------#
            #
            # item2 = BdxCrawlingItem_subdivision()
            # item2['sub_Status'] = "Active"
            # item2['SubdivisionName'] = "No Sub Division"
            # item2['SubdivisionNumber'] = self.builderNumber
            # item2['BuilderNumber'] = self.builderNumber
            # item2['BuildOnYourLot'] = 0
            # item2['OutOfCommunity'] = 0
            # item2['Street1'] = '7165 Getwell Road - Building E'
            # item2['City'] = 'Southaven'
            # item2['State'] = 'MS'
            # item2['ZIP'] = '38672'
            # item2['AreaCode'] = '662'
            # item2['Prefix'] = '253'
            # item2['Suffix'] = '0114'
            # item2['Extension'] = ""
            # item2['Email'] = ''
            # item2['SubDescription'] = "Brannon Builders has been building quality brand new homes in the Mid-South for over 40 years. They have built a reputation for building quality homes in every price range. Brannon Builders focuses on new homes in the areas of North Mississippi including DeSoto County, Southaven, Olive Branch, Hernando, and Walls.With over three decades of home building and construction management experience, you can choose Brannon Builders with confidence. Residential or commercial, we stake our name and reputation on our work – everyday, on every brand new home!  Our offices are located minutes south of Memphis, Tennessee in Southaven, Mississippi."
            # item2['SubImage'] = 'https://static.wixstatic.com/media/e9a49f_087d13ee9ec34131a3a5e5ffb8708ad6~mv2.jpg|https://static.wixstatic.com/media/e9a49f_351abedb96df4d6d82bb908e9229854f~mv2_d_3024_2016_s_2.jpg|https://static.wixstatic.com/media/e9a49f_d9b1da1776384b2fa4d3926bd06002da~mv2_d_3024_2016_s_2.jpg|https://static.wixstatic.com/media/e9a49f_c99177af28c6484aa6a566b002a58de3~mv2_d_3024_2016_s_2.jpg|https://static.wixstatic.com/media/e9a49f_5a599e1e43c04bd88e88f97c54c78fd9~mv2.jpg|https://static.wixstatic.com/media/e9a49f_ee87465a8fd94d25a1bb4a7f4d183e7b~mv2.jpg'
            # item2['SubWebsite'] = response.url
            # item2['AmenityType'] = ''
            # yield item2




    def parse3(self,response):
        subdivisonNumber = response.meta['subdivisonNumber']
        divs = response.xpath('//*[contains(text(), "bedrooms/")]/..')
        for div in divs:
            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                PlanName = div.xpath('.//span[@style="font-family:adobe-caslon-w01-smbd,serif"]/text()').get()
            except Exception as e:
                PlanName = ''
                print(e)

            try:
                PlanNumber = int(hashlib.md5(bytes(PlanName + response.url, "utf8")).hexdigest(), 16) % (
                        10 ** 30)
            except Exception as e:
                PlanNumber = ''
                print(e)

            try:
                SubdivisionNumber = self.builderNumber
                print(SubdivisionNumber)
            except Exception as e:
                SubdivisionNumber = ''
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
                BasePrice = 0
            except Exception as e:
                print(e)

            try:
                sqft = div.xpath('.//h1[@style="font-size:28px"]/text()').extract_first('')
                sqft = sqft.split("|")[1]
                sqft = sqft.replace(',', '').strip()
                BaseSqft = re.findall(r"(\d+)", sqft)[0]

            except Exception as e:
                print(e)
                BaseSqft = ''

            try:
                bath = div.xpath('.//h1[@style="font-size:28px"]/text()').extract_first()
                bath = bath.split("/")[1].split("|")[0]
                # if '-' in bath:
                #     bath = bath.split("-")[1]
                tmp = re.findall(r"(\d+)", bath)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                print(e)

            try:
                Bedrooms = div.xpath('.//h1[@style="font-size:28px"]/text()').extract_first()
                Bedrooms = Bedrooms.split("/")[0]
                Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            except Exception as e:
                print(e)



            try:
                Description = div.xpath('.//following-sibling::div/p/span/span/span/text()').extract_first('')
            except Exception as e:
                print(e)

            try:
                Garage = re.findall(r"(\d*[three]*[four]*[two]*[double]*)[ ]*[-]*garage", Description)[0]
                Garage = Garage.replace("three", "3").replace("four", "4").replace("two", "2").replace("double", "2")
                Garage = re.findall(r"(\d+)", Garage)[0]
            except Exception as e:
                print(e)
                Garage = 0

            try:

                images = ["https://static.wixstatic.com/media/" + x for x in re.findall(r'"uri":"(.*?)"', requests.get(response.xpath('//link[contains(@id,"feature")]/@href')[-1].get()).text)]
                print(len(images))

                if PlanName == 'The Avery':
                    images = images[0:2]
                elif PlanName == 'The Charleston':
                    images = images[2:8]
                elif PlanName == 'The Clayton':
                    images = images[8:10]
                elif PlanName == 'The Franklin':
                    images = images[10:24]
                elif PlanName == 'The Kirkland':
                    images = images[24:41]
                elif PlanName == 'The Lindsey':
                    # images = images[41:43]
                    images = ['https://static.wixstatic.com/media/e9a49f_44938b3b2b6a48c69211fa34bb4bd868~mv2.jpg', 'https://static.wixstatic.com/media/e9a49f_2a52d37820b3469c90f5c3b89b1c4989~mv2.jpg']
                    # print(images)
                elif PlanName == 'The Oakland':
                    images = images[43:65]
                # elif PlanName == 'The Sterling':
                else:
                    images = images[65:73]

                images = "|".join(images)



            except Exception as e:
                print(e)

            try:
                PlanWebsite = response.url
            except Exception as e:
                print(e)

                # ----------------------- Don't change anything here --------------
            unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
            item = BdxCrawlingItem_Plan()
            item['Type'] = Type
            item['PlanNumber'] = PlanNumber
            item['unique_number'] = unique_number  # < -------- Changes here
            # item['SubdivisionNumber'] = self.builderNumber
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
            item['ElevationImage'] = images
            item['PlanWebsite'] = PlanWebsite
            yield item





    # --------------------------------------------------------------------- #

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl brannon_built'.split())