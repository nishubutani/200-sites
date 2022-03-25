# -*- coding: utf-8 -*-
import hashlib
import re

import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class ZemanhomesSpider(scrapy.Spider):
    name = 'Zemanhomes'
    allowed_domains = []
    start_urls = ['http://zeman-construction.com/']

    builderNumber = "22746"

    def parse(self, response):
        print('--------------------')
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
        item['Street1'] = '535 Shelton Mill Road'
        item['City'] = 'Charlottesville'
        item['State'] = 'VA'
        item['ZIP'] = '22903'
        item['AreaCode'] = '434'
        item['Prefix'] = '987'
        item['Suffix'] = '1349'
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = "Zeman Construction is a family owned, Class A Builder specializing in residential construction & renovation as well as light commercial projects. With a passion for building and over 39 years of experience in 4 different states, owner Larry Zeman offers a unique insight into the entire construction process that sets him apart from other builders. Contact us today for your building needs!"
        item['SubImage'] = 'http://zeman-construction.com/wp-content/themes/devster/timthumb.php?src=http://zeman-construction.com/wp-content/themes/devster/images/house1.jpg&h=265&w=630&zc=1|http://zeman-construction.com/wp-content/themes/devster/timthumb.php?src=http://zeman-construction.com/wp-content/themes/devster/images/house3.jpg&h=265&w=630&zc=1'
        item['SubWebsite'] = response.url
        yield item

        link= 'http://zeman-construction.com/house-plans'
        yield scrapy.Request(url=link, callback=self.plan_links_inner)

    def plan_links_inner(self,response):

        plan_links = response.xpath('//div[@class="maincontent"]//a/@href').extract()
        for plan in plan_links:
            if '"' in plan:
                plan=plan.replace('"','')
                print('lakewood------',plan)
            plan =  plan

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

        P = re.findall('<title>(.*?) - Zeman Construction</title>',r)[0]
        PlanName=str(P)
        print('PName---->',PlanName)


        try:
            try:
                sq= re.findall('Square Footage:</strong>(.*?)<br />',r)[0]
                q=sq.split(' ')
                sqft=q[1]
                BaseSqft = sqft.replace(',', '')
                print('sqft1',BaseSqft)

            except:
                sq=re.findall('Square Footage: </strong>(.*?)<br />',r)[0]
                q=sq.split(' ')
                sqft=q[0]
                BaseSqft=sqft.replace(',','')
                print('sqft2',BaseSqft)
        except:

            try:
                sq=re.findall('Main Level: </strong>(.*?)<br />',r)[0]
                q=sq.split(' ')
                sqft = q[0]
                BaseSqft = sqft.replace(',', '')
                print('Sqft3',BaseSqft)
            except:

                print('sqft not define',response.url)


        try:
            Bt= re.findall('<strong>Bathrooms:</strong> (.*?)</p>',r)[0]
            if '.' in Bt:
                if '.0' in Bt:
                    Baths=Bt[0]
                    HalfBaths=0
                else:
                    Bt= Bt.split('.')
                    Baths= Bt[0]
                    HalfBaths= 1
            else:
                Baths=Bt
                HalfBaths= 0
        except:

            print('errror bath' )

        try:
            Bedrooms= re.findall('<strong>Bedrooms:</strong> (.*?)<br />',r)[0]

        except:

            print('errror bed')

        try:
            try:
                des= ''.join(re.findall('Square Footage:(.*?) or just',r,re.DOTALL))
                if '<strong>' in des:
                    ds =des.replace('<strong>','').replace('</strong>','')
                if '<br />' in ds:
                    des=ds.replace('<br />','').replace('<p>','').replace('</p>','')
                Description= 'House Series: '+ des

            except:
                des=''.join(re.findall('<strong> Main Level:(.*?) or just',r,re.DOTALL))
                if '<strong>' in des:
                    ds =des.replace('<strong>','').replace('</strong>','')
                if '<br />' in ds:
                    des=ds.replace('<br />','').replace('<p>','').replace('</p>','')
                Description= 'Main Level: '+ des

        except:
            Description=''
            print('erroor des')

        if PlanName == 'Timber Ridge II House Plan':
            print('---------')
            Garage = 0.0
        else:
            try:
                if 'Garage' in Description:
                    G=re.findall('» (.*?) Garage',Description)[0]
                    if G =='Integrated':
                        Garage=1.0
                    elif 'Car' in G:
                            if 'Two' in G:
                                Garage= 2.0
                            else:
                                Garage=0.0
                else:
                        Garage= 0.0

            except:
                Garage= 0.0
                print('errror garage')

        try:

            img = re.findall('<img src="http://zeman-construction.com/plans(.*?)"',r,re.DOTALL)
            ElevationImage ='http://zeman-construction.com/plans/'+ '|http://zeman-construction.com/plans'.join(img)
            print(ElevationImage)

        except:
            ElevationImage=''
            print('errror img')


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
        item['Garage'] = Garage
        item['Description'] = Description
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = response.url
        yield item

#
# from scrapy.cmdline import execute
# execute("scrapy crawl Zemanhomes".split())