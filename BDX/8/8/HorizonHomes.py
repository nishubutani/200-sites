# -*- coding: utf-8 -*-
import hashlib
import re

import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class horizonhomeSpider(scrapy.Spider):
    name = 'horizonhome'
    allowed_domains = []
    start_urls = ['https://www.newhomesinholly.com/copy-of-home-1']

    builderNumber = 52933

    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        s=response.text
        for i in range(0,2):
            try:
                # SubdivisionName = response.xpath('//span[@class="_3fUtn"]/text()').extract_first(default='').strip()
                SubdivisionName=re.findall('class="style-jtombgbrlabel">(.*?)</span>',s)[i]
                print(SubdivisionName)
            except Exception as e:
                print(e)

            try:
                SubdivisionNumber = int(hashlib.md5(bytes(SubdivisionName, "utf8")).hexdigest(), 16) % (10 ** 30)
            except Exception as e:
                print(e)

            try:
                desc = re.findall('<span style="font-family:futura-lt-w01-light,sans-serif;">(.*?)</span>',s)[i]
            except:
                desc = "Let your audience get in touch with you in just a click. Add Easy Customer Contact to your site, enter your info and you.Let site visitors reach out to you and get instant answers when they are live on your site. Handle multiple chats at the same time to reach more of your visitors."

            try:
                if SubdivisionName=='Preserve of Riverside':
                    link="https://www.newhomesinholly.com/preserve-of-riverside"
                    img="https://static.wixstatic.com/media/080aad_3c88ccb859ec4166819b309aa3bcc412~mv2.png/v1/crop/x_0,y_3,w_2754,h_3306/fill/w_236,h_284,al_c,usm_0.66_1.00_0.01/Preserve%20of%20Riverside%20Site%20Plan%20WEBPOSTE.png"
                elif SubdivisionName=='':
                    link="https://www.newhomesinholly.com/riverside-north"
                    img = "https://static.wixstatic.com/media/080aad_9f8447b0012548cf9223e1b94eb0b2d8~mv2.png"
                else:
                    pass
            except:
                img = ''

            try:
                street=re.findall('<span style="letter-spacing:0.15em;">(.*?)</span>',s)[i]
            except:
                street=''


            f = open("html/%s.html" % self.builderNumber, "wb")
            f.write(response.body)
            f.close()

            item = BdxCrawlingItem_subdivision()
            item['sub_Status'] = "Active"
            item['SubdivisionNumber'] = SubdivisionNumber
            item['BuilderNumber'] = self.builderNumber
            item['SubdivisionName'] = SubdivisionName
            item['BuildOnYourLot'] = 0
            item['OutOfCommunity'] = 0
            item['Street1'] = street
            item['City'] = "Royal Oak"
            item['State'] = 'MI'
            item['ZIP'] = '48073'
            item['AreaCode'] = '248'
            item['Prefix'] = '396'
            item['Suffix'] = '0671'
            item['Extension'] = ""
            item['Email'] = 'sales@horizonhomesmi.com'
            item['SubDescription'] = desc
            item['SubImage'] = img
            item['SubWebsite'] = link
            yield item

            plan_link = 'https://www.newhomesinholly.com/copy-of-home-2'
            yield scrapy.Request(url=plan_link, callback=self.plan_link_page,dont_filter=True)

    def plan_link_page(self,response):
        q=response.text
        plan_links = re.findall('data-state="desktop shouldUseFlex center"><a href="https://www.newhomesinholly.com(.*?)"',q,re.DOTALL)

        for plan in plan_links:

            plan='https://www.newhomesinholly.com' + plan
            yield scrapy.Request(url=plan, callback=self.plan_details,dont_filter=True)

    def plan_details(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = self.builderNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '3315 North Campbell'
        item['City'] = 'Royal Oak'
        item['State'] = 'MI'
        item['ZIP'] = '48073'
        item['AreaCode'] = '248'
        item['Prefix'] = '396'
        item['Suffix'] = '0671'
        item['Extension'] = ""
        item['Email'] = 'sales@horizonhomesmi.com'
        item['SubDescription'] =""
        item['SubImage'] = "https://static.wixstatic.com/media/080aad_6c793f322f3c47d09ce3bf337d4b73a1~mv2_d_2400_1427_s_2.jpg/v1/crop/x_242,y_0,w_1917,h_1427/fill/w_221,h_165,al_c,q_80,usm_0.66_1.00_0.01/Skyline%201500%20GR.jpg"
        item['SubWebsite'] = "https://www.newhomesinholly.com/"
        yield item

        z=response.text
        print(z)
        PlanNumber = int(hashlib.md5(bytes(response.url,"utf8")).hexdigest(), 16) % (10 ** 30)

        BaseS = re.findall(';"><span style="font-style:italic;">(.*?)sqft',z)[0]
        print(BaseS)
        BaseSqft=''.join(re.findall(r"(\d+)", BaseS, re.DOTALL))
        print(BaseSqft)

        BsPrice = ''.join(re.findall('Bath(.*?)</span>',z,re.DOTALL))
        BasePrice = ''.join(re.findall(r"(\d+)", BsPrice, re.DOTALL))
        print(BasePrice)

        if response.url=='https://www.newhomesinholly.com/copy-of-2300-2':
            Description='A spacious kitchen with an oversized island, large living area and a generous master suite create the perfect home at the perfect price<'
            Planname="Skyline 1735"

        elif response.url=='https://www.newhomesinholly.com/copy-of-1500':
            Description="Large open living spaces with a flexible second floor that allows for a loft mezzanine&nbsp;or a fourth bedroom"
            Planname="Skyline 1975"

        elif response.url=='https://www.newhomesinholly.com/copy-of-1500-1':
            Description="Thoughtful design creates a series of open spaces that make this quaint ranch feel much bigger than it seems"
            Planname="Skyline 1485"

        elif response.url=='https://www.newhomesinholly.com/copy-of-2100':
            Description="With a large front porch and a unique 2nd floor, this 3-bedroom offers something for everyon"
            Planname="Skyline 2000"

        elif response.url=='https://www.newhomesinholly.com/copy-of-2300':
            Description="An open conceptkitchen,second floor laundry, and oversized master&nbsp;make this house the perfect fit for growing families"
            Planname="Skyline 2200"

        elif response.url=="https://www.newhomesinholly.com/2300":
            Description="A first floor den, gourmet kitchen, and&nbsp;en-suite&nbsp;master sitting room create an oasis to call home"
            Planname="Skyline 2385"



        try:
            image=re.findall('&quot;width&quot;:200,&quot;height&quot;:200,&quot;uri&quot;:&quot;(.*?)&quot;,&quot;displayMode&quot;:&quot;fit&quot;',z,re.DOTALL)
            image = "https://static.wixstatic.com/media/" +"| https://static.wixstatic.com/media/".join(image)
            ElevationImage = image

        except Exception as e:
            print(str(e))

        beds =re.findall('sqft -(.*?)Bed',z)[0].strip()
        if '/' in beds:
            bed=beds.split('/')
            bed=bed[0]
        else:
            bed=beds
        bed = ''.join(re.findall(r"(\d+)", bed, re.DOTALL))
        print(bed)


        baths=re.findall('Bed Rm -(.*?)Bath',z)[0].strip()
        if '.' in baths:
            bath=baths.split('.')
            bath=bath[0]
            halfbath=1
        else:
            bath=baths
            halfbath=0

        bath = ''.join(re.findall(r"(\d+)", bath, re.DOTALL))
        print(bath)


        SubdivisionNumber = self.builderNumber  # if subdivision is not available
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = Planname
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = BasePrice
        item['BaseSqft'] = BaseSqft
        item['Baths'] = bath
        item['HalfBaths'] = halfbath
        item['Bedrooms'] = bed
        item['Garage'] = 0.0
        item['Description'] = Description
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = response.url
        yield item


# from scrapy.cmdline import execute
# execute("scrapy crawl horizonhome".split())