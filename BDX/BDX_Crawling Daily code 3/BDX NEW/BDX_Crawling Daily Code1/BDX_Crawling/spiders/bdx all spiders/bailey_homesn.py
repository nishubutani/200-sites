

# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class DexterwhiteconstructionSpider(scrapy.Spider):
    name = 'bailey_homesn'
    allowed_domains = ['https://www.baileyhomesnv.com/']
    start_urls = ['https://www.baileyhomesnv.com/']

    builderNumber = "62848"

    def parse(self, response):

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()



        images = ''
        image = response.xpath('//img/@src').extract()[1:]
        # print(image)
        for i in image:
            j = i.startswith('//images.squarespace')
            print(j)
            if j != True:
                images = images + i + '|'
        images = images.strip('|')

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '475 Hill Street Suite C'
        item['City'] = 'Reno'
        item['State'] = 'NV'
        item['ZIP'] = '89501'
        item['AreaCode'] = '775'
        item['Prefix'] ='385'
        item['Suffix'] = '3659'
        item['Extension'] = ""
        item['Email'] = 'jon@newhomeselko.com'
        item['SubDescription'] = 'Bailey Homes is a third generation Northern Nevada home builder. Doug Bailey started Bailey Homes in 1972, building homes in Reno and Lake Tahoe, NV. For the past 40 + years he has helped thousands of families get into a new Bailey home.Bailey Homes is now building quality homes in most areas of Northern Nevada including; Elko, Spring Creek, Lamoille, Carlin, Wells, Battle Mountain, Jiggs, South Fork, Fernley, Reno, Tahoe, and Incline Village.'
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        links = ['https://www.baileyhomesnv.com/','https://www.baileyhomesnv.com/incline-homes']
        # links = ['https://www.baileyhomesnv.com/']
        # links = ['https://www.baileyhomesnv.com/incline-homes']
        for link in links:
            yield scrapy.FormRequest(url=link,callback=self.parse2,dont_filter=True)



    def parse2(self, response):
        if response.url == 'https://www.baileyhomesnv.com/incline-homes':

            # divs = response.xpath('//div[@class="sqs-block html-block sqs-block-html"]/div/h2')
            divs = response.xpath('//div[@class="col sqs-col-4 span-4"]')
            for div in divs:

                try:
                    Type = 'SingleFamily'
                except Exception as e:
                    print(e)

                try:
                    PlanName = "".join(div.xpath('.//h2[@class="text-align-center"]//text()').extract())
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



                try:
                    # sqft = div.xpath("./../../../../div/div[@class='sqs-block html-block sqs-block-html'][2]/div/p/text()").extract_first('')
                    sqft = div.xpath(".//p[@class='text-align-center']//text()").extract_first('')
                    print(sqft)
                    sqft = sqft.split("|")[-1].replace(",","")
                    BaseSqft = re.findall(r"(\d+)", sqft)[0]

                except Exception as e:
                    print(e)
                    BaseSqft=''

                try:

                    # bath = div.xpath("./../../../..//div[@class='sqs-block html-block sqs-block-html'][2]/div/p/text()").extract_first('')
                    bath = div.xpath('.//p[@class="text-align-center"]//text()').extract_first('')
                    bath = bath.split("|")[1].split("|")[0].strip()
                    tmp = re.findall(r"(\d+)", bath)
                    Baths = tmp[0]
                    if len(tmp) > 1:
                        HalfBaths = 1
                    else:
                        HalfBaths = 0
                except Exception as e:
                    print(e)

                try:
                    # Bedrooms = div.xpath("./../../../..//div[@class='sqs-block html-block sqs-block-html'][2]/div/p/text()").extract_first('')
                    Bedrooms = div.xpath('//p[@class="text-align-center"]//text()').extract_first('')
                    Bedrooms = Bedrooms.split("|")[0]
                    if '-' in Bedrooms:
                        Bedrooms = Bedrooms.split("-")[1]
                    Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
                except Exception as e:
                    print(e)
                    Bedrooms = ''


                price = '0'

                try:
                    BasePrice = price
                except Exception as e:
                    print(e)

                try:
                    # Garage = div.xpath("./../../../..//div[@class='sqs-block html-block sqs-block-html'][2]/div/p/text()").extract_first('')
                    Garage = div.xpath('//p[@class="text-align-center"]//text()').extract_first('')
                    Garage = Garage.split("|")[2].split("|")[0]
                    Garage = re.findall(r"(\d+)", Garage)[0]
                except Exception as e:
                    print(e)
                    Garage = 0


                try:


                    # desc = 'Bailey Homes is a third generation Northern Nevada home builder. Doug Bailey started Bailey Homes in 1972, building homes in Reno and Lake Tahoe, NV. For the past 40 + years he has helped thousands of families get into a new Bailey home.Bailey Homes is now building quality homes in most areas of Northern Nevada including; Elko, Spring Creek, Lamoille, Carlin, Wells, Battle Mountain, Jiggs, South Fork, Fernley, Reno, Tahoe, and Incline Village.'
                    desc = ''

                    Description = desc
                except Exception as e:
                    print(e)

                try:

                    ElevationImage = 'https://images.squarespace-cdn.com/content/v1/5ace3c9136099bfff90d7094/1529010351097-6DHA4MO3N62MRUJRWRK3/ke17ZwdGBToddI8pDm48kHSvyqhBFPlZ-QAJrG4IQaJ7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1Ue3jHJqzaa8HL6NO8SgUjcI_IkFHOH8SD6gL71NZTR0AvEaPiZxQAG2PrP-ijbbzGQ/unit-1-web.jpg'
                except Exception as e:
                    print(e)


                try:
                    PlanWebsite = response.url
                except Exception as e:
                    print(e)

                    # ----------------------- Don't change anything here --------------
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
                item['Description'] = Description
                item['ElevationImage'] = ElevationImage
                item['PlanWebsite'] = PlanWebsite
                yield item

        else:
            links = response.xpath('//div/figure/a/@href').extract()
            for link in links:
                link = 'https://www.baileyhomesnv.com' + link
                print(link)
                yield scrapy.FormRequest(url=link, callback=self.parse3, dont_filter=True)
                # yield scrapy.FormRequest(url='https://www.baileyhomesnv.com/the-cedar-home', callback=self.parse3, dont_filter=True)

    def parse3(self, response):

        ab = response.xpath('//h2[@class="text-align-center"]')
        if len(ab) == 2:

            # divs = response.xpath('//div[@class="sqs-block-content"]/h2')
            divs = response.xpath('//div[@class="col sqs-col-6 span-6"]')
            for div in divs:

                try:
                    Type = 'SingleFamily'
                except Exception as e:
                    print(e)

                try:
                    PlanName = "".join(div.xpath('.//h2//text()').extract())
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



                try:
                    # sqft = div.xpath(".//../p/text()").extract_first('')
                    sqft = div.xpath('.//p[@class="text-align-center"]/text()').extract_first('')
                    print(sqft)
                    sqft = sqft.split("|")[-1].replace(",","")
                    BaseSqft = re.findall(r"(\d+)", sqft)[0]

                except Exception as e:
                    print(e)
                    BaseSqft=''

                try:

                    # bath = div.xpath('.//../p/text()').extract_first('')
                    bath = div.xpath('.//p[@class="text-align-center"]/text()').extract_first('')
                    bath = bath.split("|")[1].split("|")[0].strip()
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
                    # Bedrooms = div.xpath(".//../p/text()").extract_first('')
                    Bedrooms = div.xpath('.//p[@class="text-align-center"]/text()').extract_first('')
                    # if '-' in Bedrooms:
                    #     Bedrooms = Bedrooms.split("-")[1]
                    Bedrooms = Bedrooms.split("|")[0]
                    Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
                except Exception as e:
                    print(e)
                    Bedrooms = ''


                price = '0'

                try:
                    BasePrice = price
                except Exception as e:
                    print(e)

                try:
                    # Garage = div.xpath(".//../p/text()").extract_first('')
                    Garage = div.xpath('.//p[@class="text-align-center"]/text()').extract_first('')
                    Garage = Garage.split("|")[2].split("|")[0]
                    Garage = re.findall(r"(\d+)", Garage)[0]
                except Exception as e:
                    print(e)
                    Garage = 0


                try:

                    desc = "".join(response.xpath('//div[@class="col sqs-col-12 span-12"]/div/div/p/text()').extract()[1].strip())
                    print(desc)
                    if desc == '' or desc == ' ':
                        desc = "".join(response.xpath('//div[@class="col sqs-col-12 span-12"]/div/div/p/text()').extract()[2])

                    Description = desc
                    # if Description == '':
                    #     Description = 'Bailey Homes is a third generation Northern Nevada home builder. Doug Bailey started Bailey Homes in 1972, building homes in Reno and Lake Tahoe, NV. For the past 40 + years he has helped thousands of families get into a new Bailey home.Bailey Homes is now building quality homes in most areas of Northern Nevada including; Elko, Spring Creek, Lamoille, Carlin, Wells, Battle Mountain, Jiggs, South Fork, Fernley, Reno, Tahoe, and Incline Village.'

                except Exception as e:
                    print(e)

                try:

                    # img1 = div.xpath('.//../../../div[@class="sqs-block image-block sqs-block-image sqs-text-ready"]/div/div/figure/div/img/@data-src').extract_first('')
                    # img1 = div.xpath('.//img[@class="thumb-image"]/@data-src').extract_first('')
                    # print(img1)

                    img1 = div.xpath('//img[@class="thumb-image"]/@data-src').extract_first('')
                    print(img1)
                    images = []
                    imagedata = response.xpath('//div[@class="slide content-fill"]/img/@data-src').getall()
                    if imagedata == []:
                        # imagedata = response.xpath('//img/@data-src').getall()
                        imagedata = response.xpath('//div[@class="sqs-block gallery-block sqs-block-gallery"]//img/@data-src').getall()
                    # imagedata = response.xpath('//div[@class="slide content-fill"]/img/@data-src').getall()

                    for id in imagedata:
                        id = id
                        images.append(id)
                    ElevationImage = "|".join(images)
                    if img1 != '':
                        ElevationImage = ElevationImage + '|' + img1
                    else:
                        ElevationImage = ElevationImage
                except Exception as e:
                    print(e)


                try:
                    PlanWebsite = response.url
                except Exception as e:
                    print(e)

                    # ----------------------- Don't change anything here --------------
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
                item['Description'] = Description
                item['ElevationImage'] = ElevationImage
                item['PlanWebsite'] = PlanWebsite
                yield item
        else:

            div = response.xpath('//div[@class="sqs-block-content"]/h2')
            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                PlanName = response.xpath('//h1/strong/text()').get()
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

            try:
                sqft = div.xpath(".//../p/text()").extract_first('')
                print(sqft)
                sqft = sqft.split("|")[-1].replace(",", "")
                BaseSqft = re.findall(r"(\d+)", sqft)[0]

            except Exception as e:
                print(e)
                BaseSqft = ''

            try:

                bath = div.xpath('.//../p/text()').extract_first('')
                bath = bath.split("|")[1].split("|")[0].strip()
                tmp = re.findall(r"(\d+)", bath)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                print(e)

            try:
                Bedrooms = div.xpath(".//../p/text()").extract_first('')
                Bedrooms = Bedrooms.split("|")[0]
                Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            except Exception as e:
                print(e)
                Bedrooms = ''

            price = '0'

            try:
                BasePrice = price
            except Exception as e:
                print(e)

            try:
                Garage = div.xpath(".//../p/text()").extract_first('')
                Garage = Garage.split("|")[2].split("|")[0]
                Garage = re.findall(r"(\d+)", Garage)[0]
            except Exception as e:
                print(e)
                Garage = 0

            try:

                desc = "".join(response.xpath('//div[@class="col sqs-col-12 span-12"]/div/div/p/text()').extract()[1])
                print(desc)
                if desc == [] or desc == '':
                    desc = 'Bailey Homes is a third generation Northern Nevada home builder. Doug Bailey started Bailey Homes in 1972, building homes in Reno and Lake Tahoe, NV. For the past 40 + years he has helped thousands of families get into a new Bailey home.Bailey Homes is now building quality homes in most areas of Northern Nevada including; Elko, Spring Creek, Lamoille, Carlin, Wells, Battle Mountain, Jiggs, South Fork, Fernley, Reno, Tahoe, and Incline Village.'
                elif '|' in desc:
                    desc = "".join(response.xpath('//div[@class="col sqs-col-12 span-12"]/div/div/p/text()').extract()[0])
                Description = desc
            except Exception as e:
                print(e)

            try:
                img1 = response.xpath('//img[@class="thumb-image"]/@data-src').extract_first('')
                print(img1)
                images = []
                imagedata = response.xpath('//div[@class="slide content-fill"]/img/@data-src').getall()
                for id in imagedata:
                    id = id
                    images.append(id)
                ElevationImage = "|".join(images)
                if img1 != '':
                    ElevationImage = ElevationImage + '|' + img1
                else:
                    ElevationImage = ElevationImage
            except Exception as e:
                print(e)
                ElevationImage = ''

            try:
                PlanWebsite = response.url
            except Exception as e:
                print(e)

                # ----------------------- Don't change anything here --------------
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
            item['Description'] = Description
            item['ElevationImage'] = ElevationImage
            item['PlanWebsite'] = PlanWebsite
            yield item



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl bailey_homesn'.split())