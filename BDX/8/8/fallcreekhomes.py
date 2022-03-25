import scrapy
import re
import os
import hashlib
import scrapy
from scrapy.cmdline import execute

from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision


class FallCreekHomesSpider(scrapy.Spider):
    name = 'fallcreekhomes'
    allowed_domains =[]
    start_urls = ['https://www.homesbyfallcreek.com/']
    builderNumber = 24588

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
        item['Street1'] = '217 Airport North Office Park'
        item['City'] = 'Fort Wayne'
        item['State'] = 'IN'
        item['ZIP'] = '46825'
        item['AreaCode'] = '260'
        item['Prefix'] = '483'
        item['Suffix'] = '6731'
        item['Extension'] = ""
        item['Email'] = 'dkoler@outlook.com'
        item[
            'SubDescription'] = 'Fall Creek Homes is your locally owned, family owned, Fort Wayne custom home builder. Fall Creek Homes leads the way in building uniquely designed new homes with superior craftsmanship. Planning and building your custom Fall Creek home should be fun - not stressful. As a small, locally owned and family-run new home builder right here in Fort Wayne with more than 30 years of experience, we can help you with that.Working with customers to create thoughtfully designed homes with exceptional construction is at the heart of our company.  Let our team guide you!'
        item[
            'SubImage'] = 'https://images.squarespace-cdn.com/content/v1/5bfc8c6796d4551bd7974fbc/1548129132314-01O3N4SW3F88J274CG0A/ke17ZwdGBToddI8pDm48kP8vBXTKsKbKig5xOF_Dllx7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1Ua9nFmCg1khOdFQuAB2QoZwZzbvuhXv1qlIvigxb8OrJlotzjZwTJcqBZZbgS9G89A/1800x1000-home-page-banner.jpg|https://images.squarespace-cdn.com/content/v1/5bfc8c6796d4551bd7974fbc/1543545223531-R6PDBVF9YWHHU2MP0U9Z/ke17ZwdGBToddI8pDm48kLLfwFAJFy9uI_Z8ZHV3qNF7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1USLgHB22VM7ROJKGBx6NfVkIQ74YDUHqVRxQO-QKHyH5Nqcg1uYJ0UckdvGUXVHAnA/1800x1350-light-fixture.jpg'
        item['SubWebsite'] = response.url
        yield item

        link = 'https://www.homesbyfallcreek.com/fall-creek-floor-plans'
        yield scrapy.FormRequest(url=link,callback=self.planLinks,dont_filter=True)

    def planLinks(self,response):
        links = response.xpath('//*[@class="intrinsic"]/a/@href').extract()
        for link in links:
            url = 'https://www.homesbyfallcreek.com'+str(link)
            print(url)
            yield scrapy.FormRequest(url=url,callback=self.plan_links)

    def plan_links(self,response):
        planlinks = response.xpath('//*[contains(text(),"View")]/@href').extract()
        for url1 in planlinks:
            planlink = 'https://www.homesbyfallcreek.com' + str(url1)
            print(planlink)
            yield scrapy.FormRequest(url=planlink,callback=self.planDetail)

    def planDetail(self,response):
        try:
            PlanName = response.xpath('//*[@class="sqs-block-content"]/h2/text()').extract_first()
            print(PlanName)
        except Exception as e:
            print("PlanName: ", e)
        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
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
            Bedroo = response.xpath(
                '//*[@class="sqs-block-content"]/h2[2]/text()').extract_first().strip()
            Bedroom = Bedroo.split('|')[1]
            Bedrooms = re.findall(r"(\d+)", Bedroom)[0]
            Bedrooms = Bedrooms.strip()

        except Exception as e:
            Bedrooms = 0
            print("Bedrooms: ", e)

        try:
            Bathroo = response.xpath(
                '//*[@class="sqs-block-content"]/h2[2]/text()').extract_first().strip()
            Bathroom = Bathroo.split('|')[2]
            # Baths = Bathroom.split(' bath,')
            tmp = re.findall(r"(\d+)", Bathroom)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0

        except Exception as e:
            Baths = 0
            print("Baths: ", e)
        0

        Garage = 0
        try:
            BaseSqft = response.xpath(
                '//*[@class="sqs-block-content"]/h2[2]/text()').extract_first().strip().replace(',', '')
            if  PlanName == 'FALCON CREST I':
                BaseSqft = '1393'
            if "|" in BaseSqft:
                BaseSqf = BaseSqft.split('|')[0]
                BaseSqft = ''.join(re.findall(r"(\d+)", BaseSqf))
                BaseSqft = BaseSqft.strip()
            print(BaseSqft)
        except Exception as e:
            print("BaseSQFT: ", e)

        try:
            a = response.text
            ElevationImage = '|'.join(re.findall(r'<img src="(.*?)" alt="',a))
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
        item[
            'Description'] = 'We have access to building sites, in nearly every development in the area! Bring us your custom home plans or choose from one of the many popular plans in our library. Click one of the thumbnails below for a PDF sheet with full details.'
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item

# execute("scrapy crawl fallcreekhomes".split())