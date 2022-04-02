# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'campagnahomes'
    allowed_domains = ['https://www.campagnahomes.com']
    start_urls = ['https://www.campagnahomes.com//']

    builderNumber = "23604"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

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
        item['Street1'] = '3180 Curlew Rd. Suite 207'
        item['City'] = 'Oldsmar'
        item['State'] = 'FL'
        item['ZIP'] = '34677'
        item['AreaCode'] = ''
        item['Prefix'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = 'Campagna Homes has been building custom homes since 1952 and is honored to be ranked #1 on Houzz.com in the Tampa Bay Area Area. We define success as creating long-lasting relationships. Our clients are happy to share with you their 5-Star Experience before, during, and long after the completion of their custom home. Our promise is to earn a 5-Star review from our clients and everyone who has contact with Campagna Homes. We invite you to join our exclusive client community'
        item['SubImage'] = "https://www.campagnahomes.com/img/containers/assets/homepage/5.jpg/827af8810811086ff6c9235a8622f6fb.webp|https://www.campagnahomes.com/img/containers/assets/homepage/8.jpg/496b10371814cc3e058046709c5b9b2e.webp|https://www.campagnahomes.com/img/containers/assets/galleries/the-floridova/the-floridova-45.jpg/bbb148cd8de64a322218f512aa02c2a2.jpg|https://www.campagnahomes.com/img/containers/assets/galleries/appian-way/dsa_6596.jpg/7e2964520e6cc6233fe6bbe204a377d0.jpg|https://www.campagnahomes.com/img/containers/assets/galleries/st-tropez-model/shyhome-004.jpg/3420b966277be7b90e443ce431da6fa2.jpg|https://www.campagnahomes.com/img/containers/assets/galleries/villa-lucca/01_0e2a9422_mls.jpg/f99d8a9623cbdb4fdb3db692845add87.jpg"
        item['SubWebsite'] = 'https://www.campagnahomes.com/'
        item['AmenityType'] = ''
        yield item

        links = ['https://www.campagnahomes.com/plans','https://www.campagnahomes.com/home-remodeling']
        for link in links:
            yield scrapy.FormRequest(url=link, callback=self.parse2, dont_filter=True)

    def parse2(self, response):
        links = response.xpath("//a[contains(text(),'View these Plans')]/@href|//h3/../..//a[contains(@href,'/home-remodeling')]/div/../@href").extract()
        for link in links:
            link = 'https://www.campagnahomes.com' + link
            yield scrapy.FormRequest(url=link, callback=self.parse3, dont_filter=True)

    def parse3(self, response):

        try:
            PlanName = response.xpath('//h1/text()').extract_first('')
            print(PlanName)
        except Exception as e:
            print("PlanName: ", e)
        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = self.builderNumber
            print(SubdivisionNumber)
        except Exception as e:
            print(str(e))

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
            print(str(e))

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)
        try:
            Bedroo = response.xpath('//i[@class="fal fa-bed"]/../text()').extract_first('').replace("\n","").strip()
            if Bedroo == '':
                Bedroo = response.xpath('//i[@class="fal fa-bed"]/../text()[2]').get()
            # Bedroom = Bedroo.split(',')[0]
            Bedrooms = re.findall(r"(\d+)", Bedroo)[0]
            # Bedrooms = Bedroom.split(' Bed')[0].strip()

        except Exception as e:
            Bedrooms = 0
            print("Bedrooms: ", e)

        try:
            Bathroo = response.xpath('//i[@class="fal fa-bath"]/../text()').extract_first('').strip().replace("\n","").strip()
            if Bathroo == '':
                Bathroo = response.xpath('//i[@class="fal fa-bath"]/../text()[2]').extract_first('').strip().replace("\n","").strip()
            # Baths = Bathroo.split(',')[1]
            tmp = re.findall(r"(\d+)", Bathroo)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0

        except Exception as e:
            Baths = 0
            print("Baths: ", e)

        try:
            desc = response.xpath('//div[@class="md:flex items-center"]//p/text()|//div[@class="w-full"]/p/text()').extract_first('')
            print(desc)
        except Exception as e:
            print(e)
            desc = ''

        try:
            Garage = response.xpath(
                '//div[@class="text z-t-20 z-text-white"]/text()[6]').extract_first('').strip().replace(',', '')
            Garage = re.findall(r"(\d+)", Garage)[0]
        except Exception as e:
            print("Garage: ", e)
            Garage = 0

        try:
            BaseSqft = response.xpath('//i[@class="fal fa-ruler-combined"]/../text()').extract_first('').strip().replace(',', '')
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
        except Exception as e:
            print("BaseSQFT: ", e)

        try:
            ElevationImages = []
            # ElevationImage1 = response.xpath('//div[@class="left z-float-left"]/img/@src').extract_first('')
            ElevationImage2 = response.xpath("//a[contains(@href,'/img/containers/')]/@href").extract()
            # if ElevationImage1 != '':
            #     ElevationImage1 = 'https://www.americanfamilyhomesinc.com' + ElevationImage1
            if ElevationImage2 != []:
                for image in ElevationImage2:
                    ElevationImage2 = 'https://www.americanfamilyhomesinc.com' + image
                    ElevationImages.append(ElevationImage2)
                # ElevationImages.append(ElevationImage1)

            ElevationImage = "|".join(ElevationImages)

        except Exception as e:
            print(str(e))

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
        item['BasePrice'] = BasePrice
        item['BaseSqft'] = BaseSqft
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = desc
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item

    # ---------------------------------------------------------------------


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl campagnahomes'.split())
