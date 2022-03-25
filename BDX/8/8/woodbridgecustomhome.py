import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class woodbridgecustomhomeSpider(scrapy.Spider):
    name = 'woodbridgecustomhome'
    allowed_domains = []
    start_urls = ['http://www.woodbridgecustomhomes.com/communities.php']
    builderNumber = 49358

    def parse(self, response):
        links = response.xpath('//div[@class="results_box_content01"]/a/@href').extract()
        print(len(links))
        for link in links:
            url = 'http://www.woodbridgecustomhomes.com/' + str(link)
            # print(url)
            yield scrapy.FormRequest(url=str(url), callback=self.communitydetail, dont_filter=True)

    def communitydetail(self, response):
        subdivisonName = response.xpath('//div[@class="comm_header_right"]/h3/text()').extract_first(default="")
        subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
        f = open("html/%s.html" % subdivisonNumber, "wb")
        f.write(response.body)
        f.close()
        phoneNumber = response.xpath('//div[@class="comm_header_col01"]/h5[4]/text()').extract_first()
        location = ''.join(response.xpath('//div[@class="comm_header_col01"]/h5[1]/text()').extract())
        State = location.split(',')[-1]

        City = location.split(',')[0]
        print(State)
        print(City)
        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionName'] = subdivisonName
        item2['SubdivisionNumber'] = subdivisonNumber
        item2['BuilderNumber'] = self.builderNumber
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        item2['Street1'] = location
        item2['City'] = City
        item2['State'] = State
        item2['ZIP'] = '0000'
        item2['AreaCode'] = ''
        item2['Prefix'] = ''
        item2['Suffix'] = ''
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = response.xpath('//div[@class="right_col"]/p/text()').extract_first(default="")
        item2['SubImage'] = response.xpath('//div[@class="right_col"]/a/img/@src').extract_first(default="")
        item2['SubWebsite'] = response.url
        yield item2

        # urls = re.findall(r'<a href=(.*?)></a>',response.text).getall()
        url = 'http://www.woodbridgecustomhomes.com/plans.php'
        # print(len(links))
        # print(links)
        # for url in links:
        #     url = 'http://www.woodbridgecustomhomes.com/'+str(url)
        #     print(url)
        yield scrapy.FormRequest(url=str(url), callback=self.planlink, meta={'sbdn': self.builderNumber})

    def planlink(self, response):
        links = response.xpath('//*[@class="results_box_btn"]/a/@href').extract()
        for link in links:
            url = 'http://www.woodbridgecustomhomes.com/' + str(link)
            print(url)
            yield scrapy.FormRequest(url=str(url), callback=self.plandetail, meta={'sbdn': self.builderNumber})

    def plandetail(self, response):
        try:
            Type = 'SingleFamily'
        except Exception as e:
            Type = 'SingleFamily'
            print(e)

        try:
            PlanName = response.xpath('//*[@class="left_col"]/h4/text()').extract_first()
            if PlanName == None:
                PlanName = response.xpath('//div[@class="left_col"]/h5[5]/a/text()').extract_first()
            PlanName = re.sub('<[^<]+?>', '', str(PlanName))
            print(PlanName)
        except Exception as e:
            PlanName = ''
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % PlanNumber, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = response.meta['sbdn']
        except Exception as e:
            print(e)

        try:
            PlanNotAvailable = 0
        except Exception as e:
            print(e)

        try:
            BasePrice = 0.00
        except Exception as e:
            print(e)

        try:
            PlanTypeName = 'Single Family'
        except Exception as e:
            print(e)

        try:
            plansquare = response.xpath('//*[@class="left_col"]/h5[5]/text()').get()
            if plansquare == None:
                BaseSqft = 0.00
            BaseSqft = re.sub('<[^<]+?>', '', str(plansquare))
            BaseSqft = BaseSqft.replace(',', '').replace(' ', '')
            print(BaseSqft)
        except Exception as e:
            BaseSqft = 0.00
        try:
            planbeds = response.xpath('//*[@class="left_col"]/h5[3]/text()').extract_first()
            planbeds = re.sub('<[^<]+?>', '', str(planbeds))
            planbeds = planbeds.replace(' ', '')
            # planbeds = planbeds.split('/')[-2]
            # planbeds = planbeds.split(' ')[-2]
            print(planbeds)
            if planbeds == '':
                planbeds = 0
        except Exception as e:
            print("planbeds: ", e)
        try:
            planbath = response.xpath('//*[@class="left_col"]/h5[4]/text()').extract_first()
            if planbath == ' ' or planbath == None or planbath == '':
                planbath = response.xpath('//div[@class="left_col"] /h5[7]/text()').extract_first()
            planbath = re.sub('<[^<]+?>', '', str(planbath))
            # planbath = planbath.split('/')[-1]
            # planbath = planbath.split(' ')[-2]
            tmp = re.findall(r"(\d+)", planbath)
            planbath = tmp[0]
            print(planbath)
            if len(tmp) > 1:
                planHalfBaths = 1
            else:
                planHalfBaths = 0
            # print(planbath)
        except Exception as e:
            print("planbath: ", e)
        try:
            # cargarage = div.xpath('.//*[contains(text(),"Car Garage")]').get()
            # cargarage = re.sub('<[^<]+?>', '', str(cargarage))
            cargarage = 0
        except Exception as e:
            print("cargarage: ", e)
        try:
            PlanImage = '|'.join(response.xpath('//*[@class="right_col"]/a/@href').extract())
            # PlanImage = (for PlanImage in PlanImag: 'http://www.woodbridgecustomhomes.com/' + str(PlanImage))
            # for PlanImage in PlanImage:
            #     PlanImage = 'http://www.woodbridgecustomhomes.com/' + str(PlanImage)
            print(PlanImage)
        except Exception as e:
            print("SpecElevationImage")
        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

        try:
            unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
                    10 ** 30)  # < -------- Changes here
            item = BdxCrawlingItem_Plan()
            item['Type'] = Type
            item['PlanNumber'] = PlanNumber
            item['unique_number'] = unique_number  # < -------- Changes here
            item['SubdivisionNumber'] = SubdivisionNumber
            item['PlanName'] = PlanName
            item['PlanNotAvailable'] = PlanNotAvailable
            item['PlanTypeName'] = PlanTypeName
            item['BasePrice'] = BasePrice
            item['BaseSqft'] = BaseSqft
            item['Baths'] = planbath
            # print(item['Baths'])
            item['HalfBaths'] = planHalfBaths
            # print(item['HalfBaths'])
            item['Bedrooms'] = planbeds
            item['Garage'] = cargarage
            item['Description'] = 'Thank you for choosing Woodbridge Custom Homes! John Geer (former owner of Lambie-Geer Homes) along with his new partner, Jim Stark, have been building beautiful houses in the Kansas City area for over 30 years and strive excellence and exceeding your expectations as our customer. Our main goal at Woodbridge is to provide each valued customer with a quality-built home that truly makes their dream come true. More importantly, we want your relationship with Woodbridge Custom Homes to be a positive and rewarding building experience.Our dedication to excellence is one of our most important core values because we build each home like our own. Last of all, Quality craftsmanship, Functional Creativity and Personal Satisfaction is what you get as you step into a Woodbridge Custom Home. Please look at our available homes or contact us.'
            item['ElevationImage'] = PlanImage
            item['PlanWebsite'] = PlanWebsite
            yield item
        except Exception as e:
            print(e)

        link = 'http://www.woodbridgecustomhomes.com/homes.php'
        yield scrapy.FormRequest(url=str(link), callback=self.homelink, dont_filter=True, meta={'PN':PlanNumber})

    def homelink(self, response):
        links1 = response.xpath('//*[@class="results_box_btn"]/a/@href').extract()
        for link1 in links1:
            link1 = 'http://www.woodbridgecustomhomes.com/' + str(link1)
            print(link1)
            PlanNumber = response.meta['PN']
            yield scrapy.FormRequest(url=str(link1), callback=self.homedetail, dont_filter=True, meta={'PN': PlanNumber})


    def homedetail(self, response):
        try:
            SpecStreet1 = response.xpath('//*[@class="left_col"]/h4/text()').extract_first()
            print(SpecStreet1)
            SpecCity = response.xpath('//*[@class="left_col"]/h4/text()').extract()
            print(SpecCity)
            SpecCit = SpecCity[1]
            SpecCity = SpecCit.split(',')[0]
            SpecStat = SpecCit.split(',')[-1]
            SpecZIP = SpecStat.split(' ')[-1]
            SpecState = 'KS'
            if SpecZIP == '':
                SpecZIP = '0000'
            print(SpecZIP)
            print(SpecCity)
            # SpecZIP = response.xpath('//span[@itemprop="postalCode"]//text()').extract_first()
            unique = str(SpecStreet1) + str(SpecCity) + str(SpecState) + str(SpecZIP)
            SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % SpecNumber, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
            print(e)

        try:
            PlanNumber = response.meta['PN']
            print(PlanNumber)
        except Exception as e:
            print(e)

        try:
            SpecCountry = "USA"
        except Exception as e:
            print(e)

        try:
            # SpecPrice = str(response.xpath('normalize-space(//span[@itemprop="price"]//text())').extract_first(
            #     default='0').strip()).replace(",", "")
            # SpecPrice = re.findall(r"(\d+)", SpecPrice)[0]
            SpecPrice = 0
        except Exception as e:
            print(e)

        try:
            SpecSqft = str(response.xpath('normalize-space(//*[@class="left_col"]/h5[7]/text())').extract_first(default='0').strip()).replace(",", "").replace(" ","")
            SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
        except Exception as e:
            SpecSqft = 0

        try:
            SpecBaths = str(response.xpath(
                'normalize-space(//*[@class="left_col"]/h5[6]/text())').extract_first(
                default='0').strip()).replace(",", "")
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
            SpecBedrooms = str(response.xpath(
                'normalize-space(//*[@class="left_col"]/h5[5]/text())').extract_first(
                default='0').strip()).replace(",", "")
            SpecBedrooms = re.findall(r"(\d+)", SpecBedrooms)[0]
        except Exception as e:
            SpecBedrooms = 0

        try:
            MasterBedLocation = "Down"
        except Exception as e:
            print(e)

        try:
            # SpecGarage = response.xpath(
            #     '//div[@class="load-more-features load-more-trigger"]/div[@class="row"]/div[@class="col-sm-6"]/ul[@class="list-default"]/li[contains(text(),"Number of Garage Spaces:")]').get()
            # SpecGarage = re.findall(r"(\d+)", SpecGarage)[0]
            SpecGarage = 0
        except Exception as e:
            SpecGarage = 0

        try:
            SpecDescription = ''
            SpecDescription = str(''.join(SpecDescription)).strip()
            SpecDescription = SpecDescription.replace("\n", "").replace("  ", "")
            SpecDescription = re.sub('<[^<]+?>', '', str(SpecDescription))
        except Exception as e:
            print(e)

        try:
            ElevationImages = response.xpath('//*[@class="right_col"]/a/@href').extract()
            for ElevationImage in ElevationImages:
                ElevationImage = 'http://www.woodbridgecustomhomes.com/'+str(ElevationImage)+ '|'
                ElevationImage = ElevationImage
            SpecElevationImage = "".join(ElevationImage)
            print(SpecElevationImage)
        except Exception as e:
            print(e)


        try:
            SpecWebsite = response.url
        except Exception as e:
            print(e)

        unique = str(PlanNumber) + str(self.builderNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        # ----------------------- Don't change anything here ---------------- #
        item = BdxCrawlingItem_Spec()
        item['SpecNumber'] = SpecNumber
        item['PlanNumber'] = unique_number
        item['SpecStreet1'] = SpecStreet1
        item['SpecCity'] = SpecCity
        item['SpecState'] = 'KS'
        item['SpecZIP'] = SpecZIP
        item['SpecCountry'] = SpecCountry
        item['SpecPrice'] = SpecPrice
        item['SpecSqft'] = SpecSqft
        item['SpecBaths'] = SpecBaths
        item['SpecHalfBaths'] = SpecHalfBaths
        item['SpecBedrooms'] = SpecBedrooms
        item['MasterBedLocation'] = MasterBedLocation
        item['SpecGarage'] = SpecGarage
        item['SpecDescription'] = SpecDescription
        item['SpecElevationImage'] = SpecElevationImage
        item['SpecWebsite'] = SpecWebsite
        yield item


# execute("scrapy crawl woodbridgecustomhome".split())