


# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'buildingalaska'
    allowed_domains = ['https://buildingalaska.com/']
    start_urls = ['https://buildingalaska.com/']

    builderNumber = "63686"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()


        # images = ''
        # image = response.xpath('//div[@class="widget animated fadeInUpShort"]//img[@class="lazy loaded"]').extract()
        # for i in image:
        #     images = images + i + '|'
        # images = images.strip('|')

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '9101 Mile 6 Rd'
        item['City'] = 'Palmer'
        item['State'] = 'AK'
        item['ZIP'] = '99645'
        item['AreaCode'] = '907'
        item['Prefix'] ='707'
        item['Suffix'] = '6326'
        item['Extension'] = ""
        item['Email'] = 'rose.wmconstructionllc@gmail.com'
        item['SubDescription'] = 'WM Construction is your one-stop source for new home construction, multi-family dwellings, commercial buildings, remodels and additions in the Mat-Su Valley. Mike Thompson,  owner of WM Construction, is an exceptional builder with decades of experience. Mike and his team take great pride in building quality houses in the state that they loves. We appreciate working with the communities we’ve grown to adore and we strive to use Alaskan small business as our valued partners and vendors'
        item['SubImage'] = 'https://buildingalaska.com/wp-content/uploads/2019/11/Exterior-Front-ELKO8845-1.jpg|https://buildingalaska.com/wp-content/uploads/2019/11/Exterior-Left-Side-DSC-4620-1.jpg|https://buildingalaska.com/wp-content/uploads/2019/11/Exterior-MAX64422-1.jpg|https://buildingalaska.com/wp-content/uploads/2019/12/house-construction-1.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item


        link = 'https://buildingalaska.com/floor-plans/'
        yield scrapy.FormRequest(url=link,callback=self.parse3,dont_filter=True)


    def parse3(self,response):

        divs = response.xpath('//*[contains(@class,"et_section_regular")][@id]')
        print(len(divs))
        # print(response.text)
        divssss = response.xpath('//div[@class="el_modal_popup_trigger_element_wrapper"]')[0:16]
        print(len(divssss))

        for div,divss in zip(divs,divssss):

            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                PlanName = div.xpath('.//div[@class="et_pb_text_inner"]/h3/text()').get()
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
                sqft = div.xpath('.//div[@class="et_pb_text_inner"]/h4/text()').extract_first('')
                sqft = sqft.split("|")[0]
                sqft = sqft.replace(',', '').strip()
                if '.' in sqft:
                    sqft = sqft.split(".")[0]
                BaseSqft = re.findall(r"(\d+)", sqft)[0]

            except Exception as e:
                print(e)
                BaseSqft = ''

            try:
                bath = div.xpath('.//div[@class="et_pb_text_inner"]/h4/text()').extract_first('')
                bath = bath.split("|")[2]
                if '-' in bath:
                    bath = bath.split("-")[1]
                tmp = re.findall(r"(\d+)", bath)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                print(e)

            try:
                Bedrooms = div.xpath('.//div[@class="et_pb_text_inner"]/h4/text()').extract_first('')
                Bedrooms = Bedrooms.split("|")[1]
                Bedrooms = Bedrooms.split("|")[0]
                if '-' in Bedrooms:
                    Bedrooms = Bedrooms.split("-")[1]
                # Bedrooms = Bedrooms.split("|")[1].split("|")[0]
                Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            except Exception as e:
                print(e)

            try:
                if PlanName == 'Aurora Home Description':
                    Garage = "".join(div.xpath('.//div[@class="et_pb_text_inner"]/p/text()').extract())
                    Garage = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*car garage", Garage.lower())[1]
                else:
                    Garage = "".join(div.xpath('.//div[@class="et_pb_text_inner"]/p/text()').extract())
                    Garage = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*car garage", Garage.lower())[0]
                Garage = Garage.replace("three","3").replace("four","4").replace("two","2")
                Garage = re.findall(r"(\d+)", Garage)[0]
            except Exception as e:
                print(e)
                Garage = 0


            try:
                Description = div.xpath('.//div[@class="et_pb_text_inner"]/p/text()[1]').extract_first()
                Description = Description.encode('ascii', 'ignore').decode('utf8')
            except Exception as e:
                print(e)
                Description = ''


            try:

                images1 = div.xpath('.//span[@class="et_pb_image_wrap "]/img[@loading="lazy"]/@src').extract()
                images2 = divss.xpath('./img/@src').extract()
                print(images1)
                images = []
                for id in images1:
                    id = id
                    images.append(id)
                ElevationImage = images

                if images2 != '':
                    ElevationImage.extend(images2)

                print(ElevationImage)
            except Exception as e:
                print(e)

            try:
                PlanWebsite = response.url
            except Exception as e:
                print(e)

                # ----------------------- Don't change anything here --------------
            unique = str(PlanNumber) + str(SubdivisionNumber) + str(Baths) + str(Bedrooms) #< -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
            item = BdxCrawlingItem_Plan()
            item['Type'] = Type
            item['PlanNumber'] = PlanNumber
            item['unique_number'] = unique_number  # < -------- Changes here
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
            item['ElevationImage'] = "|".join(ElevationImage)
            item['PlanWebsite'] = PlanWebsite
            yield item




        # --------------------------------------------------------------------- #


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl buildingalaska'.split())