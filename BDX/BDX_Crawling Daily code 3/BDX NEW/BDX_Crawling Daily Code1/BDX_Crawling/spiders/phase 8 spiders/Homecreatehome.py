# -*- coding: utf-8 -*-
import hashlib
import re

import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class createHomesSpider(scrapy.Spider):
    name = 'Homecreatehome'
    allowed_domains = []
    start_urls = ['https://www.homecretehomes.com/']

    builderNumber = "16319"

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
        item['Street1'] = '3174 SW Savona Blvd'
        item['City'] = 'Port St Lucie'
        item['State'] = 'FL'
        item['ZIP'] = '34953'
        item['AreaCode'] = '772'
        item['Prefix'] = '248'
        item['Suffix'] = '4663'
        item['Extension'] = ""
        item['Email'] = 'info@homecretehomes.com'
        item['SubDescription'] = 'Homecrete Homes is your local Port St. Lucie home builder with a reputation of excellence – Homecrete has TWICE been awarded TCBA’s Builder of the Year Award. We believe in building YOUR home, not ours – providing you with the customization and modifications you need to make your new home just the way you imagine it.'
        item['SubImage'] = 'https://www.homecretehomes.com/wp-content/uploads/2020/04/3174sw-savona-model-pano-800px.jpg|https://www.homecretehomes.com/wp-content/uploads/2020/06/1.png|https://www.homecretehomes.com/wp-content/uploads/2020/06/1.png|https://www.homecretehomes.com/wp-content/uploads/2020/06/1.png|https://www.homecretehomes.com/wp-content/uploads/2020/06/1.png'
        item['SubWebsite'] = response.url
        yield item

        plan_link = 'https://www.homecretehomes.com/new-home-builder-port-st-lucie'

        yield scrapy.Request(url=plan_link, callback=self.plan_details,dont_filter=True)

    def plan_details(self, response):

        div=re.findall('class="x-container cs-ta-center max width"(.*?)VIEW BROCHURE',response.text,re.DOTALL)
        print(div)
        for i in div:
            pname= re.findall('<h3><span style="color: #215411;">(.*?)</span>',i)[0].strip()
            print(pname)
            if pname=='Tradewinds II':
                print(response.url)
            lk=re.findall('"https://www.homecretehomes.com/(.*?)"',i,re.DOTALL)
            lks=lk[:3]
            planlink="https://www.homecretehomes.com/"+lks[0]
            img="https://www.homecretehomes.com/"+lks[1]
            imagesurl="https://www.homecretehomes.com/"+lks[2]

            bth= re.findall('data-x-icon-o="&#xf80a;"  ></i>(.*?)Baths',i)[0].split(',')
            bath=bth[-1].strip()
            if '.' in bath:
                bath=bath.split('.')
                bath=bath[0]
                halfbath=1
            else:
                bath=bath
                halfbath=0

            bed= re.findall('data-x-icon-o="&#xf80a;"  ></i>(.*?)Bedrooms',i)[0].strip()
            sqft= re.findall('</i>Living Area:(.*?)Sq Feet',i)[0].replace(',','').strip()

            gr=re.findall('data-x-icon-o="&#xf80a;"  ></i>(.*?)Car Garage',i)[0].split(' ')
            garage=gr[-2].replace('></i>','')

            PlanNumber = int(hashlib.md5(bytes(str(planlink)+str(pname)+str(imagesurl), "utf8")).hexdigest(), 16) % (10 ** 30)
            unique = str(PlanNumber) + str(self.builderNumber)
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            head = {
                'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
            }
            yield scrapy.Request(url=imagesurl, callback=self.image_page,headers=head, meta={'pname':pname,'planlink':planlink,'halfbath':halfbath,'garage':garage,'bed':bed,'bath':bath,'sqft':sqft,'PN': unique_number,'Plannumber':PlanNumber,'img':img,'imageurl':imagesurl},dont_filter=True)

    def image_page(self,response):
        A = response.url
        z=response.text#.encode('ascii','ignore').decode('utf8')
        a=z#.decode("utf-8", "ignore")

        images=response.meta['img']
        image = '|'.join(re.findall('data-envira-retina="(.*?)"',a,re.DOTALL))
        ElevationImage = images +'|'+image
        print(ElevationImage)

        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = response.meta['Plannumber']
        item['unique_number'] = response.meta['PN']
        item['SubdivisionNumber'] = self.builderNumber
        item['PlanName'] = response.meta['pname']
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0
        item['BaseSqft'] = response.meta['sqft']
        item['Baths'] = response.meta['bath']
        item['HalfBaths'] = response.meta['halfbath']
        item['Bedrooms'] =response.meta['bed']
        item['Garage'] =response.meta['garage']
        item['Description'] = "Building a new home can be one of the biggest investments of your life. We want to make it one of the most rewarding. We invite you to come visit our model and explore all of your options. If you are in the market for a new home, you owe it to yourself to see how you can create the home of your dreams…"
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = response.meta['planlink']
        yield item

        url='https://www.homecretehomes.com/custom-home-builder/'
        yield scrapy.Request(url=url, callback=self.home_details,dont_filter=True)



    def home_details(self, response):

        unique = str("Plan Unknown") + str(self.builderNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
                    10 ** 30)  # < -------- Changes here
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

        home = re.findall('<h3><span style="color: #215411;">(.*?)jpg" ></a>', response.text, re.DOTALL)

        for k in home:

            try:
                SpecStreet1 =  re.findall('(.*?)</span>',k)[0].strip()

                SpecCity="Port St Lucie"
                SpecState = "FL"
                SpecZIP= '34953'

                web= re.findall('href="(.*?)"',k,re.DOTALL)
                webiste=web[1]


                ig=re.findall('data-options="thumbnail: (.*?)"',k,re.DOTALL)
                image=ig[1].replace("\'","").replace('\\','')

                unique = SpecStreet1 + SpecCity + SpecState + SpecZIP + webiste
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()

            except Exception as e:
                print(e)

            try:
                SpecBedrooms = re.findall('<li><strong>(.*?)Bedroom',k)[0].strip()
                print(SpecBedrooms)
            except Exception as e:
                print(str(e))

            try:
                SpecBaths = re.findall('Bedroom plus office,(.*?)full baths',k)[0].strip()
                if '.' in SpecBaths:
                    print(response.url)

            except Exception as e:
                print(str(e))


            try:
                SpecGarage = re.findall('baths,(.*?)car',k)[0].strip()

            except Exception as e:
                print(str(e))


            Sft= ''.join(re.findall('conditioned space(.*?)total square feet',k,re.DOTALL))
            SpecSqft = ''.join(re.findall('(\d+)',Sft,re.DOTALL))
            print(SpecSqft)

            try:
                MasterBedLocation = "Down"
            except Exception as e:
                print(e)

            try:
                SpecDescription = "At Homecrete Homes our philosophy is simple — Your Home, Built Better! To achieve this we offer the latest technology at affordable prices in the construction of Green – High Performance Energy – Sustainable homes. The environmentally friendly and sustainable homes we build focus on efficient use of energy, water and building materials. As a green builder we offer a variety of features and materials to help to improve your improve your living environment and your quality fo life."
            except Exception as e:
                print(e)


            # ----------------------- Don't change anything here --------------------- #
            item = BdxCrawlingItem_Spec()
            item['SpecNumber'] = SpecNumber
            item['PlanNumber'] = unique_number
            item['SpecStreet1'] = SpecStreet1
            item['SpecCity'] = SpecCity
            item['SpecState'] = SpecState
            item['SpecZIP'] = SpecZIP
            item['SpecCountry'] = "USA"
            item['SpecPrice'] = 0.00
            item['SpecSqft'] = SpecSqft
            item['SpecBaths'] = SpecBaths
            item['SpecHalfBaths'] = 0
            item['SpecBedrooms'] = SpecBedrooms
            item['MasterBedLocation'] = MasterBedLocation
            item['SpecGarage'] = SpecGarage
            item['SpecDescription'] = SpecDescription
            item['SpecElevationImage'] = image
            item['SpecWebsite'] = webiste
            yield item


# from scrapy.cmdline import execute
# execute("scrapy crawl Homecreatehome".split())