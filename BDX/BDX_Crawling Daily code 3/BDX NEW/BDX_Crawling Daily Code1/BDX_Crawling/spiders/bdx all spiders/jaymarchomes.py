# -*- coding: utf-8 -*-
import json

import scrapy
import requests
from scrapy.http import HtmlResponse
import hashlib
import re
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec

class JaymarchomesSpider(scrapy.Spider):
    name = 'jaymarchomes'
    allowed_domains = []
    start_urls = ['http://www.jaymarchomes.com/']

    builderNumber = "929843199539117778734802277596"

    def parse(self, response):

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        # f = open("html/%s.html" % self.builderNumber, "wb")
        # f.write(response.body)
        # f.close()

        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = "7525 SE 24th St., Ste 487"
        item['City'] = "Mercer Island"
        item['State'] = "WA"
        item['ZIP'] = "98040"
        item['AreaCode'] = "425"
        item['Prefix'] = "226"
        item['Suffix'] = "9100"
        item['Extension'] = ""
        item['Email'] = "Email"
        item['SubDescription'] = " ".join(response.xpath('//*[@class="WelcomeSection_body"]//text()').extract())
        item['AmenityType'] = ''
        try:
            options = Options()
            options.add_argument("--headless")
            driver = webdriver.Firefox(firefox_options=options)
            driver.get('https://www.jaymarchomes.com/homes-gallery')
            try:
                driver.find_element_by_xpath('//span[@data-reactid="286"]').click()
            except Exception as e:
                print(e)
            Strhtml = driver.page_source
            mainURL = driver.current_url
            driver.quit()
            response_i = HtmlResponse(url=mainURL,body=Strhtml.encode('utf8'))
            images = '|'.join(response_i.xpath('//*[@class="PhotoList_image"]/@style').extract()).replace("background-image:url('",'').replace("');",'').replace('background-image: url("','').replace('");','').strip()
        except Exception as e:
            print(e)
        item['SubImage'] = images.replace('/400','/1080')
        item['SubWebsite'] = response.url
        yield item

        res_u = requests.get('https://www.jaymarchomes.com/sitemap.xml')
        response_u = HtmlResponse(url=res_u.url,body=res_u.content)

        # ------------------------------------------------ PLANS --------------------------------------------------- #

        plan_ref = {}
        head_p = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
        plan_links = re.findall(r'<loc>(.*/plan/.*)</loc>',response_u.body.decode('utf8'))
        for plan_link in plan_links:
            res_p = requests.get(plan_link, headers=head_p)
            response_p = HtmlResponse(url=res_p.url,body=res_p.content)

            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                PlanNumber = int(hashlib.md5(bytes(response_p.url,"utf8")).hexdigest(), 16) % (10 ** 30)
            except Exception as e:
                print(e)

            try:
                PlanName = response_p.xpath('//h1/text()').extract_first(default='').strip()
            except Exception as e:
                print(e)

            try:
                PlanNotAvailable = 0
            except Exception as e:
                print(e)

            try:
                PlanTypeName = 'Single Family'
            except Exception as e:
                print(e)

            try:
                BasePrice = 0
            except Exception as e:
                print(e)


            try:
                data_json = re.findall('window.__PRELOADED_STATE__.*=\s+(.*?)</script>',response_p.text)[0]
                df = json.loads(data_json)
                Description = df['cloudData']['plans']['5702b277f410954eb27ce7b4']['data'][0]['description']
            except Exception as e:
                print(e)

            try:
                # ---------------- bedrooms
                Bedrooms = response_p.xpath('//li[contains(@style,"bed")]//text()').extract_first(default=0).strip()

                # ---------------- bathrooms
                bath_raw = ''.join(response_p.xpath('//li[contains(@style,"bath")]//text()').extract())
                if bath_raw!=0:
                    tmp = re.findall(r"(\d+)", bath_raw)
                    Baths = tmp[0]
                    if len(tmp) > 1:
                        HalfBaths = 1
                    else:
                        HalfBaths = 0
                else:
                    Baths = 0
                    HalfBaths = 0
                # ------------------ sqft
                BaseSqft = response_p.xpath('//li[contains(@style,"sqft")]//text()').extract_first(default=0).replace(',','').strip()
                # ------------------ garage
                Garage = response_p.xpath('//li[contains(text(),"Garage")]//text()').extract_first(default=0).strip()
            except Exception as e:
                print(e)

            try:
                ElevationImage = []
                img1 = df['cloudData']['plans']['5702b277f410954eb27ce7b4']['data'][0]['elevationPhotos']
                if img1!=[]:
                    for one in img1:
                        ElevationImage.append(one['contentUrl'])
                img2 = df['cloudData']['plans']['5702b277f410954eb27ce7b4']['data'][0]['floorplanPhotos']
                if img2 != []:
                    for one in img2:
                        ElevationImage.append(one['contentUrl'])
                ElevationImage = '|'.join(ElevationImage)
            except Exception as e:
                print(e)

            try:
                PlanWebsite = str(response_p.url)
                # print(PlanWebsite)
            except Exception as e:
                print(e)

            # ----------------------- Don't change anything here --------------
            try:
                unique = str(PlanName)+str(response_p.url)+str(self.builderNumber)   # < -------- Changes here
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
                plan_ref[PlanName]=unique_number

                item = BdxCrawlingItem_Plan()
                item['Type'] = Type
                item['PlanNumber'] = PlanNumber
                item['unique_number'] = unique_number  # < -------- Changes here
                item['SubdivisionNumber'] = self.builderNumber
                item['PlanName'] = PlanName
                item['PlanNotAvailable'] = PlanNotAvailable
                item['PlanTypeName'] = PlanTypeName
                item['BasePrice'] = BasePrice
                item['BaseSqft'] = BaseSqft
                item['Baths'] = Baths
                item['HalfBaths'] = HalfBaths
                item['Bedrooms'] = Bedrooms
                item['Garage'] = Garage
                item['Description'] = Description[:1500]
                item['ElevationImage'] = ElevationImage
                item['PlanWebsite'] = PlanWebsite
                yield item
            except Exception as e:
                print(e)

        print(plan_ref)
        # ------------------------------------------------ HOMES --------------------------------------------------- #

        spec_links = re.findall(r'<loc>(.*/homes/.*/.*)</loc>',response_u.body.decode('utf8'))
        for spec in spec_links:
            res_s = requests.get(spec)
            response_s = HtmlResponse(url=res_s.url,body=res_s.content)

            # ------------------------------------------- Extract Homedetails ------------------------------ #

            status = response_s.xpath('//span[@class="HomePrice_status"]/text()').extract_first(default='').strip()
            if 'Sold' in status:
                continue

            spec_json = response_s.xpath('//script[@type="application/ld+json"][2]/text()').extract_first(default='').strip()
            sdf = json.loads(spec_json)
            try:

                SpecStreet1 = sdf['address']['streetAddress']
                SpecCity = sdf['address']['addressLocality']
                SpecState = sdf['address']['addressRegion']
                SpecZIP = sdf['address']['postalCode']

                unique = SpecStreet1 + SpecCity + SpecState + SpecZIP + str(response.url)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response_s.body)
                f.close()

            except Exception as e:
                print(e)

            try:
                plan_spec_ref = 'The '+response_s.xpath('//span[@class="HomeAddress_link"]/a/text()').extract_first(default='').strip()
                try:PlanNumber = plan_ref.get(plan_spec_ref) if plan_ref.get(plan_spec_ref)!=None else print("check on this")
                except:print("check on this")
            except Exception as e:
                print(e)

            try:
                SpecCountry = "USA"
            except Exception as e:
                print(e)

            try:
                SpecPrice = response_s.xpath('//h4[contains(@class,"price")]/b/text()').extract_first(default=0).replace('$','').replace(',','').strip()
                if 'Pricing' in SpecPrice:
                    SpecPrice=0
            except Exception as e:
                print(e)

            try:
                SpecSqft = response_s.xpath('//li[contains(@style,"sqft")]//text()').extract_first(default=0).replace(',','').strip()
            except Exception as e:
                SpecSqft = 0


            try:
                SpecBaths = ''.join(response_s.xpath('//li[contains(@style,"bath")]//text()').extract())
                tmp = re.findall(r"(\d+)", SpecBaths)
                SpecBaths = tmp[0]
                if len(tmp) > 1:
                    SpecHalfBaths = 1
                else:
                    SpecHalfBaths = 0
            except Exception as e:
                SpecBaths = 0
                SpecHalfBaths = 0


            try:
                SpecBedrooms = response_s.xpath('//li[contains(@style,"bed")]//text()').extract_first(default=0).strip()
            except Exception as e:
                SpecBedrooms = 0


            try:
                MasterBedLocation = "Down"
            except Exception as e:
                print(e)

            try:
                SpecGarage = response_s.xpath('//li[contains(text(),"Garage")]//text()').extract_first(default=0).strip()
            except Exception as e:
                SpecGarage = 0


            try:
                SpecDescription = ''
            except Exception as e:
                print(e)

            try:
                SpecElevationImage = sdf['image']
            except Exception as e:
                print(e)

            try:
                SpecWebsite = response_s.url
            except Exception as e:
                print(e)

            # ----------------------- Don't change anything here ---------------- #
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
            item['SpecHalfBaths'] = SpecHalfBaths
            item['SpecBedrooms'] = SpecBedrooms
            item['MasterBedLocation'] = MasterBedLocation
            item['SpecGarage'] = SpecGarage
            item['SpecDescription'] = SpecDescription[:1500]
            item['SpecElevationImage'] = SpecElevationImage
            item['SpecWebsite'] = SpecWebsite
            yield item
            # --------------------------------------------------------------------- #





