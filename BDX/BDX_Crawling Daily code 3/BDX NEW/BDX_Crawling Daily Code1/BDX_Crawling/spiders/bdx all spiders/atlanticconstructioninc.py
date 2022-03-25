
# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'atkinsonhomesal'
    allowed_domains = ['http://atlanticconstructioninc.com/']
    start_urls = ['http://atlanticconstructioninc.com/']

    builderNumber = "62813"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        # images = ''
        # image = response.xpath('//div[@class="gallery-reel-item-src"]/img/@data-src').extract()
        # for i in image:
        #     images = images + i + '|'
        # images = images.strip('|')

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = self.builderNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '7 Doris Ave. E'
        item['City'] = 'Jacksonville'
        item['State'] = 'NC'
        item['ZIP'] = '28540'
        item['AreaCode'] = '910'
        item['Prefix'] ='938'
        item['Suffix'] = '9053'
        item['Extension'] = ""
        # item['Email'] = 'andrew@atlanticconstruction.bm'
        item['Email'] = 'aci@bizec.rr.com'
        item['SubDescription'] = 'Now in its second generation, Atlantic Construction, Inc. is in the business of making the American Dream a reality.  At Atlantic Construction, Inc., we realize that the purchase of a new home or building is one of the largest investments a family or business can make.  That is why we put forth every effort to ensure the building process is as smooth and simple as possible.  We provide convenient, one-on-one assistance through every step of the construction process, ensuring that our clients will receive the utmost attention.  Any questions or concerns will be addressed immediately by the Atlantic Construction team.We at Atlantic Construction, Inc, take the same care with our projects as we take with our clients.  Our clients have the opportunity to choose from one of our many attractive functional floor plans.  No matter which plan is chosen or how minute the detail, our clients can rest assured that every component will be treated with unprecedented levels of care and precision.Our team welcomes the opportunity to take the reins and build the projects our clients have dreamed of owning, but never thought possible.  With our talent and their ideas, we can transform those dreams into beautiful realities.  At Atlantic Construction, Inc., we won"t accept anything less than the client"s complete satisfaction.Serving Eastern North Carolina in and around Jacksonville, Camp Lejeune, Swansboro, Sneads Ferry, Morehead City, Fayetteville and the Crystal Coast.'
        item['SubImage'] = 'http://atlanticconstructioninc.com/lwdcms/image-view.php?module=gallery_res&module_id=1328&image_name=image_1&option=fit&width=1000&height=800&r=0&g=0&b=0&quality=90&use_original=1|http://atlanticconstructioninc.com/lwdcms/image-view.php?module=gallery_res&module_id=1274&image_name=image_1&option=fit&width=1000&height=800&r=0&g=0&b=0&quality=90&use_original=1|http://atlanticconstructioninc.com/lwdcms/image-view.php?module=gallery_res&module_id=1255&image_name=image_1&option=fit&width=1000&height=800&r=0&g=0&b=0&quality=90&use_original=1|http://atlanticconstructioninc.com/lwdcms/image-view.php?module=gallery_res&module_id=1250&image_name=image_1&option=fit&width=1000&height=800&r=0&g=0&b=0&quality=90&use_original=1|http://atlanticconstructioninc.com/lwdcms/image-view.php?module=gallery_res&module_id=1279&image_name=image_1&option=fit&width=1000&height=800&r=0&g=0&b=0&quality=90&use_original=1'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'http://atlanticconstructioninc.com/home-plans/'
        yield scrapy.FormRequest(url=link,callback=self.plan,dont_filter=True)

    def plan(self,response):
        links = response.xpath('//div[@class="row"]/div/a/@href').extract()
        for link in links:
            link = 'http://atlanticconstructioninc.com/' + link
            yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)

    def parse2(self,response):

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

        # try:
        #     Bas = response.xpath("//span[contains(text(),'Price')]/../text()").extract_first('')
        #     Bas = Bas.replace(",", "")
        #     BasePrice = re.findall(r"(\d+)", Bas)[0]
        # except Exception as e:
        #     print(e)

        BasePrice = 0

        try:
            sqft = response.xpath("//span[contains(text(),'Square Fee')]/../text()[2]").extract_first('')
            if '-' in sqft:
                sqft = sqft.split("-")[1]
            sqft = sqft.replace(',', '').replace(".", "").strip()
            BaseSqft = re.findall(r"(\d+)", sqft)[0]

        except Exception as e:
            print(e)
            BaseSqft = ''

        try:
            bath = response.xpath("//span[contains(text(),'Bathroom')]/../text()[2]").extract_first()
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
            Bedrooms = response.xpath("//span[contains(text(),'Bedrooms:')]/../text()[2]").extract_first()
            if '-' in Bedrooms:
                Bedrooms = Bedrooms.split("-")[1]
            # Bedrooms = Bedrooms.split("|")[1].split("|")[0]
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)
            Bedrooms = ''

        try:
            Garage = response.xpath("//span[contains(text(),'Garage')]/../text()").extract_first()
            Garage = re.findall(r"(\d+)", Garage)[0]
        except Exception as e:
            print(e)
            Garage = 0

        try:
            # Description = response.xpath("//h3/../p/text()").extract_first('').strip()
            # print(Description)
            # if Description == '':
            Description = ''
        except Exception as e:
            print(e)

        try:

            # images1 = response.xpath('//li[@class="dmCoverImgContainer"]/img/@src').extract()
            #
            # images2 = response.xpath('//div[@class="u_1929991324 imageWidget align-center"]/a/img/@src').extract_first('')
            images = []
            # imagedata = response.xpath('//li/img/@src').extract()
            imagedata = response.xpath('//div[@class="flexslider"][2]//ul[@class="slides"]/li/img/@src').extract()
            for id in imagedata:
                id = 'http://atlanticconstructioninc.com' + id
                images.append(id)
            ElevationImage = images
            print(ElevationImage)
        except Exception as e:
            print(e)

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

            # ----------------------- Don't change anything here --------------
        unique = str(PlanNumber) + str(SubdivisionNumber) + str(Baths) + str(Bedrooms)  # < -------- Changes here
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
    execute('scrapy crawl atkinsonhomesal'.split())