# -*- coding: utf-8 -*-
import hashlib
import re
import requests
import scrapy
from decimal import Decimal
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class ChaneyStottsConstructionSpider(scrapy.Spider):
    name = 'chaney_stotts_construction'
    allowed_domains = ['http://chaneystottsconstruction.com/']
    start_urls = ['http://chaneystottsconstruction.com/']

    builderNumber = "49113"


    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #
        image1 = response.xpath('//*[@class="upb_bg_img"]/@data-ultimate-bg').extract_first()
        image1 = re.findall(r'url\((.*?)\)',image1)[0]
        image2 = '|'.join(response.xpath('//*[@data-dt-img-description]/../a[contains(@href,".jpg")]/@href').extract())
        images = image1+'|'+image2.strip('|')
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = "P.O. Box 244"
        item['City'] = "Notus"
        item['State'] = "ID"
        item['ZIP'] = "83656"
        item['AreaCode'] = "208"
        item['Prefix'] = "371"
        item['Suffix'] = "8142"
        item['Extension'] = ""
        item['Email'] = "chaneystottsconstruction@gmail.com"
        item['SubDescription'] = ''.join(response.xpath('//*[@class="wpb_wrapper"]/p/text()').extract())
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        yield item


from scrapy.cmdline import execute
# execute("scrapy crawl chaney_stotts_construction".split())