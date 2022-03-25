# -*- coding: utf-8 -*-
import os
import hashlib
import re

import scrapy
from BDX_Crawling.items import BdxCrawlingItem_subdivision


class EastonHomesSpider(scrapy.Spider):
    name = 'easton_homes'
    allowed_domains = []
    start_urls = ['https://www.presbyterianseniorliving.org/community-list']
    builderNumber = 248941879697289269987134863713

    def parse(self, response):
        subdivisiondata = re.findall(r'name =(.*?)var servicesList',response.text,re.DOTALL)
        for data in subdivisiondata:
            subdivision_name = re.findall(r'"(.*?)";',data)[0]
            subdivision_links = re.findall(r'var link = "(.*?)";',data)[0]
            address = re.findall(r'var address = \("(.*?)"\)',data)[0]
            Image = re.findall(r'var image = (.*?);',data,re.DOTALL)[0].strip('"')
            phone = re.findall(r'var phone = "(.*?)";',data)[0]
            yield scrapy.Request(url=subdivision_links, callback=self.subdivisionData, meta={'subdivisionName':subdivision_name,'address':address, 'image':Image, 'phone':phone})

    def subdivisionData(self, response):

        subdivisonName = response.meta['subdivisionName']
        subdivisonNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
        f = open("html/%s.html" % subdivisonNumber, "wb")
        f.write(response.body)
        f.close()

        address = response.meta['address'].split(',')
        Street1 = address[0]
        City = address[1].strip()
        State = address[-1].strip().split(' ')[0]
        ZIP = address[-1].strip().split(' ')[-1]
        description = ''
        description = ''.join(response.xpath('//*[@id="hs_cos_wrapper_aboutContent"]//span/text()|//*[@id="hs_cos_wrapper_community_info_supporting_text"]//p//text()').extract()).strip()
        if not description:
            description = ''.join(response.xpath('//*[@id="hs_cos_wrapper_community_info_supporting_text"]//p/text()|//*[@id="hs_cos_wrapper_aboutContent"]//p/text()|//*[@id="hs_cos_wrapper_mainContent"]//p//text()').extract()).strip()
            if not description:
                description= ''.join(response.xpath('//*[@class="all--text--left"]//p//text()').extract()).strip()
        description = description.replace('Minimum and Maximum Income Limits Apply','')
        phone = response.xpath('//*[contains(text(),"Call:")]/following-sibling::text()').extract_first().strip().split('.')
        subimages = response.meta['image']
        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionName'] = subdivisonName
        item2['SubdivisionNumber'] = subdivisonNumber
        item2['BuilderNumber'] = self.builderNumber
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 1
        item2['Street1'] = Street1
        item2['State'] = State
        item2['City'] = City
        item2['ZIP'] = ZIP
        item2['AreaCode'] = phone[0]
        item2['Prefix'] = phone[1]
        item2['Suffix'] = phone[-1]
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = description
        item2['SubImage'] = subimages
        item2['SubWebsite'] = response.url
        yield item2


# from scrapy.cmdline import execute
# execute("scrapy crawl easton_homes".split())