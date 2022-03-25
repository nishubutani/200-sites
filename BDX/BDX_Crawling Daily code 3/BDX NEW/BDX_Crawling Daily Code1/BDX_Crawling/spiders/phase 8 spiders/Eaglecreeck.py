import hashlib
import re
import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class eglecreckSpider(scrapy.Spider):
    name ='eaglecrek'
    allowed_domains = []
    start_urls = ['https://eaglecreekhomes.net/']

    builderNumber = 49506

    def parse(self, response):
            url='https://eaglecreekhomes.net/neighborhoods/'
            yield scrapy.FormRequest(url=url, callback=self.page, dont_filter=True)

    def page(self,response):

        div=['https://eaglecreekhomes.net/neighborhood/pfeiffer-pines/','https://eaglecreekhomes.net/neighborhood/railview-ridge/','https://eaglecreekhomes.net/neighborhood/the-condos-at-railview/']
        for k in div:
            comn= k

            yield scrapy.FormRequest(url=comn, callback=self.community, dont_filter=True)

    def community(self, response):
        s=response.url

        try:
            SubdivisionName = response.xpath('//h1[@data-aos="fade-in"]/text()').extract_first(default='').strip()
            print(SubdivisionName)
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = int(hashlib.md5(bytes(SubdivisionName, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        try:
            desc=''.join(response.xpath('//div[@class="c-split-content__item"]//p//text()').extract())
        except:
            desc="Eagle Creek Homes stands among the top  West Michigan home builders around. Our transparent custom workflow involves clients in every step of the homebuilding process, ensuring that their vision stays on track, while remaining within budget.If you’re planning on building a home in West Michigan, we have multiple housing development communities with plots ready to build on. For something more immediate, browse our move-in ready homes featured on our site."

        try:
            img=response.xpath('//meta[@property="og:image"]/@content').extract()
            img2=re.findall('data-lazy="(.*?)"',response.text,re.DOTALL)

            if img2==[]:
                images=img
            else:
                images= '|'.join(img  + img2)
        except:
            images=''

        st= response.xpath('//div[@class="c-split-content"]//span/text()').extract_first().strip()
        if  ',' in st:
            add=st.split(',')
            print(add)
            street = add[0]

            ct = add[1].strip()
            cty = ct.split(' ')
            sat = cty[-1]
            if sat in ct:
                city = ct.replace(sat, '')
                city = city.strip()
            print(st)

        else:
            add=st.split(' ')
            print(add)
            street=' '.join(add[0:4])
            city=add[-3]

        zp=add[-1].strip()
        if 'MI' in zp:
            zp=zp.split(' ')
            zip=zp[-1]
            print(zip)
        else:
            zip=zp

        area='616'
        prefix='583'
        sufix='7700'
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
        item['City'] = city
        item['State'] = 'MI'
        item['ZIP'] = zip
        item['AreaCode'] = area
        item['Prefix'] = prefix
        item['Suffix'] = sufix
        item['Extension'] = ""
        item['Email'] = 'info@eaglecreekhomes.net'
        item['SubDescription'] = desc
        item['SubImage']= images
        item['SubWebsite'] = response.url
        yield item

        plan_link = 'https://eaglecreekhomes.net/custom-floor-plans/'
        yield scrapy.Request(url=plan_link, callback=self.plan_link_page,dont_filter=True)

    def plan_link_page(self, response):
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '1360 84th St. SW'
        item['City'] = 'Byron Center'
        item['State'] = 'MI'
        item['ZIP'] = '49315'
        item['AreaCode'] = '616'
        item['Prefix'] = '583'
        item['Suffix'] = '7700'
        item['Extension'] = ""
        item['Email'] = 'info@eaglecreekhomes.net'
        item[
            'SubDescription'] = "Eagle Creek Homes stands among the top  West Michigan home builders around. Our transparent custom workflow involves clients in every step of the homebuilding process, ensuring that their vision stays on track, while remaining within budget.If you’re planning on building a home in West Michigan, we have multiple housing development communities with plots ready to build on. For something more immediate, browse our move-in ready homes featured on our site."
        item['SubImage'] = 'https://eaglecreekhomes.net/wp-content/uploads/2019/01/20181004134939692299000000-o.jpg'
        item['SubWebsite'] = response.url
        yield item

        plan_link=response.xpath('//div[@class="c-plan-listing"]//div[@class="c-plan-listing__details"]//a/@href').extract()
        for plan in plan_link:
            plan = plan
            yield scrapy.Request(url=plan, callback=self.plan_details,dont_filter=True,meta={'sbdn':self.builderNumber})

    def plan_details(self, response):

        name=response.xpath('//div[@class="c-plan-listing__heading"]/h1/text()').extract_first(default='').strip()

        PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)

        dt=response.xpath('//div[@class="c-plan-listing__details"]//dd//text()').extract()
        print(dt)

        if len(dt)>3:
            garage=dt[-2]
            garage=''.join(re.findall(r"(\d+)", garage, re.DOTALL))
            garage=garage+'.0'

        else:
            garage=0.0

        try:
            BSft = dt[-1].replace(',','')
        except:
            BSft=0

        try:
            Desc = ''.join(response.xpath('//div[@class="c-prose"]/p/text()').extract())
            if Desc=='':
                Desc="Eagle Creek Homes stands among the top  West Michigan home builders around. Our transparent custom workflow involves clients in every step of the homebuilding process, ensuring that their vision stays on track, while remaining within budget.If you’re planning on building a home in West Michigan, we have multiple housing development communities with plots ready to build on. For something more immediate, browse our move-in ready homes featured on our site."
            if Desc=='\xa0\xa0':
                Desc=''.join(response.xpath('//div[@class="c-prose"]/p/span/text()').extract())
                print(Desc)
        except:
            Desc="Eagle Creek Homes stands among the top  West Michigan home builders around. Our transparent custom workflow involves clients in every step of the homebuilding process, ensuring that their vision stays on track, while remaining within budget.If you’re planning on building a home in West Michigan, we have multiple housing development communities with plots ready to build on. For something more immediate, browse our move-in ready homes featured on our site."

        try:
            Bed=dt[0]
        except:
            Bed=0

        try:
            Baths=dt[1].strip()
            if '.' in Baths:
                Baths=Baths.split('.')
                Baths=Baths[0]
                halfbath=1
            else:
                Baths=Baths
                halfbath=0
        except:
            Baths=0
            halfbath=0


        BasePrice= 0.00
        print(BasePrice)

        try:
            img = '|'.join(re.findall('data-lazy="(.*?)"',response.text,re.DOTALL))
        except:
            img = ''

        unique = str(self.builderNumber) + str(response.url)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = response.meta['sbdn']
        item['PlanName'] = name
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = BasePrice
        item['BaseSqft'] = BSft
        item['Baths'] = Baths
        item['HalfBaths'] = halfbath
        item['Bedrooms']=Bed
        item['Garage'] = garage
        item['Description'] = Desc
        item['ElevationImage'] = img
        item['PlanWebsite'] = response.url
        yield item

        home_link = 'https://eaglecreekhomes.net/move-in-ready-homes/'
        yield scrapy.Request(url=home_link, callback=self.home_link_page,dont_filter=True)

    def home_link_page(self, response):
        unique = str("Plan Unknown") + str(self.builderNumber)  # < -------- Changes here
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
        item['Description'] = "Eagle Creek Homes stands among the top  West Michigan home builders around. Our transparent custom workflow involves clients in every step of the homebuilding process, ensuring that their vision stays on track, while remaining within budget.If you’re planning on building a home in West Michigan, we have multiple housing development communities with plots ready to build on. For something more immediate, browse our move-in ready homes featured on our site."
        item['ElevationImage'] = "https://eaglecreekhomes.net/wp-content/uploads/2019/01/20181004135003389635000000-o.jpg"
        item['PlanWebsite'] = "https://eaglecreekhomes.net/custom-floor-plans/"
        yield item

        home_links = re.findall("<button href='(.*?)'",response.text,re.DOTALL)
        print(home_links)
        for home in home_links:
            link = home
            yield scrapy.Request(url=link, callback=self.home_details,meta={'plan_number':unique_number},dont_filter=True)

    def home_details(self, response):

                ads = ''.join(response.xpath('//div[@class="c-listing__header"]//h1/text()').extract())
                print(ads)

                add=ads.split(',')
                print(add)
                SpecStreet1 = add[0]
                print(SpecStreet1)

                SpecCity = add[-2]
                print(SpecCity)

                try:
                    SpecZIP = re.findall('Zip Code:</b>(.*?)</div>',response.text)[0].strip()
                    print(SpecZIP)
                except:
                    SpecZIP = '00000'

                SpecState='MI'

                try:
                    SpecPrice = re.findall('<b>Current Price:</b>(.*?)</div>',response.text)[0].strip()
                    SpecPrice = ''.join(re.findall(r"(\d+)", SpecPrice, re.DOTALL))
                except Exception as e:
                    print(str(e))

                unique = SpecStreet1 + SpecCity + SpecState + SpecZIP + SpecPrice
                print(unique)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()


                try:
                    PlanNumber = response.meta['plan_number']
                except Exception as e:
                    print(e)


                try:
                    SpecBedrooms = re.findall('<b>Total Bedrooms:</b>(.*?)</div>',response.text)[0].strip()
                    print(SpecBedrooms)
                except Exception as e:
                    SpecBedrooms=0
                    print(str(e))

                try:
                    SpecBaths = re.findall('<b>Total Baths:</b>(.*?)</div>',response.text)[0].strip()
                except Exception as e:
                    SpecBaths=0
                    print(str(e))

                try:
                    halfbaths=re.findall('<b>Half Baths:</b>(.*?)</div>',response.text)[0].strip()
                    print(halfbaths)
                except:
                    halfbaths=0

                try:
                    SpecGarage = re.findall('<b>Garage Type: </b>(.*?);',response.text)[0].strip()
                except Exception as e:
                    SpecGarage=0.0
                    print(str(e))

                # SpecSqft = response.xpath('//h3[@class="js-sqft"]/text()').extract_first().strip()
                SpecSqft=re.findall('<b>SqFt Above Grade:</b>(.*?)</div>',response.text)[0].strip()
                print(SpecSqft)

                try:
                    # SpecDescription = response.xpath('//div[@class="js-property-description c-listing__property-description"]/p/text()').extract_first().strip()
                    description=''.join(re.findall('Description</b><br />(.*?)<br />',response.text,re.DOTALL))
                    print(description)
                except Exception as e:
                    description="Eagle Creek Homes stands among the top  West Michigan home builders around. Our transparent custom workflow involves clients in every step of the homebuilding process, ensuring that their vision stays on track, while remaining within budget.If you’re planning on building a home in West Michigan, we have multiple housing development communities with plots ready to build on. For something more immediate, browse our move-in ready homes featured on our site."

                image = '|'.join(re.findall("fullsrc='(.*?)'",response.text,re.DOTALL))
                print(image)

                try:
                    SpecWebsite = response.url
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
                item['SpecCountry'] = 'USA'
                item['SpecPrice'] = SpecPrice
                item['SpecSqft'] = SpecSqft
                item['SpecBaths'] = SpecBaths
                item['SpecHalfBaths'] = halfbaths
                item['SpecBedrooms'] = SpecBedrooms
                item['MasterBedLocation'] = "Down"
                item['SpecGarage'] = SpecGarage
                item['SpecDescription'] = description
                item['SpecElevationImage'] = image
                item['SpecWebsite'] = SpecWebsite
                yield item

#
from scrapy.cmdline import execute
# execute("scrapy crawl eaglecrek".split())