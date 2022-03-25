import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header


class FireSideSpider(scrapy.Spider):
    name = 'fireside'
    allowed_domains = []
    start_urls = ['http://firesidehomes.com/']
    builderNumber = 24902

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
        item['Street1'] = '50 WEST SEMINOLE DRIVE'
        item['City'] = 'VENICE'
        item['State'] = 'FL'
        item['ZIP'] = '34293'
        item['AreaCode'] = '941'
        item['Prefix'] = '493'
        item['Suffix'] = '7931'
        item['Extension'] = ""
        item['Email'] = 'Skip@FiresideHomes.com'
        item['SubDescription'] = 'Quality materials, attention to detail and painstaking craftsmanship make Fireside homes a cut above the competition. Each home is uniqiely constructed to fit the needs and tastes of its owners. If you are in the market for a new home, check out what Fireside homes can create for you and your family.'
        item[
            'SubImage'] = 'http://firesidehomes.com/images/slideshow/Blocks.jpg|http://firesidehomes.com/images/photos/Model/Front-Model.jpg|http://firesidehomes.com/images/photos/Model/Kitchen.JPG|http://firesidehomes.com/images/photos/Model/Living%20Rm.JPG|http://firesidehomes.com/images/photos/Model/Den.JPG'
        item['SubWebsite'] = response.url
        yield item

        links = ['http://firesidehomes.com/pages/mccall.html','http://firesidehomes.com/pages/otherModels.html']
        for link in links:
            print(link)
            yield scrapy.FormRequest(url=link, callback=self.planLinks, dont_filter=True)

    def planLinks(self,response):
        a = response.text
        sqfts = response.xpath('//*[@align="center"]/table//tr/td[4]/div/text()').extract()
        beds = response.xpath('//*[@align="center"]/table//tr/td[5]/div/text()').extract()
        bedrooms = []
        for i in beds:
            if 'Room' not in i:
                tmp = re.findall(r"(\d+)", i)[0]
                i = tmp.strip().replace('\n','').replace('Family','').replace('+','').replace('    ','')
                bedrooms.append(i)
        baths = response.xpath('//*[@align="center"]/table//tr/td[6]/div/text()').extract()
        links = response.xpath('//*[@align="center"]/table//tr/td[2]/div/a/@href').extract()
        for sqft,bedroom,bath,link in zip(sqfts,bedrooms,baths,links):
            print(sqft,bedroom,bath,link)

        # b = re.findall(r'<td><div align="center"><a href="(.*?)">(.*?)</a>',a,re.DOTALL)
        # for pna in b:
        #     pnam = pna[1].strip()
        #     pname = pnam.replace('<br />\n','').strip().replace('         ',' ')
        #     plinks = pna[0]
        #     link = 'http://firesidehomes.com/pages/' + str(plinks)
        # plinks = re.findall(r'  <td><a href="(.*?)"><img',a)
        # for plink in plinks:
            # link = 'http://firesidehomes.com/pages/'+str(plink)
            # print(link)
            yield scrapy.FormRequest(url="http://firesidehomes.com/pages/"+str(link),callback=self.planDetail,dont_filter=True,meta={'sqft':sqft,'bed':bedroom,'bath':bath})

    def planDetail(self,response):
        print(response.url)
        try:
            PlanName = str(response.url).split('/')[-1].replace('.html','')
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
            Bedrooms = response.meta['bed']
            # Bedroom = Bedroo.split('|')[1]
            #Bedrooms = re.findall(r"(\d+)", Bedroom)[0]
            #Bedrooms = Bedrooms.strip()

        except Exception as e:
            Bedrooms = 0
            print("Bedrooms: ", e)

        try:
            Bathroom = response.meta['bath']
            # Bathroom = Bathroo.split('|')[2]
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



        try:
            Garage = 0
        except Exception as e:
            Garage = 0
            print("Garage: ", e)
        try:
            BaseSqft = response.meta['sqft']
            print(BaseSqft)
        except Exception as e:
            print("BaseSQFT: ", e)

        try:
            ElevationImage = []
            b1 = response.xpath("//*[contains(@src,'../images/floorPlans')]/@src").extract_first().replace('..','')
            b2 = response.xpath("//*[contains(@src,'../images/Rendering')]/@src").extract_first().replace('..','')
            b = "http://firesidehomes.com" + b1
            c = "http://firesidehomes.com" + b2
            ElevationImage.append(b)
            ElevationImage.append(c)
            ElevationImage = "|".join(ElevationImage)
            # ElevationImage = '|'.join(re.findall(r'<img src="(.*?)" alt="',a))
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


# execute("scrapy crawl fireside".split())