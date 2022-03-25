import hashlib
import re
import random
import scrapy
from w3lib.http import basic_auth_header

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan

#Luminati
# proxy_host = "zproxy.lum-superproxy.io"
# proxy_port = "22225"
# proxy_auth = "lum-customer-xbyte-zone-zone_us-country-us:0gi0pioy3oey"
# proxies = {"https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
#            "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}
USER_AGENT = 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Safari/537.36'

class ProminenceSpider(scrapy.Spider):
    name = 'prominence'

    builderNumber = "628267518643932891528995798397"

    def start_requests(self):
        url="http://www.prominencehomes.com"
        header = {
                  "Upgrade-Insecure-Requests": "1",
                  "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
                  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
                  # "Proxy-Authorization": basic_auth_header('lum-customer-xbyte-zone-zone_us-country-us', '0gi0pioy3oey')
                  }
        yield scrapy.Request(url=url, callback=self.parse, headers=header)


    def parse(self, response):
        try:
            f = open("html/%s.html" % self.builderNumber, "wb")
            f.write(response.body)
            f.close()
            description = ''.join(response.xpath('//font[@face="tahoma, Arial, Helvetica"]/font/text()').extract())
            descriptions = re.sub('\s+', ' ', re.sub('\r|\n|\t', ' ', description))
            item = BdxCrawlingItem_subdivision()
            item['sub_Status'] = "Active"
            item['SubdivisionNumber'] = ''
            item['BuilderNumber'] = self.builderNumber
            item['SubdivisionName'] = "No Sub Division"
            item['BuildOnYourLot'] = 0
            item['OutOfCommunity'] = 0
            item['Street1'] = "4332 Tallmadge Rd"
            item['City'] = "Rootstown"
            item['State'] = "OH"
            item['ZIP'] = "44272"
            item['AreaCode'] = "330"
            item['Prefix'] = "325"
            item['Suffix'] = "8020 "
            item['Extension'] = ""
            item['Email'] = "webmaster@prominencehomes.com"
            item['SubDescription'] = descriptions
            item['SubImage'] = '|'.join(response.urljoin('http://www.prominencehomes.com/' + i) for i in response.xpath('//font[@face="tahoma, Arial, Helvetica"]/img/@src').extract())
            item['SubWebsite'] = response.url
            yield item
        except Exception as e:
            print(e)

        try:
            link = 'http://www.prominencehomes.com/products.htm'
            header = {"Upgrade-Insecure-Requests":"1",
                    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
                    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"}

            yield scrapy.FormRequest(url=link, callback=self.plans, headers=header)
        except Exception as e:
            print(e)


    def plans(self, response):
        links = response.xpath('//p[@align="right"]/a/@href').extract()
        del links[0]
        del links[-1]
        for link in links:
            yield scrapy.Request(url='http://www.prominencehomes.com/' + link, callback=self.plan_page)


    def plan_page(self, response):
        if response != 'New Stonecreek':
            SubdivisionNumber = self.builderNumber

            try:PlanName = response.xpath('//title//text()').extract_first(default='').strip()
            except Exception as e:print(e)

            page_text = response.text

            try:PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
            except Exception as e:print(e)

            try:
                BaseSqft = response.xpath('//*[contains(text(),"Square Feet")]/text()').extract_first()
                BaseSqft = re.findall(r'(\d+) Square Feet', BaseSqft)[0]
            except:
                BaseSqft = 0

            try:
                Baths = response.xpath('//*[contains(text(),"Baths")]/text()').extract_first()
                tmp = re.findall(r"(\d+)", Baths)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except:
                Baths = 0
                HalfBaths = 0

            try:
                Bedrooms = response.xpath('//*[contains(text(),"Bedroom")]/text()').extract_first()
                Bedrooms = re.findall(r'(\d+) Bed', Bedrooms)[0]
            except:
                Bedrooms = 0

            try:Description = '|'.join(response.xpath('//td[@valign="baseline"]/following-sibling::td//text()').extract())
            except Exception as e:print(str(e))

            try:
                ElevationImage = []
                image = response.xpath('//font[@face="tahoma, Arial, Helvetica"]/img/@src').extract()
                for img in image:
                    image = 'http://www.prominencehomes.com/' + img
                    ElevationImage.append(image)
            except Exception as e:
                print(e)

            unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
            item = BdxCrawlingItem_Plan()
            item['Type'] = 'SingleFamily'
            item['PlanNumber'] = PlanNumber
            item['unique_number'] = unique_number  # < -------- Changes here
            item['SubdivisionNumber'] = self.builderNumber
            item['PlanName'] = PlanName
            item['PlanNotAvailable'] = 0
            item['PlanTypeName'] = 'Single Family'
            item['BasePrice'] = 0.00
            item['BaseSqft'] = BaseSqft
            item['Baths'] = Baths
            item['HalfBaths'] = HalfBaths
            item['Bedrooms'] = Bedrooms
            item['Garage'] = 0
            item['Description'] = ''.join(Description)
            item['ElevationImage'] = '|'.join(ElevationImage)
            item['PlanWebsite'] = response.url
            yield item


# from scrapy.cmdline import execute
# execute("scrapy crawl prominence".split())