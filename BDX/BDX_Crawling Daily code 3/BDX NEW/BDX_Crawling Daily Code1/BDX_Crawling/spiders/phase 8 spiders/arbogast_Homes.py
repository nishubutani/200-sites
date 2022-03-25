import hashlib
import re
import requests
import scrapy
from scrapy.selector import Selector
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class ArbogastHomesSpider(scrapy.Spider):
    name = 'arbogast_Homes'
    allowed_domains = ['http://www.arbogasthomes.com/']
    start_urls = ['http://www.arbogasthomes.com/']
    builderNumber = 53216

    def parse(self, response):
        f = open("html/%s.html" % self.builderNumber, "wb")
        f.write(response.body)
        f.close()
        try:
            SubImage = response.xpath('//rs-slides/rs-slide//img/@src').getall()
            img_ls = []
            for i in SubImage:
                img = 'http:' + str(i)
                img_ls.append(img)
            image1 = "|".join(img_ls)
        except:
            image1 = 0
        item = BdxCrawlingItem_subdivision()
        item['sub_Status'] = "Active"
        item['SubdivisionNumber'] = ''
        item['BuilderNumber'] = self.builderNumber
        item['SubdivisionName'] = "No Sub Division"
        item['BuildOnYourLot'] = 0
        item['OutOfCommunity'] = 0
        item['Street1'] = '2121 Lohmans Crossing Road, Suite 504-212'
        item['City'] = 'Lakeway'
        item['State'] = 'TX'
        item['ZIP'] = '78734'
        item['AreaCode'] = '512'
        item['Prefix'] = '484'
        item['Suffix'] = '8653'
        item['Extension'] = ""
        item['Email'] = "info@arbogasthomes.com"
        item['SubDescription'] = str(response.xpath('//div[@class="x-text cs-ta-justify"]/p/text()').get())
        item['SubImage'] = image1
        item['SubWebsite'] = response.url
        yield item

        url = 'http://www.arbogasthomes.com/available/'
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.Plans_link)

    def Plans_link(self, response):
        home_links = response.xpath('//a[@class="x-img x-img-link x-img-none"]/@href').getall()
        for i in home_links:
            url = 'http://www.arbogasthomes.com' + str(i)
            yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.Plans)


    def Plans(self,response):
        try:
            PlanName1 = response.xpath('//*[@class="h-custom-headline cs-ta-center h3 accent"]/span/text()[1]').get()
        except:
            PlanName1 = ''
        try:
            PlanName2 = response.xpath('//*[@class="h-custom-headline cs-ta-center h3 accent"]/span/text()[2]').get()
        except:
            PlanName2 = ''
        # try:
        #     PlanName3 = response.xpath('//*[@class="h-custom-headline cs-ta-center h5"]/span/text()').get()
        # except:
        #     PlanName3 = ''
        PlanName = (str(PlanName1) + '' + str(PlanName2) ).replace('None','')
        PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        SubdivisionNumber = self.builderNumber
        PlanNotAvailable = 0
        PlanTypeName = 'Single Family'

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)

        try:
            Price = str(re.findall(r'<span class="x-anchor-text-primary" >(.*?)</span><span class="x-anchor-text-secondary" >Price</span>',response.text)).replace('$','').replace(',','')
            Price1 = re.findall(r"(\d+)", Price)[0]
            BasePrice = Price1
        except Exception as e:
            BasePrice = 0

        try:
            BaseSqft = str(re.findall(r'<span class="x-anchor-text-primary" >(.*?)</span><span class="x-anchor-text-secondary" >Square Feet',response.text)).replace('"','').replace("'","").replace('[','').replace(']','').replace(',','')
        except Exception as e:
            BaseSqft = 0

        try:
            Bedrooms1 = str(re.findall(r'<span class="x-anchor-text-primary" >(.*?)</span><span class="x-anchor-text-secondary" >Bedrooms</span>',response.text))
            Bedrooms = re.findall(r"(\d+)", Bedrooms1)[0]
        except Exception as e:
            print(str(e))
            Bedrooms=0

        try:
            br = str(re.findall(r'<span class="x-anchor-text-primary" >(.*?)</span><span class="x-anchor-text-secondary" >Full Baths</span>',response.text))
            Baths = re.findall(r"(\d+)", br)[0]
        except Exception as e:
            Baths = 0

        try:
            br1 = str(re.findall(r'<span class="x-anchor-text-primary" >(.*?)</span><span class="x-anchor-text-secondary" >Half Baths</span>',response.text))
            HalfBaths = re.findall(r"(\d+)", br1)[0]
        except Exception as e:
            HalfBaths = 0


        try:
            img = response.xpath('//span/img/@src').getall()
            img1 = []
            for a in img:
                if 'http://' in a:
                    img1.append(a)
                else:
                    img = str('http://www.arbogasthomes.com' + str(a)).replace('[','').replace(']','').replace('\\','').replace("'","").replace('"','')
                    img1.append(img)
            img11 = '|'.join(img1)
        except:
            img11 = ''

        try:
            img2 = re.findall(r"<a href='(.*?)'><img class",response.text)
            img22 = []
            for i in img2:
                img21 = str(i).replace("'","").replace('"',"").replace('[','').replace(']','').replace(',','')
                img22.append(img21)
            imgg = '|'.join(img22)
        except:
            imgg = ''

        try:
            ElevationImage = img11 + '|' + imgg
        except:
            ElevationImage = 0

        try:
            SpecDescription = ' '.join(response.xpath('//div[@class="x-column x-sm cs-ta-center x-2-3"]/div//p//text()').getall())[0:1500]
            if SpecDescription == '':
                Description = 0
            else:
                Description = SpecDescription
        except:
            Description = 0

        unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['unique_number'] = unique_number
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = PlanNumber
        item['SubdivisionNumber'] = self.builderNumber
        item['PlanName'] = PlanName
        item['PlanNotAvailable'] = PlanNotAvailable
        item['PlanTypeName'] = PlanTypeName
        item['BasePrice'] = BasePrice
        item['BaseSqft'] = BaseSqft
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = 0
        item['Description'] = Description
        item['ElevationImage'] = ElevationImage
        item['PlanWebsite'] = PlanWebsite
        yield item


# from scrapy.cmdline import execute
# execute("scrapy crawl arbogast_Homes".split())
