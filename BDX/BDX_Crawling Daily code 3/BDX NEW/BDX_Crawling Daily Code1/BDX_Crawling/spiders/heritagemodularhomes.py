
import re
import scrapy
import os
import hashlib
import scrapy
from scrapy.utils.response import open_in_browser

from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class ImagineHomesSpider(scrapy.Spider):
    name = 'heritagemodularhomes'
    allowed_domains = ['https://heritagemodularhomes.com/']
    start_urls = ['https://heritagemodularhomes.com/']

    builderNumber = 52207


    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        # img = response.xpath('//div[@class="ws_images"]/ul/li/img/@src').getall()
        # images = []
        # for i in img:
        #     img1 = 'https://www.imaginehomessa.com' + str(i)
        #     images.append(img1)
        # images = '|'.join(images)

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '16 Harrington Ave'
        item['City'] = 'Shrewsbury'
        item['State'] = 'MA'
        item['ZIP'] = '01545'
        item['AreaCode'] = ''
        item['Prefix'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = 'Welcome to Insignia Homes, where you will always get the home that you want, built the way you want it. Choose from a dozen floor plans we have on hand, or bring your own. Either way, we will give you our absolute best price in either of our premier communities or on your own lot. You choose to do it your wayDan Veronica of Gaithersburg, Maryland had been searching for a builder to give him the home he wanted in a neighborhood where he could walk to the train for his commute to his job in Washington, DC. He found it with Insignia Homes. "These guys knew exactly what I wanted and helped me find a plan that worked for me at a price I could afford. I was able to build a fully custom home with all the amenities I desired and I got my big garage too! My hats off to Insignia for giving me the opportunity to build what is truly my dream home, my way'
        item['SubImage'] = 'https://heritagemodularhomes.com/wp-content/uploads/2021/10/winterexterior-768x576.jpeg|https://heritagemodularhomes.com/wp-content/uploads/2021/10/mobileheaderpic-768x466.jpg|https://heritagemodularhomes.com/wp-content/uploads/2022/01/1-768x576.png|https://heritagemodularhomes.com/wp-content/uploads/2022/01/2-768x1024.png|https://heritagemodularhomes.com/wp-content/uploads/2022/01/3-768x1024.png|https://heritagemodularhomes.com/wp-content/uploads/2022/01/4-768x576.png|https://heritagemodularhomes.com/wp-content/uploads/2022/01/IMG_3095-768x395.jpeg|https://heritagemodularhomes.com/wp-content/uploads/2022/01/IMG_3470-768x301.jpg|https://heritagemodularhomes.com/wp-content/uploads/2022/01/IMG_3471-768x408.jpg|https://heritagemodularhomes.com/wp-content/uploads/2022/01/IMG-0468-768x576.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'https://heritagemodularhomes.com/product-category/modular-homes/'
        yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)

    def parse2(self, response):
        links = response.xpath('//ul[@class="products columns-4"]/li/a[1]/@href').extract()
        for link in links:
            yield scrapy.FormRequest(url=link, callback=self.parse3, dont_filter=True)


        next_page = response.xpath('//a[@class="next page-numbers"]/@href').extract_first('')
        if next_page != '':
            yield scrapy.FormRequest(url=next_page, callback=self.parse2, dont_filter=True)
        else:
            pass
        
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
            Bedroo = response.xpath("//*[contains(text(),'Bedrooms')]/../td/p/text()").extract_first('').replace("\n","").strip()
            Bedrooms = re.findall(r"(\d+)", Bedroo)[0]
        except Exception as e:
            Bedrooms = 0
            print("Bedrooms: ", e)

        try:
            Bathroo = response.xpath("//*[contains(text(),'Bathrooms')]/../td/p/text()").extract_first('').strip().replace("\n","").strip()
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
            # desc = response.xpath('//div[@class="md:flex items-center"]//p/text()|//div[@class="w-full"]/p/text()').extract_first('')
            desc = ''
            print(desc)
        except Exception as e:
            print(e)
            desc = ''

        try:
            # Garage = response.xpath('//div[@class="text z-t-20 z-text-white"]/text()[6]').extract_first('').strip().replace(',', '')
            # Garage = re.findall(r"(\d+)", Garage)[0]

            Garage = 0
        except Exception as e:
            print("Garage: ", e)
            Garage = 0

        try:
            BaseSqft = response.xpath("//*[contains(text(),'SQ FT.')]/../td/p/text()").extract_first('').strip().replace(',', '')
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
        except Exception as e:
            print("BaseSQFT: ", e)

        try:
            ElevationImages = []
            # ElevationImage1 = response.xpath('//div[@class="left z-float-left"]/img/@src').extract_first('')
            ElevationImage2 = response.xpath('//div/@data-thumb').extract()
            # if ElevationImage1 != '':
            #     ElevationImage1 = 'https://www.americanfamilyhomesinc.com' + ElevationImage1
            if ElevationImage2 != []:
                for image in ElevationImage2:
                    ElevationImage2 = image.replace("-100x100","")
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

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl heritagemodularhomes".split())