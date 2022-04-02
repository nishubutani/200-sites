# -*- coding: utf-8 -*-
import hashlib
import re
import requests
import scrapy
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class CattailConstructionSpider(scrapy.Spider):
    name = 'cattail_construction'
    allowed_domains = ['https://www.cattailconstructioninc.com/']
    start_urls = ['https://www.cattailconstructioninc.com/']

    builderNumber = "52191"


    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #
        image1 = '|'.join(response.xpath('//*[@class="widget-gem-portfolio-item  "]/img/@src').extract())
        image = '|'.join(response.xpath('//div[@id="details"]/div[2]//img/@src').extract())
        images = f"{image1}|{image}"
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = ""
        item['City'] = ""
        item['State'] = ""
        item['ZIP'] = "00000"
        item['AreaCode'] = "402"
        item['Prefix'] = "250"
        item['Suffix'] = "3431"
        item['Extension'] = ""
        item['Email'] = "petersabal1@aol.com"
        item['SubDescription'] = "At Castlebridge Homes, Inc. we strive to make your home building experience a pleasant one. Our goal is to provide you with an affordable quality custom home which will offer you years of enjoyment."
        # item['SubImage'] = images
        item['SubImage'] = 'http://www.cattailconstructioninc.net/uploads/8/3/5/5/83555618/james-river-front-truplace-pix-2020_orig.jpg|http://www.cattailconstructioninc.net/uploads/8/3/5/5/83555618/published/st-martin-main-front-picture.jpg?1606843132|http://www.cattailconstructioninc.net/uploads/8/3/5/5/83555618/exterior-front-elevation-dsc5352_2_orig.jpg|http://www.cattailconstructioninc.net/uploads/8/3/5/5/83555618/brookhill-main-pic_orig.jpg|http://www.cattailconstructioninc.net/uploads/8/3/5/5/83555618/chesapeake-11-main-pic_orig.jpg|http://www.cattailconstructioninc.net/uploads/8/3/5/5/83555618/chesapeake-1-main-picexterior-front-elevation-dsc1332_orig.jpg'
        item['SubWebsite'] = "https://castlebridgehomesomaha.com"
        item['AmenityType'] = ""
        yield item
        try:
            link1 = response.xpath('//a[contains(text(),"Home Designs")]/@href').extract_first()
            res = requests.get(url=link1)
            response1 = HtmlResponse(url=res.url, body=res.content)
            links = response1.xpath('//*[@class="portfolio-icons"]/a[1]/@href').extract()
            plandetains = {}
            for link in links:
                yield scrapy.Request(url=link,callback=self.plans_details,meta={'sbdn':self.builderNumber,'PlanDetails':plandetains},dont_filter=True)
        except Exception as e:
            print(e)

    def plans_details(self,response):
        plandetails = response.meta['PlanDetails']
        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = response.meta['sbdn']
        except Exception as e:
            print(e)

        try:
            PlanName = response.xpath('//*[@class="title-h3"][1]/text()').extract_first(default='').strip()
            if '–' in PlanName:
                PlanName = PlanName.split('–')[0].strip()
        except Exception as e:
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % PlanNumber, "wb")
            f.write(response.body)
            f.close()
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
            BasePrice = '0'
        except Exception as e:
            print(e)

        try:
            Baths = response.xpath('//*[contains(text(),"Main Bath") or contains(text(),"Master Bathroom") or contains(text(),"Powder Bath")]').extract()
            Baths = len(Baths)
            if Baths > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            print(e)

        try:
            Bedrooms = response.xpath('//*[contains(text(),"Front Bedroom") or contains(text(),"Master Bedroom") or contains(text(),"Other Bedrooms") or contains(text(),"Master Bedroom Sitting Room")]').extract()
            Bedrooms = len(Bedrooms)
        except Exception as e:
            print(e)

        try:
            Garage = response.xpath('//*[contains(text(),"Garage")]/../../../..//ul/li[contains(text(),"car garage")]/text()').extract_first(default='0')
            Garage = re.findall(r"(\d+)", Garage)[0]
            BaseSqft = re.findall(r"(\d+)", PlanName)[0]
        except Exception as e:
            print(e)

        try:
            Description = ''.join(response.xpath('//meta[@itemprop="description"]/@content').extract())
            Description = Description.strip()
        except Exception as e:
            print(e)

        try:
            ElevationImage = '|'.join(response.xpath('//*[@class="vc_tta-panels"]/div//img/@src').extract())
            ElevationImage = ElevationImage.strip('|')
        except Exception as e:
            print(e)

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

        SubdivisionNumber = SubdivisionNumber #if subdivision is there
        #SubdivisionNumber = self.builderNumber #if subdivision is not available
        unique = str(PlanNumber)+str(SubdivisionNumber)
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

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl cattail_construction".split())