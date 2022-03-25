import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header

class HardingFomesSpider(scrapy.Spider):
    name = 'hardinghomes'
    allowed_domains = []
    start_urls = ['https://www.hardinghomesak.com/']

    builderNumber = 27872

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
        item['Street1'] = '5771 Heritage Heights Dr'
        item['City'] = 'Anchorage'
        item['State'] = 'AK'
        item['ZIP'] = '99516'
        item['AreaCode'] = '907'
        item['Prefix'] ='337'
        item['Suffix'] = '9109'
        item['Extension'] = ""
        item['Email'] ='harding@gci.net'
        item['SubDescription'] ="Harding Homes Of Alaska's friendly and knowledgeable team is ready to handle every part of the construction process for you. From building permits to the bathroom sink our team has risen to every challenge.  We've been building custom homes for residents of the Anchorage since 1998.  Over the years our mission is to make the building process as stress-free as possible. Attention to detail is critical and begins and ends with open communication between our clients and contractors.  We're dedicated to providing our clients with guidance at every phase of the project, from the cost-free estimate to the final walk-through. We're committed to making sure our customers enjoy every moment of creating their custom-built home, and that's why Harding Homes Of Alaska is your premier home builder."
        item['SubImage']= 'https://static.wixstatic.com/media/05aefe_95e287eec0034c35ac36cb985161cd6e.jpg/v1/fill/w_536,h_402,al_c,q_80,usm_0.66_1.00_0.01/05aefe_95e287eec0034c35ac36cb985161cd6e.jpg|https://static.wixstatic.com/media/05aefe_d958d7691e344c89a9b7f6ad8d6ee562.jpg/v1/fill/w_268,h_201,al_c,q_80,usm_0.66_1.00_0.01/05aefe_d958d7691e344c89a9b7f6ad8d6ee562.jpg|https://static.wixstatic.com/media/05aefe_418213794b474126b9205510ec6ef02c.jpg/v1/fill/w_268,h_201,al_c,q_80,usm_0.66_1.00_0.01/05aefe_418213794b474126b9205510ec6ef02c.jpg|https://static.wixstatic.com/media/05aefe_30569607bcc249f7abdfaa8258d4193f.jpg/v1/fill/w_268,h_201,al_c,q_80,usm_0.66_1.00_0.01/05aefe_30569607bcc249f7abdfaa8258d4193f.jpg|https://static.wixstatic.com/media/05aefe_883365f812064cb08577a7dc74f99141.jpg/v1/fill/w_268,h_201,al_c,q_80,usm_0.66_1.00_0.01/05aefe_883365f812064cb08577a7dc74f99141.jpg'
        item['SubWebsite'] = response.url
        yield item

        planlink = 'https://www.hardinghomesak.com/plans'
        yield scrapy.FormRequest(url=planlink,callback=self.plan_links)

    def plan_links(self,response):
        links = response.xpath('//*[@class="wp2link"]/@href').extract()
        for link in links:
            # print(link)
            # a = 'https://www.hardinghomesak.com/copy-of-paxson'
            yield scrapy.FormRequest(url=link,callback=self.planDetail)

    def planDetail(self,response):
        print(response.url)
        try:
            PlanName = response.xpath('//*[@class="txtNew"]/h2/span/text()').extract_first().strip()
            if 'Car Garage' in PlanName:
                PlanName = response.xpath('//*[@class="txtNew"]/h2/text()').extract_first().strip()
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
            Bedrooms = response.xpath('//*[contains(text(),"Bedroom")]/text()').extract_first()
            Bedrooms = re.findall(r"(\d+)",Bedrooms)[0]
            print(Bedrooms)
        except Exception as e:
            Bedrooms = 0
            print("Bedrooms: ", e)

        try:
            Bathroom = response.xpath('//*[contains(text(),"Bathroom")]/text()').extract_first()
            if PlanName == 'SUMMIT II':
                Bathroom = '3'

            if Bathroom ==  None:
                Bathroom = response.xpath('//*[contains(text(),"Baths")]/text()').extract_first()
                Baths = str(Bathroom.split(' Baths')[0].split(',')[-1]).strip()
                tmp = re.findall(r"(\d+)", Baths)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0

                print(Baths)
            Baths =  Bathroom.split('Bathroom')[0].split(',')[-1]
            tmp = re.findall(r"(\d+)", Baths)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0

        except Exception as e:
            Baths = 0
            print("Baths: ", e)

        try:
            Garage = response.xpath('//*[contains(text(),"Bathroom")]/text()').extract_first()
            if Garage ==  None:
                Garage = response.xpath('//*[contains(text(),"Baths")]/text()').extract_first()
                Garage =  Garage.split(',')[-2]
            Garage = re.findall(r"(\d+)", Garage)[0]
        except Exception as e:
            Baths = 0
            print("Baths: ", e)


        try:
            BaseSqft = response.xpath('//*[contains(text(),"Approx.")]/../text()[2]').extract_first()
            print(BaseSqft)
            if PlanName == "TURNAGAIN":
                BaseSqft = '2800'
            elif PlanName == "SUMMIT II":
                BaseSqft = '3950'
            elif '4000 sqft + 2000 sqft shop' in BaseSqft:
                BaseSqft = '4000'
            elif BaseSqft == None:
                BaseSqft = response.xpath('//*[@class="txtNew"]/h2/span/text()').extract_first()
            elif '2600sqft w/1400sqft' in BaseSqft:
                BaseSqft = '2600'
            elif BaseSqft == '':
                BaseSqft = response.xpath('//*[@class="txtNew"]/h2/span/span/span/text()[2]').extract_first()
            elif 'Car Garage.' in BaseSqft:
                BaseSqft = response.xpath('//*[@class="txtNew"]/h2/span/span/text()[2]').extract_first()
            print(BaseSqft)
            BaseSqft = BaseSqft.split('Approx.')[-1]
            BaseSqft = ''.join(re.findall(r"(\d+)",BaseSqft))
            BaseSqft = BaseSqft.strip()
            print(BaseSqft)
        except Exception as e:
            print("BaseSQFT: ", e)

        try:
            ElevationImage = re.findall('<img src="(.*?)"',response.text)
            ElevationImage = "|".join(ElevationImage)
            print(ElevationImage)

        except Exception as e:
            print(str(e))

        # try:
        #     ElevationImage = re.findall('url(\(.*?)\)', response.text)
        #     print(len(ElevationImage))
        #     ElevationImage = '|'.join(ElevationImage).replace(')', '').replace('(', '')
        #     ElevationImage = ElevationImage.strip('|')
        # except Exception as e:
        #     ElevationImage = ''

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
        item[
            'Description'] = 'We have access to building sites, in nearly every development in the area! Bring us your custom home plans or choose from one of the many popular plans in our library. Click one of the thumbnails below for a PDF sheet with full details.'
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item

if __name__ == '__main__':
    execute("scrapy crawl hardinghomes".split())

