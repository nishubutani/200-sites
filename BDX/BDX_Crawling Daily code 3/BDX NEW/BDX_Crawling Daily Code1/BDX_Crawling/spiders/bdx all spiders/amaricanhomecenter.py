import hashlib
import re

import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class ArborBuildersSpider(scrapy.Spider):
    name = 'amaricanhomecenter'
    allowed_domains = []
    builderNumber = '62703'

    start_urls = ['https://www.american-home-centers.com']

    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        links = response.xpath('//*[@id="menu-1-3b20abf"]/li/a/@href').getall()
        for link in links:
            url = link
            yield scrapy.Request(url=url,dont_filter=True,callback=self.comunity_data)

    def comunity_data(self,response):
        adderss = list(set(response.xpath('//*[@class="elementor-text-editor elementor-clearfix"]//strong/following-sibling::text()').getall()))
        street_address = []
        city_state = []
        for i in adderss:
            if 'MT' in i:
                city_state.append(i)
            else:
                street_address.append(i)
        x = response.xpath('//h1/text()').get()

        number = response.xpath('//*[@class="elementor-widget-container"]//*[@class="elementor-button-link elementor-button elementor-size-sm"]//span[@class="elementor-button-icon elementor-align-icon-left"]/following-sibling::span/text()').get()
        SubdivisionNumber = int(hashlib.md5(bytes(x, "utf8")).hexdigest(), 16) % (10 ** 30)

        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = SubdivisionNumber
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = response.xpath('//h1/text()').get()
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        # enter any address you fond on the website.
        item2['Street1'] = street_address[0]
        item2['City'] = city_state[0].split(',')[0]
        item2['State'] = city_state[0].split(',')[-1].split()[0]
        item2['ZIP'] = city_state[0].split(',')[-1].split()[-1]
        item2['AreaCode'] = number.split()[0].lstrip('(').rstrip(')')
        item2['Prefix'] = number.split()[-1].split('-')[0]
        item2['Suffix'] = number.split('-')[-1]
        item2['Extension'] = ""
        item2['Email'] = "sales@american-home-centers.com"
        item2[
            'SubDescription'] = "American Home Centers was founded in Belgrade, MT in 2008 by 20-year industry veteran Ian Taylor, C.E.O. Ten years later, American Home Centers is providing manufactured and modular homes throughout Montana and Wyoming to hundreds of happy homeowners from 3 locations in Belgrade, Billings, and Helena. Each location has several fully furnished homes on display."
        item2['SubImage'] = 'https://d132mt2yijm03y.cloudfront.net/wp-content/uploads/sites/5/2019/02/18213708/cedar-canyon-2077-bathroom-02-768x512.jpg|https://d132mt2yijm03y.cloudfront.net/wp-content/uploads/sites/5/2019/02/18213736/cedar-canyon-2077-interior-05-768x512.jpg|https://d132mt2yijm03y.cloudfront.net/wp-content/uploads/sites/5/2019/02/18213845/cedar-canyon-2077-kitchen-05-768x512.jpg|https://d132mt2yijm03y.cloudfront.net/wp-content/uploads/sites/5/2019/02/18213918/grand_manor_6009_bathroom-01-768x512.jpg|https://d132mt2yijm03y.cloudfront.net/wp-content/uploads/sites/5/2019/02/18213955/grand_manor_6009_bedroom-01-768x512.jpg|https://d132mt2yijm03y.cloudfront.net/wp-content/uploads/sites/5/2019/02/18214114/grand_manor_6009_interior-01-768x512.jpg|https://d132mt2yijm03y.cloudfront.net/wp-content/uploads/sites/5/2019/02/18214139/grand_manor_6009_kitchen-02-768x512.jpg|https://d132mt2yijm03y.cloudfront.net/wp-content/uploads/sites/5/2019/02/18214201/westwind-homes-cedar-canyon-2020-bedroom-1-768x512.jpg|https://d132mt2yijm03y.cloudfront.net/wp-content/uploads/sites/5/2019/02/18214339/westwind-homes-pinehurst-2506-interior-6-768x512.jpg'
        item2['SubWebsite'] =response.url
        item2['AmenityType'] = ''
        yield item2
        links = response.xpath('//*[@class="fp-card-details"]//a/@href').getall()
        for link in links:
            url = 'https://www.american-home-centers.com' + link
            yield scrapy.Request(url=url, dont_filter=True, callback=self.plan_data,meta={'SubdivisionNumber':SubdivisionNumber})

    def plan_data(self,response):
        plan_name = response.xpath('//h1/text()').get()
        plan_number = int(hashlib.md5(bytes(plan_name, "utf8")).hexdigest(), 16) % (10 ** 30)
        data = ''.join(response.xpath('//*[@class="elementor-text-editor elementor-clearfix"]/text()').getall())
        try:
            SpecSqft = re.findall('(\d+) sqft', data)
            SpecSqft = SpecSqft[0].strip()
        except Exception as e:
            SpecSqft = 0

        try:
            # SpecBaths = data.split('Bath')[0].split('/')[-1].strip()
            # SpecBaths = re.findall(r'BATHS:<.*?>(\d)',str(response.text))
            SpecBaths = str(response.text).split('BATHS:</strong>')[-1].split('<strong>')[0].strip()
            SpecBaths = SpecBaths[0].strip()
            if '.5' in SpecBaths:
                SpecHalfBaths = 1
                SpecBaths.replace('.5','')
            else:
                SpecHalfBaths = 0
        except Exception as e:
            SpecBaths = 0
            SpecHalfBaths = 0

        # try:
        #     SpecBedrooms = re.findall('(\d+) Bdr', data)
        #     SpecBedrooms = SpecBedrooms[0].strip()
        # except Exception as e:
        #     SpecBedrooms = 0
        try:
            # SpecBedrooms = re.findall('BEDS: (\d)', response.text) #BEDS: (\d)
            SpecBedrooms = str(response.text).split('BEDS:</strong>')[-1].split('<strong>')[0].strip() #BEDS: (\d)
            SpecBedrooms = SpecBedrooms[0].strip()
        except Exception as e:
            SpecBedrooms = 0


        unique = str(plan_name) + str(response.meta['SubdivisionNumber'])
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['unique_number'] = unique_number
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = plan_number
        item['SubdivisionNumber'] = response.meta['SubdivisionNumber']
        item['PlanName'] = plan_name
        item['PlanNotAvailable'] = 1
        item['PlanTypeName'] = "Single Family"
        item['BasePrice'] = 0
        item['BaseSqft'] = SpecSqft
        item['Baths'] = SpecBaths
        item['HalfBaths'] = SpecHalfBaths
        item['Bedrooms'] = SpecBedrooms
        item['Garage'] = 0
        item['Description'] = data
        item['ElevationImage'] = "|".join(response.xpath("//*[@class='gallery-icon ']/a/@href").getall())
        item['PlanWebsite'] = response.url
        yield item


    # def homedata(self,response):
    #     address = response.xpath('//iframe/@src').get().split('q=')[-1].split()[0].split('%2C')
    #     try:
    #         SpecStreet1 = address[0].replace("+",' ')
    #         SpecCity =address[1].replace("+",'')
    #         SpecState = address[-1].strip('+').split('+')[0]
    #         SpecZIP =address[-1].strip('+').split('+')[-1]
    #         unique = str(SpecStreet1) + str(SpecCity) + str(SpecState) + str(SpecZIP)
    #         SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
    #         f = open("html/%s.html" % SpecNumber, "wb")
    #         f.write(response.body)
    #         f.close()
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         PlanNumber = response.meta['plan_number']
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         SpecCountry = "USA"
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         SpecPrice = 0.0
    #     except Exception as e:
    #         print(e)
    #     data = ''.join(response.xpath('//*[@class="elementor-text-editor elementor-clearfix"]/text()').getall())
    #
    #     try:
    #         SpecSqft = re.findall('(\d+) sqft', data)
    #         SpecSqft = SpecSqft[0].strip()
    #     except Exception as e:
    #         SpecSqft = 0
    #
    #     try:
    #         SpecBaths = data.split('Bath')[0].split('/')[-1].strip()
    #
    #         if '.5' in SpecBaths:
    #             SpecHalfBaths = 1
    #             SpecBaths.replace('.5','')
    #         else:
    #             SpecHalfBaths = 0
    #     except Exception as e:
    #         SpecBaths = 0
    #         SpecHalfBaths = 0
    #
    #     try:
    #         SpecBedrooms = re.findall('(\d+) Bdr', data)
    #         SpecBedrooms = SpecBedrooms[0].strip()
    #     except Exception as e:
    #         SpecBedrooms = 0
    #
    #     try:
    #         MasterBedLocation = "Down"
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         SpecGarage = 0
    #     except Exception as e:
    #         SpecGarage = 0
    #
    #     try:
    #         SpecDescription = data.replace('\\r','')
    #         SpecDescription = str(''.join(SpecDescription)).strip()
    #         SpecDescription = SpecDescription.replace("\n", "").replace("  ", "")
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         ElevationImage = response.xpath('//*[@class="elementor-image-gallery"]//img/@src').extract()
    #         ElevationImage = "|".join(ElevationImage)
    #         SpecElevationImage = ElevationImage
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         SpecWebsite = response.url
    #     except Exception as e:
    #         print(e)
    #
    #     # ----------------------- Don't change anything here ---------------- #
    #     item = BdxCrawlingItem_Spec()
    #     item['SpecNumber'] = SpecNumber
    #     item['PlanNumber'] = PlanNumber
    #     item['SpecStreet1'] = SpecStreet1
    #     item['SpecCity'] = SpecCity
    #     item['SpecState'] = SpecState
    #     item['SpecZIP'] = SpecZIP
    #     item['SpecCountry'] = SpecCountry
    #     item['SpecPrice'] = SpecPrice
    #     item['SpecSqft'] = SpecSqft
    #     item['SpecBaths'] = SpecBaths
    #     item['SpecHalfBaths'] = SpecHalfBaths
    #     item['SpecBedrooms'] = SpecBedrooms
    #     item['MasterBedLocation'] = MasterBedLocation
    #     item['SpecGarage'] = SpecGarage
    #     item['SpecDescription'] = SpecDescription
    #     item['SpecElevationImage'] = SpecElevationImage
    #     item['SpecWebsite'] = SpecWebsite
    #     yield item





if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl amaricanhomecenter".split())