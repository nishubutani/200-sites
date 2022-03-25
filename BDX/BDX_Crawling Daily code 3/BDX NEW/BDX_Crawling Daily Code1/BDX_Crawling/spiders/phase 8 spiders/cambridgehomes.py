# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header

class CambridgehomesSpider(scrapy.Spider):
    name = 'cambridgehomes'
    allowed_domains = []
    start_urls = ['http://www.cambridgehomesomaha.com/']

    builderNumber = 23548
    def parse(self,response):
        f= open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = 'CAMBRIDGE HOMES'
        item['City'] = ' OMAHA'
        item['State'] = 'NE'
        item['ZIP'] = '99228'
        item['AreaCode'] = '402'
        item['Prefix'] = '933'
        item['Suffix'] = '3883'
        item['Extension'] = ""
        item['Email'] = 'CAMBRIDGEHOMESOMAHA@OUTLOOK.COM'
        item[
            'SubDescription'] = "With over 45 years of construction experience, Cambridge Homes will ensure your ultimate satisfaction.Isn't it time you checked out a Cambridge Home?"
        item[
            'SubImage'] = 'https://images.squarespace-cdn.com/content/v1/54679d01e4b07084eb8c8ef9/1515715733572-ZOBZIQ9QODFCN91B0L1W/ke17ZwdGBToddI8pDm48kGyeMaNdLNazR00gG5luzpZ7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1UcSnmFVn2-Ie_qiYCyfMv_9daAoMldipkjdfXN2O2fmdgmTRBiKRmkE4Ib_L80v6RA/MR-12.jpg|ke17ZwdGBToddI8pDm48kNbLqx_FIYjfhtEsCHEHzad7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1UX_hdIVndeO72MD00jTnc1n42Pd5vs4VrV4yXG_EV_fzwRAeN1AbZG4OR41R6pDVyg'
        item['SubWebsite'] = response.url
        yield item
# execute("scrapy crawl cambridgehomes".split())