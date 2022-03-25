import hashlib
import re
import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class haldemanhome(scrapy.Spider):
    name ='haldemanhome'
    allowed_domains = []
    start_urls = ['http://www.hennesseyhomesinc.com/']

    builderNumber = 51544

    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

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
        item['Street1'] = 'Haldeman Homes, P.O. Box 6262'
        item['City'] = 'Auburn'
        item['State'] = 'CA'
        item['ZIP'] = '95602'
        item['AreaCode'] = '530'
        item['Prefix'] ='823'
        item['Suffix'] = '2059'
        item['Extension'] = ""
        item['Email'] ='shannon@haldemanhomes.com'
        item['SubDescription'] = "Our portfolio of projects include hundreds of custom homes featuring varying architectural styles such as Tuscan, Contemporary, Spanish, Craftsman Storybook, Tahoe, Victorian and more. We have commercial projects up to 40,000 square feet using various types of construction including wood framed, steel and concrete tilt up."
        item['SubImage']= "https://images.squarespace-cdn.com/content/v1/54eac5fae4b0feaa47752295/1560456131550-98B2ASPMMARMOI5BWMNL/ke17ZwdGBToddI8pDm48kHweAscJiWH-lNaF3MCIHbl7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0jAoOkRmPE63FUjiJOEKAz7XdI10HFX1DTX-32tl1HZywuGGYn-VnEZdSI8BS5b_og/In+The+Land+small.jpg?format=2500w|https://images.squarespace-cdn.com/content/v1/54eac5fae4b0feaa47752295/1566185078580-AAGX9M5MOHVVLU06Q9KW/ke17ZwdGBToddI8pDm48kLkXF2pIyv_F2eUT9F60jBl7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0iyqMbMesKd95J-X4EagrgU9L3Sa3U8cogeb0tjXbfawd0urKshkc5MgdBeJmALQKw/IMG_7817+small.jpg?format=2500w|https://images.squarespace-cdn.com/content/v1/54eac5fae4b0feaa47752295/1562979119113-YRHWY76W1WLSYXL9X3Z9/ke17ZwdGBToddI8pDm48kLkXF2pIyv_F2eUT9F60jBl7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0iyqMbMesKd95J-X4EagrgU9L3Sa3U8cogeb0tjXbfawd0urKshkc5MgdBeJmALQKw/Commercial+TIs.jpg?format=2500w|https://images.squarespace-cdn.com/content/v1/54eac5fae4b0feaa47752295/1560454998966-QBL8KUJ1W7Y65SRII733/ke17ZwdGBToddI8pDm48kMQ4wTzo2awNDr8kRNxSikhZw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZUJFbgE-7XRK3dMEBRBhUpzryrumNFFjEciWSP2on4fHdbCALEbeHd5-On5eIGIabTxG9G4uY1mTW6dKpnkJITE/eaglesnest_twilight.jpg?format=2500w"
        item['SubWebsite'] = response.url
        yield item

#
# from scrapy.cmdline import execute
# execute("scrapy crawl haldemanhome".split())
