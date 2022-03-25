#   //*[@class="menu-main-menu-container"]//*[@class="  sub-menu "]/li/a/@href  ======= Community links]
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header

class DanDolanHomesComSpider(scrapy.Spider):
    name = 'DanDolanHomes'
    allowed_domains = []
    start_urls = ['http://dandolanhomes.com/']
    builderNumber = 19734

    def parse(self, response):
        for i in range(1,8):
            if i == 1:
                subdivisonName = 'The Fountains'
                subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % subdivisonNumber, "wb")
                f.write(response.body)
                f.close()
                item2 = BdxCrawlingItem_subdivision()
                item2['sub_Status'] = "Active"
                item2['SubdivisionName'] = subdivisonName
                item2['SubdivisionNumber'] = subdivisonNumber
                item2['BuilderNumber'] = self.builderNumber
                item2['BuildOnYourLot'] = 0
                item2['OutOfCommunity'] = 1
                item2['Street1'] = 'Devils Glen Rd & Thunder Ridge Rd'
                item2['City'] = 'Bettendorf'
                item2['State'] = 'IA'
                item2['ZIP'] = '52722'
                item2['AreaCode'] = '563'
                item2['Prefix'] = '381'
                item2['Suffix'] = '4088'
                item2['Extension'] = ""
                item2['Email'] = ""
                item2['SubDescription'] = 'Call our office at 563-381-4088 to ask about reserving a lot. Lots are going quickly, so give us a call today! Dan Dolan Homes is bringing new villas to Bettendorf at Devil’s Glen and Thunder Ridge. We are glad to announce our newest community The Villas at the Fountains.'
                item2['SubImage'] = "http://dandolanhomes.com/wp-content/uploads/2019/04/logo-dandolanhomes-hr-1.jpg"
                item2['SubWebsite'] = 'http://dandolanhomes.com/the-fountains/'
                yield item2

            elif i == 2:
                subdivisonName = 'Glengevlin'
                subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % subdivisonNumber, "wb")
                f.write(response.body)
                f.close()
                item2 = BdxCrawlingItem_subdivision()
                item2['sub_Status'] = "Active"
                item2['SubdivisionName'] = subdivisonName
                item2['SubdivisionNumber'] = subdivisonNumber
                item2['BuilderNumber'] = self.builderNumber
                item2['BuildOnYourLot'] = 0
                item2['OutOfCommunity'] = 1
                item2['Street1'] = 'Devils Glen Rd & Thunder Ridge Rd'
                item2['City'] = 'Bettendorf'
                item2['State'] = 'IA'
                item2['ZIP'] = '52722'
                item2['AreaCode'] = '563'
                item2['Prefix'] = '381'
                item2['Suffix'] = '4088'
                item2['Extension'] = ""
                item2['Email'] = ""
                item2['SubDescription'] = 'Dan Dolan Homes is bringing a little bit of Ireland to Bettendorf at Devil’s Glen and Thunder Ridge. We are glad to announce our newest community The Villas at Glengevlin.'
                item2['SubImage'] = "http://dandolanhomes.com/wp-content/uploads/2017/04/communities-glengevlin.jpg"
                item2['SubWebsite'] = 'http://dandolanhomes.com/glengevlin/'
                yield item2
            elif i == 3:
                subdivisonName = 'Hopewell'
                subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % subdivisonNumber, "wb")
                f.write(response.body)
                f.close()
                item2 = BdxCrawlingItem_subdivision()
                item2['sub_Status'] = "Active"
                item2['SubdivisionName'] = subdivisonName
                item2['SubdivisionNumber'] = subdivisonNumber
                item2['BuilderNumber'] = self.builderNumber
                item2['BuildOnYourLot'] = 0
                item2['OutOfCommunity'] = 1
                item2['Street1'] = 'Hopewell Ave & Devils Glen Rd'
                item2['City'] = 'Bettendorf'
                item2['State'] = 'IA'
                item2['ZIP'] = '52722'
                item2['AreaCode'] = '563'
                item2['Prefix'] = '381'
                item2['Suffix'] = '4088'
                item2['Extension'] = ""
                item2['Email'] = ""
                item2['SubDescription'] = 'We at Dan Dolan Homes understand that each new homeowner is aspiring for something different – something that is just right for them. Whether you are buying your first home in which your new family will grow, or you are looking to downsize and enjoy retirement and grandchildren, while having the ability to age in place. Dan Dolan Homes is all about making homes accessible for everyone.'
                item2['SubImage'] = "http://dandolanhomes.com/wp-content/uploads/2017/05/interior-default-1.jpg"
                item2['SubWebsite'] = 'http://dandolanhomes.com/hopewell/'
                yield item2
            elif i == 4:
                subdivisonName = 'Jersey Farms'
                subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % subdivisonNumber, "wb")
                f.write(response.body)
                f.close()
                item2 = BdxCrawlingItem_subdivision()
                item2['sub_Status'] = "Active"
                item2['SubdivisionName'] = subdivisonName
                item2['SubdivisionNumber'] = subdivisonNumber
                item2['BuilderNumber'] = self.builderNumber
                item2['BuildOnYourLot'] = 0
                item2['OutOfCommunity'] = 1
                item2['Street1'] = 'Fairhaven Rd'
                item2['City'] = 'Davenport'
                item2['State'] = 'IA'
                item2['ZIP'] = '00000'
                item2['AreaCode'] = '563'
                item2['Prefix'] = '381'
                item2['Suffix'] = '4088'
                item2['Extension'] = ""
                item2['Email'] = ""
                item2['SubDescription'] = 'We at Dan Dolan Homes understand that each new homeowner is aspiring for something different – something that is just right for them. Whether you are buying your first home in which your new family will grow, or you are looking to downsize and enjoy retirement and grandchildren, while having the ability to age in place. Dan Dolan Homes is all about making homes accessible for everyone.'
                item2['SubImage'] = "http://dandolanhomes.com/wp-content/uploads/2017/05/interior-default-1.jpg"
                item2['SubWebsite'] = 'http://dandolanhomes.com/jersey-farms/'
                yield item2
            elif i == 5:
                subdivisonName = 'Mill Creek'
                subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % subdivisonNumber, "wb")
                f.write(response.body)
                f.close()
                item2 = BdxCrawlingItem_subdivision()
                item2['sub_Status'] = "Active"
                item2['SubdivisionName'] = subdivisonName
                item2['SubdivisionNumber'] = subdivisonNumber
                item2['BuilderNumber'] = self.builderNumber
                item2['BuildOnYourLot'] = 0
                item2['OutOfCommunity'] = 1
                item2['Street1'] = 'Clinton Community School District'
                item2['City'] = 'Clinton'
                item2['State'] = 'IA'
                item2['ZIP'] = '52732'
                item2['AreaCode'] = '563'
                item2['Prefix'] = '381'
                item2['Suffix'] = '4088'
                item2['Extension'] = ""
                item2['Email'] = ""
                item2['SubDescription'] = 'We at Dan Dolan Homes understand that each new homeowner is aspiring for something different – something that is just right for them. Whether you are buying your first home in which your new family will grow, or you are looking to downsize and enjoy retirement and grandchildren, while having the ability to age in place. Dan Dolan Homes is all about making homes accessible for everyone.'
                item2['SubImage'] = "http://dandolanhomes.com/wp-content/uploads/2017/05/interior-default-1.jpg"
                item2['SubWebsite'] = 'http://dandolanhomes.com/mill-creek/'
                yield item2
            elif i == 6:
                subdivisonName = 'Riverbend'
                subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % subdivisonNumber, "wb")
                f.write(response.body)
                f.close()
                item2 = BdxCrawlingItem_subdivision()
                item2['sub_Status'] = "Active"
                item2['SubdivisionName'] = subdivisonName
                item2['SubdivisionNumber'] = subdivisonNumber
                item2['BuilderNumber'] = self.builderNumber
                item2['BuildOnYourLot'] = 0
                item2['OutOfCommunity'] = 1
                item2['Street1'] = 'Clinton Community School District'
                item2['City'] = 'Clinton'
                item2['State'] = 'IA'
                item2['ZIP'] = '00000'
                item2['AreaCode'] = ''
                item2['Prefix'] = ''
                item2['Suffix'] = ''
                item2['Extension'] = ""
                item2['Email'] = ""
                item2['SubDescription'] = 'The Riverbend subdivision brings a new and exciting design concept to a desirable Muscatine area. Take advantage of the park-like and wooded views from your screened-in porch on a private cul-de-sac. Riverbend is located just off Hwy 61 and offers convenient access to shopping, dining, and entertainment. Townhomes and single-family homes are available for purchase; say good-bye to lawn care and snow removal and enjoy the age-in-place design of our properties that offer no-step entries, wide doorways, and full basements with an option to finish!'
                item2['SubImage'] = "http://dandolanhomes.com/wp-content/uploads/2017/05/interior-default-1.jpg"
                item2['SubWebsite'] = 'http://dandolanhomes.com/riverbend/'
                yield item2
            elif i == 7:
                subdivisonName = 'town-and-country'
                subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
                f = open("html/%s.html" % subdivisonNumber, "wb")
                f.write(response.body)
                f.close()
                item2 = BdxCrawlingItem_subdivision()
                item2['sub_Status'] = "Active"
                item2['SubdivisionName'] = subdivisonName
                item2['SubdivisionNumber'] = subdivisonNumber
                item2['BuilderNumber'] = self.builderNumber
                item2['BuildOnYourLot'] = 0
                item2['OutOfCommunity'] = 1
                item2['Street1'] = '315 Meuse Ct'
                item2['City'] = 'Blue Grass'
                item2['State'] = 'IA'
                item2['ZIP'] = '52726'
                item2['AreaCode'] = ''
                item2['Prefix'] = ''
                item2['Suffix'] = ''
                item2['Extension'] = ""
                item2['Email'] = ""
                item2['SubDescription'] = 'Our townhomes and single-family properties within the Towne & Country subdivision offers small town living with quick access to Hwy 61, Davenport, and Muscatine. Blue Grass is also only 6 miles from Buffalo Beach, which provides a boat launch and beach to enjoy during the summer months or a beautiful view of the Mississippi River in the fall. All homes are Dan Dolan quality with energy star rated efficiency!'
                item2['SubImage'] = "http://dandolanhomes.com/wp-content/uploads/2017/05/interior-default-1.jpg"
                item2['SubWebsite'] = 'http://dandolanhomes.com/town-and-country/'
                yield item2

from scrapy.cmdline import execute
# execute("scrapy crawl DanDolanHomes".split())