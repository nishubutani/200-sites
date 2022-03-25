# -*- coding: utf-8 -*-
import hashlib
import re

import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class catesfineSpider(scrapy.Spider):
    name = 'catesfine'
    allowed_domains = []
    start_urls = ['https://catesfinehomes.com/']

    builderNumber = 53362

    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

        img=response.xpath('//div[@class="wpb_content_element media media_el animate_onoffset"]//img/@src').extract()

        images=response.xpath('//section[@id="portfolio-preview-items"]//img/@src').extract()

        subimage='|'.join(img + images)

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '2000 Industrial Blvd.'
        item['City'] = 'Stillwater'
        item['State'] = 'MN'
        item['ZIP'] = '55082'

        item['AreaCode'] = '651'
        item['Prefix'] = '439'
        item['Suffix'] = '2844'
        item['Extension'] = ""
        item['Email'] = 'jennifer@catesfinehomes.com'
        item[
            'SubDescription'] = 'The year was 1970. Stillwater was experiencing its first large-scale home development.Beige and gray houses, a handful of floor plans: dozens of houses went up quickly and they all looked the same. Judd and Julie Cates saw an opportunity to take an entirely different direction. They held architectural construction and quality craftsmanship in high regard, and they believed there would always be homeowners who shared this passion. Cates Construction was founded, and the family business grew steadily along with their crew of school-age kids: Shawn, Jay, Jennifer and Jeff.After renaming the company Cates Fine Homes in 2005, to better distinguish their market niche, Jay, Jennifer and Jeff assumed shared leadership of the company as Judd scaled back into retirement.What’s the secret to business longevity? How can a family builder thrive through five decades, surviving market adversities including double-digit mortgage interest rates and a great recession that all but brought home building to a halt? The Cates family business has stayed true to its original values and remained flexible to take on projects big and small, from remodeling a master bath to total renovations and, of course, new custom homes.Few fine home builders can claim 50 years, and it’s an accomplishment worth celebrating. We owe it all to our customers.'
        item['SubImage'] = subimage
        item['SubWebsite'] = response.url
        yield item


# from scrapy.cmdline import execute
# execute("scrapy crawl catesfine".split())