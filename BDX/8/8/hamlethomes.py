import hashlib
import re

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import scrapy
from selenium import webdriver
import time
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan


class HamlethomesSpider(scrapy.Spider):
    name = 'hamlethomes'
    allowed_domains = ['hamlet-homes.com']
    start_urls = ['https://hamlet-homes.com/']
    builderNumber = '27674'

    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = self.builderNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '84 4800 S # 200'
        item['City'] = 'Murray'
        item['State'] = 'UT'
        item['ZIP'] = '84107'
        item['AreaCode'] = '540'
        item['Prefix'] = '207'
        item['Suffix'] = '4609'
        item['Extension'] = ""
        item['Email'] = 'LiveNew@HamletHomes.org'
        item[
            'SubDescription'] = " now building in waterfront communities in awesome  Colonial Beach ~ See why Home can mean Living!  Please come take a stroll on the beach & arrive home to Happy! Life is grand year 'round here! Waterfront restaurants, live bands & entertainment, beaches, boating & fishing tournaments, playgrounds, parks, picnics & parades, casino, car shows & crafts ~ it's all here to love in Colonial Beach!.delivering new homes as well in Ladysmith: Lake Caroline &Lake Landor lakefront communities ~ Enjoy watersports, tennis courts, clubhouse, exercise facilities, basketball, hiking, picnics and playgrounds, large outdoor swimming pools, and lake beaches to love! ~  it's all here in these immaculately kept gated communities close to Richmond or Fredericksburg!"
        image = re.findall(r'<img src="(.*?)"',response.text)
        item[
            'SubImage'] = '|'.join(response.urljoin('https:' + i) for i in image)
        item['SubWebsite'] = response.url
        yield item

        planlinks = ['https://hamlet-homes.com/ramblers','https://hamlet-homes.com/classic-colonials']

        for link in planlinks:
            options = Options()
            options.headless = True
            driver = webdriver.Chrome(chrome_options=options, executable_path="chromedriver.exe")

            driver.maximize_window()
            time.sleep(15)

            driver.get(link)

            res = driver.page_source
            response = HtmlResponse(url=driver.current_url, body=bytes(res.encode('utf-8')))


            divs = response.xpath('//*[@class="widget widget-content widget-content-content-2"]')
            if not divs:
                divs = response.xpath('//*[@class="widget widget-gallery widget-gallery-gallery-1"]')

            for div in divs:
                d = div.extract()

                detail = div.xpath('.//*[@typography="HeadingBeta"]//text()').get().strip('~')
                try:
                    planname = detail.split('~')[0].strip()
                except:
                    planname = ''
                try:
                    sqft = detail.split('~')[1].strip()

                    sqft = re.findall(r'(\d+)', sqft)[0]
                except:
                    sqft = 0
                try:
                    bedroom = re.findall(r'(\d)br',detail)[-1]
                except:
                    try:
                        bedroom = re.findall(r'(\d) br', detail)[-1]
                    except:
                        bedroom = 0
                try:
                    bathroom = re.findall(r'(\d.\d)ba',detail)[-1]
                except:
                    try:
                        bathroom = re.findall(r'(\d)ba', detail)[-1]
                    except:
                        bathroom = ''

                if len(bathroom) > 1:
                    bathroom = bathroom[0]
                    halfbath = 1
                else:
                    halfbath = 0

                try:
                    image = div.xpath('.//img/@src').getall()
                    if  image == []:
                        image = re.findall(r'<img src="(.*?)"',d)

                except:
                    image = ''

                PlanNumber = int(hashlib.md5(bytes(planname, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % PlanNumber, "wb")
                f.write(response.body)
                f.close()

                SubdivisionNumber = self.builderNumber  # if subdivision is not available
                unique = str(PlanNumber) + str(SubdivisionNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

                item = BdxCrawlingItem_Plan()
                item['Type'] = 'SingleFamily'
                item['PlanNumber'] = PlanNumber
                item['unique_number'] = unique_number
                item['SubdivisionNumber'] = SubdivisionNumber
                item['PlanName'] = planname
                item['PlanNotAvailable'] = 0
                item['PlanTypeName'] = 'Single Family'
                item['BasePrice'] = 0
                item['BaseSqft'] = sqft
                item['Baths'] = bathroom
                item['HalfBaths'] = halfbath
                item['Bedrooms'] = bedroom
                item['Garage'] = 0
                item['Description'] = "It's Time to Live New !!"
                item['ElevationImage'] = "|".join(response.urljoin('https:' + i) for i in image)
                item['PlanWebsite'] = response.url
                yield item


from scrapy.cmdline import execute
# execute("scrapy crawl hamlethomes".split())