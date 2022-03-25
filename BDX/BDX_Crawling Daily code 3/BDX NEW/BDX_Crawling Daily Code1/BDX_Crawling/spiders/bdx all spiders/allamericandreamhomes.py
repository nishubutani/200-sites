import hashlib
import re

import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan


class AllamericandreamhomesSpider(scrapy.Spider):
    name = 'allamericandreamhomes'
    allowed_domains = ['allamericandreamhomes.com']
    start_urls = ['https://allamericandreamhomes.com/']
    builderNumber = 62665

    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

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
        item['Street1'] = '591 Maple St./BUS41'
        item['City'] = 'Peshtigo'
        item['State'] = 'WI'
        item['ZIP'] = '54157'
        item['AreaCode'] = '888'
        item['Prefix'] = '582'
        item['Suffix'] = '4421'
        item['Extension'] = ""
        item['Email'] = 'kandjvanbeek@allamericandreamhomes.com'
        item['SubDescription'] = response.xpath(
            '//*[@class="span3 "]/p/text()').get().strip()
        item[
            'SubImage'] = '|'.join(
            response.xpath('//*[@class="camera_wrap camera"]/div/@data-src').getall())
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        planlink = 'https://allamericandreamhomes.com/home-plans/'

        yield scrapy.Request(url=planlink,callback=self.planlinks)

    def planlinks(self,response):
        links = response.xpath('//p/a[contains(@href,"home-plans")]/@href').getall()
        for link in links:
            yield scrapy.Request(url=link,callback=self.sublinks,dont_filter=True)

    def sublinks(self,response):
        links = response.xpath('//h2/following-sibling::p/a/@href').getall()
        if not links:
            links = response.xpath('//p/a[contains(@href,"home-plans")]/@href|//div[@class="span8 right right"]//a/@href').getall()
        if links == ['https://allamericandreamhomes.com']:
            yield scrapy.Request(url=response.url, callback=self.links,dont_filter=True)
        else:
            for link in links:
                yield scrapy.Request(url=link, callback=self.links)

    def links(self,response):
        links = response.xpath('//h3[@class="listing-title"]/a/@href').getall()
        for link in links:
            yield scrapy.Request(url=link,callback=self.plandetails,dont_filter=True)

    def plandetails(self,response):

        item = BdxCrawlingItem_Plan()

        planname = response.xpath('//h1[@class="entry-title"]/text()').get()

        try:
            bathroom = response.xpath('//th[contains(text(),"Bathrooms:")]/following-sibling::td/text()').get().strip()
            if '1/2' in bathroom:
                bathroom = bathroom.split()[0]
                halfbath = 1
            elif '3/4' in bathroom:
                bathroom = bathroom.split()[0]
                if '-' in bathroom:
                    bathroom = bathroom.split("-")[0]
                halfbath = 1
            elif '.5' in bathroom:
                bathroom = bathroom.split('.')[0]
                halfbath = 1
            else:
                bathroom = bathroom

                halfbath = 0
        except:
            try:
                bathroom = response.xpath('//*[@class="listing-bathrooms"]/text()').get()
                bathroom = re.findall('(\d+)', bathroom)[0]
                if '1/2' in bathroom:
                    bathroom = bathroom.split()[0]
                    halfbath = 1
                elif '.5' in bathroom:
                    bathroom = bathroom.split('.')[0]
                    halfbath = 1
                else:
                    bathroom = bathroom

                    halfbath = 0

            except:

                bathroom = 0
                halfbath = 0
        try:
            bedrooms = response.xpath('//th[contains(text(),"Bedrooms:")]/following-sibling::td/text()').get().strip()
        except:
            try:
                bedrooms = response.xpath('//*[@class="listing-bedrooms"]/text()').get()
                bedrooms = re.findall('(\d+)', bedrooms)[0]
            except:
                bedrooms = 0

        try:
            garage = response.xpath('//th[contains(text(),"GARAGE:")]/following-sibling::td/text()').get().strip()
        except:

            garage = 0

        try:
            sqft = response.xpath('//th[contains(text(),"Square Feet:")]/following-sibling::td/text()').get().strip().replace(',','')
            sqft = re.findall('(\d+)',sqft)[0]
        except:
            try:
                sqft = response.xpath('//*[@class="listing-sqft"]/text()').get()
                sqft = re.findall('(\d+)', sqft)[0]
            except:

                sqft = 0

        planimage = '|'.join(response.xpath('//*[@id="listing-gallery"]//img/@src').getall())
        if not planimage:
            planimage = '|'.join(response.xpath('//*[@id="listing-image"]//img/@src').getall())
            if not planimage:
                planimage = '|'.join(response.xpath('//*[@class="listing-image-wrap"]//img/@src').getall())

        item['Description'] = ','.join(response.xpath('//div[@id="listing-description"]//ul/li/text()').getall())
        if not item['Description']:
            try:
                item['Description'] = re.findall('property="og:description" content="(.*?)"',response.text)[0].replace('&quot;','').replace('&nbsp;','')
                item['Description'] = re.sub('\s+',' ',item['Description'])
            except:
                item['Description'] = 'All American Dream Homes is a licensed General Contractor in both Wisconsin and Michigan. Our in-house general contracting department specializes in correlating your turn-key project.'

        PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
        f = open("html/%s.html" % PlanNumber, "wb")
        f.write(response.body)
        f.close()

        unique = str(PlanNumber) + str(self.builderNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

        item['PlanName'] = planname
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = self.builderNumber
        item['PlanNotAvailable'] = '0'
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = '0'
        item['Baths'] = bathroom
        item['HalfBaths'] = halfbath
        item['Bedrooms'] = bedrooms
        item['Garage'] = garage
        item['BaseSqft'] = sqft
        item['ElevationImage'] = planimage
        item['PlanWebsite'] = response.url

        yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl allamericandreamhomes".split())
