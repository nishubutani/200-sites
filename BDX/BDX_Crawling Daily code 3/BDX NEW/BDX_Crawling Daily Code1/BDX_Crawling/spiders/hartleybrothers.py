
import hashlib
import json
import re
import scrapy
from scrapy.utils.response import open_in_browser

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan


class HickmanhomesSpider(scrapy.Spider):
    name = 'hartleybrothers'
    allowed_domains = ['hartleybrothers.com']
    start_urls = ['https://www.hartleybrothers.com/']
    builderNumber = '28032'

    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = self.builderNumber
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '1325 NW 53rd Ave, Suite D'
        item['City'] = 'Gainesville'
        item['State'] = 'FL'
        item['ZIP'] = '32609'
        item['AreaCode'] = ''
        item['Prefix'] = ''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = 'Hartley Brothers is founded on integrity, quality, and attention to detail.  We have been building in Gainesville and the surrounding counties for over 40 years.  We have established a long standing reputation for producing quality construction, with pleasing architectural design in a cost effective manner.'
        item['SubImage'] = 'https://static.wixstatic.com/media/4a4bab_3fccbe444aba4f36acaaf18a042a8148~mv2.jpg|https://static.wixstatic.com/media/4a4bab_9994a7ae054f416fbac4b884cb86d8ee~mv2.jpg|https://static.wixstatic.com/media/4a4bab_e8640e120df14db6b3f29bc23f3b435b~mv2.jpg|https://static.wixstatic.com/media/4a4bab_21af216288874957bdb84d48b137999c~mv2.jpg|https://static.wixstatic.com/media/4a4bab_f94d02e2c50b41fbb2881d210b3f27dc~mv2.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        try:
            for i in range(0,19):
                offset = i + 6

                url = "https://www.hartleybrothers.com/_api/cloud-data/v1/wix-data/collections/query"
                payload = "{\"collectionName\":\"Properties\",\"dataQuery\":{\"filter\":{\"$and\":[{\"$and\":[]},{\"$and\":[]},{\"$and\":[]},{\"$and\":[]},{\"$and\":[]},{\"$and\":[]},{\"$and\":[]},{\"$and\":[]},{\"$and\":[]}]},\"sort\":[{\"fieldName\":\"top6\",\"order\":\"DESC\"},{\"fieldName\":\"sqftGroup\",\"order\":\"DESC\"}],\"paging\":{\"offset\":0,\"limit\":" + str(offset) + "}},\"options\":{},\"include\":[],\"segment\":\"LIVE\",\"appId\":\"cf640999-be5c-4181-a6e1-2a5783bcfc6e\"}"

                headers = {
                    'Accept': 'application/json, text/plain, */*',
                    'authorization': 'wixcode-pub.c52e1ae1a74945b2d463b00a70048542d9ca29f9.eyJpbnN0YW5jZUlkIjoiYjk3MTE5MTMtNTgyNC00ODgzLWE2MDEtNTEwMDAzNDZhMmFkIiwiaHRtbFNpdGVJZCI6Ijc1NDUwZmY5LWVjZTktNDU3MS1hMTZlLTlhZjcyZDYyYjE0YiIsInVpZCI6bnVsbCwicGVybWlzc2lvbnMiOm51bGwsImlzVGVtcGxhdGUiOmZhbHNlLCJzaWduRGF0ZSI6MTY0OTU3NTczMjI4MywiYWlkIjoiZmZkYmUzN2UtYTI4MS00YmM0LWEzZDEtNGNiOGI4ZWI5NmE1IiwiYXBwRGVmSWQiOiJDbG91ZFNpdGVFeHRlbnNpb24iLCJpc0FkbWluIjpmYWxzZSwibWV0YVNpdGVJZCI6ImVjMWEwZDEwLWRkOWEtNDdkOS04MWZjLWY3NmIxOGY4YTU1OCIsImNhY2hlIjpudWxsLCJleHBpcmF0aW9uRGF0ZSI6bnVsbCwicHJlbWl1bUFzc2V0cyI6IlNob3dXaXhXaGlsZUxvYWRpbmcsSGFzRG9tYWluLEFkc0ZyZWUiLCJ0ZW5hbnQiOm51bGwsInNpdGVPd25lcklkIjoiNGE0YmFiM2UtYzllNS00MDU1LTgwMWUtZDlhNmNlOGY3NDViIiwiaW5zdGFuY2VUeXBlIjoicHViIiwic2l0ZU1lbWJlcklkIjpudWxsfQ==',
                    'commonConfig': '%7B%22brand%22%3A%22wix%22%2C%22BSI%22%3A%2205f87674-6b16-492f-8ab3-1a8fafb65534%7C3%22%7D',
                    'Content-Type': 'application/json',
                    'Referer': 'https://www.hartleybrothers.com/_partials/wix-thunderbolt/dist/clientWorker.c1969c62.bundle.min.js',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
                    'x-wix-brand': 'wix',
                    'X-Wix-Client-Artifact-Id': 'wix-thunderbolt',
                    'Cookie': 'XSRF-TOKEN=1649505258|JCwfJAcAPRX0'
                }
                yield scrapy.FormRequest(url=url,callback=self.links,dont_filter=True,body=payload,headers=headers,method="POST")
        except:
            pass

    def links(self,response):

        data = json.loads(response.text)
        # total = data['pagingMetadata']['total']

        data_len = data['items']
        data_len = len(data_len)

        for i in range(0,data_len):
            try:
                PlanName = data['items'][i]['title']
            except Exception as e:
                print("PlanName: ", e)

            try:
                Type = 'SingleFamily'
            except Exception as e:
                print(e)

            try:
                PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
            except Exception as e:
                print(e)

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
                Bedroo = data['items'][i]['bedrooms']
                Bedrooms = re.findall(r"(\d+)", Bedroo)[0]
            except Exception as e:
                Bedrooms = 0
                print("Bedrooms: ", e)

            try:
                Bathroo = data['items'][i]['bathrooms']
                tmp = re.findall(r"(\d+)", Bathroo)
                Baths = tmp[0]
                if len(tmp) > 1:
                    HalfBaths = 1
                else:
                    HalfBaths = 0
            except Exception as e:
                Baths,HalfBaths = 0,0
                print("Baths: ", e)


            try:
                Garage = data['items'][i]['agentEmail']
                Garage = re.findall(r"(\d+)", Garage)[0]
                print(Garage)
            except Exception as e:
                print(e)
                Garage = 0

            try:
                BaseSqft = data['items'][i]['sqft']
                # BaseSqft = BaseSqft.split(";")[0]
                BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
            except Exception as e:
                BaseSqft = ""
                print("BaseSQFT: ", e)

            try:
                desc = "".join(response.xpath('//div[@class="et_pb_text_inner"]/p/text()[1]').extract())
            except Exception as e:
                print(e)
                desc =  ''

            try:
                ElevationImages = []
                image  = response.xpath('//span[@class="et_pb_image_wrap "]/img/@src').extract()
                if image != []:
                    for link in image:
                        ElevationImages.append(link)
                ElevationImages = "|".join(ElevationImages)
            except Exception as e:
                print(str(e))

            unique = str(PlanNumber) + str(self.builderNumber)  # < -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
            item = BdxCrawlingItem_Plan()
            item['Type'] = Type
            item['PlanNumber'] = PlanNumber
            item['unique_number'] = unique_number  # < -------- Changes here
            item['SubdivisionNumber'] = self.builderNumber
            item['PlanName'] = PlanName
            item['PlanNotAvailable'] = PlanNotAvailable
            item['PlanTypeName'] = PlanTypeName
            item['BasePrice'] = BasePrice
            item['BaseSqft'] = BaseSqft
            item['Baths'] = Baths
            item['HalfBaths'] = HalfBaths
            item['Bedrooms'] = Bedrooms
            item['Garage'] = Garage
            item['Description'] = desc
            item['ElevationImage'] = ElevationImages
            item['PlanWebsite'] = PlanWebsite
            yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl hartleybrothers".split())