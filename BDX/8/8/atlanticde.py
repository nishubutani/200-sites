# -*- coding: utf-8 -*-
import hashlib
import re
import time

from scrapy.http import HtmlResponse
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities

import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision


class AtlanticdeSpider(scrapy.Spider):
    name = 'atlanticde'
    # allowed_domains = ['atlanticde.com']
    start_urls = ['http://atlanticde.com/']
    builderNumber = '12626'

    def parse(self, response):

        options = Options()
        options.headless = True
        from selenium import webdriver


        driver = webdriver.Chrome(chrome_options=options, executable_path="chromedriver.exe")
        driver.maximize_window()
        time.sleep(10)

        driver.get('http://resortcustomhomes.com/featured-communities/')


        res = driver.page_source
        response = HtmlResponse(url=driver.current_url, body=bytes(res.encode('utf-8')))
        print(response)
        subdivision_names = response.xpath('//*[@class="title-heading-left"]/text()').getall()
        del subdivision_names[0]
        images = response.xpath('//*[@class="fusion-one-third one_third fusion-layout-column fusion-column-last fusion-spacing-yes"]')
        discriptions = response.xpath('//*[@class="fusion-image-carousel fusion-image-carousel-fixed lightbox-enabled fusion-carousel-border"]')
        for subdivision_name,discription,image  in zip(subdivision_names,discriptions,images):
            subdivision_name = subdivision_name
            if subdivision_name == 'The Peninsula – East Millsboro':
                street = '26937 Bay Farm Road'
                city = 'Millsboro'
                state = 'DE'
                zipcode = '19966'
            elif subdivision_name == 'Hawkseye – Lewes':
                street = 'Wolf Pointe,Black Marlin Drive'
                city = 'Lewes'
                state = 'DE'
                zipcode = '19958'
            elif subdivision_name == 'Rehoboth Beach Yacht & Country Club – Rehoboth Beach':
                street = '221 W Side Drive'
                city = 'Rehoboth Beach'
                state = 'DE'
                zipcode = '19971'
            elif subdivision_name == 'Kings Creek Country Club – Rehoboth Beach':
                street = '1 Kings Creek Circle'
                city = 'Rehoboth Beach'
                state = 'DE'
                zipcode = '19971'
            dis= discription.xpath('.//li/text()').getall()
            image = images.xpath('.//li//a/@href').getall()

            f = open("html/%s.html" % self.builderNumber, "wb")
            f.write(response.body)
            f.close()
            item = BdxCrawlingItem_subdivision()
            item['sub_Status'] = "Active"

            SubdivisionNumber = int(
                hashlib.md5(bytes(str(subdivision_name) + str(self.builderNumber), "utf8")).hexdigest(),
                16) % (10 ** 30)
            item['SubdivisionNumber'] = SubdivisionNumber
            item['BuilderNumber'] = self.builderNumber
            item['SubdivisionName'] = subdivision_name
            item['BuildOnYourLot'] = 0
            item['OutOfCommunity'] = 0
            item['Street1'] = street
            item['City'] = city
            item['State'] = state
            item['ZIP'] = zipcode
            item['AreaCode'] = '302'
            item['Prefix'] = '645'
            item['Suffix'] = '8222'
            item['Extension'] = ""
            item['Email'] = 'info@ResortCustomHomes.com '
            item['SubDescription'] = ''.join(dis)
            item['SubImage'] =  '|'.join(image)
            item['SubWebsite'] = response.url
            yield item

from scrapy.cmdline import execute
# execute("scrapy crawl atlanticde".split())




