
# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class vtshomeshomesSpider(scrapy.Spider):
    name = 'focalpointhomes'
    allowed_domains = []
    start_urls = ['https://focalpointhomes.com/']

    builderNumber = "25104"

    def parse(self, response):
        print('--------------------')
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

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
        item['Street1'] = '6756 OLD MCLEAN VILLAGE DR. SUITE 100'
        item['City'] = 'MCLEAN'
        item['State'] = 'VA'
        item['ZIP'] = '22101'
        item['AreaCode'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Prefix'] = ""
        item['Email'] = ''
        item['SubDescription'] = "Focal Point only hires those who are intelligent, experienced, and driven to succeed; however, more importantly, we also only employ those who have impeccable integrity and who care deeply about our customers and the quality of the homes we build for them."
        item['SubImage'] = 'https://471cnv1oagubqby1r32lcg9e-wpengine.netdna-ssl.com/wp-content/uploads/2019/08/4a72201b6707610a6d1718d5f0cc5749.jpg|https://471cnv1oagubqby1r32lcg9e-wpengine.netdna-ssl.com/wp-content/uploads/2019/08/1-web-or-mls-6709-Osborn-St-01-431x323.jpg|https://471cnv1oagubqby1r32lcg9e-wpengine.netdna-ssl.com/wp-content/uploads/2019/08/6d8ece9fbe1cc43a178941f78bbb74f0.jpg|https://471cnv1oagubqby1r32lcg9e-wpengine.netdna-ssl.com/wp-content/uploads/2021/08/IMG_0887-Reversed-431x323.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link= 'https://focalpointhomes.com/'
        yield scrapy.Request(url=link, callback=self.plan_links_inner,dont_filter=True)

    def plan_links_inner(self,response):

        divs =  response.xpath('//div[@class="houseplans-grid"]')
        for div in divs:
            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)
            try:
                plan_slug = div.xpath('.//following-sibling::h3/text()').get('')
            except Exception as e:
                print(e)


            try:
                PlanName = plan_slug.split('-')[0].strip()
                print(PlanName)
            except Exception as e:
                print(e)

            try:
                PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
                print(PlanName)
                f = open("html/%s.html" % PlanNumber, "wb")
                f.write(response.body)
                f.close()
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
                BasePrice = div.xpath('.//h3/span/text()').get('0').replace(',','')
                BasePrice = re.findall(r"(\d+)", BasePrice)[0]
            except Exception as e:
                print(e)
                BasePrice = 0

            try:
                Baths = plan_slug.split('-')[1].strip()
                Baths = Baths.split("/")[1]
                Baths = re.findall(r"(\d+)", Baths)
                Bath = Baths[0]
                print(Baths)
                if len(Baths) > 1:
                    HalfBaths = 1
                else:
                    try:
                        half_Baths = plan_slug.split('-')[1].strip()
                        half_Baths = half_Baths.split("/")[2]
                        HalfBaths = re.findall(r"(\d+)", half_Baths)[0]
                    except:
                        HalfBaths = 0
            except Exception as e:
                print(e)

            try:
                Bedrooms = plan_slug.split('-')[1].strip().split("/")[0]
                Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
                print(Bedrooms)
            except Exception as e:
                print(e)

            try:
                # Garage = div.xpath(".//*[contains(text(),'Garage')]/text()").extract_first(default='0').strip().replace(",", "")
                # Garage = Garage.split(" ")[0]
                # Garage = re.findall(r"(\d+)", Garage)[0]
                Garage = 0.0
                print(Garage)
            except Exception as e:
                print(e)
                Garage = 0.0


            try:
                BaseSqft = 0
                # BaseSqft = div.xpath(".//*[contains(text(),'SQ.')]/text()").extract_first(
                #     default='0').strip().replace(",", "")
                # # BaseSqft = BaseSqft.split(" ")[0]
                print(BaseSqft)

            except Exception as e:
                print(e)

            try:
                Description = ""

                print(Description)
            except Exception as e:
                Description = ''

            try:
                images = []
                image1 = div.xpath('.//*[@class="cover"]/@src').extract_first('')
                image2 = div.xpath('.//following-sibling::div[@class="plan-actions"]/a/@href').extract()
                if image1 != "":
                    images.append(image1)
                if image2 != []:
                    for im in image2:
                        print(im)
                        if '.pdf' not in im:
                            images.append(im)
                ElevationImage = "|".join(images)
                print(ElevationImage)
            except Exception as e:
                print(e)
                ElevationImage = ''

            try:
                PlanWebsite = response.url
            except Exception as e:
                print(e)

                # SubdivisionNumber = SubdivisionNumber #if subdivision is there
            SubdivisionNumber = self.builderNumber  # if subdivision is not available
            unique = str(PlanName) + str(SubdivisionNumber)
            print(unique)
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

            item = BdxCrawlingItem_Plan()
            item['Type'] = Type
            item['PlanNumber'] = PlanNumber
            item['unique_number'] = unique_number
            item['SubdivisionNumber'] = SubdivisionNumber
            item['PlanName'] = PlanName
            item['PlanNotAvailable'] = PlanNotAvailable
            item['PlanTypeName'] = PlanTypeName
            item['BasePrice'] = BasePrice
            item['BaseSqft'] = BaseSqft
            item['Baths'] = Bath
            item['HalfBaths'] = HalfBaths
            item['Bedrooms'] = Bedrooms
            item['Garage'] = Garage
            item['Description'] = Description
            item['ElevationImage'] = ElevationImage
            item['PlanWebsite'] = PlanWebsite
            yield item



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl focalpointhomes".split())