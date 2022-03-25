import hashlib
import re
import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class compassSpider(scrapy.Spider):
    name ='compass'
    allowed_domains = []
    start_urls = ['https://compassal.com/']

    builderNumber = 48380

    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        img=re.findall('<img src="https://compassal.com/wp-content/uploads/2016(.*?)"',response.text,re.DOTALL)
        print(img)
        images='https://compassal.com/wp-content/uploads/2016'+ '|https://compassal.com/wp-content/uploads/2016'.join(img)

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
        item['Street1'] = '2225 Highway 72 East'
        item['City'] = 'Huntsville'
        item['State'] = 'AL'
        item['ZIP'] = '35811'
        item['AreaCode'] = '256'
        item['Prefix'] ='217'
        item['Suffix'] = '5444'
        item['Extension'] = ""
        item['Email'] ='sales@compassal.com'
        item['SubDescription'] = "Trust your dream to Compass Homes.Once you’ve purchased the land in your ideal area, Compass Homes works with you, discussing all the implications and possibilities for your new house.Let us build a home on your land that fits all your specifications. Compass Homes understands that building a home is a process, and during that process, ideas are subject to change. Rather than developing cookie-cutter neighborhoods, we work closely with you to create your perfect house.We monitor progress, relay information, and check back with our clients periodically throughout the construction of your home to make sure everyone has the same vision in mind. More than that, we want you to be involved in each decision, giving you the power to define every element of the design. Our attention to detail allows us to execute your ideas."
        item['SubImage']= images
        item['SubWebsite'] = response.url
        yield item

        plan_link = 'https://compassal.com/product-category/our-plans/'
        yield scrapy.Request(url=plan_link, callback=self.plan_link_page,dont_filter=True)

    def plan_link_page(self, response):
        link=response.xpath('//div[@class="products_wrapper isotope_wrapper"]//a[@class="button button_large button_js"]/@href').extract()
        for i in link:
            link=i
            print(link)
            yield scrapy.Request(url=link, callback=self.plan_details,dont_filter=True)

    def plan_details(self, response):

        PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)

        name=response.xpath('//h1[@itemprop="name"]/text()').extract_first()

        try:

            try:
                halfbath = response.xpath(
                    '//tr[@class="woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_half-bathrooms"]//td[@class="woocommerce-product-attributes-item__value"]//text()').extract_first()
                print(halfbath)
                if halfbath == None:
                    halfbath = 0
            except:
                halfbath = 0

            bath=response.xpath('//tr[@class="woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_bathrooms"]//td[@class="woocommerce-product-attributes-item__value"]//text()').extract_first()
            print(bath)
            if '.'in bath:
                bath=bath.split('.')
                b=bath[0]
                b1=b.split('or')
                bath=b1[-1].strip()
                halfbath=1
            if 'or' in bath:
                bath=bath.split('or')
                bt=bath[0]
                bath=bt.split('-')
                bath=bath[-1]
            if 'to' in bath:
                bath=bath.split(' ')
                bath=bath[-1]
        except:
            bath=0


        bed= response.xpath('//tr[@class="woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_bedrooms"]//td[@class="woocommerce-product-attributes-item__value"]//text()').extract_first()
        if 'to' in bed:
            bed = bed.split(' ')
            bed = bed[-1]
        if '+' in bed:
            bed=bed.replace('+','')

        if name=='Grayson Signature':
            print(bed)
        try:
            sqft= response.xpath('//tr[@class="woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_approx-sq-ft"]//td[@class="woocommerce-product-attributes-item__value"]//text()').extract_first().replace(',','')
            print('sqft--->',sqft,response.url)

        except:
            sqft=response.xpath('//tr[@class="woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_approx-sq-ft"]//td[@class="woocommerce-product-attributes-item__value"]//text()').extract_first()
            sqft=sqft.replace(',','')
        try:
            price=response.xpath('//tr[@class="woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_price"]//td[@class="woocommerce-product-attributes-item__value"]//text()').extract_first()
            price=price.replace('$','').replace(',','')
        except:
            price=0

        try:
            garage= response.xpath('//tr[@class="woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_garages"]//td[@class="woocommerce-product-attributes-item__value"]//text()').extract_first().strip()
            if 'or' in garage:
                garage = garage.split('or')
                garage = garage[-1]
            if 'Car' in garage:
                garage=garage.replace('Car','').strip()
            if 'to' in garage:
                garage=garage.split(' ')
                garage=garage[-1]


            Garage = ''.join(re.findall(r"(\d+)", garage, re.DOTALL))
            Garage = Garage + '.0'
            print('garage--->',Garage)

            if garage=='No Garage':
                Garage=0.0
                print('garage-',Garage)
        except:
            Garage=0.0

        try:
            Desc ="Thank you for considering BlueStone Custom Builders to make your dream home a reality!As a 'Cost Plus' builder, we build custom homes in Omaha in the $400,000 – $1,000,000 price range, partnering with you throughout the entire home building process to ensure your dream home needs are met.Contact us today at (402) 871-4411 or to view model homes in Omaha and new construction homes in Omaha to find what you like best, and let’s build your dream home together!BlueStone Custom Builders is the premier custom home builder in Omaha, Nebraska; click here to see what people are saying about us."
        except:
            Desc = ''

        try:
            p = ''.join(re.findall('<div class="mobile-top-related-products">(.*?)<img loading',response.text,re.DOTALL))
            plimg=re.findall('<a href="(.*?)"',p,re.DOTALL)

            im=''.join(re.findall('class="mobile-image-gallery"(.*?)</figure>',response.text,re.DOTALL))
            im=re.findall('data-thumb="(.*?)"',im,re.DOTALL)

            images='|'.join(im + plimg)
        except:
            images= ''

        SubdivisionNumber=self.builderNumber
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
        item['BasePrice'] = price
        item['BaseSqft'] = sqft
        item['Baths'] = bath.strip()
        item['HalfBaths'] = halfbath
        item['Bedrooms'] = bed
        item['Garage'] = Garage
        item['Description'] = Desc
        item['ElevationImage'] = images
        item['PlanWebsite'] = response.url
        yield item

#
# from scrapy.cmdline import execute
# execute("scrapy crawl compass".split())