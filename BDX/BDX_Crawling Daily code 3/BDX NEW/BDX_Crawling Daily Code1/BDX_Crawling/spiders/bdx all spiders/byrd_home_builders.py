# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from scrapy.cmdline import execute
from scrapy.utils.response import open_in_browser

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class byrdhomebuildersSpider(scrapy.Spider):
    name = 'byrd_home_builders'
    allowed_domains = ['www.byrdhomebuildersinc.com/']
    start_urls = ['http://www.byrdhomebuildersinc.com/']
    builderNumber = "53945"

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
        item['Street1'] = '11211 Hwy 43 North Axis'
        item['City'] = 'Creola'
        item['State'] = 'Al'
        item['ZIP'] = '36505'
        item['AreaCode'] = '251'
        item['Prefix'] ='675'
        item['Suffix'] = '0245'
        item['Extension'] = ""
        item['Email'] ='paulapbyrd@bellsouth.net'
        item['SubDescription'] ='The staff at Byrd Home Builders were very professional and friendly. They treated us very well. We always understood that they felt that they were not just building a house for us - they were building a place that we would call home. Our home is high quality and we appreciate Byrd Home Builders'
        item['SubImage']= 'http://www.byrdhomebuildersinc.com/images/svss_gardening.jpg|http://www.byrdhomebuildersinc.com/images/Abby_CrackingUpSwinging.jpg|http://www.byrdhomebuildersinc.com/images/images.jpg|http://www.byrdhomebuildersinc.com/models/Images/logo.png|http://www.byrdhomebuildersinc.com/images/MattSwinging-m.jpg|http://www.byrdhomebuildersinc.com/ROSE%20WEAVER%20FRONT.jpg|http://www.byrdhomebuildersinc.com/image001.gif|http://www.byrdhomebuildersinc.com/SPEC2.JPG'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        url = 'http://www.byrdhomebuildersinc.com/models/models.htm'
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.parse_planlink,
                                 meta={'sbdn': self.builderNumber})


    def parse_planlink(self,response):

        try:
            links = response.xpath('//td[@width="786"]//p/a/@href').extract()
            plandetains = {}
            for link in links:
                yield scrapy.Request(url="http://www.byrdhomebuildersinc.com/models/" + str(link),callback=self.plans_details, meta={'sbdn':self.builderNumber,'PlanDetails':plandetains},dont_filter=True)
                # yield scrapy.Request(url="http://www.byrdhomebuildersinc.com/models/rockford.htm",callback=self.plans_details, meta={'sbdn':self.builderNumber,'PlanDetails':plandetains},dont_filter=True)
        except Exception as e:
            print(e)

    def plans_details(self,response):
        item = BdxCrawlingItem_Plan()
        plandetails = response.meta['PlanDetails']

        try:
            Type = 'SingleFamily'
            item['Type'] = Type
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = response.meta['sbdn']
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//u/b/font/text()').extract_first(default='').strip()
            print(PlanName)
        except Exception as e:
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
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
            BasePrice = '0'
        except Exception as e:
            print(e)


        try:
            Baths = str(response.xpath('//div/p[2]//*[contains(text(),"bath")]/text()').extract_first(default='0').strip()).replace(",", "").replace("\n","")
            print(Baths)
            bath=Baths.split(' baths')[0].replace("2 1/2","2.5")
            # bath=Baths.split('\tbaths')[0].replace("\r","").replace("\t","").strip()
            bath1=bath.split(" ")[-1]
            tmp = re.findall(r"(\d+)", bath1)
            if tmp == []:
                bath = Baths.split(' bath')[0]
                bath1 = bath.split(" ")[-1]
                tmp = re.findall(r"(\d+)", bath1)
                if tmp == []:
                    bath = Baths.split(' full baths')[0]
                    bath1 = bath.split(" ")[-1]
                    tmp = re.findall(r"(\d+)", bath1)
                    if tmp == []:
                        bath = Baths.split('\tbaths')[0].replace("\r", "").replace("\t", "").strip()
                        bath1 = bath.split(" ")[-1]
                        tmp = re.findall(r"(\d+)", bath1)
            Baths = tmp[0]
            print(Baths)
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            print(e)

        try:
            Bedrooms = str(response.xpath('//div/p[2]//*[contains(text(),"bedroom")]/text()').extract_first(default='0').strip()).replace(",", "")
            bedroom=Bedrooms.split(' bedroom')[0]
            # if bedroom == '0':
                # bedroom = Bedrooms.split(' Bedroom')[0]
            bedroom1=bedroom.split(" ")[-1]
            print(bedroom1)
            Bedrooms = re.findall(r'(\d+)',bedroom1)[0]

            if Bedrooms == '0':
                Bedrooms = str(response.xpath('//div/p[2]//*[contains(text(),"Bedroom")]/text()').extract_first(
                    default='0').strip()).replace(",", "").replace("\r", "").replace("\t", "").replace("\n","").strip()
                bedroom = Bedrooms.split(' Bedroom')[0]
                # if bedroom == '0':
                # bedroom = Bedrooms.split(' Bedroom')[0]
                bedroom1 = bedroom.split(" ")[-1]
                print(bedroom1)
                Bedrooms = re.findall(r'(\d+)', bedroom1)[0]
        except Exception as e:
            print(e)

        try:

            Garage = 0.00

            BaseSqft = str(response.xpath('//td[@bgcolor="#C9C994"]/div/div/div/p/font/text()').extract_first(default='0').strip()).replace(",", "")

            if not BaseSqft:
                BaseSqft = str(response.xpath('normalize-space(//*[contains(text(),"Living Sq. Ft.")]/following-sibling::text())').extract_first(default='0').strip()).replace(",", "")
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
            print(BaseSqft)
        except Exception as e:
            print(e)

        try:

            Description = response.xpath('normalize-space(//div/p[2]//*[contains(text(),"")])').extract_first(default='').strip()
            # Description = re.sub('<[^<]+?>', '',str(Description))
            print(Description)

            if not Description:
                Description=response.xpath('normalize-space(//div/p/b/*[contains(text(),"")])').extract_first(default='').strip()
                # Description= re.sub('<[^<]+?>', '',str(Description))
                print(Description)
        except Exception as e:
            print(e)

        try:
            # ElevationImage = response.xpath('//td[@bgcolor="#C9C994"]/div/div/div/div/p/img/@src').getall()
            # for i in ElevationImage:
            #     ElevationImage = ''.join('http://www.byrdhomebuildersinc.com/models/' + str(i))
            #     ElevationImage = ElevationImage.strip('|')
            #     print(ElevationImage)
            #
            # if not ElevationImage:
            #     ElevationImage = response.xpath('//td[@bgcolor="#C9C994"]/div/div/div/div/div/img/@src').getall()
            #     for i in ElevationImage:
            #         ElevationImage = ''.join('http://www.byrdhomebuildersinc.com/models/' + str(i))
            #         ElevationImage = ElevationImage.strip('|')
            #         print(ElevationImage)
            #
            #     if not ElevationImage:
            #         ElevationImage = response.xpath('//div[@align="center"]//@src').getall()
            #         for i in ElevationImage:
            #             ElevationImage = ''.join('http://www.byrdhomebuildersinc.com/models/' + str(i))
            #             ElevationImage = ElevationImage.strip('|')
            #             print(ElevationImage)
            ElevationImage = response.xpath('//div[@align="center"]//@src').getall()
            for i in ElevationImage:
                ElevationImage = ''.join('http://www.byrdhomebuildersinc.com/models/' + str(i))
                ElevationImage = ElevationImage.strip('|')
                print(ElevationImage)


            ElevationImage2 = response.xpath('//div[@align="center"]/div[@align="center"]/div[@align="center"]/div[@align="center"]//img/@src').extract_first('')
            if ElevationImage2 != '':
                ElevationImage2 = 'http://www.byrdhomebuildersinc.com/models/' + ElevationImage2
                ElevationImage = ElevationImage + '|' + ElevationImage2

            else:
                ElevationImage = ElevationImage


        except Exception as e:
            print(e)

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

        SubdivisionNumber = SubdivisionNumber #if subdivision is there
        #SubdivisionNumber = self.builderNumber #if subdivision is not available
        unique = str(PlanNumber)+str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        plandetails[PlanName] = unique_number


        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
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
    execute('scrapy crawl byrd_home_builders'.split())
