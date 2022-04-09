import hashlib
import re
import scrapy
from scrapy.utils.response import open_in_browser

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan


class HickmanhomesSpider(scrapy.Spider):
    name = 'hawthornecreekhomes'
    allowed_domains = ['henrywalkerhomes.com']
    start_urls = ['https://henrywalkerhomes.com/']
    builderNumber = '28138'

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
        item['Street1'] = '873 E. Ashford Ave'
        item['City'] = 'Nixa'
        item['State'] = 'MO'
        item['ZIP'] = '65714'
        item['AreaCode'] = ''
        item['Prefix'] = ''
        item['Suffix'] = '  '
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = 'Hawthorne Creek Homes is owned and operated by Stan and Regina Gutshall, who have over 40 years experience in new home construction from Florida to California. Having built homes in major metropolitan markets, they have brought innovative designs and cutting edge technology to the Southwest Missouri market'
        item['SubImage'] = 'https://hawthornecreekhomes.com/wp-content/uploads/2019/09/HCH-Brookstone-FH.jpg|https://hawthornecreekhomes.com/wp-content/uploads/2019/09/HCH-Brookstone-EC.jpg|https://hawthornecreekhomes.com/wp-content/uploads/2019/09/HCH-Salibury-FH.jpg|https://hawthornecreekhomes.com/wp-content/uploads/2019/09/HCH-Salibury-EC.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'https://hawthornecreekhomes.com/floor-plans/'
        yield scrapy.FormRequest(url=link,callback=self.links,dont_filter=True)

    def links(self,response):
        links = response.xpath('//h2[@class="entry-title"]/a/@href').extract()
        for link in links:
            yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)

    def parse2(self,response):
        try:
            PlanName = "".join(response.xpath('//h2/text()').extract()[1:2])
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
            Bedroo = response.xpath("//*[contains(text(),'Bedrooms')]/../text()").extract_first().strip()
            Bedrooms = re.findall(r"(\d+)", Bedroo)[1]
        except Exception as e:
            Bedrooms = 0
            print("Bedrooms: ", e)

        try:
            Bathroo = response.xpath("//*[contains(text(),'Bath')]/../text()").extract_first().strip()
            tmp = re.findall(r"(\d+)", Bathroo)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            Baths,HalfBaths = 0,0
            print("Baths: ", e)


        try:
            Garage = response.xpath("//*[contains(text(),'Gar')]/../text()").extract_first('').strip()
            Garage = re.findall(r"(\d+)", Garage)[1]
            print(Garage)
        except Exception as e:
            print(e)
            Garage = 0

        try:
            BaseSqft = response.xpath("//*[contains(text(),'Are')]/../text()").extract_first().strip().replace(',', '')
            BaseSqft = BaseSqft.split(";")[0]
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
        except Exception as e:
            BaseSqft = ""
            print("BaseSQFT: ", e)

        try:
            desc = "".join(response.xpath('//div[@class="et_pb_text_inner"]/p/text()[1]').extract())
        except Exception as e:
            print(e)
            desc =  ''

        try:
            ElevationImages = []
            image  = response.xpath('//span[@class="et_pb_image_wrap "]/img/@src').extract()
            if image != []:
                for link in image:
                    ElevationImages.append(link)
            ElevationImages = "|".join(ElevationImages)
        except Exception as e:
            print(str(e))

        unique = str(PlanNumber) + str(self.builderNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['Type'] = Type
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number  # < -------- Changes here
        item['SubdivisionNumber'] = self.builderNumber
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
    execute("scrapy crawl hawthornecreekhomes".split())