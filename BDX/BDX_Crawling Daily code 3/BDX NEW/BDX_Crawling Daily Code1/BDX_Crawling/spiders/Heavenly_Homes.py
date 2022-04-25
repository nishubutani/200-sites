import re

import scrapy
import os
import hashlib
import scrapy
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class HeavenlyHomesSpider(scrapy.Spider):
    name = 'Heavenly_Homes'
    allowed_domains = ['www.heavenly-homes.com']
    start_urls = ['https://heavenly-homes.com/contact-us/']

    builderNumber = "28312"
    count = 0

    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        SubImage = re.findall(r'style="background-image:url(.*?);"></div></div>',response.text)
        # print(SubImage)
        img_ls = []
        for i in SubImage:
            img = str(i).replace("[","").replace("'","").replace("(","").replace(")","").replace("]","")
            img_ls.append(img)
        image1 = "|".join(img_ls)
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '10810 Katy Freeway #205'
        item['City'] = 'Houston'
        item['State'] = 'TX'
        item['ZIP'] = '77043'
        item['AreaCode'] = '281'
        item['Prefix'] = '582'
        item['Suffix'] = '6596'
        item['Extension'] = ""
        item['Email'] = 'info@heavenly-homes.com'
        item['SubDescription'] = '''Heavenly Homes is committed to giving you the opportunity to be a part of building your new home rather than just watching. Whether you have a question about the way something is being done, you would like to have something modified, or you just want to walk the house prior to the next stage of construction, we promise to answer all your questions. After all, shouldn’t you know how your home is being builtHeavenly Homes knows that the complexities of today’s homes are extensive and building to suit all the specific needs of our clients is our top priority. Custom features such as, media rooms, smart homes, safe rooms, wine grottos, and elevators are just a few common features people are requesting in their custom homes today. President of Heavenly Homes, Rory Caton, knows the importance of these custom features and will be assisting you throughout the design, budgeting, and overall construction process. After receiving individual honors in his Construction Science degree, Rory graduated Cum Laude from the College of Architecture at Texas A & M University. Since childhood, he has been fascinated with how and why things work. “I love looking at everything from a small patio to a multi-storied building, analyzing how the form of the structure affects the function, and what could have been done to make it better, whether functionally or aesthetically.” Rory has been blessed with an ability to take geometric shapes and combine them into something that is not only pleasing to the eye, but satisfies the reason for its creation. Now he has taken that natural ability and honed it over time to create wonderful living spaces for every family’s needs here at Heavenly Homes.'''
        item['SubImage'] = image1
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

        url = 'https://heavenly-homes.com/'
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.Plans)
    #
    def Plans(self, response):
        urls = str(response.xpath('//li[@id="menu-item-27"]/a/@href').get())
        # print('PLANS------------------->', urls)
        yield scrapy.FormRequest(url=urls, dont_filter=True, callback=self.Plans_link)

    def Plans_link(self,response):
        links = response.xpath('//h3[@class="snpshpwp_blog_title"]/a/@href').getall()
        for link in links:
            url = str(link)
            yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.Plans_Details)
            # print(url)

    def Plans_Details(self, response):

        Type = 'SingleFamily'

        PlanName = response.xpath('//div[@class="fbuilder_column fbuilder_column-3-4"]/div/div/h1/text()').get().strip()

        PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)

        SubdivisionNumber = self.builderNumber

        PlanNotAvailable = 0

        PlanTypeName = 'Single Family'

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)
        #
        Bedrooms = (response.xpath('//div[@class="frb_text"]/li[2]/text()').get().replace("Bedrooms: ","")).strip()

        a = response.xpath('//div[@class="frb_text"]/li[3]/text()').get().replace("Bathrooms: ","")
        if '/' in a:
            a = a.split('/')
            Baths = (a[0].replace('Full','')).strip()
            HalfBaths = (a[1].replace('Half','').replace('half','')).strip()
        else:
            Baths = a
            HalfBaths = 0

        try:
            Garage = response.xpath('//div[@class="frb_text"]/li[4]/text()').get()
            Garage = re.findall(r"(\d+)", Garage)[0]
            if Garage == "34":
                Garage = "4"
        except:
            Garage = 0

        try:
            BaseSqft = response.xpath('//div[@class="frb_text"]/li[1]/text()').get().replace(',', '').replace('Square Footage:','').replace('Sq. Ft.','').replace('Sq.Ft.','').replace('Sq. ft.','').replace('Sq.ft.','').strip()
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
        except:
            BaseSqft = PlanName.split(' ')[3]

        try:
            # EleImg = str(re.findall(r'<img class="frb_image_flat" src="(.*?)" alt=""',response.text)).replace('"','').replace('[','').replace(']','').replace('(','').replace(')','')
            EleImg = '|'.join(response.xpath('//span[@class="frb_image_inner"]/img/@src').getall()).replace('"','').replace('[','').replace(']','').replace('(','').replace(')','')
            if 'https' in EleImg:
                ElevationImage1 = EleImg.replace('"','').replace('[','').replace(']','').replace('(','').replace(')','').replace("'","")
            else:
                ElevationImage1 = ('https://heavenly-homes.com' + str(EleImg)).replace('"','').replace('[','').replace(']','').replace('(','').replace(')','').replace("'","")
        except Exception as e:
            ElevationImage1 = ''
            print(str(e))

        try:
            ElevationImage2a = response.xpath('//div[@class="frb_media_file_inner"]/a/@href').getall()
            ElevationImage2b = response.xpath('//a[@class="jig-link jig-loaded"]/img/@src').getall()
            if ElevationImage2a != []:
                ElevationImage2 = '|'.join(ElevationImage2a)
            elif ElevationImage2b != []:
                ElevationImage2 = '|'.join(ElevationImage2b)
            else:
                ElevationImage2 = ''
        except Exception as e:
            ElevationImage2 = ''
            print(e)

        try:
            if 'FLOOR PLAN 4493' in PlanName:
                ElevationImage2 = 'https://heavenly-homes.com/wp-content/uploads/2016/08/4493-elevation-1024x684.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/day_backyard-1024x678.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/DSC_9836-1024x684.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/DSC_9716-1024x684.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/DSC_9761-1024x684.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/DSC_9706-1024x684.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/DSC_9702-1024x684.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/DSC_9694-1024x684.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/DSC_9758-1024x684.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/DSC_9722-1024x684.jpg'
            elif 'FLOOR PLAN 4081' in PlanName:
                ElevationImage2 = 'https://heavenly-homes.com/wp-content/uploads/2016/08/1Q7B0024-1024x687.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/1Q7B0023-copy-1024x683.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/1Q7B0026-1024x684.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/1Q7B0029-Edit-1024x685.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/1Q7B0096-1024x688.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/1Q7B0034-686x1024.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/1Q7B0085-1024x684.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/1Q7B0058-1024x683.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/1Q7B0048-1024x683.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/1Q7B0050-1024x683.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/1Q7B0049-1024x683.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/1Q7B0053-1024x683.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/1Q7B0064-1024x692.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/1Q7B0039-1024x683.jpg|https://heavenly-homes.com/wp-content/uploads/2016/08/1Q7B0046-Edit-1024x683.jpg'
            ElevationImage = ElevationImage1 + '|' + ElevationImage2
        except:
            ElevationImage = 0

        BasePrice = 0

        if 'FLOOR PLAN 4081' in PlanName:
            BaseSqft = 4081
            Bedrooms = 4
            Baths = 4
            HalfBaths = 2
            Garage = 4
        elif 'FLOOR PLAN 5616' in PlanName:
            BaseSqft = 5616
        elif 'FLOOR PLAN 11,079' in PlanName:
            BaseSqft = 11079


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
        item['Description'] = ""
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite

        yield item
        #
if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl Heavenly_Homes".split())
