# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header

class DannysullivanconstructionComSpider(scrapy.Spider):
    name = 'ncmodulars'
    allowed_domains = []
    start_urls = ['']

    builderNumber = "902323489771880310750227781615"
