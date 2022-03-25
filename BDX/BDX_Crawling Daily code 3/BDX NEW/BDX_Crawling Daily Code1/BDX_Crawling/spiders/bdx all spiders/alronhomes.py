import hashlib
import re

import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan


class ArborBuildersSpider(scrapy.Spider):
    name = 'alronhomes'
    allowed_domains = []
    builderNumber = 62688

    def start_requests(self):
        url = 'https://alronhomes.com/gallery'
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'referer': 'https://alronhomes.com/meadowview',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
        }
        yield scrapy.Request(url=url,headers=headers,dont_filter=True,callback=self.parse)

    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionNumber'] = self.builderNumber
        item2['BuilderNumber'] = self.builderNumber
        item2['SubdivisionName'] = "No Sub Division"
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        # enter any address you fond on the website.
        item2['Street1'] = '15626 West High St.'
        item2['City'] = 'Middlefield'
        item2['State'] = 'OH'
        item2['ZIP'] = '44062'
        item2['AreaCode'] = '440'
        item2['Prefix'] = "632"
        item2['Suffix'] = "4663"
        item2['Extension'] = ""
        item2['Email'] = "aaron@alronhomes.com"
        item2['SubDescription'] = "Alron Homes is a homebuilding company and member of the Home Builders Association, located in Middlefield (Geauga County), Ohio that was established by two Amish brothers, Al and Aaron Miller. Al and Aaron decided to combine their knowledge and 23-plus years of experience to start a home building company. Alron Homes serves Geauga County and the surrounding communities, using only the highest quality materials and craftsmanship available"
        item2['SubImage'] = '|'.join(response.xpath('//*[@data-dm-multisize-attr="href"]/@data-image-url').getall()[0:66])
        item2['SubWebsite'] = 'https://alronhomes.com'
        item2['AmenityType'] = ''
        yield item2

        url = 'https://alronhomes.com/floor-plans'
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'referer': 'https://alronhomes.com/meadowview',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
        }
        yield scrapy.Request(url=url,dont_filter=True,headers=headers,callback=self.planextract)

    def planextract(self,response):
        links = response.xpath('//*[@data-dm-multisize-attr="href"]/@href').getall()
        for link in links:
            url = 'https://alronhomes.com' + link
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'max-age=0',
                'referer': 'https://alronhomes.com/meadowview',
                'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
            }
            yield scrapy.Request(url=url,dont_filter=True,headers=headers,callback=self.plandata)
            # yield scrapy.Request(url='https://alronhomes.com/woodside',dont_filter=True,headers=headers,callback=self.plandata)

    def plandata(self,response):
        data = ''.join(response.xpath('//p[@class="text-align-center"]/span/text()').getall())
        Type = 'SingleFamily'

        try:
            PlanName = response.xpath('//h1[@class="text-align-center"]/span/text()').extract_first()
        except Exception as e:
            PlanName = ''
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % PlanNumber, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
            print(e)

        SubdivisionNumber = self.builderNumber

        PlanNotAvailable = 0

        PlanTypeName = 'Single Family'

        try:
            BasePrice = 0.00
        except Exception as e:
            print(e)
        else:
            try:
                add_slug = data.replace(',','')
                BaseSqft = re.findall('(\d+) Total Sq Ft', add_slug)
                BaseSqft = BaseSqft[0].strip()

            except Exception as e:
                print(e)

            try:
                Bath = data.split('Bed')[-1].split('Bath')[0].strip()
                # Bath = Bath[0].strip()
                if '.5' in Bath:
                    HalfBaths = 1
                    Bath = Bath.replace('.5','').strip()
                else:
                    HalfBaths = 0
                # print(SpecBaths)
            except Exception as e:
                print(str(e))

            try:
                Bedrooms = re.findall('(\d+) Bed', data)

                Bedrooms = Bedrooms[0].strip()
                if Bedrooms == '':
                    Bedrooms = 0

            except Exception as e:
                Bedrooms = 0
                print(e)

            # try:
            #     Garage = re.findall('(\d+) Sq Ft Garage', data)
            #     if Garage != None:
            #         Garage = 1
            # except:
            Garage = 0.00

        # Garage = 0.00

        try:
            Description = ''.join(data)
        except Exception as e:
            print(e)

        try:
            ElevationImage1 = response.xpath('//*[@class="u_1796934096 dmRespCol small-12 medium-12 large-12"]//img/@data-dm-image-path').getall()[:-1]
            print(ElevationImage1)
        except Exception as e:
            print(e)
            ElevationImage1 = []

        try:
            ElevationImage2 = response.xpath('//*[@data-dm-multisize-attr="href"]/@data-image-url').extract()
        except Exception as e:
            print(e)
            ElevationImage2 = []

            # ElevationImage = []
        try:
            ElevationImage = ElevationImage1+ElevationImage2
            ElevationImage = "|".join(ElevationImage)
        except Exception as e:
            print(e)

        PlanWebsite = response.url

        # ----------------------- Don't change anything here --------------
        unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
                10 ** 30)  # < -------- Changes here
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
        item['Baths'] = Bath
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item['Description'] = ''
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item







if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl alronhomes".split())