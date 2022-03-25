import hashlib
import re
import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class InsigniaSpider(scrapy.Spider):
    name ='Insignia'
    allowed_domains = []
    start_urls = ['https://insigniahomesinc.com/']

    builderNumber = "13327"

    def parse(self, response):
            url='https://insigniahomesinc.com/ourcommunities.php'
            yield scrapy.FormRequest(url=url, callback=self.page, dont_filter=True)

    def page(self,response):

        # div=response.xpath('//div[@id="boxcontainer"]/a[@class="community"]/@href').extract()
        # div=div[:4]
        div=response.xpath('//div[@id="boxcontainer"]')
        for i in div:
            a = i.xpath(
                './/p[@style="font-size:20px; font-weight: bold; color: red;"]//text()').extract_first()
            print(a)
            if a !='Sold Out!':
                    link=i.xpath('./a[@class="community"]/@href').extract_first()
                    comn='https://insigniahomesinc.com/' + link
                    yield scrapy.FormRequest(url=comn, callback=self.community, dont_filter=True)

    def community(self, response):
        s=response.url
        # ------------------- If No communities found ------------------- #
        try:
            SubdivisionName = response.xpath('//h1/text()').extract_first(default='').strip()
            print(SubdivisionName)
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = int(hashlib.md5(bytes(SubdivisionName, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        try:
            desc=''.join(response.xpath('//p/text()').extract())
        except:
            desc="Welcome to Insignia Homes, where you will always get the home that you want, built the way you want it. Choose from a dozen floor plans we have on hand, or bring your own. Either way, we will give you our absolute best price in either of our premier communities or on your own lot. You choose to do it your way."

        try:
            img='|'.join(response.xpath('//span[@class="thumbs"]/a//@src').extract())
            img=img.replace('./','http://www.insigniahomesinc.com/')

        except:
            img=''

        url=response.xpath('//iframe/@src').extract_first()
        sr=re.findall('!2s(.*?)!5e',url)[0]
        add=sr.split('%2C')
        street1 =add[0].replace('+',' ')
        ct=add[1].replace('+',' ').strip()
        st=add[-1].replace('+',' ')
        zipe=st.split(' ')
        zp=zipe[-1]
        sat=zipe[1]
        area='410'
        prefix='775'
        sufix='0688'


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
        item['Street1'] = street1
        item['City'] = ct
        item['State'] = sat
        item['ZIP'] = zp
        item['AreaCode'] = area
        item['Prefix'] = prefix
        item['Suffix'] = sufix
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = desc
        item['SubImage']=img
        item['SubWebsite'] = response.url
        yield item

        plan_link = 'http://www.insigniahomesinc.com/ourmodels.php'
        yield scrapy.Request(url=plan_link, callback=self.plan_link_page,meta={'sbdn': SubdivisionNumber},dont_filter=True)

    def plan_link_page(self, response):

        subdivisonNumber = response.meta['sbdn']
        plan_link=response.xpath('//div[@id="boxcontainer"]/a[@class="community"]/@href').extract()
        for plan in plan_link:
            plan = 'http://www.insigniahomesinc.com/'+ plan
            print(plan)
            yield scrapy.Request(url=plan, callback=self.plan_details,meta={'sbdn':  subdivisonNumber},dont_filter=True)

    def plan_details(self, response):

        SubdivisionNumber = response.meta['sbdn']

        name=response.xpath('//h1/text()').extract_first(default='').strip()

        PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)

        BSft = response.xpath('//ul[@class="information"][1]/li[1]/text()').extract_first()
        BaseSqft=''.join(re.findall(r"(\d+)", BSft, re.DOTALL))

        data=response.xpath('//ul[@class="information"][1]//li[3]/text()').extract_first()
        print(data)


        if 'Bath' not in data:
            print(response.url)
            data=response.xpath('//ul[@class="information"][1]//li[2]/text()').extract_first()

        else:
            data=data

        if ';' in data:
            dt=data.split(';')
        else:
            if ',' in data:

                dt=data.split(',')
                print(dt)
            else:
                dt=data.split('/')


        Bed=dt[0]
        Bed=''.join(re.findall(r"(\d+)", Bed,re.DOTALL))
        if response.url=='http://www.insigniahomesinc.com/models_coventry.php':
            Bed=3

        Baths=dt[1].strip()

        if '.' in Baths:
             Bath=Baths.split('.')
             Bath=Bath[0].strip()
             Halfbath=1
        elif response.url=='https://insigniahomesinc.com/models_coventry.php':
            Bath=2
            Halfbath=0
        elif '/' in Baths:
            Bath = Baths.split(' ')
            Bath = Bath[0].strip()
            Halfbath = 1

        else:

             if 'Bath'in Baths:
                 Bath=Baths.replace(' Bath','')
                 if 'Full' in Bath:
                     Bath=Bath.replace(' Full','')
                 print(Bath)
             Halfbath=0
        if 's' in Bath:
            Bath=Bath.replace('s','')
        try:
          Garage=response.xpath('//ul[@class="information"][1]/li[5]/text()').extract_first()
          print(Garage)
          if 'Garage' in Garage:
              Garage= ''.join(re.findall(r"(\d+)", Garage, re.DOTALL))
              Garage=Garage+ '.0'

          else:
                Garage=0.0
                print(Garage)
        except:
            Garage=0.0

        BasePrice= 0.00
        print(BasePrice)

        Desc = ', '.join(response.xpath('//ul[@class="information"]/li/text()').extract())

        try:
            img = '|'.join(response.xpath('//span[@class="thumbs"]/a//@src').extract())
            img = img.replace('./', 'http://www.insigniahomesinc.com/')

        except:
            img = ''

        unique = str(name) + str(response.url)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = name
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = BasePrice
        item['BaseSqft'] = BaseSqft
        item['Baths'] = Bath
        item['HalfBaths'] = Halfbath
        item['Bedrooms']=Bed
        item['Garage'] = Garage
        item['Description'] = Desc
        item['ElevationImage'] = img
        item['PlanWebsite'] = response.url
        yield item

#
# from scrapy.cmdline import execute
# execute("scrapy crawl Insignia".split())