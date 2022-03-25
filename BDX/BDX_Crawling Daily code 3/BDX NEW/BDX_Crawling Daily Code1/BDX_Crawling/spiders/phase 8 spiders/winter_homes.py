# -*- coding: utf-8 -*-
import scrapy
import hashlib
import re
import scrapy
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec



class WinterHomesSpider(scrapy.Spider):
    name = 'winter_homes'
    allowed_domains = ['builtbywinterhomes.com']
    start_urls = ['https://www.builtbywinterhomes.com/new-home/communities']
    builderNumber = "51078"


    def parse(self,response):
        cummunity_details = {}
        community_links = response.xpath('//a[@class="stroke-button"]/@href').extract()
        print(community_links)

        subdivisionname = response.xpath('//h3[1]/text()').extract()
        print(subdivisionname)
        address = response.xpath('//h3[2]/text()').extract()
        for community_link,subdivisionname,address in zip(community_links,subdivisionname,address):
            if "https://www.builtbywinterhomes.com" not in community_link:
                community_link = "https://www.builtbywinterhomes.com" + str(community_link)
            yield scrapy.FormRequest(url=community_link,
                                     callback=self.community_details,meta={"subdivisionname":subdivisionname,"address":address,'cummunity_details':cummunity_details})

    def community_details(self, response):


        SubdivisionName = response.meta['subdivisionname']
        address = response.meta['address']
        cummunity_details = response.meta['cummunity_details']

        item = BdxCrawlingItem_subdivision()



        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()

        item['sub_Status'] = "Active"
        SubdivisionNumber = int(
            hashlib.md5(bytes(str(SubdivisionName) + str(self.builderNumber), "utf8")).hexdigest(), 16) % (10 ** 30)
        print(SubdivisionNumber)
        cummunity_details['subdivisionname'] = SubdivisionNumber
        item['SubdivisionNumber'] = SubdivisionNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = SubdivisionName
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = " "
        item['City'] = address.split(',')[0].strip()
        item['State'] ="AL"
        # item['State'] = address.split(',')[1].split()[0].strip()
        item['ZIP'] = address.split(',')[1].split()[1].strip()
        item['AreaCode'] = "256"
        item['Prefix'] = "278"
        item['Suffix'] = "1551"
        item['Extension'] = ""
        item['Email'] = "info@builtbywinterhomes.com"

        item[
            'SubDescription'] = response.xpath(
            '//div[@class="communityintro"]/text()[1]').extract_first(
            default="")

        SubImage = response.xpath('//div[@class="jai-map-container hover-popup"]//img/@src').extract_first()
        SubImage = 'https://www.builtbywinterhomes.com' + str(SubImage)
        if not SubImage:
            SubImage = "https://www.builtbywinterhomes.com/images/site/banner-communities-subdivisions.jpg"
        item['SubImage'] = SubImage
        item['SubWebsite'] = response.url
        yield item


        yield scrapy.Request(url=response.url, callback=self.parse_planlink, dont_filter=True,meta={'SubdivisionNumber':SubdivisionNumber,"cummunity_details":cummunity_details})




    def parse_planlink(self,response):

        try:
            cummunity_details = response.meta['cummunity_details']
            plandetails = {}
            plans = response.xpath('//table[@class="floorplans"]//td')
            for plan in plans:
                planname = plan.xpath('.//div[@class="middle"]/div/h2/text()').get()
                des = plan.xpath('.//div[@class="middle"]/div/h2/following-sibling::text()').get()


                if 'Garage' not in des:

                    des = des.replace(',','',1)
                    # feet = des.rsplit(',',2)[0].replace(',','')
                    feet = re.findall(r'(\d+)',des)[0]
                    # bedroom = des.rsplit(',',2)[1]
                    bedroom = re.findall(r'(\d+)',des)[1]
                    # bathroom = des.rsplit(',',2)[2]
                    bathroom = re.findall(r"(\d+)", des)[2]
                    tmp = bathroom[0]

                    try:
                        HalfBaths = re.findall(r"(\d+)", des)[3]

                        if HalfBaths:
                            HalfBaths = 1
                        else:
                            HalfBaths = 0
                    except Exception as e :
                        HalfBaths = 0




                    SubdivisionNumber = response.meta['SubdivisionNumber']
                    u_number = str(planname) + str(feet) + str(bathroom) + str(bedroom)
                    PlanNumber = int(hashlib.md5(bytes(u_number, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % PlanNumber, "wb")
                    f.write(response.body)
                    f.close()
                    unique = str(PlanNumber) + str(SubdivisionNumber)
                    unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    plandetails[planname] = unique_number



                    item = BdxCrawlingItem_Plan()
                    item['Type'] = 'SingleFamily'
                    item['PlanNumber'] = PlanNumber
                    item['unique_number'] = unique_number
                    item['SubdivisionNumber'] = SubdivisionNumber
                    item['PlanName'] = planname
                    item['PlanNotAvailable'] = 0
                    item['PlanTypeName'] = 'Single Family'
                    item['BasePrice'] = 0
                    item['BaseSqft'] = feet
                    item['Baths'] = tmp
                    item['HalfBaths'] = HalfBaths
                    item['Bedrooms'] = bedroom
                    item['Garage'] = 0
                    item['Description'] = 'We are a custom home building company that has been building homes and developing communities in the Athens-Limestone area since 2002.'
                    image1 = plan.xpath('.//img[@class="image"]/@src').get()

                    image2 = plan.xpath('.//img[@alt="icon elevation"]/@src').get()


                    if image1:
                        if 'https://www.builtbywinterhomes.com' not in image1:
                            image1 = "https://www.builtbywinterhomes.com" + str(image1)

                        if 'https://www.builtbywinterhomes.com' not in image2:
                            image2 = "https://www.builtbywinterhomes.com" + str(image2)
                        Image = image1+'|'+image2
                    else :
                        if 'https://www.builtbywinterhomes.com' not in image2:
                            image2 = "https://www.builtbywinterhomes.com" + str(image2)
                        Image=image2
                    item['ElevationImage'] = Image
                    item['PlanWebsite'] = response.url

                    yield item
                    yield scrapy.Request(url=response.url, callback=self.home_list, dont_filter=True,
                                         meta={'PN': plandetails,"cummunity_details":cummunity_details,'SubdivisionNumber':SubdivisionNumber})



        except Exception as e:
            print(e)

    def home_list(self,response):
        SubdivisionNumber = response.meta['SubdivisionNumber']
        unique = str("Plan Unknown") + str(SubdivisionNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['unique_number'] = unique_number
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = "Plan Unknown"
        item['SubdivisionNumber'] = SubdivisionNumber
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

        try:
            # cummunity_details = response.meta['cummunity_details']
            PN = response.meta['PN']
            PlanNumber = unique_number

            home_div = response.xpath('//div[@class = "homescontainer"]')
            for div in home_div:
                link = div.xpath('.//h4/a/@href').extract_first()
                if 'https://www.builtbywinterhomes.com' not in link:
                    link = 'https://www.builtbywinterhomes.com' + str(link)
                yield scrapy.Request(url=link, callback=self.HomesDetails,
                                         meta={'PlanNumber': PlanNumber,'PN':PN},
                                         dont_filter=True)
        except Exception as e:
            print(e)

    def HomesDetails(self, response):
        PN = response.meta['PN']
        # cummunity_details = response.meta['cummunity_details']
        # subdivisionname = response.xpath('normalize-space(//th[contains(text(),"Neighborhood")]/following-sibling::td/text()').extract_first(default='').strip()

        PlanNumber = response.meta['PlanNumber']





        address = response.xpath('//h1[@itemprop="headline"]/text()').get()
        SpecStreet1 = address.split(',')[0].replace('\n','').replace('\t','')
        SpecCity = address.split(',')[1].strip()
        # SpecState = address.split(',')[2].strip().split(' ')[0]
        SpecState = "AL"
        SpecZIP = address.split(',')[2].strip().split(' ')[1]

        try:
            unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
            SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % SpecNumber, "wb")
            f.write(response.body)
            f.close()

            SpecCountry = "USA"



            SpecPrice = response.xpath('//strong[contains(text(),"Asking Price")]/following-sibling::text()').get()
            SpecPrice = re.findall(r"(\d+)", SpecPrice.replace(',',''))[0]



            SpecSqft = str(response.xpath(
                'normalize-space(//strong[contains(text(),"Square Feet")]/following-sibling::text())').extract_first(
                default='0').strip()).replace(",", "")
            SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]



            SpecBaths = str(response.xpath(
                'normalize-space(//strong[contains(text(),"Bathrooms")]/following-sibling::text())').extract_first(
                default='0').strip()).replace(",", "")
            tmp = re.findall(r"(\d+)", SpecBaths)
            SpecBaths = tmp[0]
            if len(tmp) > 1:
                SpecHalfBaths = 1
            else:
                SpecHalfBaths = 0



            SpecBedrooms = str(
                response.xpath('//strong[contains(text(),"Bedrooms")]/following-sibling::text()').extract_first(
                    default='0').strip()).replace(",", "")
            SpecBedrooms = re.findall(r'(\d+)', SpecBedrooms)[0]



            MasterBedLocation = "Down"



            SpecGarage = response.xpath(
                'normalize-space(//th[contains(text(),"Garage")]/following-sibling::td/text())').extract_first(default='0')
            SpecGarage = SpecGarage.replace("Two","'2'").replace('Three','"3"').replace('one','"1"')

            SpecGarage = re.findall(r"(\d+)", SpecGarage)[0]



            SpecDescription = response.xpath('//div[@itemprop="articleBody"]/div[@class="ba-gallery "]/following-sibling::text()[1]').extract_first(
                default='').strip()


            image = []
            SpecElevationImage = response.xpath('//div[@class="ba-image"]/img/@src').get()

            for i in range(1,6):
                if '/01' in SpecElevationImage:
                    a = '/0'+ str(i)
                    a = SpecElevationImage.replace('/01',a)
                    image.append(a)

                else:
                    a = str(i)
                    a = SpecElevationImage.replace('/1','/'+ a)
                    image.append(a)

            images = '|'.join(image)



            # ElevationImage = '|'.join(
            #     response.urljoin(self.start_urls[0] + i) for i in response.xpath('//*[@class="sn-144"]/img/@src').extract())
            # ElevationImage = ElevationImage + '|' + '|'.join(
            #     response.urljoin(self.start_urls[0] + i) for i in response.xpath('//*[@class="sn-156"]//a/@href').extract())
            # SpecElevationImage = ElevationImage + '|' + '|'.join(
            #     response.urljoin(self.start_urls[0] + i) for i in response.xpath('//*[@class="zoomImg"]/@src').extract())
            # SpecElevationImage = SpecElevationImage.strip('|')



            SpecWebsite = response.url


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
            item['SpecDescription'] = SpecDescription
            item['SpecElevationImage'] = images
            item['SpecWebsite'] = SpecWebsite
            yield item

        except Exception as e:
            print(e)


from scrapy.cmdline import execute
# execute("scrapy crawl winter_homes".split())





