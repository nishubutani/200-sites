import json
import re
import scrapy
import os
import hashlib
import scrapy
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, \
    BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision


class hcbuilderSpider(scrapy.Spider):
    name = 'hcbuilder'
    allowed_domains = ['https://hbcbuilder.com/']
    start_urls = ['https://hbcbuilder.com/contact/']

    builderNumber = '33166'

    # count = 0

    def parse(self, response):

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)

        subdivisonName = "HC Builder"
        subdivisonNumber = self.builderNumber
        img = ["https://hbcbuilder.com/wp-content/uploads/2015/05/custom-builder-kitchen.jpg",
                 "https://hbcbuilder.com/wp-content/uploads/2015/05/custom-home-builder-kitchen.jpg",
                 "https://hbcbuilder.com/wp-content/uploads/2015/05/homes-by-chris-custom-home.jpg"]
        Image = "|".join(img)

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = subdivisonNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = subdivisonName
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = "1621 Hampshire Ct"
        item['City'] = "Liberty"
        item['State'] = "MO"
        item['ZIP'] = "64068"
        item['AreaCode'] = "816"
        item['Prefix'] = "781"
        item['Suffix'] = "5700"
        item['Extension'] = ""
        item['Email'] = "Chris@HBCBuilder.com"
        item['SubDescription'] = "Thank you for your interest in Homes by Chris. We have provided a number of ways for you to get in touch with us. Since we are out of the office and at job sites frequently, please be patient with us. We will get back with you as soon as we can."
        item['SubImage'] = Image
        item['SubWebsite'] = ""
        item['AmenityType'] = ""
        yield item

        url = "https://hbcbuilder.com/models-plans/"
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.plan_links)

    def plan_links(self, response):
        plan_links = response.xpath('//*[@class="uagb-post__title"]/a/@href').extract()
        for plan in plan_links:
            url = plan
            # url = "https://hbcbuilder.com/hadley"
            # "https://hbcbuilder.com/beckett/" # "https://hbcbuilder.com/hadley/"
            yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.plan_details)

    def plan_details(self, response):

        PlanName = response.xpath('//h1/text()').get()
        if not PlanName:
            PlanName = response.xpath('//div[@id="home-wrap"]/h1/text()').get()
            if not PlanName:
                PlanName = response.url
                PlanName = PlanName.split("/")[-2]

        Type = 'SingleFamily'

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)

        except Exception as e:
            print(e)

        SubdivisionNumber = self.builderNumber

        PlanNotAvailable = 0
        PlanTypeName = 'Single Family'

        unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        PlanWebsite = response.url
        Description = ''.join(response.xpath('//*[contains(text(),"Description")]/../../..//p//text()').getall())

        try:
            Bedrooms = response.xpath('//*[@class="elementor-image-box-title"]//text()').get()
            if Bedrooms == None:
                Bedrooms = response.xpath('//*[contains(text(),"Bedrooms:")]/../text()').get()
            Bedrooms = re.findall(r'\d+', Bedrooms)[0]
            Baths1 = response.xpath('//*[@class="elementor-image-box-title"]//text()').getall()[1]
            if Baths1 == None:
                Baths1 = response.xpath('//*[@class="elementor-image-box-title"]//text()').getall()
            Baths = re.findall(r'\d+', Baths1)[0]
            tmp = len(Baths1)
            if tmp > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
            try:
                BaseSqft = response.xpath('//*[@class="elementor-image-box-title"]//text()').getall()[-1]
                # BaseSqft = "".join(BaseSqft)
                BaseSqft = BaseSqft.replace("Square Feet:", "")
                BaseSqft = BaseSqft.replace(",", "")

                BaseSqft = re.findall(r'\d+', BaseSqft)[0]

            except Exception:

                BaseSqft = response.xpath('//*[contains(text(),"Square Feet:")]//parent::li//text()').getall()
                BaseSqft = "".join(BaseSqft)
                BaseSqft = BaseSqft.replace("Square Feet:", "")
                BaseSqft = BaseSqft.split("-")[-1]
                BaseSqft = BaseSqft.replace(",", "")
                BaseSqft = re.findall(r'\d+', BaseSqft)[0]

            # BaseSqft
            Garage = response.xpath('//*[@class="elementor-image-box-title"]//text()').getall()[2]
            if Garage == None:
                Garage = response.xpath('//*[contains(text(),"Garages:")]/../text()').get()
                if Garage == None:
                    Garage = response.xpath('//*[contains(text(),"Garages:")]/text()').get()
            Garage = re.findall(r'\d+', Garage)[0]
            try:
                BasePrice = response.xpath('//*[contains(text(),"Price:")]/text()').get()
                BasePrice = BasePrice.replace(",","")
                BasePrice = BasePrice.replace("$", "")
                BasePrice = re.findall(r'\d+', BasePrice)[0]
            except Exception:
                BasePrice = 0
            try:
                img = response.xpath('//*[@class="elementor-gallery__container e-gallery-container e-gallery-masonry e-gallery--ltr e-gallery--lazyload"]/a/@href').getall()
                Image = "|".join(img)
            except Exception as e:
                Image = 'dsefseferfef'
                print("Error in image",e)


        except Exception:
            print("errorrrrrrr")
        #     Bedrooms = response.xpath('//div[@class="entry-content"]//*[contains(text(),"Bedrooms:")]/text()').get()
        #     if Bedrooms == None:
        #         Bedrooms = response.xpath('//*[contains(text(),"Bedrooms:")]/text()').get()
        #     Bedrooms = re.findall(r'\d+', Bedrooms)[0]
        #     Baths1 = response.xpath('//div[@class="entry-content"]//*[contains(text(),"Bathrooms:")]/text()').get()
        #     if Baths1 == None:
        #         Baths1 = response.xpath('//*[contains(text(),"Bathrooms:")]/text()').get()
        #     Baths = re.findall(r'\d+', Baths1)[0]
        #     tmp = len(Baths1)
        #     if tmp > 1:
        #         HalfBaths = 1
        #     else:
        #         HalfBaths = 0
        #     try:
        #         BaseSqft = response.xpath('//*[contains(text(),"Square Feet:")]//parent::li//text()').getall()
        #         # BaseSqft = "".join(BaseSqft)
        #         BaseSqft = BaseSqft.replace("Square Feet:", "")
        #         BaseSqft = BaseSqft.replace(",", "")
        #
        #         BaseSqft = re.findall(r'\d+', BaseSqft)[0]
        #
        #     except Exception:
        #
        #         BaseSqft = response.xpath('//*[contains(text(),"Square Feet:")]//parent::li//text()').getall()
        #         BaseSqft = "".join(BaseSqft)
        #         BaseSqft = BaseSqft.replace("Square Feet:", "")
        #         BaseSqft = BaseSqft.split("-")[-1]
        #         BaseSqft = BaseSqft.replace(",", "")
        #         BaseSqft = re.findall(r'\d+', BaseSqft)[0]
        #
        #     # BaseSqft
        #     Garage = response.xpath('//div[@class="entry-content"]//*[contains(text(),"Garages:")]/text()').get()
        #     if Garage == None:
        #         Garage = response.xpath('//*[contains(text(),"Garages:")]/text()').get()
        #     Garage = re.findall(r'\d+', Garage)[0]
        #     BasePrice = 0
        #     img = response.xpath('//dt[@class="gallery-icon landscape"]/a/img/@src').getall()
        #     Image = "|".join(img)

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
        item['ElevationImage'] = Image
        item['PlanWebsite'] = PlanWebsite


        yield item

    #     url = "https://hbcbuilder.com/available-homes/"
    #     yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.home_links, meta={'PN': unique_number})
    #
    # def home_links(self, response):
    #     PN = response.meta['PN']
    #     home_links = response.xpath('//span[@class="listing-status active"]/.././a/@href').extract()
    #     for links in home_links:
    #         url = links
    #
    #         yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.home_details, meta={'PN': PN})
    #
    # def home_details(self, response):
    #
    #     PlanNumber = response.meta['PN']
    #     MasterBedLocation = "down"
    #
    #     SpecDescription = response.xpath('//*[@itemprop="description"]/p[1]//text()').getall()
    #     SpecDescription = "".join(SpecDescription)
    #     SpecPrice = response.xpath('//tr[@class="wp_listings_listing_price"]/td[2]/text()').get()
    #     if "TBD" in SpecPrice:
    #         SpecPrice = 0
    #     else:
    #
    #         SpecPrice = SpecPrice.replace(",", "")
    #         SpecPrice = SpecPrice.replace("$", "")
    #         SpecPrice = SpecPrice.replace(" ", "")
    #
    #     SpecStreet = response.xpath('//tr[@class="wp_listings_listing_address"]/td[2]/text()').get()
    #     SpecCity = response.xpath('//tr[@class="wp_listings_listing_city"]/td[2]/text()').get()
    #     SpecState = "MO"
    #     SpecZIP = response.xpath('//tr[@class="wp_listings_listing_zip"]/td[2]/text()').get()
    #     SpecCountry = "USA"
    #
    #     SpecBedrooms = response.xpath('//tr[@class="wp_listings_listing_bedrooms"]/td[2]/text()').get()
    #     SpecBaths1 = response.xpath('//tr[@class="wp_listings_listing_bathrooms"]/td[2]/text()').get()
    #     SpecBaths = re.findall(r'\d+',SpecBaths1)[0]
    #     SpecHalfBaths = response.xpath('//tr[@class="wp_listings_listing_half_bath"]/td[2]/text()').get()
    #     if SpecHalfBaths == None :
    #
    #         tmp = len(SpecBaths1)
    #         if tmp < 1:
    #             SpecHalfBaths = 1
    #         else:
    #             SpecHalfBaths = 0
    #
    #     SpecSqft = response.xpath('//tr[@class="wp_listings_listing_sqft"]/td[2]/text()').get()
    #     SpecSqft = SpecSqft.replace(",","")
    #     SpecGarage = 0
    #
    #     ElevationImage = response.xpath('//li[@class="blocks-gallery-item"]//img/@src').getall()
    #     ElevationImage = "|".join(ElevationImage)
    #     if ElevationImage == None:
    #         ElevationImage = response.xpath('//*[@itemprop="description"]/p[2]/img/@src').get()
    #     elif len(ElevationImage) < 4:
    #         ElevationImage = response.xpath('//*[@itemprop="description"]/p[2]/img/@src').get()
    #
    #     unique = SpecStreet + SpecCity + SpecState + SpecZIP
    #     SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
    #
    #     SpecWebsite = response.url
    #     item = BdxCrawlingItem_Spec()
    #     item['SpecNumber'] = SpecNumber
    #     item['PlanNumber'] = PlanNumber
    #     item['SpecStreet1'] = SpecStreet
    #     item['SpecCity'] = SpecCity
    #     item['SpecState'] = SpecState
    #     item['SpecZIP'] = SpecZIP
    #     item['SpecCountry'] = SpecCountry
    #     item['SpecPrice'] = SpecPrice
    #     item['SpecSqft'] = SpecSqft
    #     item['SpecBaths'] = SpecBaths
    #     item['SpecHalfBaths'] = SpecHalfBaths
    #     item['SpecBedrooms'] = SpecBedrooms
    #     item['MasterBedLocation'] = MasterBedLocation
    #     item['SpecGarage'] = SpecGarage
    #     item['SpecDescription'] = SpecDescription.encode('ascii', 'ignore').decode('utf8').strip('')
    #     item['SpecElevationImage'] = ElevationImage
    #     item['SpecWebsite'] = SpecWebsite
    #     yield item

        # ----------------------- Don't change anything here --------------------- #

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl hcbuilder".split())
