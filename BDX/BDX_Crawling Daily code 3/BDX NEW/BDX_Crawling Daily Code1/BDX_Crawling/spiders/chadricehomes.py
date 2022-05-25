import hashlib
import re
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
class mybrookfieldSpider(scrapy.Spider):
    name = 'chadricehomes'
    allowed_domains = []
    start_urls = ['https://www.chadricehomes.com/deer-brook']

    builderNumber = "50488"

    def parse(self, response):

        try:
            SubdivisionName = response.xpath('//p/strong/text()').extract_first(default='').strip()
            print(SubdivisionName)
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = int(hashlib.md5(bytes(SubdivisionName, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)


        try:
            desc=''.join(response.xpath('//div[@class="sqs-block-content"]/p[1]/text()[1]').extract()[:1])
        except:
            desc=""

        try:
            img='|'.join(response.xpath('//figure[@class="loading content-fill"]/img/@data-src').extract())
        except:
            img=''

        area = ''
        prefix = ''
        sufix = ''

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        a = []
        # aminity = ''.join(response.xpath('//*[@class="ll-features-content__half right col-md-1of2"]/ul[1]/li/text()').extract())
        try:
            aminity = desc
            aminity = aminity.title()
        except Exception as e:
            print(e)

        amenity_list = ["Pool", "Playground", "GolfCourse", "Tennis", "Soccer", "Volleyball", "Basketball",
                        "Baseball", "Views", "Lake", "Pond", "Marina", "Beach", "WaterfrontLots", "Park",
                        "Trails", "Greenbelt", "Clubhouse", "CommunityCenter"]
        for i in amenity_list:
            if i in aminity:
                # print(i)
                a.append(i)
        ab = '|'.join(a)


        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = SubdivisionNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = SubdivisionName
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '6517 NW 149th St'
        item['City'] = "Oklahoma"
        item['State'] = "OK"
        item['ZIP'] = "73142"
        item['AreaCode'] = area
        item['Prefix'] = prefix
        item['Suffix'] = sufix
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = desc
        item['SubImage']=img
        item['SubWebsite'] = response.url
        item['AmenityType'] = ab
        yield item

        links = response.xpath('//div[@class="collection"]/a/@href').extract()
        for i1 in links:
            i1 = 'https://www.chadricehomes.com' + i1
            # print("ur linnk is ",i1)
            yield scrapy.FormRequest(url=i1, callback=self.home_detail,meta={'SubdivisionNumber':SubdivisionNumber})

    def home_detail(self, response):
        SubdivisionNumber = response.meta['SubdivisionNumber']
        try:
            PlanName = response.xpath('//p/strong/text()').extract_first()
            print(PlanName)
        except Exception as e:
            print("PlanName ", e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % PlanNumber, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
            print(e)

        try:
            # BasePrice = response.xpath('//*[contains(text(),"Priced")]/text()').extract_first()
            # if BasePrice == None or BasePrice == '':
            #     BasePrice = response.xpath('//*[contains(text(),"Starting at")]/text()').extract_first().replace(',',
            #                                                                                                      '')
            # BasePrice = BasePrice.replace(',', '')
            # BasePrice = re.findall(r"(\d+)", BasePrice)[0]
            BasePrice = 0
            print(BasePrice)
            BasePrice = 0
        except Exception as e:
            BasePrice = 0
        try:
            BaseSqft = response.xpath('//h2/following-sibling::h3/text()').extract_first()
            BaseSqft = BaseSqft.split("·")
            for loo in BaseSqft:
                loo = loo.replace(",","")
                if 'sqFT' in loo:
                    BaseSqft = re.findall(r"(\d+)", loo)[0]
                    break
            print(BaseSqft)

        except Exception as e:
            BaseSqft = 0
        try:
            Bedrooms = response.xpath('//h2/following-sibling::h3/text()').extract_first()
            Bedrooms = Bedrooms.split("·")
            for loo in Bedrooms:
                if "bed" in loo or 'BED' in loo:
                    Bedrooms = re.findall(r"(\d+)", loo)[0]
                    break
            print(Bedrooms)
        except Exception as e:
            Bedrooms = 0
        try:
            Baths = response.xpath('//h2/following-sibling::h3/text()').extract_first()
            Baths = Baths.split("·")
            for loo in Baths:
                if "bath" in loo:
                    tmp = re.findall(r"(\d+)", loo)
                    Baths = tmp[0]

                    if 'half' in loo:
                        try:
                            HalfBaths = "".join(re.findall(r'bath(.*?)half', loo))
                            HalfBaths = re.findall(r"(\d+)", HalfBaths)[0]
                        except Exception as e:
                            HalfBaths = 0
                    else:
                        if len(tmp) > 1:
                            HalfBaths = 1
                            print(HalfBaths)
                        else:
                            HalfBaths = 0
                            print(HalfBaths)

                    break
        except Exception as e:
            Baths = 0
            HalfBaths = 0

        try:
            Garage = response.xpath('//h2/following-sibling::h3/text()').extract_first()
            Garage = Garage.split("·")
            for loo in Garage:
                if "garage" in loo:
                    Garage = re.findall(r"(\d+)", loo)[0]
                else:
                    Garage = ''
            print(Garage)
        except Exception as e:
            Garage = 0

        try:
            ElevationImage2 = response.xpath('//img[@class="thumb-image"]/@data-src').extract()
            ElevationImage = '|'.join(ElevationImage2)
        except Exception as e:
            ElevationImage = ""

        # SubdivisionNumber = self.builderNumber  # if subdivision is not available
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = PlanName
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = BasePrice
        item['BaseSqft'] = BaseSqft
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = ""
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = response.url
        yield item



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl chadricehomes".split())