# -*- coding: utf-8 -*-
import hashlib
import re

import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class VictorySpider(scrapy.Spider):
    name = 'victorygatehomes'
    allowed_domains = []
    start_urls = ['https://www.vgcustomhomes.com']

    builderNumber = "20826"

    def parse(self, response):
        print('--------------------')
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #


        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        r=response.text

        try:
            img= 'https://www.vgcustomhomes.com'+ '|https://www.vgcustomhomes.com'.join(response.xpath('//div[@id="carousel-bgslideshow-1616"]//img/@src').extract())

        except:
            img=''

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '7656 Lutz Ave'
        item['City'] = 'Massillon'
        item['State'] = 'OH'
        item['ZIP'] = '44646'
        item['AreaCode'] = '330'
        item['Prefix'] = '408'
        item['Suffix'] = '7656'
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = "VictoryGate Custom Homes is a first-generation home builder dedicated to building high quality custom homes that are affordable and unique.  Each client's needs and wants are important in our building process. As a company, we take pride in our homes and our craftsmanship. VictoryGate Custom Homes will build in Stark County and all surrounding areas, to better meet our client's needs. VictoryGate was awarded as a top builder in the Nation in 2016 and 2017 by the National Home Builders Association and we certainly live up to that title. We look forward to working with you as we build your dream home!"
        item['SubImage'] = img
        item['SubWebsite'] = response.url
        yield item

        planlink= ['ranch-homes','two-story-homes']
        for i in planlink:
            link= 'https://www.vgcustomhomes.com/home-plans/' + i
            yield scrapy.Request(url=link, callback=self.plan_links_inner)

    def plan_links_inner(self,response):

        s=response.text
        plan_links = response.xpath('//section[@id="g-container-main"]//div//h2/a/@href').extract()
        for plan in plan_links:
            plan =  'https://www.vgcustomhomes.com' + plan
            yield scrapy.Request(url=plan, callback=self.plan_details)


    def plan_details(self, response):
        r=str(response.text)

        try:
            PlanNumber = int(hashlib.md5(bytes(response.url,"utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = self.builderNumber
            print(SubdivisionNumber)
        except Exception as e:
            print(str(e))

        P = response.xpath('//div[@class="page-header"]//text()').extract()
        PlanName= str(P[1]).strip()
        print(PlanName)


        data=response.xpath('//div[@itemprop="articleBody"]/p').extract()
        print(data)

        s= str(data[1]).replace('<p>','')
        s1=s.replace('</p>','')
        s2=s1.split('<br>')
        try:
            sq= str(s2[0]).replace(',','')
            BaseSqft=sq.replace('Sq Ft: ','')
        except:
            BaseSqft=''
            print('sqft')


        try:
            Bt= s2[2].replace('Bathrooms: ','')
            B=Bt.split(' ')
            Baths=B[0]
            try:
                HalfBaths=B[1]
                HalfBaths= 1
                print(Bt)
            except:
                HalfBaths= 0
                if '.' in Bt:
                    B = Bt.split('.')
                    Baths = B[0]
                    HalfBaths=1


        except:
            Baths=''
            HalfBaths=''

        try:
            Bedrooms=str(s2[1]).replace('Bedrooms: ','')
            print(Bedrooms)
        except:
            Bedrooms=''

        try:
            des= str(data[2]).replace('<p>','')
            ds= des.replace('</p>','')
            if 'car garage' in ds:
                gr = re.findall(' (.*?)-car garage', ds)[0]
                gr= gr.split(' ')
                G=gr[-1]
                Garage=int(G)
                Description=ds
                print('garage',Garage)
            else:
                Description=''
                Garage=0.0
        except:
            Description=''
            Garage=0.0


        try:

            Eimage= '|'.join(re.findall('data-image="(.*?)"',r,re.DOTALL))
            img = re.findall('src="/images/(.*?)"',r,re.DOTALL)
            img='https://www.vgcustomhomes.com/images/'+ '|https://www.vgcustomhomes.com/images/'.join(img)
            if 'https://www.vgcustomhomes.com/images/logo/vg-logo250.png' in img:
                img=img.replace('https://www.vgcustomhomes.com/images/logo/vg-logo250.png|','')
                if 'https://www.vgcustomhomes.com/images/homepage/nahb.png' in img:
                    img=img.replace('https://www.vgcustomhomes.com/images/homepage/nahb.png','')
            print(img)

            ElevationImage= Eimage + img
            print(ElevationImage)

        except:
            ElevationImage=''

        SubdivisionNumber = self.builderNumber  # if subdivision is not available
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = PlanName
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0.00
        item['BaseSqft'] = BaseSqft
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage + .0
        item['Description'] = Description
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = response.url
        yield item


#
# from scrapy.cmdline import execute
# execute("scrapy crawl victorygatehomes".split())