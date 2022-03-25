import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header

class westonhomesSpider(scrapy.Spider):
    name = 'westonhomes'
    allowed_domains = []
    start_urls = ['https://westonhomesinc.com/']
    builderNumber = 21780
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
        item['Street1'] = 'Weston Homes, Inc. 17407 Wild Cherry Lane'
        item['City'] = 'King George'
        item['State'] = 'VA'
        item['ZIP'] = '22485'
        item['AreaCode'] = ''
        item['Prefix'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = 'Weston Homes, Inc. of King George, Virginia has a proven track record of satisfied homeowners! Something needs changing in this next sentence…We’re one of the home builders in the King George, Spotsylvania and Fredericksburg area that you need to talk to, with a demonstrated reputation for quality and performance, we take pride in being competitive without sacrificing quality or workmanship. Weston Homes, Inc. is the professional and trusted local home builder in King George, Virginia that you can rely on and trust.'
        item['SubImage'] = 'https://westonhomesinc.com/wp-content/uploads/2015/02/slide11-1000x478.jpg|https://westonhomesinc.com/wp-content/uploads/2015/02/slide61-1000x478.jpg|https://westonhomesinc.com/wp-content/uploads/2015/02/slide71-1000x478.jpg|https://westonhomesinc.com/wp-content/uploads/2015/02/slide31-1000x478.jpg'
        item['SubWebsite'] = response.url
        yield item

        url = 'https://westonhomesinc.com/homes/'
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.homelink,
                                 meta={'sbdn': self.builderNumber})

    def homelink(self,response):
        # homelinks = response.xpath('//div[@class="entry-content"]/table/tbody/tr/td[2]/p[2]/a/@href').extract()
        # print(homelinks)
        links=re.findall(r'href="(.*?)">More Details</a></td>',response.text)
        print(len(links))
        for homelink in links:
            link = 'https://westonhomesinc.com'+str(homelink)
            print(link)
            yield scrapy.FormRequest(url=str(link),dont_filter= True, callback=self.homedetail, meta={'sbdn': self.builderNumber})

    def homedetail(self,response):
        if response.url == 'https://westonhomesinc.com/homes/clarksville/':
            PlanName = 'Clarksville'
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
            print(PlanNumber)
            f = open("html/%s.html" % PlanNumber, "wb")
            f.write(response.body)
            f.close()
            SubdivisionNumber = response.meta['sbdn']
            PlanNotAvailable = 0
            BasePrice = 0.00
            PlanTypeName = 'Single Family'
            BaseSqft = '2328'
            planbeds = '4'
            planbath = '2'
            planHalfBaths = '1'


            PlanImage = ''
            PlanWebsite = response.url

        try:
            Type = 'SingleFamily'
        except Exception as e:
            Type = 'SingleFamily'
            print(e)

        try:
            PlanName = response.xpath('//div[@class="one-column"]/div/div/h1/text()').extract_first()
            PlanName = re.sub('<[^<]+?>', '', str(PlanName))
            print(PlanName)
        except Exception as e:
            PlanName = ''
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
            print(PlanNumber)
            f = open("html/%s.html" % PlanNumber, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = response.meta['sbdn']
        except Exception as e:
            print(e)

        try:
            PlanNotAvailable = 0
        except Exception as e:
            print(e)

        try:
            BasePrice = 0.00
        except Exception as e:
            print(e)

        try:
            PlanTypeName = 'Single Family'
        except Exception as e:
            print(e)

        try:
            plansquare = response.xpath('//div[@class="entry-content"]/p[6]/span/span/text()').extract_first()
            if PlanName == 'Clarksville':
                plansquare = '2328'
            if PlanName == 'Blackstone':
                plansquare = '2434'
            if plansquare == None or plansquare == '(PDF)':
                plansquare = response.xpath('//div[@class="entry-content"]/p[7]/span[1]/span/text()').extract_first()
            if plansquare == '(PDF)' or plansquare == None:
                plansquare = response.xpath('//div[@class="entry-content"]/p[5]/span/span/text()').extract_first()
            plansquare = re.sub('<[^<]+?>', '', str(plansquare))
            BaseSqft = plansquare.split('sq')[0].strip()
            BaseSqft = BaseSqft.split('x ')[-1]
            BaseSqft = BaseSqft.replace(',','')
            print(BaseSqft)
        except Exception as e:
            print("BaseSqft: ", e)
        try:
            planbeds = response.xpath('//div[@class="entry-content"]/ul/li[1]/text()').get()
            if PlanName == 'Clarksville':
                planbeds = '4'
            planbeds = re.sub('<[^<]+?>', '', str(planbeds))
            planbeds = planbeds.split('s ')[-1]
            print(planbeds)
            if planbeds == '':
                planbeds = 0
        except Exception as e:
            print("planbeds: ", e)
        try:
            planbath = response.xpath('//div[@class="entry-content"]/ul/li[2]/text()').extract_first()
            if PlanName == 'Clarksville':
                planbath = '2.5'

            planbath = re.sub('<[^<]+?>', '', str(planbath))
            planbath = planbath.split('s ')[-1]
            print(planbath)
            # planbath = planbath.split('/')[-1]
            # planbath = planbath.split(' ')[-2]
            if PlanName == 'Clarksville':
                planHalfBaths = '1'
            tmp = re.findall(r"(\d+)", planbath)
            planbath = tmp[0]
            print(planbath)
            if len(tmp) > 1:
                planHalfBaths = 1
                print(planHalfBaths)
            else:
                planHalfBaths = 0
                print(planHalfBaths)
            # print(planbath)
        except Exception as e:
            print("planbath: ", e)
        try:
            # cargarage = response.xpath('//div[@class="entry-content"]/ul/li[3]/text()').extract_first()
            # cargarage = re.sub('<[^<]+?>', '', str(cargarage))
            if PlanName == 'Magnolia Springs':
                cargarage = 3
            elif PlanName == 'Lakeshore':
                cargarage = 0
            elif PlanName == 'River Gate':
                cargarage = 3
            elif PlanName == 'Clarksville':
                cargarage = 1
            else:
                cargarage = 1
            print(cargarage)
        except Exception as e:
            print("cargarage: ", e)
        try:
            # PlanImage = response.xpath('//div[@class="entry-content"]/p/img/@src').extract()
            PlanImage = '|'.join(response.xpath('//*[@class="gallery-item"]//a/@href').extract())
            # PlanImage = 'https://westonhomesinc.com/' + PlanImage
            print(PlanImage)
        except Exception as e:
            print("SpecElevationImage: ", e)
        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)
        try:
            unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
                    10 ** 30)  # < -------- Changes here
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
            item['Baths'] = planbath
            print(item['Baths'])
            item['HalfBaths'] = planHalfBaths
            print(item['HalfBaths'])
            item['Bedrooms'] = planbeds
            item['Garage'] = cargarage
            item['Description'] = 'Weston Homes, Inc. of King George, Virginia has a proven track record of satisfied homeowners! Something needs changing in this next sentence…We’re one of the home builders in the King George, Spotsylvania and Fredericksburg area that you need to talk to, with a demonstrated reputation for quality and performance, we take pride in being competitive without sacrificing quality or workmanship. Weston Homes, Inc. is the professional and trusted local home builder in King George, Virginia that you can rely on and trust.'
            item['ElevationImage'] = PlanImage
            item['PlanWebsite'] = PlanWebsite
            yield item
        except Exception as e:
            print(e)

# execute("scrapy crawl westonhomes".split())