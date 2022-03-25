import hashlib
import json
import re
import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class cardinalSpider(scrapy.Spider):
    name ='cardinalcrest'
    allowed_domains = []
    start_urls = ['https://www.cardinalcresthomes.com/']

    builderNumber = 49268

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
        item['Street1'] =  "P.O. BOX 1355"
        item['City'] = 'Liberty'
        item['State'] = 'MO'
        item['ZIP'] = '64069'
        item['AreaCode'] = '816'
        item['Prefix'] ='499'
        item['Suffix'] = '3156'
        item['Extension'] = ""
        item['Email'] =''
        item['SubDescription'] = "Meet a custom home builder that provides true custom experiences. From the in house architectural services, to the step by step interior design consulting, we strive to make the home building process memorable. Cardinal Crest creates timeless homes that will focus equally on design and function. Utilizing the newest technologies we put as much emphasis on the aesthetics as the structural components to ensure a quality built home."
        item['SubImage']= 'https://www.cardinalcresthomes.com/media/view/2019/01/1679_homestead-8_4694.jpg'
        item['SubWebsite'] = response.url
        yield item

        plan_link = "https://www.cardinalcresthomes.com/plans/grid?page=1&method=single"
        yield scrapy.Request(url=plan_link, callback=self.plan_link_page,dont_filter=True)

    def plan_link_page(self, response):
        z = json.loads(response.text)
        page = z['pages']
        print(page)

        for j in range(1,page+1):
            link="https://www.cardinalcresthomes.com/plans/grid?page="+str(j)+"&method=single"
            print(link)
            yield scrapy.Request(url=link, callback=self.plan_details,dont_filter=True)

    def plan_details(self, response):
        print(response.url)
        div=response.text
        data=json.loads(div)

        s=len(data['results'])

        for i in range(0,s+1):
            try:
                name=data['results'][i]['name']
            except:
                name=''

            try:
                url=data['results'][i]['brochure']
                print('url',url)
            except:
                url='https://www.cardinalcresthomes.com/'

            PlanNumber = int(hashlib.md5(bytes(str(url)+str(name), "utf8")).hexdigest(), 16) % (10 ** 30)

            try:
                Desc =data['results'][i]['description']
            except:
                Desc = "Meet a custom home builder that provides true custom experiences. From the in house architectural services, to the step by step interior design consulting, we strive to make the home building process memorable. Cardinal Crest creates timeless homes that will focus equally on design and function. Utilizing the newest technologies we put as much emphasis on the aesthetics as the structural components to ensure a quality built home."

            try:
                img = '|'.join(data['results'][i]['images'])
                print(img)
            except:
                img = ''

            try:
                Bed=data['results'][i]['bedrooms']
                if '-' in Bed:
                    Bed=Bed.split('-')
                    Bed=Bed[-1]

            except:
                Bed=0

            try:
                sqft=data['results'][i]['square_footage']
                if ',' in sqft:
                    sqft=sqft.replace(',','')
                print('sqft',sqft)
            except:
                print(url,sqft)

            SubdivisionNumber=self.builderNumber
            unique = str(SubdivisionNumber) + str(url) + str(name)
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
            item['BaseSqft']=sqft
            item['Baths'] = 0
            item['HalfBaths'] = 0
            item['Bedrooms'] = Bed
            item['Garage'] = 0.0
            item['Description'] = Desc
            item['ElevationImage'] = img
            item['PlanWebsite'] = url
            yield item

            link='https://www.cardinalcresthomes.com/projects/grid?page=1&method=single'
            yield scrapy.Request(url=link, callback=self.project, dont_filter=True)

    def project(self, response):
            p=json.loads(response.text)
            page=p['pages']

            for j in range(1, page+1):
                link = "https://www.cardinalcresthomes.com/projects/grid?page=" + str(j) + "&method=single"
                print(link)
                yield scrapy.Request(url=link, callback=self.project_details, dont_filter=True)

    def project_details(self, response):


                info = json.loads(response.text)
                a=response.url
                print(a)

                s = len(info['results'])

                for i in range(0, s + 1):
                    try:
                        name = info['results'][i]['name']
                    except:
                        name = ''

                    try:
                        url = info['results'][i]['brochure']
                        print('url', url)
                    except:
                        url = 'https://www.cardinalcresthomes.com/'


                    try:
                        img = '|'.join(info['results'][i]['images'])
                        print(img)
                    except:
                        img = ''

                    try:
                        Bed = info['results'][i]['project_bedrooms']
                        if '-' in Bed:
                            Bed = Bed.split('-')
                            Bed = Bed[-1]

                    except:
                        Bed = 0

                    try:
                        Bath=info['results'][i]['project_bathrooms']
                        if '.' in Bath:
                            print(Bath)
                            Bath=Bath.split('.')
                            Bath=Bath[0]
                            Halfbath=1
                        else:
                            Bath=Bath
                            Halfbath=0
                    except:
                        Bath=0
                        Halfbath=0

                    try:
                        sqft= info['results'][i]['project_sqft'].replace(',','')
                    except:
                        sqft=0

                    PlanNumber = int(hashlib.md5(bytes(str(url) + str(sqft) +str(name), "utf8")).hexdigest(), 16) % (10 ** 30)

                    SubdivisionNumber = self.builderNumber
                    unique = str(SubdivisionNumber) + str(url) + str(name) +str(sqft)
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
                    item['Baths'] = Bath
                    item['HalfBaths'] = Halfbath
                    item['Bedrooms'] = Bed
                    item['Garage'] = 0.0
                    item['Description'] = "We work with our clients through the entire design process. Starting with simple concept sketches all the way to choosing that perfect light fixture. It has always been our goal to design and build timeless and cohesive homes that make sense inside and out. Below we showcase some of the projects we have had the privilege to work on."
                    item['ElevationImage'] = img
                    item['PlanWebsite'] = url
                    yield item

#
# from scrapy.cmdline import execute
# execute("scrapy crawl cardinalcrest".split())