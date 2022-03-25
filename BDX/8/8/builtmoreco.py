import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class BuiltmorecoSpider(scrapy.Spider):
    name = 'builtmoreco'
    allowed_domains = []
    start_urls = ['https://biltmoreco.com/']
    builderNumber = 49106

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
        item['Street1'] = '1580 W Cayuse Creek Dr.'
        item['City'] = 'Meridian'
        item['State'] = 'ID'
        item['ZIP'] = '83646'
        item['AreaCode'] = '208'
        item['Prefix'] = '895'
        item['Suffix'] = '0500'
        item['Extension'] = ""
        item['Email'] = ''
        item[
            'SubDescription'] = '“Biltmore…Built Better” isn’t just a slogan. We pride ourselves on the fact that the comment we hear the most from our clients is “I can’t believe I can get all of this in a Biltmore Co. home.” Our company’s combined expertise means that we understand how to integrate your requests of “We’re looking for more space,” “We’re looking to downsize” or “We work from home”. We have built it all! We’re excited to work for you and with you, and we thank you in advance for allowing us to be a part of one of the most exciting decisions you’ll ever make.'
        item[
            'SubImage'] = 'https://biltmoreco.com/files/18-Kitchen-2.jpg|https://biltmoreco.com/files/Entry-Up-Close.jpg|https://biltmoreco.com/files/18-Kitchen-2.jpg'
        item['SubWebsite'] = response.url
        yield item

        link = 'https://biltmoreco.com/floor-plans/'
        yield scrapy.FormRequest(url=link, callback=self.plan_link, dont_filter=True,meta={'sbdn':self.builderNumber})

    def plan_link(self, response):
        plan_links = response.xpath('//*[@class="SearchListingWrapper"]/a/@href').extract()
        print(len(plan_links))
        for plan_link in plan_links:
            plan_lin = 'https://biltmoreco.com' + str(plan_link)
            # a = 'https://biltmoreco.com/floor-plan-details/?id=59'
            yield scrapy.FormRequest(url=plan_lin, callback=self.plandetail, dont_filter=True,meta={'sbdn':self.builderNumber})

    def plandetail(self, response):
        a = ''.join(re.findall(r'<article class="content">(.*?) <div class="tp-bannertimer tp-bottom" style="visibility: hidden !important;"',response.text,re.DOTALL))
        print(response.url)

        try:
            Type = 'SingleFamily'
        except Exception as e:
            Type = 'SingleFamily'
            print(e)

        try:
            PlanName = ''.join(response.xpath('//*[contains(text(),"The")]/text()').get())
            PlanName = re.sub('<[^<]+?>', '', str(PlanName))
            # print(PlanName)
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

        try:
            SubdivisionNumber = self.builderNumber
        except Exception as e:
            print(e)

        try:
            PlanNotAvailable = 0
        except Exception as e:
            print(e)

        try:
            BasePrice = 0.00
        except Exception as e:
            print(e)

        try:
            PlanTypeName = 'Single Family'
        except Exception as e:
            print(e)

        try:
            plansquare = response.xpath('//*[contains(text(),"SqFt")]/../text()').get()
            plansquare = re.sub('<[^<]+?>', '', str(plansquare))
            BaseSqft = plansquare.split(' ')[0].strip().replace(',','')
            # print(BaseSqft)
        except Exception as e:
            print("BaseSqft: ", e)
        try:
            planbeds = response.xpath('//*[contains(text(),"Beds")]/../text()').get()
            planbeds = re.sub('<[^<]+?>', '', str(planbeds))
            # print(planbeds)
            if planbeds == '':
                planbeds = 0
        except Exception as e:
            print("planbeds: ", e)
        try:
            planbath = response.xpath('//*[contains(text(),"Baths")]/../text()').get()
            planbath = re.sub('<[^<]+?>', '', str(planbath))
            tmp = re.findall(r"(\d+)", planbath)
            planbath = tmp[0]
            print(planbath)
            if len(tmp) > 1:
                planHalfBaths = 1
                print(planHalfBaths)
            else:
                planHalfBaths = 0
                print(planHalfBaths)
            # print(planbath)
        except Exception as e:
            print("planbath: ", e)
        try:
            cargarage = response.xpath('//*[contains(text(),"Garages")]/../text()').get()
            cargarage = re.sub('<[^<]+?>', '', str(cargarage))
            if 'RV' in cargarage:
                cargarage = response.xpath('//div[@class="tabcontent"]/div/p/text()[3]').get()
            elif '+' in cargarage:
                cargarage = cargarage.replace('+','')
            cargarage = re.findall(r"(\d+)",cargarage)[0]
            # print(cargarage)
        except Exception as e:
            print("cargarage: ", e)
        try:
            Description = "".join(re.findall(r"<p>(.*?)</p>",response.text)).strip().replace('&nbsp;','')
            # if Description == '':
            #     Description = re.findall(r"<br />(.*?)</p>",re.DOTALL)
            if Description == '':
                Description = ''.join(response.xpath('//div[@class="tabcontent"]/div/p/text()[6]').extract()).strip().replace('&nbsp;','')
            print(Description)
        except Exception as e:
            Description = ' '
            print('Description:',e)
        try:
            PlanImage = []
            PlanImages = re.findall(r'<img src="(.*?)" alt=""', a, re.DOTALL)
            for PlanImag in PlanImages:
                PlanImage1 = 'https://biltmoreco.com'+ str(PlanImag)
                print(PlanImage1)
                PlanImage.append(PlanImage1)
            PlanImage = '|'.join(PlanImage)
            print(PlanImage)
        except Exception as e:
            print("SpecElevationImage: ", e)
        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)
        try:
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
            item['Baths'] = planbath
            # print(item['Baths'])
            item['HalfBaths'] = planHalfBaths
            # print(item['HalfBaths'])
            item['Bedrooms'] = planbeds
            item['Garage'] = cargarage
            item['Description'] = Description
            item['ElevationImage'] = PlanImage
            item['PlanWebsite'] = PlanWebsite
            print(item)
            yield item
        except Exception as e:
            print(e)

if __name__ == '__main__':
  execute("scrapy crawl builtmoreco".split())
