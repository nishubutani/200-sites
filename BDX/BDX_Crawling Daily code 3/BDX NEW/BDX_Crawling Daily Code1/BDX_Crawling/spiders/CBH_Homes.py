import hashlib
import json
import re

import requests
import scrapy
from scrapy.selector import Selector
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class CbhHomesSpider(scrapy.Spider):
    name = 'CBH_Homes'
    allowed_domains = ['www.cbhhomes.com']
    # start_urls = ['https://cbhhomes.com/wp/wp-admin/admin-ajax.php?action=get_communities&page=1&count=0&types=standard,locale']
    start_urls = ['https://cbhhomes.com/']
    builderNumber = 33284

    def parse(self,response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        SubImage = ['https://cbhhomes.com/content/uploads/2020/09/cbh-homes-goldengrove-monterey-29_WEB.jpg','https://d3oojtlku6hh2y.cloudfront.net/570x380/crop/center/ParagonImages/Property/P10/IMLS/98776839/0/0/0/1d1d09db7cac807632b240fdfd0f7281/6/4ed41f890d3adcfb50a27cef673de133/98776839.JPG','https://cbhhomes.com/content/uploads/2019/08/CBH-Website-Homepage-Community-Photos-Boise-01-Hero.jpg','https://cbhhomes.com/content/uploads/2019/08/CBH-Website-Homepage-Community-Photos-Meridian-01-Hero.jpg','https://cbhhomes.com/content/uploads/2020/01/cbh-homes-woodburn-hermosa-furnished-21.jpg']
        img_ls = []
        for i in SubImage:
            img_ls.append(i)
        image1 = "|".join(img_ls)
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '1977 East Overland Road'
        item['City'] = 'Meridian'
        item['State'] = 'ID'
        item['ZIP'] = '83642'
        item['AreaCode'] = '208'
        item['Prefix'] = '991'
        item['Suffix'] = '4931'
        item['Extension'] = ""
        item['Email'] = 'newhomes@cbhhomes.com'
        item['SubDescription'] = '''The capital city of Idaho is one of the safest, most affordable and fastest-growing cities in the entire nation. The aptly named “City of Trees” is home to countless activities and opportunities that bring people from all over the world to visit and stay. Get ready to explore.CBH Homes is Idaho’s largest new home builder. Founded in 1992 in Boise, Idaho we offer homebuyers the largest selection of new homes in Boise, Nampa, Caldwell, Twin Falls and other areas across southern Idaho. Over 21,000 people live in a CBH home. We are recipients of the acclaimed National Housing Quality Award and are proud to have been named among the Best Places To Work in Idaho for the last nine consecutive years.'''
        item['SubImage'] = image1
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        url = 'https://cbhhomes.com/wp/wp-admin/admin-ajax.php?action=get_floor_plans&page=1&count=0'
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.Plans)

    def Plans(self,response):
        data = response.text
        data1 = json.loads(data)
        x = len(data1["items"])
        print(x)
        for i in range(0,x):
            Type = 'SingleFamily'

            PlanName = str(data1["items"][i]["title"])
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
            SubdivisionNumber = self.builderNumber
            unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            PlanNotAvailable = 0
            PlanTypeName = 'Single Family'

            url = data1["items"][i]["url"]

            image = data1["items"][i]["image"]

            sqft = data1["items"][i]["sqft"]

            Bedrooms = data1["items"][i]["bedrooms"]["max"]

            bathrooms = str(data1["items"][i]["bathrooms"]["max"])
            Bath = re.findall(r"(\d+)", bathrooms)
            Baths = Bath[0]
            tmp = Bath
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0
            try:
                res = requests.get(url=url)
                res2 = Selector(text=res.text)

                PlanWebsite = res.url

                image1 = '|'.join(res2.xpath('//div[@class="info"]/ul/li/strong/a[@data-fancybox="listing-photos"]/@href').getall())
                image2 = '|'.join(res2.xpath('//div[@style="left: 0px; transform: translateX(20%);"]/div/img/@src').getall())
                try:
                    image3 = res2.xpath('//iframe[@id="interactive-floor-plan"]/@src').get()
                except:
                    image3 = '|'.join(res2.xpath('//div[@class="item-wrapper layout"]/div/a/img/@src').getall())
                ElevationImage = str(image) + '|' +str(image1) + '|' + str(image2)+ '|' + str(image3)

                Description = res2.xpath('//section[@class="floor-plan-description"]/p/text()').get()
                # try:
                #     Garage = res2.xpath('//*[@id="top-menu-container"]/div[2]/div[2]/div/div[2]/div/div[4]/div[1]/text()').get()
                # except:
                Garage = 0

                BasePrice = 0

                # unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
                # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
                item = BdxCrawlingItem_Plan()
                item['Type'] = Type
                item['PlanNumber'] = PlanNumber
                item['unique_number'] = unique_number  # < -------- Changes here
                item['SubdivisionNumber'] = SubdivisionNumber
                item['PlanName'] = PlanName
                item['PlanNotAvailable'] = PlanNotAvailable
                item['PlanTypeName'] = PlanTypeName
                item['BasePrice'] = BasePrice
                item['BaseSqft'] = str(sqft)
                item['Baths'] = Baths
                item['HalfBaths'] = HalfBaths
                item['Bedrooms'] = Bedrooms
                item['Garage'] = Garage
                item['Description'] = Description
                item['ElevationImage'] = ElevationImage
                item['PlanWebsite'] = PlanWebsite
                yield item
                # homes_links = res2.xpath('//div[@class="actions"]/a/@href').getall()
                homes_links = re.findall(r'url&quot;:&quot;(.*?)&quot;,&quot;image',res.text)
                # xyz = []
                for hl in homes_links:
                    url1 = hl.replace('[','').replace('"','').replace("'","").replace(']','').replace('\\','')
                    # xyz.append(url1)
                    yield scrapy.FormRequest(url=url1, dont_filter=True, callback=self.Home_Details,meta={'PN': item['unique_number']})
                # abc = ' | '.join(xyz)
                # print(abc)
        #
            except Exception as e:
                print(e)
    def Home_Details(self,response):
        try:

            SpecStreet1 = response.xpath('//div[@class="content"]/div/h1/text()').extract_first().strip()
            add = response.xpath('//div[@class="content"]/div/h1/span/text()').get().strip()
            SpecCity = add.split(',')[0]
            SpecState = add.split(',')[1].split(' ')[1]
            ZIP = add.split(',')[1].split(' ')[-1]
            SpecZIP = ''.join(re.findall(r"(\d+)", ZIP))

            unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
            # print(unique)
            SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

            f = open("html/%s.html" % SpecNumber, "wb")
            f.write(response.body)
            f.close()

        except Exception as e:
            print("Address-------",e)

        try:
            PlanNumber = response.meta['PN']
        except Exception as e:
            print(e)

        try:
            SpecCountry = "USA"
        except Exception as e:
            print(e)

        try:
            SpecPrice = response.xpath('//div[@class="list-price"]/h2/text()').get()
            SpecPrice = SpecPrice.replace('$', '')
            SpecPrice = re.sub(',', '', SpecPrice)
            SpecPrice = SpecPrice.strip()
        except Exception as e:
            print(str(e))

        try:
            SpecBedrooms = response.xpath('//dl[@class="stats"]/div[1]/div[2]/dd/text()').get().strip()
        except Exception as e:
            print(str(e))
            SpecBedrooms=0

        try:
            SpecBath = response.xpath('//dl[@class="stats"]/div[2]/div[2]/dd/text()').get().strip()
            SpecBaths = re.findall(r"(\d+)", SpecBath)
            SpecBaths = SpecBaths[0]
            tmp = SpecBath
            if len(tmp) > 1:
                SpecHalfBaths = 1
            else:
                SpecHalfBaths = 0
            # print(SpecBaths)
        except Exception as e:
            print(str(e))

        try:
            SpecGarage = response.xpath('//dl[@class="stats"]/div[3]/div[2]/dd/text()').get().strip()
            SpecGarage = str(re.findall(r"(\d+)", SpecGarage)).replace("'","").replace('"','').replace('[','').replace(']','')
        except Exception as e:
            print(str(e))
            SpecGarage=0

        try:
            SpecSqft = response.xpath('//dl[@class="stats"]/div[4]/div[2]/dd/text()').get().strip().replace(',','')
        except Exception as e:
            print(str(e))

        try:
            MasterBedLocation = "Down"
        except Exception as e:
            print(e)

        try:
            ElevationImage = '|'.join(response.xpath('//div[@class="links"]/a[@data-fancybox="listing-photos"]/@href').getall())
        except Exception as e:
            print(str(e))
        try:
            Des = response.xpath('//div[@class="home-description"]/p/text()').get()
        except:
            Des = 0
        try:
            SpecWebsite = response.url
        except Exception as e:
            print(e)

        # ----------------------- Don't change anything here --------------------- #
        item = BdxCrawlingItem_Spec()
        item['SpecNumber'] = SpecNumber
        item['PlanNumber'] = PlanNumber
        item['SpecStreet1'] = SpecStreet1
        item['SpecCity'] = SpecCity
        item['SpecState'] = SpecState
        item['SpecZIP'] = SpecZIP
        item['SpecCountry'] = SpecCountry
        item['SpecPrice'] = SpecPrice
        item['SpecSqft'] = SpecSqft
        item['SpecBaths'] = SpecBaths
        item['SpecHalfBaths'] = SpecHalfBaths
        item['SpecBedrooms'] = SpecBedrooms
        item['MasterBedLocation'] = MasterBedLocation
        item['SpecGarage'] = SpecGarage
        item['SpecDescription'] = Des
        item['SpecElevationImage'] = ElevationImage
        item['SpecWebsite'] = SpecWebsite
        yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl CBH_Homes".split())

