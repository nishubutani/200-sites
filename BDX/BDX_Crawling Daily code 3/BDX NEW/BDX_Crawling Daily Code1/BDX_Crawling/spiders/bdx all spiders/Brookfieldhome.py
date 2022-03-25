import hashlib
import re
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
class mybrookfieldSpider(scrapy.Spider):
    name = 'mybrookfield'
    allowed_domains = []
    start_urls = ['https://brookfieldcustomhomes.com/']

    builderNumber = "22978"

    def parse(self, response):

        url='https://brookfieldcustomhomes.com/communities/'
        yield scrapy.FormRequest(url=url, callback=self.page, dont_filter=True)

    def page(self,response):
        a=response.text

        div=re.findall('<a href="https://brookfieldcustomhomes.com/communities/(.*?)">',a,re.DOTALL)
        print(div)
        com=div[1:]
        for k in com:
            comn = 'https://brookfieldcustomhomes.com/communities/'+ k

            yield scrapy.FormRequest(url=comn, callback=self.community, dont_filter=True)

    def community(self, response):

        try:
            SubdivisionName = response.xpath('//h1/text()').extract_first(default='').strip()
            print(SubdivisionName)
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = int(hashlib.md5(bytes(SubdivisionName, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        data=response.xpath('//div[@class="col-sm-12 no-gutters"]//h3/text()').extract_first().strip()
        st=data.split(',')
        street1=st[0]
        ct=st[-2].strip()
        dv=st[-1].split(' ')
        sat=dv[-2]
        if sat=='Oklahoma':
            sat='OK'
            ct='Goldsby'
        zp=dv[-1]

        try:
            desc=''.join(response.xpath('//div[@class="col-sm-12 no-gutters"]//p/text()').extract())
            if desc=='':
                desc="Building Dreams.That's our motto...Whether it’s our in-house architectural department, interior designers, community managers, construction managers, or our extensive 3,000 square foot design center, we are here to help bring all aspects of building, under one roof."
        except:
            desc="Building Dreams.That's our motto...Whether it’s our in-house architectural department, interior designers, community managers, construction managers, or our extensive 3,000 square foot design center, we are here to help bring all aspects of building, under one roof."

        try:
            img='|'.join(response.xpath('//div[@class="image-background image-large carousel-img show-medium"]/@style').extract())
            img=img.replace("background-image: url(","").replace(");","")
        except:
            img=''

        area = '405'
        prefix = '310'
        sufix = '6656'

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
        item['Email'] = 'Sales@brookfieldcustomhomes.com'
        item['SubDescription'] = desc
        item['SubImage']=img
        item['SubWebsite'] = response.url
        yield item

        plan_link = 'https://brookfieldcustomhomes.com/plans/'
        yield scrapy.Request(url=plan_link, callback=self.plan_link_page,meta={'sbdn': SubdivisionNumber},dont_filter=False)

    def plan_link_page(self, response):
        s=response.text
        subdivisonNumber = response.meta['sbdn']
        plan_links=re.findall('<a href="https://brookfieldcustomhomes.com/plans/(.*?)">',s,re.DOTALL)
        plan=plan_links[1:]
        for j in plan:
            link = 'https://brookfieldcustomhomes.com/plans/'+ j
            yield scrapy.Request(url=link, callback=self.plan_details,meta={'sbdn':  subdivisonNumber},dont_filter=False)

    def plan_details(self, response):

        SubdivisionNumber = response.meta['sbdn']

        name=response.xpath('//div[@class="col-md-9 col-sm-12 margin-b-sm"]//h1/text()').extract_first().strip()

        PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)

        info=response.xpath('//div[@class="col-md-7 col-sm-12 col-xs-12 no-gutters margin-t-sm margin-b-sm"]//h5/text()').extract()
        print(info)

        BSft = info[-1]
        BaseSqft = BSft.replace(' ft', '').replace(',','')
        print(BaseSqft)

        Bed=info[0].replace(' Bed','')

        Baths=info[1].replace(' Bath','')
        if '.' in Baths:
            Bath=Baths.split('.')
            Bath=Bath[0]
            Halfbath=1
        else:
            Bath=Baths
            Halfbath=0

        try:
            Garage=info[2].replace(' Garage','')
        except:
            Garage=0.0

        try:
            BsPrice = response.xpath('//div[@class="margin-b-sm"]//h4/text()').extract_first()
            if '-' in BsPrice:
                bs=BsPrice.split('-')
                BsPrice=bs[-1]
            BasePrice=''.join(re.findall(r"(\d+)", BsPrice,re.DOTALL))
            if response.url=='https://brookfieldcustomhomes.com/plans/159-012226/':
                if int(BasePrice)<40000:
                    BasePrice=0.00
            print(BasePrice)
        except:
            print(response.url)

        try:
            Desc = response.xpath('//div[@class="col-md-9 col-sm-12 margin-b-sm"]//p/text()').extract_first(default=True)
            if Desc==True:
                Desc=', '.join(response.xpath('//div[@class="col-md-9 col-sm-12 margin-b-sm"]//text()').extract()).replace('\t','').strip().replace('\n','').replace(',',' ')
                print(Desc)
        except:
            Desc=''

        try:
            img = '|'.join(response.xpath(
                '//div[@class="image-background image-large carousel-img show-medium container-border"]/@style').extract())
            img = img.replace("background-image: url(", "").replace(");", "")
        except:
            img = ''

        unique = str(SubdivisionNumber) + str(response.url)
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

        a = response.xpath('//div[@class="card"]')
        if a==[]:
            home_link = 'https://brookfieldcustomhomes.com/homes/'
            yield scrapy.Request(url=home_link, callback=self.home_link_page, meta={'PN': unique_number},
                                 dont_filter=True)
        else:
            s = response.xpath('//i[@class="fa fa-circle text-green"]/@aria-hidden').extract_first()
            print(s)
            n=response.xpath('//i[@class="fa fa-star text-yellow"]/@aria-hidden').extract_first()
            print(n)
            p=response.xpath('//i[@class="fa fa-star text-yellow"]/@aria-hidden').extract_first()
            if s=='true' or n=='true' or p=='true':
                url=response.xpath('//div[@class="card"]/a/@href').extract()
                for i in url:
                    link=i
                    yield scrapy.Request(url=link, callback=self.home_details, meta={'PN': unique_number}, dont_filter=True)


    def home_link_page(self, response):
            r = response.text
            PlanNumber = response.meta['PN']

            home_links = re.findall('<a href="https://brookfieldcustomhomes.com/homes/(.*?)">', r, re.DOTALL)
            home = home_links[1:]
            for home in home:
                home = 'https://brookfieldcustomhomes.com/homes/' + home
                yield scrapy.Request(url=home, callback=self.home_details, meta={'PN': PlanNumber}, dont_filter=True)

    def home_details(self, response):

            PlanNumber = response.meta['PN']
            s = response.xpath('//*[contains(text(),"Status: ")]//text()').extract()
            s = s[-1].strip()

            if s != 'Sold':

                data = response.xpath(
                    '//div[@class="col-md-7 col-sm-12 col-xs-12 no-gutters margin-t-sm margin-b-sm"]//h5/text()').extract()
                try:
                    SpecBedrooms = data[0].replace(' Bed', '')
                except Exception as e:
                    print(str(e))

                SpecBaths = data[1].replace(' Bath', '')
                if '.' in SpecBaths:
                    Bath = SpecBaths.split('.')
                    SpecBaths = Bath[0]
                    Spechalfbath = 1
                else:
                    SpecBaths = SpecBaths
                    Spechalfbath = 0

                try:
                    SpecGarage = data[2].replace(' Garage', '')
                except:
                    SpecGarage = 0.0

                Bsqft = data[-1]
                SpecSqft = Bsqft.replace(' ft', '').replace(',', '')

                try:
                    MasterBedLocation = "Down"
                except Exception as e:
                    print(e)

                try:
                    SpecDescription = response.xpath(
                        '//div[@class="col-md-9 col-sm-12 margin-b-sm"]//p/text()').extract_first(default=True)
                    if SpecDescription == True:
                        SpecDescription = ', '.join(
                            response.xpath('//div[@class="col-md-9 col-sm-12 margin-b-sm"]//text()').extract()).replace(
                            '\t', '').strip().replace('\n', '').replace(',',' ')
                except Exception as e:
                    print(e)

                try:
                    img = '|'.join(response.xpath(
                        '//div[@class="image-background image-large carousel-img show-medium"]/@style').extract())
                    img = img.replace("background-image: url(", "").replace(");", "")
                except:
                    img = ''

                try:
                    add = ''.join(response.xpath('//h2[@class="margin-b-sm margin-t-none"]/text()').extract())
                    add = add.split(',')
                    SpecStreet1 = add[0].strip()
                    SpecCity = add[-2].strip()
                    st = add[-1].split(' ')
                    SpecState = st[-2]
                    if SpecState == 'Oklahoma':
                        SpecState = 'OK'
                    SpecZIP = st[-1]

                    try:
                        SpecPrice = response.xpath('//div[@class="margin-b-sm"]//h4/text()').extract_first()
                        SpecPrice = ''.join(re.findall(r"(\d+)", SpecPrice, re.DOTALL))
                    except Exception as e:
                        print(str(e))

                    unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()

                except Exception as e:
                    print(e)

                try:
                    PlanNumber = response.meta['PN']
                except Exception as e:
                    print(e)

                try:
                    SpecCountry = "USA"
                except Exception as e:
                    print(e)

                # ----------------------- Don't change anything here --------------------- #
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = PlanNumber
                item['SpecStreet1'] = SpecStreet1
                item['SpecCity'] = SpecCity
                item['SpecState'] = SpecState
                item['SpecZIP'] = SpecZIP
                item['SpecCountry'] = SpecCountry
                item['SpecPrice'] = SpecPrice
                item['SpecSqft'] = SpecSqft
                item['SpecBaths'] = SpecBaths
                item['SpecHalfBaths'] = Spechalfbath
                item['SpecBedrooms'] = SpecBedrooms
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = SpecGarage
                item['SpecDescription'] = SpecDescription
                item['SpecElevationImage'] = img
                item['SpecWebsite'] = response.url
                yield item

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl mybrookfield".split())