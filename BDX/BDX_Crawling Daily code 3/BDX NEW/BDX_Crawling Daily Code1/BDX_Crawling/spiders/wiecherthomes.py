

import hashlib
import re
import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class autumnhomeSpider(scrapy.Spider):
    name ='wiecherthomes'
    allowed_domains = []
    start_urls = ['https://www.autumnhomesinc.com/']

    builderNumber = "51333"

    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

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
        item['Street1'] = '3073 Skyview Lane'
        item['City'] = 'Eugene'
        item['State'] = 'OR'
        item['ZIP'] = '97405'
        item['AreaCode'] = ''
        item['Prefix'] =''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] =''
        item['SubDescription'] = "Bruce Wiechert Custom Homes, Inc has been building unique and beautiful homes in Lane County for over 20 years.Each home is crafted with imagination, attention to quality and a commitment to provide excellent service to our homeowners. Our motto,We don't build for friends...it just ends up that way,is a tribute to how we feel about our customers."
        item['SubImage']= "https://images.squarespace-cdn.com/content/v1/5845e37c03596e15cdfc795f/1483663906894-SOLN60AIPCUZGJOG7QU5/544+Wedgewood+Dr+Eugene+OR+97404_large-001.jpg?format=750w|https://images.squarespace-cdn.com/content/v1/5845e37c03596e15cdfc795f/1483663921894-F7A54MAVDL0JVVGMFWCF/801+SW+Quince_large-18.jpg?format=750w|https://images.squarespace-cdn.com/content/v1/5845e37c03596e15cdfc795f/1483663976972-SMNBBTRH9LVXE5FNO79R/877+Oakway+Rd+Eugene+OR+97401_large-001.jpg?format=750w|https://images.squarespace-cdn.com/content/v1/5845e37c03596e15cdfc795f/1483664001761-TYNKRN1YNTYW7JT23QB1/947+Riverstone_large-001.jpg?format=750w|https://images.squarespace-cdn.com/content/v1/5845e37c03596e15cdfc795f/1483664028389-0DZVQDZ3CK8KV40RA7EG/951+Pennington_large-001.jpg?format=750w"
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link = 'https://www.wiecherthomes.com/models-floorplans'
        yield scrapy.FormRequest(url=link,callback=self.plan_links,dont_filter=True)

    def plan_links(self,response):
        links = response.xpath('//div[@class="summary-title"]/a/@href').extract()
        for link in links:
            link = 'https://www.wiecherthomes.com' + link
            yield scrapy.FormRequest(url=link,callback=self.plans,dont_filter=True)

    def plans(self,response):
        try:
            Type = 'SingleFamily'
        except Exception as e:
            Type = 'SingleFamily'
            print(e)

        try:
            PlanName = response.xpath('.//h2//text()').extract()[0].strip()
        except Exception as e:
            PlanName = ''
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
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
            BasePrice = 0.00
        except Exception as e:
            print(e)

        try:
            BaseSqft = response.xpath("//h3[contains(text(),'bed')]/text()").extract_first(default='0')
            BaseSqft = BaseSqft.split('·')[2].strip()
            BaseSqft = BaseSqft.replace(',', '')
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]

        except Exception as e:
            print(e)

        try:
            Baths = response.xpath("//h3[contains(text(),'bed')]/text()").extract_first(default='0')
            Baths = Baths.split("·")[1]
            Baths = Baths.split("·")[0]
            Baths = re.findall(r"(\d+)", Baths)[0]
            print(Baths)
            if len(Baths) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0

        except Exception as e:
            Baths = 0
            print(e)

        try:
            Bedrooms = response.xpath("//h3[contains(text(),'bed')]/text()").extract_first(default='0')
            Bedrooms = Bedrooms.split("·")[0]
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)
            Bedrooms = 0

        try:
            gara = "".join(response.xpath('//div[@class="sqs-block-content"]//p/text()').extract())
            Garage = re.findall(r"(\d*[three]*[four]*[two]*)[ ]*[-]*car garage", gara.lower())[0]
            Garage = Garage.replace("three", "3").replace("four", "4").replace("two", "2")
            Garage = re.findall(r"(\d+)", Garage)[0]

        except Exception as e:
            print(e)
            Garage = 0

        try:
            Description = ''
        except Exception as e:
            print(e)

        try:
            ElevationImage = response.xpath('//figure[@class="loading content-fill"]/img/@data-src').extract_first(default='')
        except Exception as e:
            print(e)
            ElevationImage = ""

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

        # ----------------------- Don't change anything here --------------
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
        item['Description'] = Description
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl wiecherthomes".split())