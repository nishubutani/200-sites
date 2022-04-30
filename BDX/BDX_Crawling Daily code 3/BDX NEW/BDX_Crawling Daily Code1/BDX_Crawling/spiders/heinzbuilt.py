import re
import scrapy
import os
import hashlib
import scrapy
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision


class ImagineHomesSpider(scrapy.Spider):
    name = 'heinzbuilt'
    allowed_domains = ['https://hellersite.com/']
    start_urls = ['https://hellersite.com/']

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
        item['Street1'] = '6261 W Founders Dr'
        item['City'] = 'Eagle'
        item['State'] = 'ID'
        item['ZIP'] = '83616'
        item['AreaCode'] = ''
        item['Prefix'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = ''
        item['SubImage'] = 'https://static.wixstatic.com/media/227047_d35c95d7de41446a99d6689f7c51ca31~mv2.jpg|https://static.wixstatic.com/media/227047_4bd839cc6c2941e2b6d6ef90398d78c3~mv2.jpg|https://static.wixstatic.com/media/227047_a2f23d2546d94725ae059eeb9e6ae7c2~mv2.jpg|https://static.wixstatic.com/media/227047_cb4aa2667b2f4a60adaa199ef734717c~mv2.jpg|https://static.wixstatic.com/media/227047_d96e72392ce342b5bd0e46abddd35887~mv2.jpg|https://static.wixstatic.com/media/227047_21031ae0f4d2436c9bb2f535364befdf~mv2.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'https://www.heinzbuilt.com/available-homes'
        yield scrapy.FormRequest(url=link, callback=self.parse2, dont_filter=True)

    def parse2(self, response):

        divs = response.xpath('//div[@role="gridcell"]')
        for div in divs:

            try:
                status = div.xpath(".//span[contains(text(),'Coming Soon')]/text()").extract_first('')
                print(status)
            except Exception as e:
                print(e)

            if status == "Coming Soon":

                try:
                    PlanName = div.xpath('.//h2/span/text()').extract_first('')
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
                    Bedroo = div.xpath(".//span[contains(text(),'beds')]/../../../../../following-sibling::div/p/span/span/span/text()").extract_first('').replace("\n","").strip()
                    Bedrooms = re.findall(r"(\d+)", Bedroo)[0]
                except Exception as e:
                    Bedrooms = 0
                    print("Bedrooms: ", e)

                try:
                    Bathroo = div.xpath(".//span[contains(text(),'bath')]/../../../../../following-sibling::div/p/span/span/span/text()").extract_first(
                        '').strip().replace("\n", "").strip()
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
                    BaseSqft = div.xpath(".//span[contains(text(),'sqft')]/../../../../../following-sibling::div/p/span/span/span/text()").extract_first(
                        '').strip().replace(',', '')
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
                            ElevationImage2 = image.replace("-100x100", "")
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

    execute("scrapy crawl heinzbuilt".split())