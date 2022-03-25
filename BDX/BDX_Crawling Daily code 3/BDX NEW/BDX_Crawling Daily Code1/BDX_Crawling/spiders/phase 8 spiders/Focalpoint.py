import hashlib
import re

import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class focalpoint(scrapy.Spider):
    name = 'focalpoint'
    allowed_domains = []
    start_urls = ['https://focalpointhomes.com/']

    builderNumber = "25104"

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
        item['Street1'] = '6756 OLD MCLEAN VILLAGE DR. SUITE 100'
        item['City'] = 'MCLEAN'
        item['State'] = 'VA'
        item['ZIP'] = '22101'
        item['AreaCode'] = '703'
        item['Prefix'] = '356'
        item['Suffix'] = '1231'
        item['Extension'] = ""
        item['Email'] = 'JEFFJ@FOCALPOINTHOMES.COM'
        item['SubDescription'] = "We build homes to order on lots owned by our customers; however, we also build homes on lots we've purchased for sale to those who have more immediate needs. Listed below you'll find properties we own that are in various stages of permitting and construction. Select one early in the process and make all of the option decisions yourself!"
        item['SubImage'] = 'https://471cnv1oagubqby1r32lcg9e-wpengine.netdna-ssl.com/wp-content/uploads/2019/08/IMG_0759-Reversed-1024x768.jpg|https://471cnv1oagubqby1r32lcg9e-wpengine.netdna-ssl.com/wp-content/uploads/2019/08/Front-Elev-IMG_0564-1024x768.jpg|https://471cnv1oagubqby1r32lcg9e-wpengine.netdna-ssl.com/wp-content/uploads/2019/08/Entry-IMG_0527-e1578689621115-768x1024.jpg'
        item['SubWebsite'] = response.url
        yield item

        plan_link = "https://focalpointhomes.com/"
        yield scrapy.Request(url=plan_link, callback=self.plan_link_page,dont_filter=True)
    def plan_link_page(self,response):
        div=re.findall('<div class="houseplans-grid">(.*?)</div><!--',response.text,re.DOTALL)
        div=div[:15]
        for i in div:

            name = re.findall('<h3>(.*?)-',i)[0].strip()
            print(name)

            PlanNumber = int(hashlib.md5(bytes(str(name), "utf8")).hexdigest(), 16) % (10 ** 30)


            info = re.findall('<h3>(.*?)<span>',i)[0]
            bed=re.findall('-(.*?)BR',info)[0].strip()

            bath=re.findall('/(.*?)BA',info)[0].strip()
            if '.' in bath:
                bath=bath.split('.')
                bath=bath[0]
                halfbath=1
            else:
                bath=bath
                halfbath=0

            if 'HB' in info:
                halfbaths=int(re.findall('BA/(.*?)HB',info)[0])
            else:
                halfbaths=0
            print(bath,bed)

            try:
                price=''.join(re.findall('<span>(.*?)</span>',i,re.DOTALL))
                price = ''.join(re.findall(r"(\d+)", price, re.DOTALL))
                print(price)
            except:
                price=0.00

            Desc = "We build homes to order on lots owned by our customers; however, we also build homes on lots we've purchased for sale to those who have more immediate needs. Listed below you'll find properties we own that are in various stages of permitting and construction. Select one early in the process and make all of the option decisions yourself!"

            try:
                imgs = re.findall('href="https://471cnv1oagubqby1r32lcg9e-wpengine.netdna-ssl.com/wp-content/uploads(.*?)"',i,re.DOTALL)
                pic=imgs[:-1]
                if pic==[]:
                    img=''.join(re.findall('src="(.*?)"',i,re.DOTALL))
                    print(img)
                else:
                    img='https://471cnv1oagubqby1r32lcg9e-wpengine.netdna-ssl.com/wp-content/uploads'+'|https://471cnv1oagubqby1r32lcg9e-wpengine.netdna-ssl.com/wp-content/uploads'.join(pic)
            except:
                img = ''


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
            item['BasePrice'] = price
            item['BaseSqft'] = 0
            item['Baths'] = bath
            item['HalfBaths'] = halfbath + halfbaths
            item['Bedrooms'] = bed
            item['Garage'] = 0
            item['Description'] = Desc
            item['ElevationImage'] = img
            item['PlanWebsite'] = response.url
            yield item


# from scrapy.cmdline import execute
# execute("scrapy crawl focalpoint".split())