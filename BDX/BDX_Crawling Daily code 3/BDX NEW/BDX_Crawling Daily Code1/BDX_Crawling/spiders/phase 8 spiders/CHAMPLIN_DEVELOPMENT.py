# -*- coding: utf-8 -*-
import hashlib
import json
import re
import requests
import scrapy
from decimal import Decimal
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class ChamplinDevelopmentSpider(scrapy.Spider):
    name = 'Champlin_Development'
    allowed_domains = ['http://www.champlindevelopment.com/']
    start_urls = ['http://www.champlindevelopment.com/']

    builderNumber = "52164"


    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #
        # image2_list = []
        # image1 = '|'.join(response.urljoin("https://img1.wsimg.com" + re.findall(r'//img1.wsimg.com(.*?).jpg',i)[0] + ".jpg") for i in
        #                   response.xpath('//*[@data-ux="Background"]/script/text()').extract())
        # res_i = requests.get(url="https://img1.wsimg.com/blobby/go/1d8ea83e-5850-4978-a2e4-8087500ed566/gpub/c013d06d650ecc50/script.js")
        # response_i = HtmlResponse(url=res_i.url, body=res_i.content)
        # img_links = re.findall(r'{"lightboxUrl":"(.*?).jpg',response_i.text)
        # for img in img_links:
        #     img = re.sub(r'\\u002F','/',img)
        #     image2_list.append(f"https:{img}.jpg")
        # images = f"{image1}|{'|'.join(image2_list)}"
        # item = BdxCrawlingItem_subdivision()
        # item['sub_Status'] = "Active"
        # item['SubdivisionNumber'] = ''
        # item['BuilderNumber'] = self.builderNumber
        # item['SubdivisionName'] = "No Sub Division"
        # item['BuildOnYourLot'] = 0
        # item['OutOfCommunity'] = 0
        # item['Street1'] = ""
        # item['City'] = "Checotah"
        # item['State'] = "OK"
        # item['ZIP'] = "74426"
        # item['AreaCode'] = "918"
        # item['Prefix'] = "473"
        # item['Suffix'] = "7020"
        # item['Extension'] = ""
        # item['Email'] = "e.davis@cedarloghomesofokla.com"
        # item['SubDescription'] = response.xpath('//h4/../div//span/text()').extract_first().strip()
        # item['SubImage'] = images
        # item['SubWebsite'] = response.url
        # yield item

        # IF you have Communities
        comm_selectors = response.xpath('//*[contains(text(),"Current Communities")]/../../following-sibling::div[1]//h3')
        for comm_selector in comm_selectors:
            comm_link = "http://www.champlindevelopment.com" + comm_selector.xpath('./a/@href').extract_first()
            city_state = comm_selector.xpath('./../p/text()').extract_first()
            yield scrapy.Request(url=comm_link, callback=self.process_communities, dont_filter=True,meta={'city_state':city_state})


    def process_communities(self,response):
        try:
            address = response.xpath('//p/text()').extract_first()
            images = response.xpath('//img/@data-image').extract_first()
            SubdivisionName = response.xpath('//h1/text()').extract_first().strip()
            SubdivisionNumber = int(hashlib.md5(bytes(SubdivisionName + str(self.builderNumber), "utf8")).hexdigest(),16) % (10 ** 30)
            if response.xpath('//h1/../ul/li/p/text()'):
                SubDescription = ''.join(response.xpath('//h1/../ul/li/p/text()').extract()).strip()
            elif response.xpath('//h1/../p[2]/text()'):
                SubDescription = ''.join(response.xpath('//h1/../p[2]/text()').extract()).strip()
            else:
                SubDescription = "Our goal at Champlin Development and in the communities we build, is to help you find a home that fits your needs, your budget and your timeframe. We listen to your needs and desires for the type of home you are looking for and make suggestions based on what you want. We have several floor plans to view, and over 30 years of building homes in Cache Valley. The best part? You won’t find another builder as focused on craftsmanship for our active adult buyers as we are. We'd love to hear your story and see if we have the right home for you."
            item = BdxCrawlingItem_subdivision()
            item['sub_Status'] = "Active"
            item['SubdivisionNumber'] = SubdivisionNumber
            item['BuilderNumber'] = self.builderNumber
            item['SubdivisionName'] = SubdivisionName
            item['BuildOnYourLot'] = 0
            item['OutOfCommunity'] = 1
            item['Street1'] = address.replace(response.meta['city_state'],'').strip()
            item['City'] = response.meta['city_state'].split(',')[0].strip()
            item['State'] = response.meta['city_state'].split(',')[1].strip()
            item['ZIP'] = response.xpath('//*[@class="site-address"]/text()').extract_first().split(',')[-2].strip()
            phone = ' '.join(response.xpath('//strong//text()').extract())
            if phone == '':
                phone1 = '435-224-0881'
            else:
                phone1 = phone.split(' ')[-1]
            item['AreaCode'] = phone1.split('-')[0].strip()
            item['Prefix'] = phone1.split('-')[1].strip()
            item['Suffix'] = phone1.split('-')[2].strip()
            item['Extension'] = ""
            item['Email'] = 'hello@champlindevelopment.com'
            item['SubDescription'] = SubDescription
            item['SubImage'] = images
            item['SubWebsite'] = response.url
            yield item
        except Exception as e:
            print(e)

        if response.xpath('//h3[contains(text(),"Available Plans")]'):
            PlanDetails = {}
            yield scrapy.Request(url=response.url, callback=self.plans_details, dont_filter=True, meta={'sbdn':self.builderNumber, 'PlanDetails':PlanDetails, "SubdivisionNumber":SubdivisionNumber})

    def plans_details(self, response):
        selectors = response.xpath('//p/../h3')
        for selector in selectors:
            plandetails = response.meta['PlanDetails']

            try:
                Type = 'SingleFamily'
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
                PlanWebsite = response.url
            except Exception as e:
                print(e)

            try:
                Description = response.xpath('//h1/../p[2]/text()').extract_first()
                Description = Description.strip()
            except Exception as e:
                print(e)

            try:
                PlanName = selector.xpath('./text()').extract_first(default='').strip()
                if '–' in PlanName:
                    PlanName = PlanName.split('–')[0].strip()
            except Exception as e:
                print(e)

            try:
                PlanNumber = int(hashlib.md5(bytes(response.url+PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % PlanNumber, "wb")
                f.write(response.body)
                f.close()
            except Exception as e:
                print(e)

            try:
                BasePrice = '0'
            except Exception as e:
                print(e)

            try:
                Baths = selector.xpath('./../p/text()').extract_first().split('|')[1].strip()
                tmp = re.findall(r"(\d+)", Baths)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                print(e)

            try:
                Bedrooms = selector.xpath('./../p/text()').extract_first().split('|')[0].strip()
                Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
            except Exception as e:
                print(e)

            try:
                Garage = '0'
                BaseSqft = selector.xpath('./../p/text()').extract_first().split('|')[2].strip()
                BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
            except Exception as e:
                print(e)

            try:
                ElevationImage = selector.xpath('./../../..//img/@data-src').extract_first().strip()
            except Exception as e:
                print(e)

            SubdivisionNumber = response.meta['SubdivisionNumber']  # if subdivision is there
            # SubdivisionNumber = self.builderNumber #if subdivision is not available
            unique = str(PlanNumber) + str(SubdivisionNumber)
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            plandetails[PlanName] = unique_number
            item = BdxCrawlingItem_Plan()
            item['Type'] = Type
            item['PlanNumber'] = PlanNumber
            item['unique_number'] = unique_number
            item['SubdivisionNumber'] = SubdivisionNumber
            item['PlanName'] = PlanName
            item['PlanNotAvailable'] = PlanNotAvailable
            item['PlanTypeName'] = PlanTypeName
            item['BasePrice'] = BasePrice
            item['BaseSqft'] = BaseSqft
            item['Baths'] = Baths
            item['HalfBaths'] = HalfBaths
            item['Bedrooms'] = Bedrooms
            item['Garage'] = Garage
            item['Description'] = Description
            item['ElevationImage'] = ElevationImage
            item['PlanWebsite'] = PlanWebsite
            yield item


from scrapy.cmdline import execute
# execute("scrapy crawl Champlin_Development".split())