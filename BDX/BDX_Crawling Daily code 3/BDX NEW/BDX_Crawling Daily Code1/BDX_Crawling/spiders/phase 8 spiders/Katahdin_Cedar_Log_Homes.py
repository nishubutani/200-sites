# -*- coding: utf-8 -*-
import hashlib
import json
import re
import requests
import scrapy
from decimal import Decimal
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class KatahdinCedarLogHomesSpider(scrapy.Spider):
    name = 'katahdin_cedar_log_homes'
    allowed_domains = ['https://cedarloghomesofokla.com/']
    start_urls = ['https://cedarloghomesofokla.com/']

    builderNumber = "24298"


    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #
        image2_list = []
        image1 = '|'.join(response.urljoin("https://img1.wsimg.com" + re.findall(r'//img1.wsimg.com(.*?).jpg',i)[0] + ".jpg") for i in
                          response.xpath('//*[@data-ux="Background"]/script/text()').extract())
        res_i = requests.get(url="https://img1.wsimg.com/blobby/go/1d8ea83e-5850-4978-a2e4-8087500ed566/gpub/c013d06d650ecc50/script.js")
        response_i = HtmlResponse(url=res_i.url, body=res_i.content)
        img_links = re.findall(r'{"lightboxUrl":"(.*?).jpg',response_i.text)
        for img in img_links:
            img = re.sub(r'\\u002F','/',img)
            image2_list.append(f"https:{img}.jpg")
        images = f"{image1}|{'|'.join(image2_list)}"
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = ""
        item['City'] = "Checotah"
        item['State'] = "OK"
        item['ZIP'] = "74426"
        item['AreaCode'] = "918"
        item['Prefix'] = "473"
        item['Suffix'] = "7020"
        item['Extension'] = ""
        item['Email'] = "e.davis@cedarloghomesofokla.com"
        item['SubDescription'] = response.xpath('//h4/../div//span/text()').extract_first().strip()
        item['SubImage'] = images
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        try:
            link = "https://cedarloghomesofokla.com" + response.xpath('//a[contains(text(),"Floor Plans")]/@href').extract_first()
            PlanDetails = {}
            yield scrapy.Request(url=link,callback=self.parse_plan,meta={'sbdn':self.builderNumber,'PlanDetails':PlanDetails},dont_filter=True)
        except Exception as e:
            print(e)

    def parse_plan(self,response):
        PN = response.meta['PlanDetails']
        sbdn = response.meta['sbdn']
        link = "https://img1.wsimg.com/blobby/go/1d8ea83e-5850-4978-a2e4-8087500ed566/gpub/3a15dc392f424240/script.js"
        yield scrapy.Request(url=link, callback=self.plans_details, dont_filter=True, meta={"PN": PN,"sbdn": sbdn})

    def plans_details(self, response):
        data = re.findall(r'"galleryImages":(.*?)]',response.text)[0] + "]"
        data1 = json.loads(data)
        plandetails = response.meta['PN']
        data_list = []
        ElevationImages = {}
        elevation_data = []
        list1,name = [],[]
        for index,value in enumerate(data1):
            if 'bath' in value['caption']:
                plans_data = {}
                try:
                    try:
                        Type = 'SingleFamily'
                        plans_data['Type'] = Type
                    except Exception as e:
                        print(e)

                    try:
                        if '~' in value['caption']:
                            PlanName = value['caption'].split('~')[0].strip()
                            if len(PlanName.split()) > 1:
                                PlanName = value['caption'].split()[0].strip()
                        plans_data['PlanName'] = PlanName
                    except:
                        PlanName = ''

                    try:
                        PlanNumber = int(hashlib.md5(bytes(response.url+PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
                        f = open("html/%s.html" % PlanNumber, "wb")
                        f.write(response.body)
                        f.close()
                        plans_data['PlanNumber'] = PlanNumber
                    except Exception as e:
                        print(e)

                    try:
                        PlanNotAvailable = 0
                        plans_data['PlanNotAvailable'] = PlanNotAvailable
                    except Exception as e:
                        print(e)

                    try:
                        PlanTypeName = 'Single Family'
                        plans_data['PlanTypeName'] = PlanTypeName
                    except Exception as e:
                        print(e)

                    try:
                        BasePrice = '0'
                        plans_data['BasePrice'] = BasePrice
                    except Exception as e:
                        print(e)

                    try:
                        Baths = value['caption'].split('~')
                        if (len(Baths)) > 2:
                            Baths = value['caption'].split('~')[2].split('/')[1].strip()
                        else:
                            Baths = value['caption'].split('~')[1].split('/')[1].strip()
                        tmp = re.findall(r"(\d+)", Baths)
                        Baths = tmp[0]
                        if len(tmp) > 1:
                            HalfBaths = 1
                        else:
                            HalfBaths = 0
                        plans_data['Baths'] = Baths
                        plans_data['HalfBaths'] = HalfBaths
                    except Exception as e:
                        print(e)

                    try:
                        Bedrooms = value['caption'].split('~')
                        if (len(Bedrooms)) > 2:
                            Bedrooms = value['caption'].split('~')[2].split('/')[0].strip()
                        else:
                            Bedrooms = value['caption'].split('~')[1].split('/')[0].strip()
                        Bedrooms = re.findall(r"(\d+)", Bedrooms)[0]
                        plans_data['Bedrooms'] = Bedrooms
                    except Exception as e:
                        print(e)

                    try:
                        Garage = '0'
                        plans_data['Garage'] = Garage
                        BaseSqft = value['caption'].split('~')
                        if (len(BaseSqft)) > 2:
                            BaseSqft = value['caption'].split('~')[1].strip().replace(",", "")
                        else:
                            BaseSqft = value['caption'].split('~')[0].strip().replace(",", "")
                        BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
                        plans_data['BaseSqft'] = BaseSqft
                    except Exception as e:
                        print(e)

                    try:
                        Description = "Our customers have told us that log home floor plans and designs are very important in the planning process. Scroll through our standard floor plans below. We suggest that you choose a plan that is close to how you envision YOUR Log Home, print it off and play around with it. Modify it to make it your own. When you are satisfied with your modifications,you can email, mail or fax it to us  for a free price quote including shipping to your land location. If you don't see a plan that is close to what you are looking for, don't worry! We can work with other plans that you may have,or  custom log home floor plans that you have sketched yourself. You can also take a look at our interactive catalog and plan book. There are 30 of our most popular designs inside."
                        plans_data['Description'] = Description
                    except Exception as e:
                        print(e)

                    try:
                        PlanWebsite = "https://cedarloghomesofokla.com/floor-plans"
                        plans_data['PlanWebsite'] = PlanWebsite
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)
                data_list.append(plans_data)

            if '~' in value['caption']:
                plan_name = value['caption'].split('~')[0].strip()
                if len(plan_name.split()) > 1:
                    plan_name = value['caption'].split()[0].strip()
            else:
                plan_name = value['caption'].split()[0]
            if plan_name == PlanName or ';' in plan_name:
                image = "https:" + value['image']['image']
                list1.append(image)
                name.append(plan_name)
            else:
                tmp_plan = plan_name
                image = "https:" + value['image']['image']
                list1.append(image)
                name.append(tmp_plan)
            if name[index] != name[index-1]:
                if ';' not in plan_name and name[index] != name[index-2]:
                    ElevationImages[name[index-1]] = list1[0:-1]
                    list1 = [list1[-1]]
                    elevation_data.append(ElevationImages)
            if len(data1) == index+1:
                ElevationImages[name[index - 1]] = list1
                elevation_data.append(ElevationImages)
        for data_plan in data_list:
            planname1=data_plan['PlanName']
            data_plan['ElevationImage'] = '|'.join(ElevationImages[planname1])
            try:
                # SubdivisionNumber = SubdivisionNumber  # if subdivision is there
                SubdivisionNumber = self.builderNumber #if subdivision is not available
                unique = str(data_plan['PlanNumber']) + str(SubdivisionNumber)
                unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                plandetails[data_plan['PlanName']] = unique_number
                item = BdxCrawlingItem_Plan()
                item['Type'] = data_plan['Type']
                item['PlanNumber'] = data_plan['PlanNumber']
                item['unique_number'] = unique_number
                item['SubdivisionNumber'] = SubdivisionNumber
                item['PlanName'] = data_plan['PlanName']
                item['PlanNotAvailable'] = data_plan['PlanNotAvailable']
                item['PlanTypeName'] = data_plan['PlanTypeName']
                item['BasePrice'] = data_plan['BasePrice']
                item['BaseSqft'] = data_plan['BaseSqft']
                item['Baths'] = data_plan['Baths']
                item['HalfBaths'] = data_plan['HalfBaths']
                item['Bedrooms'] = data_plan['Bedrooms']
                item['Garage'] = data_plan['Garage']
                item['Description'] = data_plan['Description']
                item['ElevationImage'] = data_plan['ElevationImage']
                item['PlanWebsite'] = data_plan['PlanWebsite']
                yield item
            except Exception as e:
                print(e)


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl katahdin_cedar_log_homes".split())