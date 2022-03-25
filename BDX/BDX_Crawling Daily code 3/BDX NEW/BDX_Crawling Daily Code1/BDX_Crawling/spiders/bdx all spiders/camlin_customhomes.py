# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class camlin_customhomes(scrapy.Spider):
    name = 'camlin_customhomes'
    # allowed_domains = ['https://www.camlincustomhomes.com']
    # start_urls = ['https://www.camlincustomhomes.com/communities/waters-edge-at-sanctuary-cove']
    start_urls = ['https://www.camlincustomhomes.com/communities']

    builderNumber = "63716"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()


        links = response.xpath('//a[@class="button block"]/@href').extract()
        for link1 in links:
            link = 'https://www.camlincustomhomes.com' + link1
            print(link)
            yield scrapy.Request(url=link,callback=self.parse2,dont_filter=True)

    def parse2(self,response):

        subdivisonName = response.xpath('//h1/text()').extract_first(default="")

        addres = response.xpath("//img[contains(@src,'googleapis')]/@src").extract_first('')
        if addres != '':

            addres = addres.split("staticmap?center=")[1]
            addres = addres.split("&z")[0]
            # print(addres)


            try:
                street = addres.split(",")[0].replace("\n","")
                # print(street)
            except Exception as e:
                print(e)
                street = ''


            try:

                coma =  addres.split(",")
                coma = len(coma)


                if coma != 3:
                    city  = addres.split(",")[0]
                    city = city.split(" ")[-1].strip()
                    # print(city)
                else:
                    city = addres.split(",")[1].strip()
                    # print(city)
            except Exception as e:
                print(e)
                city  = ''



            try:
                state = addres.split(",")[-1].strip()
                state = state.split(" ")[0].replace("Florida","FL")
                # print(state)
            except Exception as e:
                print(e)

            try:
                zip_code = addres.split(",")[-1].strip()
                zip_code = zip_code.split(" ")[1].strip()
                # print(zip_code)

                # if zip_code == 'Florida':
                #     zip_code = '00000'
            except Exception as e:
                print(e)
                zip_code = '00000'

                if subdivisonName == 'Communities - Redfish Cove':
                    zip_code = '34221'

            try:
                desc = "".join(response.xpath("//span[contains(text(),'Description')]/../p/text()").extract())
                # print(desc)
            except Exception as e:
                print(e)
                desc = ''



            subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)

            f = open("html/%s.html" % subdivisonNumber, "wb")
            f.write(response.body)
            f.close()


            a = []
            # aminity = ''.join(response.xpath('//*[@class="ll-features-content__half right col-md-1of2"]/ul[1]/li/text()').extract())
            try:
                aminity = ''.join(response.xpath(
                    '//p/text()').extract())
            except Exception as e:
                print(e)

            amenity_list = ["Pool", "Playground", "GolfCourse", "Tennis", "Soccer", "Volleyball", "Basketball",
                            "Baseball", "Views", "Lake", "Pond", "Marina", "Beach", "WaterfrontLots", "Park",
                            "Trails", "Greenbelt", "Clubhouse", "CommunityCenter"]
            for i in amenity_list:
                if i in aminity:
                    a.append(i)
            ab = '|'.join(a)



            try:
                images = []
                image = response.xpath("//div/a[contains(@href,'/content')]/@href").extract()[1:]
                for i in image:
                    i = 'https://www.camlincustomhomes.com' + i
                    print(i)
                    if '.pdf' not in i:
                        if 'legendsbay' not in i:
                            images.append(i)
                # images = "|".join([ "https://static.wixstatic.com/media/" + str(json.loads(x)['imageData']['uri']) for x in div.xpath('.//*[@data-image-info]/@data-image-info').extract()])
                # print(images.split("|"))

                images = "|".join(images)

            except Exception as e:
                print(e)
                images = ''

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
            item2['AreaCode'] = '941'
            item2['Prefix'] = '748'
            item2['Suffix'] = '1622'
            item2['Extension'] = ""
            item2['Email'] = 'sales.camlin@gmail.com'
            item2['SubDescription'] = desc
            item2['SubImage'] = images
            item2['SubWebsite'] = response.url
            item2['AmenityType'] = ab
            yield item2


            link = 'https://www.camlincustomhomes.com/gallery'
            yield scrapy.FormRequest(url=link,callback=self.parse3,dont_filter=True , meta={'subdivisonNumber':subdivisonNumber})

    def parse3(self,response):
        subdivisonNumber = response.meta['subdivisonNumber']
        links = response.xpath('//div[@class="block square"]/div/a/@href').extract()
        for link in links:
            link = 'https://www.camlincustomhomes.com' + link
            yield scrapy.FormRequest(url=link,callback=self.plan,dont_filter=True,meta={'subdivisonNumber':subdivisonNumber})


    def plan(self,response):
        SubdivisionNumber = response.meta['subdivisonNumber']
        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//h2/text()').get()
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
            BasePrice = 0
        except Exception as e:
            print(e)

        try:

            sqft = response.xpath("//span[contains(text(),'Features')]/following-sibling::p/text()").extract_first('')
            if '–' in sqft:
                sqft = sqft.split("–")[0]
            sqft = sqft.replace(',', '').strip()
            if '.' in sqft:
                sqft = sqft.split(".")[0]
            BaseSqft = re.findall(r"(\d+)", sqft)[0]

        except Exception as e:
            print(e)
            BaseSqft = ''

        try:

            bath = response.xpath("//span[contains(text(),'Features')]/following-sibling::p/text()").extract_first()
            bath = bath.split(",")[2]
            print(bath)
            tmp = re.findall(r"(\d+)", bath)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            print(e)

        try:

            Bedrooms = response.xpath("//span[contains(text(),'Features')]/following-sibling::p/text()").extract_first()
            Bedrooms = Bedrooms.split(",")[1]
            Bedrooms = Bedrooms.split("–")[2]

            # Bedrooms = Bedrooms.split("|")[1].split("|")[0]
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)

        try:
            # Garage = response.xpath('//div[@itemprop="description"]/p/text()[3]').extract_first('')
            # Garage = re.findall(r"(\d*[three]*[four]*[two]*)[-]*[ ]*car garage", response.text.lower())[0]
            Garage = Garage = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*car garage", response.text.lower())[0]
            Garage = Garage.replace("three", "3").replace("four", "4").replace("two", "2")
            Garage = re.findall(r"(\d+)", Garage)[0]
        except Exception as e:
            print(e)
            Garage = 0

        try:
            Description = response.xpath("//span[contains(text(),'About This Home')]/../p/text()").extract_first('')
        except Exception as e:
            print(e)
            Description = ''



        price = 0

        try:

            images1 = response.xpath('//div[@class="block square"]/div/a/@href').extract()
            images2 = response.xpath('//div[@class="entry-image relative"]/a/img/@data-src').extract_first('')
            if ',' in images2:
                images2 = images2.split(",")[0]
                print(images2)

            images = []
            for id in images1:
                id =  'https://www.camlincustomhomes.com'+ id
                if '-sml' not in id:
                    images.append(id)
            ElevationImage = images

            if images2 != '':
                ElevationImage.append(images2)

            print(ElevationImage)
        except Exception as e:
            print(e)

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

            # ----------------------- Don't change anything here --------------
        unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
                10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['Type'] = Type
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number  # < -------- Changes here
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = PlanName
        item['PlanNotAvailable'] = PlanNotAvailable
        item['PlanTypeName'] = PlanTypeName
        item['BasePrice'] = price
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
    execute('scrapy crawl camlin_customhomes'.split())