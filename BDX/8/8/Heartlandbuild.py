import re

import scrapy
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class HeartlandbuildSpider(scrapy.Spider):
    name = 'Heartlandbuild'
    allowed_domains = ['www.heartlandbuild.com']
    start_urls = ['https://www.heartlandbuild.com/']
    builderNumber = 54155

    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        desc = ' '.join(response.xpath('//div[@class="content-left"]//text()').getall()[0:13])
        sub_image = re.findall(r'<img src="(.*?)" alt="Heartland Builders" />',response.text)
        images = []
        for img in sub_image:
            image = 'https://www.heartlandbuild.com/' + img
            images.append(image)
        images = '|'.join(images)
        item = BdxCrawlingItem_subdivision()

        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '3030 Forest Park Dr.'
        item['City'] = 'Dyer'
        item['State'] = 'IN'
        item['ZIP'] = '46311'
        item['AreaCode'] = '219'
        item['Prefix'] = '227'
        item['Suffix'] = '9533'
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = desc.replace('\n','').replace('\t','').replace('                               ',' ').replace('                  ',' ').strip()
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        yield item
    #
        url = 'https://www.heartlandbuild.com/model-homes.php'
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.Plans_link)

    def Plans_link(self, response):
        urls = response.xpath("//*[contains(text(),'View Gallery')]/../a/@href").extract()
        for i in urls:
            url = 'https://www.heartlandbuild.com/' + str(i)
            # print('PLANS------------------->', url)
            yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.Plans_Details)
    #
    def Plans_Details(self, response):

        Type = 'SingleFamily'

        PlanName = response.xpath('//div[@class="whole"]/h1/text()').extract_first().strip()

        PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)

        SubdivisionNumber = self.builderNumber

        PlanNotAvailable = 0

        PlanTypeName = 'Single Family'

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

        Bedrooms = str(re.findall(r'ft (.*?) bedrooms<',response.text))
        if Bedrooms != '[]':
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            # print(Bedrooms)
        else:
            Bedrooms = str(re.findall(r'ft (.*?) bedrooms <',response.text))
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            # print('172.--------------',Bedrooms)

        a = re.findall(r'>(.*?) baths ',response.text)[0]
        b = str(a).split(">")[-1].strip()
        # print('bathrooms----',b)
        Baths = b.split()[0]
        if '2.5' in b:
            Baths = 2
            # print('This is Baths----------',Baths)
        else:
            Baths = Baths
            # print('this is Baths-----',Baths)
        if len(b) > 1:
            HalfBaths = 1
            # print('this is halfbaths--------',HalfBaths)
        else:
            HalfBaths = 0
            # print('this is halfbaths--------',HalfBaths)

        Garage = str(re.findall(r'baths (.*?) car garage<',response.text)[0]).replace('|','')
        Garage = Garage.strip()
        # if '.5' in Garage:
        #     g = Garage.split('.5')[0]
        #     Garage = int(g) +1
        #     # print('##########', Garage)
        # else:
        #     Garage = Garage
            # print('$$$$$$$$$$$$$',Garage)

        try:
            BaseSqft = str(re.findall(r'>(.*?) sq. ft',response.text)[0]).replace('<span>','').replace('<span data-mce-mark="1">2 Bedroom Ranch</span> <br />','').replace('<span data-mce-mark="1">','').replace('3 Bedroom Ranch<br /> ','').replace('<span style="font-size: large;">','').replace('<span style="font-size: medium;">','')
            # print(response.url,BaseSqft)
        except Exception as e:
            print(e,response.url)
            BaseSqft = 0

        try:
            Price = re.findall(r'\$(.*?)</p>',response.text)[0]
            # print(response.url,Price)
        except Exception as e:
            print(e)
            Price = 0
            # print(response.url,Price)

        try:
            Description = 'Welcome to Heartland Builders of NWI. My name is Rick Mossell; I have been building homes for over 25 years and have built over 600 homes. My goal has always been the same: To build you   quality home. To make the process as smooth as possible by me personally, the builder, working with you from start to finish. No middle people. Fewer things can go wrong this way. To build your dream home.'
        except:
            Description = ''

        try:
            img1 = response.xpath('//div[@class="whole"]/div[@id="gallery"]/img/@src').get()
            if img1 != None:
                img1 = 'https://www.heartlandbuild.com' + str(response.xpath('//div[@class="whole"]/div[@id="gallery"]/img/@src').get()).replace('..','')
            else:
                img = response.xpath('//div[@class="whole"]/div[@id="gallery"]//img/@src').getall()
                img1_list = []
                for j in img:
                    k = 'https://www.heartlandbuild.com' + str(j).replace('..','')
                    img1_list.append(k)
                img1 = '|'.join(img1_list)

        except:
            img1 = ''
            print('img1 mei error......',response.url)
        try:
            img2 = response.xpath('//div[@class="whole"]/div[@id="thumbs"]/p/img/@src').getall()
            imgs = []
            for i in img2:
                image = 'https://www.heartlandbuild.com' + str(i).replace('..','')
                imgs.append(image)
            imgs = '|'.join(imgs)
        except:
            imgs = ''
            print('img2 mei error....',response.url)

        ElevationImage = img1 + '|' + imgs



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
        item['BasePrice'] = str(Price).replace('</span>','').replace('<span>','').replace(',','')
        item['BaseSqft'] = BaseSqft
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = Description
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = response.url
        yield item

# from scrapy.cmdline import execute
# execute("scrapy crawl Heartlandbuild".split())
