import hashlib
import re

import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan


class YourgeminihomesSpider(scrapy.Spider):
    name = 'yourgeminihomes'
    allowed_domains = ['www.yourgeminihomes.com']
    start_urls = ['http://www.yourgeminihomes.com']
    builderNumber = '26148'

    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '1685 Pleasant Hill Rd'
        item['City'] = 'Bowling Green'
        item['State'] = 'KY'
        item['ZIP'] = '42103'
        item['AreaCode'] = '270'
        item['Prefix'] = '782'
        item['Suffix'] = '8893'
        item['Extension'] = ""
        item['Email'] = 'href="kelly@yourgeminihomes.com"'
        item[
            'SubDescription'] = 'Gemini Homes is a custom home builder located in Bowling Green, KY. We specialize in building quality homes that fulfill your exact specifications. In addition to custom home design'


        item[
            'SubImage'] = 'http://www.yourgeminihomes.com/images/KY-GC-4-768x510.jpg'
        item['SubWebsite'] = response.url
        yield item

        try:
            link = response.xpath('//a[contains(text(),"Home Plans")]/@href').get()

            link = 'http://www.yourgeminihomes.com/' + str(link)
            yield scrapy.Request(url=link, callback=self.parse_planlink, dont_filter=True)
        except Exception as e:
            print(e)

    def parse_planlink(self, response):

        plannames = response.xpath('//div[@align="left"]//h2/text()').getall()
        beds = response.xpath('//div[@align="left"]//*[contains(text(),"Bedrooms")]/text()').getall()
        baths = response.xpath('//div[@align="left"]//li[2]')
        Baths = []
        for i in baths:
            bath = i.xpath('.//text()').getall()
            for b in bath:
                if len(bath)>1:

                    Bath = " ".join(bath)
                    Baths.append(Bath)

                else:

                    Baths.append(b)

                print(Baths)
        # baths = response.xpath('//div[@align="left"]//*[contains(text(),"Baths")]/text()').getall()
        sqfts = response.xpath('//div[@align="left"]//li[3]/text()').getall()
        # feet = response.xpath('//div[@align="left"]//li[3][contains(text(),"Sq Ft")]/text()').getall()
        # sqfts.append(feet)
        images = response.xpath('//div[@align="left"]//img/@src').getall()


        for planname,bed,bath,sqft,image in zip(plannames,beds,Baths,sqfts,images):
            print((beds))
            print((Baths))
            print((plannames))
            print((sqfts))
            print((images))
            item = BdxCrawlingItem_Plan()

            item['PlanName'] = planname
            item['Bedrooms'] = re.findall(r'(\d+)',bed)[0].strip()
            bathrooms = re.findall(r'(\d+)',bath.replace('2 -1/2','2.5').replace('2-1/2','2.5').replace(' -1/2','.5'),)
            print(bathrooms)
            tmp = bathrooms[0]
            item['Baths'] = tmp


            if len(bathrooms) > 1:
                item['HalfBaths'] = 1
            else:
                item['HalfBaths'] = 0
            if item['PlanName'] == 'The Payton':
                item['Baths'] = 3
                item['HalfBaths'] = 0

            item['BaseSqft'] = re.findall(r'(\d+)',sqft.replace(',',''))[0].strip()
            item['ElevationImage'] = 'http://www.yourgeminihomes.com/' + str(image)
            item['Description'] = 'Another plan with a grand entrance & formal dining room!  Great plan with that extra bedroom & bath downstairs for any desired room.  The upstairs has great play rooms'

            try:
                PlanNumber = int(hashlib.md5(bytes(planname, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % PlanNumber, "wb")
                f.write(response.body)
                f.close()

                SubdivisionNumber = self.builderNumber  # if subdivision is there
                # SubdivisionNumber = self.builderNumber #if subdivision is not available
                unique = str(PlanNumber) + str(SubdivisionNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

                item['PlanNumber'] = PlanNumber
                item['unique_number'] = unique_number
                item['SubdivisionNumber'] = SubdivisionNumber

            except Exception as e:
                print(e)

            item['Type'] = 'SingleFamily'
            item['PlanNotAvailable'] = 0
            item['PlanTypeName'] = 'Single Family'
            item['BasePrice'] = 0
            item['Garage'] = 0
            item['PlanWebsite'] = response.url
            yield item

from scrapy.cmdline import execute
# execute("scrapy crawl yourgeminihomes".split())




