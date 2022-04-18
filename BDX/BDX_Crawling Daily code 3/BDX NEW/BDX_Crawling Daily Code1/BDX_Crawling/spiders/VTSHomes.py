# -*- coding: utf-8 -*-
import hashlib
import re

import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class vtshomeshomesSpider(scrapy.Spider):
    name = 'vtshomes'
    allowed_domains = []
    start_urls = ['http://www.vtshomes.com/']

    builderNumber = "21070"

    def parse(self, response):
        print('--------------------')
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #


        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        img=response.xpath('//div[@id="slideshowbox"]//img/@src').extract()
        SubImage = 'http://www.vtshomes.com/' + '|http://www.vtshomes.com/'.join(img)

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '7 Town Center Dr, Suite 102'
        item['City'] = 'Huntsville'
        item['State'] = 'AL'
        item['ZIP'] = '35806'
        item['AreaCode'] = '256'
        item['Prefix'] = '704'
        item['Suffix'] = '3333'
        item['Extension'] = ""
        item['Email'] = 'info@vtshomes.com'
        item['SubDescription'] = "VTS builds homes where Value meets Tradition and Stability. We know today's homebuyers are seeking value and quality craftsmanship to provide both daily joy and long-term stable investment. Value, tradition and stability are the underpinnings of every home we design. At VTS Homes, we maintain the traditions of quality and character that are typically only seen in established, traditional neighborhoods.VTS Homes can build your next home in one of our communities or on your lot."
        item['SubImage'] = SubImage
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        link= 'http://www.vtshomes.com/portfolio-of-homes.php#providence'
        yield scrapy.Request(url=link, callback=self.plan_links_inner)

    def plan_links_inner(self,response):

        plan_links = response.xpath('//ul[@id="slideshowbox"]//li').extract()

        for i in plan_links:
            img= re.findall('<img src="(.*?)"',i)[0]
            ElevationImage ='http://www.vtshomes.com/'+ img

            url=re.findall('<a class="pdf" href="(.*?)"',i)[0]
            url = 'http://www.vtshomes.com/portfolio-of-homes.php'

            Name= str(re.findall('</a>(.*?)</p>',i,re.DOTALL))
            nm=re.findall(' (.*?)<br>',Name)[0]
            PlanName =nm.strip()

            bt= ''.join(re.findall('<br>(.*?)</p>',i,re.DOTALL))
            bt = bt.split(',')
            BS =bt[0].split(' ')
            BaseSqft=BS[0]

            Bedrooms=bt[1].replace(' BR','').strip()

            bath=bt[2].replace(' BA','').strip()
            if '.' in bath:
                bath=bath.split('.')
                Baths=bath[0]
                HalfBaths=1
            else:
                Baths=bath
                HalfBaths=0

            try:
                d =i.split('</a>')[1]
                des=d.replace('\n','').replace('\r','').replace('\t','').replace('<br>',', ').replace('</p>','').replace('</li>','')
                description=des.strip()
                print(description)

            except:
                pass

            try:
                PlanNumber=int(hashlib.md5(bytes(PlanName,"utf8")).hexdigest(), 16) % (10 ** 30)
            except Exception as e:
                print(str(e))

            try:
                SubdivisionNumber = self.builderNumber
                print(SubdivisionNumber)
            except Exception as e:
                print(str(e))



            SubdivisionNumber = self.builderNumber  # if subdivision is not available
            unique = str(PlanNumber) + str(SubdivisionNumber)
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            item = BdxCrawlingItem_Plan()
            item['Type'] = 'SingleFamily'
            item['PlanNumber'] = int(hashlib.md5(bytes(response.url,"utf8")).hexdigest(), 16) % (10 ** 30)
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
            item['Garage'] = 0.0
            item['Description'] = description
            item['ElevationImage'] = ElevationImage
            item['PlanWebsite'] = url
            yield item

        home_link = 'http://www.vtshomes.com/move-in-ready-homes.php'
        yield scrapy.Request(url=home_link, callback=self.home_details, meta={'PN': unique_number})

    def home_details(self, response):
        unique = str("Plan Unknown") + self.builderNumber  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['unique_number'] = unique_number
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = "Plan Unknown"
        item['SubdivisionNumber'] = self.builderNumber
        item['PlanName'] = "Plan Unknown"
        item['PlanNotAvailable'] = 1
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0
        item['BaseSqft'] = 0
        item['Baths'] = 0
        item['HalfBaths'] = 0
        item['Bedrooms'] = 0
        item['Garage'] = 0
        item['Description'] = ""
        item['ElevationImage'] = ""
        item['PlanWebsite'] = ""
        yield item

        s=str(response.text)

        try:
            ad=re.findall('<div class="address">(.*?)</div>',s)[0].strip()
            ad=ad.split(',')
            SpecStreet1= ad[0]

            SpecCity= ad[1]

            SpecState = ad[2].strip()

            SpecZIP = '35806'

            unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
            print(unique)
            SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

            f = open("html/%s.html" % SpecNumber, "wb")
            f.write(response.body)
            f.close()

        except Exception as e:
            print(e)

        try:
            data=re.findall('<div class="amenities">(.*?)</div>',s)[0].strip()
            d=data.split('/')
            print(d)
            SpecBedrooms= d[0].replace(' BR ','').strip()
            SpecBaths = d[1].replace(' BA','').strip()
            SpecGarage = d[2].replace('-Car Garage','').strip()
            SpecSqft= d[3].replace(' Sq. Ft.','').replace(',','')
        except Exception as e:
            print(str(e))


        try:
            Price = re.findall('<h3>(.*?)</h3',s)[0].strip()
            S=Price.split('-')
            Sq=S[-1]
            SpecPrice = Sq.replace(' $','').replace(',','')
        except Exception as e:
            print(str(e))


        try:
            SpecDescription = re.findall('<div class="description">(.*?)<br />',s)[0]
            print(SpecDescription)
        except Exception as e:
            print(e)

        try:

            img = re.findall('<img src="images/move-in-ready-homes/(.*?)"',s)[0]
            ElevationImage= 'http://www.vtshomes.com/images/move-in-ready-homes/'+ img


        except Exception as e:
            print(str(e))

        try:
            website = re.findall('<a class="blue underline" href="(.*?)"',s)[0]
            SpecWebsite= 'http://www.vtshomes.com/' + website
        except Exception as e:
            print(e)

        # ----------------------- Don't change anything here --------------------- #
        item = BdxCrawlingItem_Spec()
        item['SpecNumber'] = SpecNumber
        item['PlanNumber'] =  unique_number
        item['SpecStreet1'] = SpecStreet1
        item['SpecCity'] = SpecCity
        item['SpecState'] = SpecState
        item['SpecZIP'] = SpecZIP
        item['SpecCountry'] = 'USA'
        item['SpecPrice'] = SpecPrice
        item['SpecSqft'] = SpecSqft
        item['SpecBaths'] = SpecBaths
        item['SpecHalfBaths'] = 0
        item['SpecBedrooms'] = SpecBedrooms
        item['MasterBedLocation'] = "Down"
        item['SpecGarage'] = SpecGarage
        item['SpecDescription'] = SpecDescription
        item['SpecElevationImage'] = ElevationImage
        item['SpecWebsite'] = SpecWebsite
        yield item

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl vtshomes".split())