# -*- coding: utf-8 -*-
import os
import hashlib
import re

import requests
import scrapy
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser

from BDX_Crawling.items import BdxCrawlingItem_subdivision,BdxCrawlingItem_Plan
from scraper_api import ScraperAPIClient
# client = ScraperAPIClient('f846a41474d44096b8f9df3b08055d86')
client = ScraperAPIClient('df1a32d04b794153ad1c51a152bf520f')
from w3lib.http import basic_auth_header
class DonGardnerSpider(scrapy.Spider):
    name = 'don_gardner'
    allowed_domains = []
    start_urls = ['https://quotes.toscrape.com/']
    builderNumber = 698901737911430202742918739420



    def parse(self,response):
        open_in_browser(response)


        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = "86 Villa Road"
        item['City'] = "Greenville"
        item['State'] = "SC"
        item['ZIP'] = "29615"
        item['AreaCode'] = "864"
        item['Prefix'] = "288"
        item['Suffix'] = "7580"
        item['Extension'] = ""
        item['Email'] = "info@dongardner.com"
        item['SubDescription'] = "We've been designing dream homes for nearly four decades and a lot has changed in that time: Styles, preferences, options, not to mention personal tastes. One thing that hasn't changed is the fact that every home is unique - the perfect home depends on the family or individual. Since 1978, Donald A. Gardner Architects, Inc. has been redefining the residential, pre-design house industry. And there's a reason why thousands of satisfied homeowners and builders choose our plans above any others in the industry every year: trust."
        item['SubImage'] = '|'.join(response.xpath('//picture//img/@src').extract())
        if not item['SubImage']:
            item['SubImage'] = 'https://12b85ee3ac237063a29d-5a53cc07453e990f4c947526023745a3.ssl.cf5.rackcdn.com/cms-uploads/2b51bb5e8cbd9459c101e8e47bdedbcb.jpg|https://12b85ee3ac237063a29d-5a53cc07453e990f4c947526023745a3.ssl.cf5.rackcdn.com/cms-uploads/e152e7510f75327417804d0b8afb719b.jpg|https://12b85ee3ac237063a29d-5a53cc07453e990f4c947526023745a3.ssl.cf5.rackcdn.com/cms-uploads/adbc73258fa2231bca0ee54dad77003a.jpg'
        item['SubWebsite'] = ""
        item['AmenityType'] = ""
        yield item

        plan_url = 'https://www.dongardner.com/search?plan_name=&living_low=&living_high=&bedroom_low=0.00&bedroom_high=6.00&bathroom_low=0.00&bathroom_high=6.00&half_bathroom_low=0.00&half_bathroom_high=4.00&stories_low=0.00&stories_high=4.00&garage_locations=&foundations=&features=&styles=&house_width_min=&house_width_max=&house_depth_min=&house_depth_max=&master_width_min=&master_width_max=&master_depth_min=&master_depth_max=&page=1&per_page=12&order_by=WebUpLoad%2520desc'
        self.header = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
                       # "Proxy-Authorization": basic_auth_header('lum-customer-c_11e7173f-zone-zone_us-ip-181.215.81.140', 'mqy4l03550gl')
                       }
        # yield scrapy.Request(url=plan_url, callback=self.ParsePlans, dont_filter=True, headers=self.header, meta={'sbdn':item['BuilderNumber'],"proxy": "https://zproxy.lum-superproxy.io:22225"})
        yield scrapy.Request(client.scrapyGet(url=plan_url), callback=self.ParsePlans, dont_filter=True, headers=self.header, meta={'sbdn':item['BuilderNumber']})

    def ParsePlans(self, response):
        planurls = response.xpath('//*[contains(text(),"view plan")]/@href').extract()
        for url in planurls:
            url = 'https://www.dongardner.com' + url
            yield scrapy.Request(client.scrapyGet(url=url), callback=self.PlanDetails, headers=self.header, dont_filter=True, meta=response.meta)
        nextpage = response.xpath('//*[contains(text(),"Next")]/@href').extract_first()
        if nextpage:
            yield scrapy.Request(url='https://www.dongardner.com' + nextpage, callback=self.ParsePlans, headers=self.header, dont_filter=True, meta=response.meta)

    def PlanDetails(self, response):
        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = response.meta['sbdn']
        except Exception as e:
            print(e)

        try:
            # PlanName = response.url.split('/')[-1].strip().replace('-',' ').title()
            PlanName = response.xpath("//h2/text()").extract_first('')

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
            BasePrice = 0.00
        except Exception as e:
            print(e)

        try:
            Baths = str(response.xpath('//*[contains(text(),"Bathrooms")]/../text()').extract_first())
            tmp = re.findall(r"(\d+)", Baths)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
        except Exception as e:
            print(e)

        try:
            Bedrooms = response.xpath('//*[contains(text(),"Bedrooms")]/../text()').extract_first(default=0)
            Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
        except Exception as e:
            print(e)

        try:
            Garage = 0
        except Exception as e:
            print(e)
        try:
            BaseSqft = str(response.xpath('//*[contains(text(),"Total Sq. Ft")]/../text()').extract_first(default=0.00)).replace(",", "")
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
        except Exception as e:
            print(e)

        try:
            Description = ''.join(response.xpath('//*[@class="medium-7 columns plan-web-description"]/article//text()').extract()).split('Floor Plans\n')[0].strip()
        except Exception as e:
            print(e)

        try:
            ElevationImage = '|'.join(re.findall(r'"large":"(.*?)",',response.text)).replace('\\','')
            ElevationImage = ElevationImage + '|' + '|'.join(response.xpath('//*[@class="floor-img-wrap"]/img/@src').extract())
            ElevationImage = ElevationImage.strip('|')
        except Exception as e:
            print(e)

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = SubdivisionNumber  # if subdivision is there
            # SubdivisionNumber = self.builderNumber #if subdivision is not available
            unique = str(PlanNumber) + str(SubdivisionNumber)
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
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
            item['Description'] = Description.strip()
            item['ElevationImage'] = ElevationImage
            item['PlanWebsite'] = PlanWebsite
            yield item
        except Exception as e:
            print(e)

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl don_gardner".split())