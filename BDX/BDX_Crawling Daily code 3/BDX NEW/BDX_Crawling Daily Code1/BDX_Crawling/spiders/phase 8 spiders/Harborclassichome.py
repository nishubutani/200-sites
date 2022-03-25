import hashlib
import re

import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class harborclasic(scrapy.Spider):
    name = 'harborclasic'
    allowed_domains = []
    start_urls = ['https://harborclassichomes.com/community/']

    builderNumber = "51938"

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
        item['Street1'] = '493 Lancaster Street,Suite 1'
        item['City'] = 'Leominster'
        item['State'] = 'MA'
        item['ZIP'] = '01453'
        item['AreaCode'] = '978'
        item['Prefix'] = '751'
        item['Suffix'] = '8257'
        item['Extension'] = ""
        item['Email'] = 'HarborClassicHomes@gmail.com'
        item['SubDescription'] = "For over 20 years, Harbor Classic Homes has had the privilege of being an exceptional home builder in central Massachusetts. Our goal is simple – to build you the home of your dreams with craftsman style quality and unparalleled professionalism."
        item['SubImage'] = 'https://harborclassichomes.com/wp-content/uploads/2018/06/Header_Cardinal-I.jpg'
        item['SubWebsite'] = response.url
        yield item

        pl = "https://harborclassichomes.com/listings/"
        yield scrapy.FormRequest(url=pl, callback=self.plan_link_page, dont_filter=True)

    def plan_link_page(self,response):
        link=response.xpath('//main[@class="content"]//a[@class="more-link"]/@href').extract()
        for i in link:
            url= i
            yield scrapy.FormRequest(url=url, callback=self.plandata, dont_filter=True)

    def plandata(self,response):
        s=response.url
        info=response.text

        name = re.findall('<title>(.*?)-',info)[0].strip()
        print(name)

        PlanNumber = int(hashlib.md5(bytes(str(name), "utf8")).hexdigest(), 16) % (10 ** 30)


        bath= re.findall('<strong>Baths:</strong>(.*?)</li>',info)[0].strip()
        if '.' in bath:
            bath=bath.split('.')
            bath=bath[0]
            halfbath=1
        else:
            bath=bath
            halfbath=0

        bed = ''.join(re.findall('<strong>Bedrooms:(.*?)</li>', info,re.DOTALL))
        bed = ''.join(re.findall(r"(\d+)", bed, re.DOTALL))

        sq = re.findall('Total Square Feet:(.*?)Floors:',info,re.DOTALL)
        sf=sq[0]
        sqft=sf.replace(',','').strip()

        Desc = "Our wide selection of customizable single-family home plans has been designed to bring comfort, quality, and livability for a variety of needs. Whether you reside in one of our pristine communities or on your private lot, with Harbor Classic Homes, you’ll always feel at home."

        try:
            imgs = re.findall('href="https://harborclassichomes.com/wp-content/uploads/(.*?)"',info,re.DOTALL)
            imgs='https://harborclassichomes.com/wp-content/uploads/'+imgs[-1]
            img2= 'https://harborclassichomes.com/wp-content/uploads/'+re.findall('"url":"https://harborclassichomes.com/wp-content/uploads/(.*?)"',info)[0]
            pic=img2+'|'+imgs
            # pic= 'https://harborclassichomes.com/wp-content/uploads/'+'|https://harborclassichomes.com/wp-content/uploads/'.join(pic)
            print(pic)
        except:
            pic = ''

        SubdivisionNumber = self.builderNumber  # if subdivision is not available
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = name
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0.00
        item['BaseSqft'] = sqft
        item['Baths'] = bath
        item['HalfBaths'] = halfbath
        item['Bedrooms'] = bed
        item['Garage'] = 0
        item['Description'] = Desc
        item['ElevationImage'] = pic
        item['PlanWebsite'] = response.url
        yield item


# from scrapy.cmdline import execute
# execute("scrapy crawl harborclasic".split())