# -*- coding: utf-8 -*-
import hashlib
import re

import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class MurryHomesSpider(scrapy.Spider):
    name = 'murryhomes'
    allowed_domains = []
    start_urls = ['http://www.murrycommunities.com/']

    builderNumber = "15791"

    def parse(self, response):

        community_link = 'http://www.murrycommunities.com/our-communities/'
        yield scrapy.Request(url=community_link, callback=self.properties)

    def properties(self, response):

        links = ['http://www.murrycommunities.com/community/sawgrass-at-crossgates/','http://www.murrycommunities.com/community/winding-creek-at-crossgates/']
        # links = response.xpath('//ul[@class="sub-menu"]//a/@href').extract()
        for i in links:
            link = i
            yield scrapy.Request(url=link, callback=self.property_details)

    def property_details(self, response):
        s = str(response.text)

        subdivisonName = re.findall('<p class="comm-name">(.*?)</p>', s)[0]
        print(subdivisonName)

        subdivisonNumber = int(hashlib.md5(bytes(subdivisonName + self.builderNumber, "utf8")).hexdigest(), 16) % (
                10 ** 30)
        print(subdivisonNumber)

        f = open("html/%s.html" % subdivisonNumber, "wb")
        f.write(response.body)
        f.close()

        add = str(re.findall('<div class="btm">(.*?)</div>', s, re.DOTALL))
        s1 = re.findall('<a href="https://www.google.com/maps/dir//(.*?)"', add)[0]
        try:
            s1 = s1.split('<br>')
            street1 = str(s1[0]).strip()
            print('street', street1)
        except:
            print('streeteoro')

        try:
            s2 = s1[1].split(' ')
            city = str(s2[1]).replace(',', '')
            print('city', city)
        except:
            print('cityeror')

        try:
            state = str(s2[2])
            print(state)
        except:
            print('staterror')

        try:
            zip = s2[3]
            print(zip)
        except:
            print('ziperro')

        try:
            ph = re.findall('<a href="tel:(.*?)">', s)[0]
            ph = ph.split('-')
            Ac = ph[0]
            Pr = ph[1]
            Sf = ph[2]
        except:
            Ac = ''
            Pr = ''
            Sf = ''
            zip = ''

        SubDescription = ''.join(response.xpath('//div[@class="content"]//text()').extract())

        try:
            img = response.xpath('//div[@class="slider-cont"]//img/@src').extract()
            subimg = 'http://www.murrycommunities.com' + '|http://www.murrycommunities.com'.join(img)
        except:
            subimg = ''

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionName'] = subdivisonName
        item['SubdivisionNumber'] = subdivisonNumber
        item['BuilderNumber'] = self.builderNumber
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = street1
        item['City'] = city
        item['State'] = state
        item['ZIP'] = zip
        item['AreaCode'] = Ac
        item['Prefix'] = Pr
        item['Suffix'] = Sf
        item['Extension'] = ""
        item['Email'] = ""
        item['SubDescription'] = SubDescription
        item['SubImage'] = subimg
        item['SubWebsite'] = response.url
        yield item

        # plan = ['http://www.murrycommunities.com/community/woods-edge/','http://www.murrycommunities.com/community/sutherland-at-woods-edge/']
        # plan = ['http://www.murrycommunities.com/community/sawgrass-at-crossgates/','http://www.murrycommunities.com/community/winding-creek-at-crossgates/']
        # for i in plan:
        #     plan = i
        yield scrapy.Request(url=str(response.url), callback=self.plan, meta={'sbdn': subdivisonNumber}, dont_filter=True)

    def plan(self, response):
        rs= str(response.text)

        for i in response.xpath('//*[@class="details"]'):
            A = i.xpath('./p/text()').extract()
            print(A)
            PlanName=A[0].strip()

            BaseSqft = A[2].replace(' sq. ft.', '').replace(',', '').strip()
            print(BaseSqft)

            Bedroom=A[3].strip()

            b = A[4]
            try:
                b=A[4].strip()
                b=b.split(' ')
                Baths=b[0]
                HalfBaths= 1

            except:
                Baths=b[0]
                HalfBaths= 0


            G =A[5].replace('Car','').strip()
            Garage=G + '.0'

            try:
                    p=A[6].split(' ')
                    BasePrice=p[-1].replace('$','').replace('s','')
                    if BasePrice=='':
                        BasePrice=p[-2].replace('$','').replace('s','')
            except:
                print('--')


            website = response.url
            try:
                if PlanName=='New Yorker':
                    img='http://www.murrycommunities.com/wp-content/uploads/2018/12/NEW-YORKER-FRONT-OPTIONS-LABELED-copy.jpg|http://www.murrycommunities.com/wp-content/uploads/2018/12/Y-1.png|http://www.murrycommunities.com/wp-content/uploads/2018/12/Y-2-1.png'
                elif PlanName=='Heather':
                    img = 'http://www.murrycommunities.com/wp-content/uploads/2018/12/HEATHER-FRONT-OPTIONS-LABELED.jpg|http://www.murrycommunities.com/wp-content/uploads/2018/12/Heather-1.png|http://www.murrycommunities.com/wp-content/uploads/2018/12/Heather2.png'
                elif PlanName == 'Harmon Carriage Home':
                    img = 'http://www.murrycommunities.com/wp-content/uploads/2019/01/Harmon-rend.png|http://www.murrycommunities.com/wp-content/uploads/2019/01/Harmon-1.png'
                elif PlanName == 'Norman 2 Carriage Home':
                    img = 'http://www.murrycommunities.com/wp-content/uploads/2019/01/norm2-1.png|http://www.murrycommunities.com/wp-content/uploads/2019/01/Screen-Shot-2019-02-14-at-9.51.40-AM.png'
                elif PlanName == 'Casper':
                    img = 'http://www.murrycommunities.com/wp-content/uploads/2019/01/The-Casper-Rend-1.png|http://www.murrycommunities.com/wp-content/uploads/2019/01/Screen-Shot-2019-02-28-at-12.10.33-PM.png|http://www.murrycommunities.com/wp-content/uploads/2019/01/Screen-Shot-2019-02-28-at-12.10.38-PM.png'
                elif PlanName == 'The Els':
                    img = 'http://www.murrycommunities.com/wp-content/uploads/2019/01/Els-Rend-copy.png|http://www.murrycommunities.com/wp-content/uploads/2019/01/Screen-Shot-2019-02-28-at-12.01.25-PM.png|http://www.murrycommunities.com/wp-content/uploads/2019/01/Screen-Shot-2019-02-28-at-12.01.32-PM.png'
                elif PlanName == 'The Els II':
                    img = 'http://www.murrycommunities.com/wp-content/uploads/2019/01/ElsII.png|http://www.murrycommunities.com/wp-content/uploads/2019/01/Screen-Shot-2019-02-28-at-11.59.03-AM.png'
                elif PlanName == 'Norman 4 Carriage Home':
                    img = 'http://www.murrycommunities.com/wp-content/uploads/2019/01/Norman-4.png|http://www.murrycommunities.com/wp-content/uploads/2019/01/Screen-Shot-2019-02-28-at-12.12.55-PM.png|http://www.murrycommunities.com/wp-content/uploads/2019/01/Screen-Shot-2019-02-28-at-12.12.59-PM.png'
                elif PlanName == 'Rivermeade':
                    img = 'http://www.murrycommunities.com/wp-content/uploads/2018/12/RIVERMEADE-FRONT-OPTIONS-LABELED.jpg|http://www.murrycommunities.com/wp-content/uploads/2018/12/Riv.png'
                else:
                    img = re.findall('<img width="1300" height="700" src="(.*?)"', rs)[0]
                    img='http://www.murrycommunities.com' + img

                    pass
            except:
                print('error')

            SubdivisionNumber = response.meta['sbdn']  # if subdivision is not available
            # unique = str(PlanNumber) + str(SubdivisionNumber)
            # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            item = BdxCrawlingItem_Plan()
            item['Type'] = 'SingleFamily'
            item['PlanWebsite'] = website
            item['PlanNumber'] = int(hashlib.md5(bytes(website, "utf8")).hexdigest(), 16) % (10 ** 30)
            unique = str(item['PlanNumber']) + str(SubdivisionNumber) + str(PlanName) + str(BaseSqft)
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            item['unique_number'] = unique_number
            item['SubdivisionNumber'] = SubdivisionNumber
            item['PlanName'] = PlanName
            item['PlanNotAvailable'] = 0
            item['PlanTypeName'] = 'Single Family'
            item['BasePrice'] = BasePrice
            item['BaseSqft'] = BaseSqft
            item['Baths'] = Baths
            item['HalfBaths'] = HalfBaths
            item['Bedrooms'] = Bedroom
            item['Garage'] = Garage
            item['Description'] = ''
            item['ElevationImage'] = img
            yield item



# from scrapy.cmdline import execute
#
# execute("scrapy crawl murryhomes".split())