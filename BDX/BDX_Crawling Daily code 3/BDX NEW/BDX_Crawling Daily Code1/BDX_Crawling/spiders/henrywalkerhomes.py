import hashlib
import re
import scrapy
from scrapy.utils.response import open_in_browser

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan


class HickmanhomesSpider(scrapy.Spider):
    name = 'henrywalkerhomes'
    allowed_domains = ['henrywalkerhomes.com']
    start_urls = ['https://henrywalkerhomes.com/']
    builderNumber = '17169'

    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = self.builderNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '1216 W. Legacy Crossing Blvd'
        item['City'] = 'Centerville'
        item['State'] = 'UT'
        item['ZIP'] = '84014'
        item['AreaCode'] = ''
        item['Prefix'] = ''
        item['Suffix'] = '  '
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = 'Henry Walker Homes builds exquisite and elegant new homes in Davis, Salt Lake, and Weber County, Utah. Build your home today or choose one of our quick move-in homes and see how we live by our motto: Henry Has It'
        item['SubImage'] = 'https://henrywalkerhomes.com/wp-content/uploads/2020/10/design-process-new.jpg.webp|https://henrywalkerhomes.com/wp-content/uploads/2020/05/gallery1.jpg|https://henrywalkerhomes.com/wp-content/uploads/2020/05/design-center-video-still.jpg|https://henrywalkerhomes.com/wp-content/uploads/2020/05/gallery3.jpg|https://henrywalkerhomes.com/wp-content/uploads/2020/05/LindsaySalazar-21-scaled.jpg|https://henrywalkerhomes.com/wp-content/uploads/2020/05/gallery9.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'https://henrywalkerhomes.com/floor-plans/'
        yield scrapy.FormRequest(url=link,callback=self.links,dont_filter=True)

    def links(self,response):
        links = response.xpath('//div[@class="work-info"]/a/@href').extract()
        for link in links:
            yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)

    def parse2(self,response):
        try:
            PlanName = response.xpath('//h2/text()').extract_first()
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
            Bedroo = response.xpath("//*[contains(text(),'Bedrooms')]/following-sibling::p/text()").extract_first().strip()
            Bedrooms = re.findall(r"(\d+)", Bedroo)
        except Exception as e:
            Bedrooms = 0
            print("Bedrooms: ", e)

        try:
            Bathroo = response.xpath("//*[contains(text(),'Bath')]/following-sibling::p/text()").extract_first().strip()
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
            Garage = response.xpath("//*[contains(text(),'Gar')]/following-sibling::p/text()").extract_first('').strip()
            print(Garage)
        except Exception as e:
            print(e)
            Garage = 0

        try:
            BaseSqft = response.xpath("//*[contains(text(),'Square Feet')]/following-sibling::p/text()").extract_first().strip().replace(',', '')
            BaseSqft = BaseSqft.split(";")[0]
            BaseSqft = ''.join(re.findall(r"(\d+)", BaseSqft))
            BaseSqft = re.findall(r"(\d+)", BaseSqft)
        except Exception as e:
            BaseSqft = ""
            print("BaseSQFT: ", e)

        try:
            desc = "".join(response.xpath('//div[@class="wpb_text_column wpb_content_element "]//div[@class="wpb_wrapper"]/p//text()').extract())
        except Exception as e:
            print(e)
            desc =  ''

        try:
            ElevationImages = []
            image  = response.xpath('//img[@class="skip-lazy "]/@src').extract()
            if image != []:
                for link in image:
                    ElevationImages.append(link)
            ElevationImages = "|".join(ElevationImages)
        except Exception as e:
            print(str(e))

        unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
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
        item['Description'] = desc
        item['ElevationImage'] = ElevationImages
        item['PlanWebsite'] = PlanWebsite
        yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl henrywalkerhomes".split())