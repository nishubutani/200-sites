import json
import re

import scrapy
import os
import hashlib
import scrapy
from scrapy.utils.response import open_in_browser

from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, \
    BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision


class chadrickhomesSpider(scrapy.Spider):
    name = 'chadrickhomes'
    allowed_domains = ['www.chadrickhomes.com']
    start_urls = ['https://www.chadricehomes.com/deer-brook']

    builderNumber = '50488'

    # count = 0

    def parse(self, response):
        comm_links = list()
        comm_links = response.xpath('//li[@class="page-collection active-link"]/../li/a/@href').extract()
        comm_links1 = comm_links
        print(comm_links1)
        # comm_links2 = comm_links1.remove('/afton-grove')
        # print(comm_links2)

        for link in comm_links1:
            url = str(link)
            url = "https://www.chadricehomes.com" + url
            yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.parse_comm_data)

    def parse_comm_data(self, response):

        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)

        f.close()

        add = response.xpath(
            '//div[@class = "sqs-block map-block sqs-block-map sized vsize-12"]/@data-block-json').get()
        json_response = json.loads(add)
        subdivisonName = json_response['location']['addressTitle']
        Street1 = json_response['location']['addressLine1']
        address2 = json_response['location']['addressLine2']
        City = address2.split(",")[0]
        State = address2.split(",")[1].strip()
        Zip = address2.split(",")[2].strip()
        if "Chapel Creek" in subdivisonName:
            img = ["https://images.squarespace-cdn.com/content/v1/5600e07be4b01d1d828589f8/1492533611847-51U0QGM3RZIHP7M9V2Q0/ke17ZwdGBToddI8pDm48kDHPSfPanjkWqhH6pl6g5ph7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0mwONMR1ELp49Lyc52iWr5dNb1QJw9casjKdtTg1_-y4jz4ptJBmI9gQmbjSQnNGng/Photo+Apr+05%2C+2+10+31+PM.jpg","https://images.squarespace-cdn.com/content/v1/5600e07be4b01d1d828589f8/1492533613657-FZR7XZ5IU22XQ3O1VW7T/ke17ZwdGBToddI8pDm48kDHPSfPanjkWqhH6pl6g5ph7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0mwONMR1ELp49Lyc52iWr5dNb1QJw9casjKdtTg1_-y4jz4ptJBmI9gQmbjSQnNGng/Photo+Apr+05%2C+2+13+30+PM.jpg","https://images.squarespace-cdn.com/content/v1/5600e07be4b01d1d828589f8/1492533614759-TWV5U3LLKTBAYXVSJU8Z/ke17ZwdGBToddI8pDm48kDHPSfPanjkWqhH6pl6g5ph7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0mwONMR1ELp49Lyc52iWr5dNb1QJw9casjKdtTg1_-y4jz4ptJBmI9gQmbjSQnNGng/Photo+Apr+05%2C+2+13+56+PM.jpg","https://images.squarespace-cdn.com/content/v1/5600e07be4b01d1d828589f8/1492533615808-RLD8NTNSAYPXQZG2U8IS/ke17ZwdGBToddI8pDm48kDHPSfPanjkWqhH6pl6g5ph7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0mwONMR1ELp49Lyc52iWr5dNb1QJw9casjKdtTg1_-y4jz4ptJBmI9gQmbjSQnNGng/Photo+Apr+05%2C+2+14+18+PM.jpg","https://images.squarespace-cdn.com/content/v1/5600e07be4b01d1d828589f8/1492533615808-RLD8NTNSAYPXQZG2U8IS/ke17ZwdGBToddI8pDm48kDHPSfPanjkWqhH6pl6g5ph7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0mwONMR1ELp49Lyc52iWr5dNb1QJw9casjKdtTg1_-y4jz4ptJBmI9gQmbjSQnNGng/Photo+Apr+05%2C+2+14+18+PM.jpg","https://images.squarespace-cdn.com/content/v1/5600e07be4b01d1d828589f8/1492533617578-85EYQJNR94DU0LEAJE7C/ke17ZwdGBToddI8pDm48kDHPSfPanjkWqhH6pl6g5ph7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0mwONMR1ELp49Lyc52iWr5dNb1QJw9casjKdtTg1_-y4jz4ptJBmI9gQmbjSQnNGng/Photo+Apr+05%2C+2+15+30+PM.jpg","https://images.squarespace-cdn.com/content/v1/5600e07be4b01d1d828589f8/1492533618932-EBM1ZTNS35HVJW3UWSR8/ke17ZwdGBToddI8pDm48kDHPSfPanjkWqhH6pl6g5ph7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0mwONMR1ELp49Lyc52iWr5dNb1QJw9casjKdtTg1_-y4jz4ptJBmI9gQmbjSQnNGng/Photo+Apr+05%2C+2+16+15+PM.jpg","https://images.squarespace-cdn.com/content/v1/5600e07be4b01d1d828589f8/1492533620311-PMK4X6B915S1XLUQK2JT/ke17ZwdGBToddI8pDm48kDHPSfPanjkWqhH6pl6g5ph7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0mwONMR1ELp49Lyc52iWr5dNb1QJw9casjKdtTg1_-y4jz4ptJBmI9gQmbjSQnNGng/Photo+Apr+05%2C+2+16+48+PM.jpg","https://images.squarespace-cdn.com/content/v1/5600e07be4b01d1d828589f8/1492533621483-3A4J6QNCQY5ED26DBXN6/ke17ZwdGBToddI8pDm48kDHPSfPanjkWqhH6pl6g5ph7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0mwONMR1ELp49Lyc52iWr5dNb1QJw9casjKdtTg1_-y4jz4ptJBmI9gQmbjSQnNGng/Photo+Apr+05%2C+2+17+12+PM.jpg","https://images.squarespace-cdn.com/content/v1/5600e07be4b01d1d828589f8/1492533622499-WNCCM6KDN986PNNN3VYB/ke17ZwdGBToddI8pDm48kDHPSfPanjkWqhH6pl6g5ph7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0mwONMR1ELp49Lyc52iWr5dNb1QJw9casjKdtTg1_-y4jz4ptJBmI9gQmbjSQnNGng/Photo+Mar+30%2C+1+07+00+PM.jpg","https://images.squarespace-cdn.com/content/v1/5600e07be4b01d1d828589f8/1492533623963-P0ATZ59J3SNR6IK527UL/ke17ZwdGBToddI8pDm48kDHPSfPanjkWqhH6pl6g5ph7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0mwONMR1ELp49Lyc52iWr5dNb1QJw9casjKdtTg1_-y4jz4ptJBmI9gQmbjSQnNGng/Photo+Mar+30%2C+1+07+45+PM.jpg","https://images.squarespace-cdn.com/content/v1/5600e07be4b01d1d828589f8/1492533625174-GXN5KFC28KQPVBPCI0XF/ke17ZwdGBToddI8pDm48kDHPSfPanjkWqhH6pl6g5ph7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0mwONMR1ELp49Lyc52iWr5dNb1QJw9casjKdtTg1_-y4jz4ptJBmI9gQmbjSQnNGng/Photo+Mar+30%2C+1+08+08+PM.jpg"]
            Image = "|".join(img)
        elif "Deer Brook" in subdivisonName :
            img = ["https://images.squarespace-cdn.com/content/v1/5600e07be4b01d1d828589f8/1524164357955-8IV070FV7H0P58J4ZV5N/ke17ZwdGBToddI8pDm48kEIApj57Y0MQIurbwkGADs4UqsxRUqqbr1mOJYKfIPR7LoDQ9mXPOjoJoqy81S2I8GRo6ASst2s6pLvNAu_PZdIl0ul5lb-21CeNfBPGKHNYbUy_3B--3-Tz1UDJDsRZhzDXBBLHShEvZBmU2YTlB04/CRHomeslogo1.jpg","https://images.squarespace-cdn.com/content/v1/5600e07be4b01d1d828589f8/1557807476216-KYJ2M3EFOT6H6JSKIGJL/ke17ZwdGBToddI8pDm48kDHPSfPanjkWqhH6pl6g5ph7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0mwONMR1ELp49Lyc52iWr5dNb1QJw9casjKdtTg1_-y4jz4ptJBmI9gQmbjSQnNGng/IMG_4730.jpeg","https://images.squarespace-cdn.com/content/v1/5600e07be4b01d1d828589f8/1557807492115-4GH6ORDLNLKVHRF4TUBL/ke17ZwdGBToddI8pDm48kLBnCuLS4rYL7yVlMx_8oR57gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1UeSDz6IyKK09zZ-7q_gpQHSSpVyuY93tgEx5P2GE3RQd71VtgaaASevlyRsadXtEgw/IMG_4731.jpeg"]
            Image = "|".join(img)
        else:
            Image = "https://images.squarespace-cdn.com/content/v1/5600e07be4b01d1d828589f8/1524164357955-8IV070FV7H0P58J4ZV5N/ke17ZwdGBToddI8pDm48kEIApj57Y0MQIurbwkGADs4UqsxRUqqbr1mOJYKfIPR7LoDQ9mXPOjoJoqy81S2I8GRo6ASst2s6pLvNAu_PZdIl0ul5lb-21CeNfBPGKHNYbUy_3B--3-Tz1UDJDsRZhzDXBBLHShEvZBmU2YTlB04/CRHomeslogo1.jpg"
        try:
            subdivisonNumber = int(
                hashlib.md5(bytes(str(subdivisonName) + str(self.builderNumber), "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        SubDescription = response.xpath('//div[@class="sqs-block-content"]/p/text()').get()





        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = subdivisonNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = subdivisonName
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = Street1
        item['City'] = City
        item['State'] = State
        item['ZIP'] = Zip
        item['AreaCode'] = "405"
        item['Prefix'] = "748"
        item['Suffix'] = "0333"
        item['Extension'] = ""
        item['Email'] = "CHADRICE86@YAHOO.COM"
        item['SubDescription'] = SubDescription
        item['SubImage'] = Image
        item['SubWebsite'] = ""
        item['AmenityType'] = ""
        yield item
        #     try:


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl chadrickhomes".split())
