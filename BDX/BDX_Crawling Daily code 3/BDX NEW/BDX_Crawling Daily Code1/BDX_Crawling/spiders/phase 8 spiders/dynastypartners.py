import hashlib
import re
import scrapy
import requests
import soup as soup
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header
from bs4 import BeautifulSoup

class DynastyPartnersSpider(scrapy.Spider):
    name = 'dynastypartners'
    allowed_domains = []
    start_urls = ['https://www.dynastypartners.com/']
    builderNumber = 49173

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
        item['Street1'] = 'PO Box 373 Johnston, '
        item['City'] = 'Johnston'
        item['State'] = 'IA'
        item['ZIP'] = '50131'
        item['AreaCode'] = '515'
        item['Prefix'] = '707'
        item['Suffix'] = '8343'
        item['Extension'] = ""
        item['Email'] = 'scott@dynastypartners.com'
        item[
            'SubDescription'] = 'From design to finish, our reputation is built on trust.  When you build your new custom home with Dynasty, you get the highest level of service, true custom design and unmatched construction quality.Building your dream home begins just like any other dream; with imagination and creativity.  Of course, bringing dreams to life requires more than just imagination.  It takes planning and hard work.  At Dynasty Partners we ask ourselves what kind of community do you dream to live in, how will your home look and how will it function for you and your family.  It is as important to us as it is to you which is why we are the premier custom home builder in Des Moines.'
        item[
            'SubImage'] = 'https://static.wixstatic.com/media/6fbf59_0c47a39038d24ee3b1203bb90a84075e~mv2.jpg/v1/fill/w_1599,h_1057,al_c/6fbf59_0c47a39038d24ee3b1203bb90a84075e~mv2.jpg|https://scontent-iad3-1.cdninstagram.com/v/t51.29350-15/118187019_123806896095601_495590002224343888_n.jpg?_nc_cat=100&_nc_sid=8ae9d6&_nc_ohc=pPN2hKdt-vYAX-anVH3&_nc_ht=scontent-iad3-1.cdninstagram.com&oh=9230bc223704c9aede117a70dc8ad8c0&oe=5F86AAC9|https://scontent-iad3-1.cdninstagram.com/v/t51.29350-15/118119127_607543199906384_1436856064726194414_n.jpg?_nc_cat=104&_nc_sid=8ae9d6&_nc_ohc=bCaxdgxXboAAX9_XSdf&_nc_ht=scontent-iad3-1.cdninstagram.com&oh=8bc1989ac67c5db8d1913ba84b436b00&oe=5F87B071|https://scontent-iad3-1.cdninstagram.com/v/t51.29350-15/117931678_1470865016431871_4611913324519880080_n.jpg?_nc_cat=108&_nc_sid=8ae9d6&_nc_ohc=qd_srqGTkbEAX-L1v3b&_nc_ht=scontent-iad3-1.cdninstagram.com&oh=f6a2162c6a79db4d9604c89738845167&oe=5F89B151|https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/97172852_237146234378120_2150597738507193509_n.jpg?_nc_cat=107&_nc_sid=8ae9d6&_nc_ohc=rvcSQAh4IZUAX_D_DQi&_nc_ht=scontent-iad3-1.cdninstagram.com&oh=74cc9e24393db847ba00eb52b52d6230&oe=5F8A8557'
        item['SubWebsite'] = response.url
        yield item

        planLink = 'https://www.dynastypartners.com/plans'
        yield scrapy.FormRequest(url=planLink,callback=self.planDetail)

    def planDetail(self,response):
        divs = response.xpath('//div[@class="style-k1za8iqninlineContent"]/div/div')
        print(len(divs))
        for div in divs:
            try:
                PlanName = div.xpath('.//*[@class="font_2"]/span/span/span/span/span/text()').extract_first()
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
                Bedroo = div.xpath(
                    './/*[contains(text(),"Bedrooms")]/text()').extract_first().strip()
                print(Bedroo)
                Bedroom = Bedroo.split(',')[0]
                Bedrooms = re.findall(r"(\d+)", Bedroom)[0]
                # Bedrooms = Bedroom.split(' Bed')[0].strip()

            except Exception as e:
                Bedrooms = 0
                print("Bedrooms: ", e)

            try:
                Bathroo = div.xpath(
                    './/*[contains(text(),"Baths")]/text()').extract_first().strip()
                print(Bathroo)
                Baths = Bathroo.split(',')[1]
                tmp = re.findall(r"(\d+)",Baths)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0

            except Exception as e:
                Baths = 0
                print("Baths: ", e)

            Garage = 0
            try:
                BaseSqft = div.xpath(
                    './/*[contains(text(),"Total Sq. Ft.")]/../../../../../div[6]/p/span/span/span/text()').extract_first().strip().replace(',', '')
                BaseSqft = re.findall(r"(\d+)",BaseSqft)[0]
                if len(BaseSqft) == 3:
                    BaseSqft = BaseSqft + '0'
            except Exception as e:
                print("BaseSQFT: ", e)

            try:
                ElevationImage = div.xpath('//*[@class="style-k1zc62belink"]/wix-image/img/@src').extract_first().split('/v1/')[0]
                print(ElevationImage)
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
            item['Description'] = 'We have access to building sites, in nearly every development in the area! Bring us your custom home plans or choose from one of the many popular plans in our library. Click one of the thumbnails below for a PDF sheet with full details.'
            item['ElevationImage'] = ElevationImage
            item['PlanWebsite'] = PlanWebsite
            yield item
# execute("scrapy crawl dynastypartners".split())