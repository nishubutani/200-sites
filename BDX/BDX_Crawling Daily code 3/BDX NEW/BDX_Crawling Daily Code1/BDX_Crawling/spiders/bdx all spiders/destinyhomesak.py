


# -*- coding: utf-8 -*-
import re
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class RivertoRiverLogHomesSpiderSpider(scrapy.Spider):
    name = 'destinyhomesak'
    allowed_domains = ['destinyhomesak.com']
    start_urls = ['https://www.destinyhomesak.com/']
    builderNumber = 52497


    def parse(self, response):


        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = ''
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        #enter any address you fond on the website.
        item2['Street1'] = ''
        item2['City'] = 'WASILA'
        item2['State'] = 'AK'
        item2['ZIP'] = '00000'
        item2['AreaCode'] = ''
        item2['Prefix'] = ""
        item2['Suffix'] = " "
        item2['Extension'] = ""
        item2['Email'] = ""
        item2['SubDescription'] = "Destiny Homes Construction began building homes in Matanuska Susitna Valley since 2010, but its story began long before that. Paul Losik, the owner of Destiny Homes Construction started to work in construction business in 2002. He was a project manager for one of the home builders here in the Valley. Working as a project manager, he learned that communication is a key component in client and builder relationship. With his own company, Paul is a hands-on builder who inspects job sites daily and takes pride in making sure that all the stages of the building process are completed in a professional, timely manner and at the same time with the highest quality standards. Destiny Homes has many plans for you to choose from or we can adjust them to your specification or even design your dream home from scratch. From designing plan, clearing the lot and managing home construction until giving keys to the buyers, Paul always works hard to build the highest quality home for the clients"
        item2['SubImage'] = "https://lh3.googleusercontent.com/3IAu9Y43Lg7iFwteCcJV5gTgDU4LzONoMyDXfeeQIqUyJ5sV0ycfNUxbKBjtgV0W_OAEqloj-WNiZZIUQHFAmEa3dsNLlfE2YZliofY3kEhDz6Ef1wiT=s1600|https://lh3.googleusercontent.com/0EHtccQs6LXD5HhhPiAPfrvFvih5ToljVxYwQ-jiG-QPrzS0wZ5tOc0CwYfjmjnfC0zBhlsWUmoz_Phbgqt5GQ3SMLxz5ZVLTcK6JC9JOE57QGxK9bO9Lg=s999"
        item2['SubWebsite'] = 'https://www.destinyhomesak.com/'
        # item2['AmenityType'] = ''
        yield item2



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl destinyhomesak'.split())