from scrapy.cmdline import execute
# execute("scrapy crawl jaymarchomes".split())

'''
common comm images:
'https://www.jaymarchomes.com/images/uploaded/858115707989782_idea-house-great-room.jpg|https://www.jaymarchomes.com/images/uploaded/379998654592782_jimkat2_copy.png|https://www.jaymarchomes.com/images/uploaded/393873222172260_san-marino-kitchen.jpg|https://www.jaymarchomes.com/images/uploaded/213558939285576_idea-house-wine-room.jpg|https://www.jaymarchomes.com/images/uploaded/109832932241261_kidplay1.png|https://www.jaymarchomes.com/images/uploaded/545903003774583_idea-house-mb2.jpg|https://www.jaymarchomes.com/images/uploaded/241052879020571_san-marino-deck.jpg|https://www.jaymarchomes.com/images/uploaded/235810711048543_kitchen1_copy.png|https://www.jaymarchomes.com/images/uploaded/704840474762022_san-marino-mb.jpg|https://www.jaymarchomes.com/images/uploaded/604309115093201_copenhagen-kitchen.jpg|https://www.jaymarchomes.com/images/uploaded/776362258475273_jm_park_007_copyweb.jpg.|https://www.jaymarchomes.com/images/uploaded/222880304791033_copenhagen-gr.jpg|https://www.jaymarchomes.com/images/uploaded/148152378853410_idea-house-deck.jpg'
'''