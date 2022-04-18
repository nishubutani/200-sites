import hashlib
import re
import scrapy
from scrapy.utils.response import open_in_browser

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan


class HickmanhomesSpider(scrapy.Spider):
    name = 'hartlandhomescorp'
    allowed_domains = ['hartlandhomescorp.com']
    start_urls = ['https://www.hartlandhomescorp.com/']
    builderNumber = '28026'

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
        item['Street1'] = '11181 Riddle Dr'
        item['City'] = 'Spring Hill'
        item['State'] = 'FL'
        item['ZIP'] = '34609'
        item['AreaCode'] = ''
        item['Prefix'] = ''
        item['Suffix'] = '  '
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = 'Hartland Homes deeply values our local real estate brokers and agents who accompany you to the model home on your first visit to the model.  If you are not working with a Real Estate Agent, we have sales professionals who are ready to answer any questions or concerns you may have.  In any case, either with or without a Real Estate Agent, we are commited to building you a beautiful new Hartland Home.  Please have your Real Esate Agent contact us for information on our co-broke agreement.'
        item['SubImage'] = 'https://www.hartlandhomescorp.com/wp-content/uploads/francesca_main.jpg|https://www.hartlandhomescorp.com/wp-content/uploads/francesca_02.jpg|https://www.hartlandhomescorp.com/wp-content/uploads/francesca_09.jpg|https://www.hartlandhomescorp.com/wp-content/uploads/joann_b_main.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'https://www.hartlandhomescorp.com/floorplans/'
        yield scrapy.FormRequest(url=link,callback=self.links,dont_filter=True)

    def links(self,response):
        links = response.xpath('//h2[@class="floorplan-excerpt-heading"]/a/@href').extract()
        for link in links:
            yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)

    def parse2(self,response):
        try:
            PlanName = response.xpath('//h1/text()').extract_first()
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
            Bedroo = response.xpath("//*[contains(text(),'Bedrooms')]/following-sibling::div/text()").extract_first().strip()
            Bedrooms = re.findall(r"(\d+)", Bedroo)
        except Exception as e:
            Bedrooms = 0
            print("Bedrooms: ", e)

        try:
            Bathroo = response.xpath("//*[contains(text(),'Bath')]/following-sibling::div/text()").extract_first().strip()
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
            Garage = response.xpath("//*[contains(text(),'Gar')]/following-sibling::div/text()").extract_first('').strip()
            print(Garage)
        except Exception as e:
            print(e)
            Garage = 0

        try:
            BaseSqft = response.xpath("//*[contains(text(),'Tota')]/following-sibling::div/text()").extract_first().strip().replace(',', '')
            BaseSqft = BaseSqft.split(";")[0]
            BaseSqft = ''.join(re.findall(r"(\d+)", BaseSqft))
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
        except Exception as e:
            BaseSqft = ""
            print("BaseSQFT: ", e)

        try:
            desc = "".join(response.xpath("//*[contains(text(),'About This Home')]/../p/text()").extract())
        except Exception as e:
            print(e)
            desc =  ''

        try:
            ElevationImages = []
            image  = response.xpath('//a[@class="floorplan-gallery"]/@href').extract()
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
    execute("scrapy crawl hartlandhomescorp".split())