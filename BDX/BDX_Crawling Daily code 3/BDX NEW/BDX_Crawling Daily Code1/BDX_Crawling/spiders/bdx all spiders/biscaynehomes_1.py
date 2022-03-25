import hashlib
import json
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class biscaynehomesSpider(scrapy.Spider):

    name = 'biscaynehomes1'
    allowed_domains = []
    start_urls = ['https://www.biscaynehomes.com']

    builderNumber = "55156"

    def parse(self, response):

        item2 = BdxCrawlingItem_subdivision()
        item2['sub_Status'] = "Active"
        item2['SubdivisionName'] = "No Sub Division"
        item2['SubdivisionNumber'] = self.builderNumber
        item2['BuilderNumber'] = self.builderNumber
        item2['BuildOnYourLot'] = 0
        item2['OutOfCommunity'] = 0
        item2['Street1'] = '31800 Epperson Boulevard'
        item2['City'] = 'Wesley Chapel'
        item2['State'] = 'FL'
        item2['ZIP'] = '33545'
        item2['AreaCode'] = '813'
        item2['Prefix'] = '291'
        item2['Suffix'] = '4886'
        item2['Extension'] = ""
        item2['Email'] = "info@biscaynehomes.com"
        item2['SubDescription'] = ''
        item2['SubImage'] = 'https://www.biscaynehomes.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Flagoon-residences.a8350c8b.jpg&w=1920&q=75|https://www.biscaynehomes.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2FDMF_2018_19_24.a3754634.jpg&w=640&q=75|https://www.biscaynehomes.com/_next/static/media/DMF_1983_4_9.482624a4.jpg'
        item2['SubWebsite'] = response.url
        item2['AmenityType'] = ''
        yield item2

        link = 'https://www.biscaynehomes.com/early-move-in'
        yield scrapy.FormRequest(url=link,callback=self.pars22,dont_filter=True)

    def pars22(self,response):
        links = response.xpath('//div[@class="grid grid-cols-1 gap-y-4 md:grid-cols-2 md:gap-x-6 md:gap-y-10 lg:gap-x-8"]/a//h3/text()').extract()

        for link in links:
            name = link.split(" ")[0].lower()
            print(name)

            link = 'https://www.biscaynehomes.com/_next/data/jswjkMX4R9hFK1jCyvBYP/community/robins-cove/' + name + '.json'
            print(link)


            # link = 'https://www.biscaynehomes.com' + link
            # link = 'https://www.biscaynehomes.com/_next/data/jswjkMX4R9hFK1jCyvBYP/community/robins-cove/egret.json'
            # link = 'https://www.biscaynehomes.com/_next/data/jswjkMX4R9hFK1jCyvBYP/community/robins-cove/osprey.json'
            yield scrapy.FormRequest(url=link,callback=self.pats,dont_filter=True)

    def pats(self,response):

        datas = response.text
        data1 = json.loads(datas)


        try:
            loop = data1['pageProps']['model']['variants']
            loop = len(loop)
        except Exception as e:
            print(e)
            loop = ''

        for i in range(0,loop):
            try:
                PlanName = data1['pageProps']['model']['variants'][i]['title']
                print(PlanName)
            except Exception as e:
                print(e)
                PlanName = ''

            try:
                Bed = data1['pageProps']['model']['variants'][i]['beds']
                print(Bed)

                if '-' in Bed:
                    Bed = Bed.split('-')[-1]
                    Bedrooms = re.findall(r'(\d+)', Bed)[0]
                else:
                    Bedrooms = re.findall(r'(\d+)', Bed)[0]
            except Exception as e:
                print(e)

            try:
                bath = data1['pageProps']['model']['variants'][i]['baths']
                if '-' in bath:
                    bath = bath.split('-')[-1]
                    tmp = re.findall(r"(\d+)", bath)
                    if tmp != []:
                        Baths = tmp[0]
                        if len(tmp) > 1:
                            HalfBaths = 1
                        else:
                            HalfBaths = 0
                    else:
                        Baths = 0
                        HalfBaths = 0
                else:
                    tmp = re.findall(r"(\d+)", bath)
                    if tmp != []:
                        Baths = tmp[0]
                        if len(tmp) > 1:
                            HalfBaths = 1
                        else:
                            HalfBaths = 0
                    else:
                        Baths = 0
                        HalfBaths = 0
            except Exception as e:
                print(e)

            try:
                garage = data1['pageProps']['model']['variants'][i]['garages']
                Garage = re.findall(r'\d+', garage)[0]
            except Exception as e:
                print(e)

            try:
                Sqft = data1['pageProps']['model']['variants'][i]['area']
                print(type(Sqft))
                if '-' in Sqft:
                    Sqft = Sqft.split('-')[-1]
                    Sqft = Sqft.replace(',', '')
                    BaseSqft = re.findall(r'\d+', Sqft)[0]
                else:
                    Sqft = Sqft.replace(',', '')
                    BaseSqft = re.findall(r'\d+', Sqft)[0]
            except Exception as e:
                print(e)

            try:
                price = data1['pageProps']['model']['variants'][i]['price']
                base_price = re.findall(r'\d+', price)[0]
            except Exception as e:
                print(e)
                base_price = 0



            try:
                Description = ''
                # ElevationImage = 'https://www.biscaynehomes.com'+ div.xpath('//*[@class="h-48 md:h-88 relative"]/div/child::picture/img/@src').extract_first(default='').strip()
                ElevationImage = ''
                PlanWebsite = response.url

            except Exception as e:
                print(e)

            Type = 'SingleFamily'
            PlanNotAvailable = 0
            PlanTypeName = 'Single Family'

        # ------------------- If Plan Found found ------------------------- #

            PlanNumber = int(hashlib.md5(bytes(response.url + PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
            SubdivisionNumber = self.builderNumber  # if subdivision is not available
            unique = str(PlanNumber) + str(SubdivisionNumber)
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            item = BdxCrawlingItem_Plan()
            item['Type'] = Type
            item['PlanNumber'] = PlanNumber
            item['unique_number'] = unique_number
            item['SubdivisionNumber'] = SubdivisionNumber
            item['PlanName'] = PlanName
            item['PlanNotAvailable'] = PlanNotAvailable
            item['PlanTypeName'] = PlanTypeName
            item['BasePrice'] = base_price
            item['BaseSqft'] = BaseSqft
            item['Baths'] = Baths
            item['HalfBaths'] = HalfBaths
            item['Bedrooms'] = Bedrooms
            item['Garage'] = Garage
            item['Description'] = Description
            item['ElevationImage'] = ElevationImage
            item['PlanWebsite'] = PlanWebsite
            yield item






    #---------------------- old code ---------------------------------------#




    #     try:
    #         PlanName = div.xpath('.//h2/text()').extract_first(default='').strip()
    #         print(PlanName)
    #         Type = 'SingleFamily'
    #         PlanNotAvailable = 0
    #         PlanTypeName = 'Single Family'
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         Bed = div.xpath('.//*[@class="font-sans text-xl leading-none xl:text-3xl"]/text()').get()
    #         print(Bed)
    #
    #         if '-' in Bed:
    #             Bed = Bed.split('-')[-1]
    #             Bedrooms = re.findall(r'(\d+)', Bed)[0]
    #         else:
    #             Bedrooms = re.findall(r'(\d+)', Bed)[0]
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         bath = div.xpath('.//*[@class="font-sans text-xl leading-none xl:text-3xl"]/text()').getall()[1]
    #         if '-' in bath:
    #             bath = bath.split('-')[-1]
    #             tmp = re.findall(r"(\d+)", bath)
    #             if tmp != []:
    #                 Baths = tmp[0]
    #                 if len(tmp) > 1:
    #                     HalfBaths = 1
    #                 else:
    #                     HalfBaths = 0
    #             else:
    #                 Baths = 0
    #                 HalfBaths = 0
    #         else:
    #             tmp = re.findall(r"(\d+)", bath)
    #             if tmp != []:
    #                 Baths = tmp[0]
    #                 if len(tmp) > 1:
    #                     HalfBaths = 1
    #                 else:
    #                     HalfBaths = 0
    #             else:
    #                 Baths = 0
    #                 HalfBaths = 0
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         garage = div.xpath('.//*[@class="font-sans text-xl leading-none xl:text-3xl"]/text()').getall()[2]
    #         Garage = re.findall(r'\d+', garage)[0]
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         Sqft = div.xpath('.//*[@class="font-sans text-xl leading-none xl:text-3xl"]/text()').getall()[3]
    #         if '-' in Sqft:
    #             Sqft = Sqft.split('-')[-1]
    #             Sqft = Sqft.replace(',', '')
    #             BaseSqft = re.findall(r'\d+', Sqft)[0]
    #         else:
    #             Sqft = Sqft.replace(',', '')
    #             BaseSqft = re.findall(r'\d+', Sqft)[0]
    #     except Exception as e:
    #         print(e)
    #
    #     try:
    #         price = div.xpath('.//*[@class="mt-2 font-sans text-xl leading-none text-left sm:text-3xl xl:text-4xl lg:mt-4"]/text()').get()
    #         price = price.replace(',','').replace('$','')
    #         base_price = re.findall(r'\d+', price)[0]
    #     except Exception as e:
    #         print(e)
    #         base_price = 0
    #
    #
    #
    #     try:
    #         Description = ''
    #         ElevationImage = 'https://www.biscaynehomes.com'+ div.xpath('//*[@class="h-48 md:h-88 relative"]/div/child::picture/img/@src').extract_first(default='').strip()
    #         PlanWebsite = response1.url
    #
    #     except Exception as e:
    #         print(e)
    #
    # # ------------------- If Plan Found found ------------------------- #
    #
    #     PlanNumber = int(hashlib.md5(bytes(response.url + PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
    #     SubdivisionNumber = self.builderNumber  # if subdivision is not available
    #     unique = str(PlanNumber) + str(SubdivisionNumber)
    #     unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
    #     item = BdxCrawlingItem_Plan()
    #     item['Type'] = Type
    #     item['PlanNumber'] = PlanNumber
    #     item['unique_number'] = unique_number
    #     item['SubdivisionNumber'] = SubdivisionNumber
    #     item['PlanName'] = PlanName
    #     item['PlanNotAvailable'] = PlanNotAvailable
    #     item['PlanTypeName'] = PlanTypeName
    #     item['BasePrice'] = base_price
    #     item['BaseSqft'] = BaseSqft
    #     item['Baths'] = Baths
    #     item['HalfBaths'] = HalfBaths
    #     item['Bedrooms'] = Bedrooms
    #     item['Garage'] = Garage
    #     item['Description'] = Description
    #     item['ElevationImage'] = ElevationImage
    #     item['PlanWebsite'] = PlanWebsite
    #     yield item



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl biscaynehomes1".split())