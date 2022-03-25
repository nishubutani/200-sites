# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class Advantage_HomesSpider(scrapy.Spider):
    name = 'basic_Homes'
    allowed_domains = ['']
    start_urls = ['https://www.designbasics.com/']

    builderNumber = "49964"

    def parse(self, response):
        a=response.text
        print(a)

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
        item['Street1'] = '11112 John Galt Blvd.'
        item['City'] = 'Omaha'
        item['State'] = 'NE'
        item['ZIP'] = '68137'
        item['AreaCode'] = '402'
        item['Prefix'] = '331'
        item['Suffix'] = '9223'
        item['Extension'] = ""
        item['Email'] = ''
        item[
            'SubDescription'] = 'Our Builder-Centric Preferred Builder Program is a great way to add more home designs to your portfolio at a lower cost and take advantage of extra savings.Choose between our GOLD and PLATINUM programs and watch your savings multiply!'
        item['SubImage'] = 'https://www.agilehomes.com/images/homepageimage/photo1.jpg'
        item['SubWebsite'] = response.url
        yield item

        plan_link = "https://www.designbasics.com/plan-search/"
        yield scrapy.FormRequest(url=plan_link, callback=self.planpage,
                                 dont_filter=True)

    def planpage(self,response):
        for i in range(-1,237):
            pg="https://www.designbasics.com/plan-search/?pg=" +str(i)
            print(pg)
            yield scrapy.FormRequest(url=pg, callback=self.plan_link,
                                     dont_filter=True)

    def plan_link(self, response):
        s=response.text
        link=re.findall('<a href="/plan-view(.*?)"',s,re.DOTALL)
        for k in link:
            lk="https://www.designbasics.com//plan-view" + k
            print(lk)
            yield scrapy.FormRequest(url=lk, callback=self.plan_data,
                                     dont_filter=True)

    def plan_data(self,response):
        t=response.url
        a=response.text
        # print(a)
        try:
            name = re.findall('<h1 class="entry-title main_title">(.*?)</h1>',a)[0].strip()
            if '#' in name:
                name=name.replace('#','')

        except:
            pass

        data= ''.join(re.findall('<meta name="description" content="(.*?)"',a,re.DOTALL))

        sq=re.findall('<strong class="total_heated_area">(.*?)</strong>',a)[0]

        bath=re.findall('<strong class="bathrooms">(.*?)</strong>',a)[0]
        bed=re.findall('<strong class="bedrooms">(.*?)</strong>',a)[0]
        garage=re.findall('<strong class="garage">(.*?)</strong>',a)[0]

        try:
            BaseSqft = sq
        except:
            BaseSqft=0

        try:
            Bath = bath

        except:
            print('eror in baths', response.url)

        try:
            bed = bed
        except:
            print('eror in bed', response.url)

        try:
            garage=garage+'.0'
        except:
            garage=0.0

        try:
            ig='|'.join(re.findall('<img loading="lazy" src="(.*?)"',a,re.DOTALL))

            try:
                img2= ''.join(re.findall('<div class="numbertext">(.*?)class="card"',a,re.DOTALL))
                pic='|'.join(re.findall('<img src="(.*?)"',img2,re.DOTALL))
            except:
                pic=''

            if pic!="":
                elevimg= ig+"|"+pic
            else:
                elevimg= ig

        except:
            elevimg=''

        try:
            description= ''.join(re.findall(' <h2>Plan Description</h2>(.*?)What&#039;',a,re.DOTALL)).strip()

            description = re.compile(r'<[^>]+>').sub('', description)
            description=re.sub(u'[^\u0020-\uD7FF\u0009\u000A\u000D\uE000-\uFFFD\U00010000-\U0010FFFF]+', '', description)

            if '\r' in description:
                description=description.replace('\r','')
            if '\t' in description:
                description=description.replace('\t','')
            if '\n' in description:
                description = description.replace('\n', '')
            print(description)


        except:
            description='Our Builder-Centric Preferred Builder Program is a great way to add more home designs to your portfolio at a lower cost and take advantage of extra savings.Choose between our GOLD and PLATINUM programs and watch your savings multiply!'

        SubdivisionNumber=self.builderNumber
        PlanNumber= int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['unique_number'] = unique_number
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = PlanNumber
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = name
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = "Single Family"
        item['BasePrice'] = 0.00
        item['BaseSqft'] = BaseSqft
        item['Baths'] = Bath
        item['HalfBaths'] = 0
        item['Bedrooms'] = bed
        item['Garage'] = garage
        item['Description'] = description
        item['ElevationImage'] = elevimg
        item['PlanWebsite'] = response.url
        yield item


# from scrapy.cmdline import execute
# execute("scrapy crawl basic_Homes".split())