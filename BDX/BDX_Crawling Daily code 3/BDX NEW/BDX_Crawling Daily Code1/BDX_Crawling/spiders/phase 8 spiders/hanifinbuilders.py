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


class DannysullivanconstructionComSpider(scrapy.Spider):
    name = 'hanifinbuilders'
    allowed_domains = []
    start_urls = ['https://hanifinbuilders.com/']
    builderNumber = 27756

    def start_requests(self):
        url = "https://hanifinbuilders.com/"
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'If-Modified-Since': 'Mon, 05 Oct 2020 08:51:50 GMT',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'Cookie': 'exp_last_visit=1601622341; exp_last_activity=1601888253; exp_tracker=%7B%220%22%3A%22index%22%2C%22token%22%3A%22a2eb2c9c31bd9d4233621b6886318619%22%7D; exp_csrf_token=480ab04a5e4ab47e1403a977514bf74b8da8ac1a'
        }
        yield scrapy.FormRequest(url=url, callback=self.parse, dont_filter=True, headers=headers)

    def parse(self, response):
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
        item['Street1'] = '420 Kenwood Avenue'
        item['City'] = 'Delmar'
        item['State'] = 'NY'
        item['ZIP'] = '12054'
        item['AreaCode'] = '518'
        item['Prefix'] = '439'
        item['Suffix'] = '9033'
        item['Extension'] = ""
        item['Email'] = 'info@hanifinbuilders.com'
        item[
            'SubDescription'] = "Hanifin Home Builders is currently updating all of our Standard Model drawings to high resolution and color.Futher down the page you'll find several of our original Standard Models."
        item[
            'SubImage'] = 'https://hanifinbuilders.com/images/slide_01b.jpg|https://hanifinbuilders.com/images/slide_02.jpg|https://hanifinbuilders.com/images/slide_04.jpg'
        item['SubWebsite'] = response.url
        yield item

        planlink = 'https://hanifinbuilders.com/index.php/home-builder/Home-Models'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Referer': 'https://hanifinbuilders.com/index.php/home-builder/Homes-For-Sale',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
        }
        yield scrapy.FormRequest(url=planlink, callback=self.plinks, headers=headers, dont_filter=True)

    def plinks(self, response):
        links = response.xpath(
            '//div[@class="col-lg-4 col-md-3 col-sm-3 fw_light m_bottom_45 m_xs_bottom_30"]//*[contains(text(),"Details")]/@href').extract()
        for plink in links:
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cache-Control': 'max-age=0',
                'Host': 'hanifinbuilders.com',
                'Referer': 'https://hanifinbuilders.com/index.php/home-builder/Home-Models',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
            }
            print(plink)
            # a = 'https://hanifinbuilders.com/index.php/home-builder/Home-Models-Details/bennett'
            yield scrapy.FormRequest(url=plink, callback=self.planDetail, headers=headers, dont_filter=True)

    def planDetail(self, response):
        print(response.url)
        try:
            PlanName = response.xpath('//*[@class="row"]//h2/text()').get()
            print(PlanName)
        except Exception as e:
            print("PlanName: ", e)
        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = self.builderNumber
            print(SubdivisionNumber)
        except Exception as e:
            print(str(e))

        try:
            PlanNotAvailable = 0
        except Exception as e:
            print(e)

        try:
            PlanTypeName = 'Single Family'
        except Exception as e:
            print(e)

        try:
            BasePrice = 0
        except Exception as e:
            print(str(e))

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)
        try:
            Bedroo = response.xpath('//*[contains(text(),"bedroom")]/text()').get()
            Bedroom = Bedroo.split('bedroo')[0]
            Bedroom = Bedroom.split('square feet')[-1]
            Bedrooms = re.findall(r"(\d+)", Bedroom)[0]
            Bedrooms = Bedrooms.strip()

        except Exception as e:
            Bedrooms = 0
            print("Bedrooms: ", e)

        try:
            Bathroo = response.xpath('//*[contains(text(),"bath")]/text()').get()
            Bathroom = Bathroo.split('bath')[0]
            Baths = Bathroom.split('bedroom')[-1].strip()
            tmp = re.findall(r"(\d+)", Baths)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0

        except Exception as e:
            Baths = 0
            print("Baths: ", e)

        try:
            Garage = response.xpath('//*[contains(text(),"Car Garage")]/text()').get()
            if Garage == None:
                Garage = response.xpath('//*[contains(text(),"car garage")]/text()').get()
            Garage = Garage.split('bathrooms')[-1]
            Garage = re.findall(r"(\d+)", Garage)[0]
            Garage = Garage.strip()
        except Exception as e:
            Garage = 0
            print("Garage: ", e)
        try:
            BaseSqft = response.xpath('//*[contains(text(),"square feet")]/text()').get()
            BaseSqft = BaseSqft.split('square feet')[1].strip()
            print(BaseSqft)
        except Exception as e:
            print("BaseSQFT: ", e)

        try:
            # ElevationImage = []
            ElevationImage = response.xpath(
                '//*[@class="col-lg-9 col-md-9 col-sm-9 m_xs_bottom_30"]//*[contains(@src,"im")]/@src').getall()
            ElevationImage = "|".join(ElevationImage)
        except Exception as e:
            print(str(e))

        unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['Type'] = Type
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number  # < -------- Changes here
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = PlanName
        item['PlanNotAvailable'] = PlanNotAvailable
        item['PlanTypeName'] = PlanTypeName
        item['BasePrice'] = BasePrice
        item['BaseSqft'] = BaseSqft
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item[
            'Description'] = "Hanifin Home Builders is currently updating all of our Standard Model drawings to high resolution and color.Futher down the page you'll find several of our original Standard Models."
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item

        hlink = 'https://hanifinbuilders.com/index.php/home-builder/Homes-For-Sale'
        head1 = {'Accept-Encoding': 'gzip, deflate, br',
                 'Accept-Language': 'en-US,en;q=0.9',
                 'Cookie': '__utmc=223605378; __utmz=223605378.1600078847.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); exp_last_visit=1601622886; exp_csrf_token=9e128f16a347fb0c187e19c8ab725ccba40e5e61; __utma=223605378.1499735967.1600078847.1601622110.1601977435.7; __utmt=1; __utmb=223605378.12.10.1601977435; exp_last_activity=1601978224; exp_tracker=%7B%220%22%3A%22images%2Fshadow.png%22%2C%221%22%3A%22home-builder%2FHomes-For-Sale%22%2C%222%22%3A%22images%2Fshadow.png%22%2C%223%22%3A%22home-builder%2FHomes-For-Sale%22%2C%224%22%3A%22images%2Fshadow.png%22%2C%22token%22%3A%22cf3d3b23adbe8ab4ce59a6d0dde68ee3%22%7D',
                 'Host': 'hanifinbuilders.com',
                 'If-Modified-Since': 'Tue, 06 Oct 2020 09:57:03 GMT',
                 'Sec-Fetch-Dest': 'document',
                 'Sec-Fetch-Mode': 'navigate',
                 'Sec-Fetch-Site': 'none',
                 'Sec-Fetch-User': '?1',
                 'Upgrade-Insecure-Requests': '1',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
        yield scrapy.FormRequest(url=hlink, callback=self.homeDetail, headers=head1, dont_filter=True)

    def homeDetail(self, response):
        unique = str("Plan Unknown") + str(self.builderNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['unique_number'] = unique_number
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = "Plan Unknown"
        item['SubdivisionNumber'] = self.builderNumber
        item['PlanName'] = "Plan Unknown"
        item['PlanNotAvailable'] = 1
        item['PlanTypeName'] = "Single Family"
        item['BasePrice'] = 0
        item['BaseSqft'] = 0
        item['Baths'] = 0
        item['HalfBaths'] = 0
        item['Bedrooms'] = 0
        item['Garage'] = 0
        item['Description'] = ""
        item['ElevationImage'] = ""
        item['PlanWebsite'] = ""
        yield item

        try:
            SpecStreet1 = '45 Darroch Road'
            SpecCity = 'Delmar'
            SpecState = 'NY'
            SpecZIP = '00000'
            unique = str(SpecStreet1) + str(SpecCity) + str(SpecState) + str(SpecZIP)
            SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % SpecNumber, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
            print(e)

        # try:
        #     PlanNumber = response.meta['PN']
        # except Exception as e:
        #     print(e)

        try:
            MasterBedLocation = "Down"
        except Exception as e:
            print(e)

        try:
            SpecWebsite = response.url
        except Exception as e:
            print(e)

        # ----------------------- Don't change anything here ---------------- #
        item = BdxCrawlingItem_Spec()
        item['SpecNumber'] = SpecNumber
        item['PlanNumber'] = unique_number
        item['SpecStreet1'] = '45 Darroch Road'
        item['SpecCity'] = 'Delmar'
        item['SpecState'] = 'NY'
        item['SpecZIP'] = SpecZIP
        item['SpecCountry'] = "USA"
        item['SpecPrice'] = '569000'
        item['SpecSqft'] = '2600'
        item['SpecBaths'] = '2'
        item['SpecHalfBaths'] = '1'
        item['SpecBedrooms'] = '4'
        item['MasterBedLocation'] = MasterBedLocation
        item['SpecGarage'] = '0'
        item[
            'SpecDescription'] = "Hanifin Home Builders is currently updating all of our Standard Model drawings to high resolution and color.Futher down the page you'll find several of our original Standard Models."
        item[
            'SpecElevationImage'] = 'https://hanifinbuilders.com/images/uploads/249/45_darroch_front_elevation__medium.jpg'
        item['SpecWebsite'] = SpecWebsite
        yield item


if __name__ == '__main__':
    execute("scrapy crawl hanifinbuilders".split())
