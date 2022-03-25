import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class HillCountrySpider(scrapy.Spider):
    name = 'hillcountry'
    allowed_domains = []
    start_urls = ['https://www.hillcountryclassics.com/']
    builderNumber = 32680

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
        item['Street1'] = '34535 Interstate 10 W'
        item['City'] = 'Boerne'
        item['State'] = 'TX'
        item['ZIP'] = '78006'
        item['AreaCode'] = '866'
        item['Prefix'] = '924'
        item['Suffix'] = '5888'
        item['Extension'] = ""
        item['Email'] = ''
        item[
            'SubDescription'] = 'Hill Country Classics Custom Homes has a large selection of Texas home floor plans with footprints from 600 to 2,500 square feet. If you have ideas or plans of your own, our staff designer specializes in creating custom homes in the Texas Hill Country and can help you put your ideas on paper. HCC will work to make your ideas function with the most efficient use of space to create a unique living space for you.'
        item[
            'SubImage'] = 'https://www.hillcountryclassics.com/images/galleries/home-top/william-travis-1438-cropped.jpg|https://www.hillcountryclassics.com/images/galleries/home-top/american-flag.jpg|https://www.hillcountryclassics.com/images/galleries/Thurman/AA17-65_Thurman-43_800x533.jpg|https://www.hillcountryclassics.com/images/galleries/home-top/AA_17-61_Powell_13_Edit.jpg|https://www.hillcountryclassics.com/images/galleries/home-top/Squires_8.jpg'
        item['SubWebsite'] = response.url
        yield item
        plan_link = 'https://www.hillcountryclassics.com/plans'
        yield scrapy.FormRequest(url=plan_link, callback=self.planurl, dont_filter=True,
                                 meta={'sbdn': self.builderNumber})

    # def plan_link(self,response):
    #     links = response.xpath('//*[@class="uk-button uk-button-link"]/@href').extract()
    #     for link in links[1:]:
    #         url = 'https://www.hillcountryclassics.com' + str(link)
    #         print(url)
    #         # url = 'https://www.hillcountryclassics.com/plans/the-blanco'
    #         yield scrapy.FormRequest(url=url,callback=self.planurl,dont_filter=True,meta={'sbdn':self.builderNumber})

    def planurl(self, response):
        urls = response.xpath('//*[contains(text(),"Read more")]/@href').extract()
        del urls[17]
        print(urls)
        for ur in urls[1:]:
            url = 'https://www.hillcountryclassics.com' + str(ur)
            # print(url)
            # l = 'https://www.hillcountryclassics.com/plans/the-campwood'
            yield scrapy.FormRequest(url=url, callback=self.plan_detail, dont_filter=True)

    def plan_detail(self, response):
        try:
            PlanName = response.xpath('//*[@class="uk-article "]/h1/text()').extract_first()
            print(PlanName)
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
            Bedroo = response.xpath('//*[contains(text(),"Bed")]/text()').extract_first().strip()
            print(Bedroo)
            Bedroom = Bedroo.split('|')[0]
            Bedrooms = re.findall(r"(\d+)", Bedroom)[0]
            # Bedrooms = Bedroom.split(' Bed')[0].strip()
            print(Bedrooms)
        except Exception as e:
            Bedrooms = 0
            print("Bedrooms: ", e)

        try:
            Bathroo = response.xpath(
                '//*[contains(text(),"Bath")]/text()').extract_first().strip()
            print(Bathroo)
            Baths = Bathroo.split('|')[1]
            tmp = re.findall(r"(\d+)", Baths)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0

        except Exception as e:
            Baths = 0
            print("Baths: ", e)

        Garage = 0
        try:
            BaseSqft = response.xpath(
                '//*[contains(text()," Sq. Ft.")]/text()[4]').extract_first()
            print(BaseSqft)
            if BaseSqft == '--------------------------------':
                BaseSqft = response.xpath('//*[contains(text()," Sq. Ft.")]/text()[5]').extract_first()
            if BaseSqft == None:
                BaseSqft = re.findall(r"<br />Total: (.*?) Sq. Ft.</p>",response.text,re.DOTALL)[0]
            BaseSqft = BaseSqft.replace(',','').strip()
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]

        except Exception as e:
            print("BaseSQFT: ", e)

        try:
            ElevationImages = []
            ElevationImage = response.xpath('//*[@class="tm-article-content uk-margin"]/p[3]/img/@src').extract()
            for ElevationIma in ElevationImage:
                ElevationImag = 'https://www.hillcountryclassics.com' + str(ElevationIma)
                ElevationImages.append(ElevationImag)
            ElevationImages = list(dict.fromkeys(ElevationImages))
            ElevationImages = "|".join(ElevationImages)
            print(ElevationImage)
        except Exception as e:
            print(str(e))

        SubdivisionNumber = self.builderNumber  # if subdivision is not available
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = PlanName
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = BasePrice
        item['BaseSqft'] = BaseSqft
        item['Baths'] = Baths
        item['HalfBaths'] = HalfBaths
        item['Bedrooms'] = Bedrooms
        item['Garage'] = Garage
        item[
            'Description'] = "Hill Country Classics Custom Homes has a large selection of floor plans ranging from as small as 600 square feet, to well over 2,500 square feet. Should you have ideas or plans of your own, our staff designer can help you put your ideas on paper. HCC will work to make your ideas function with the most efficient use of space and design.You can view floor plans for each of our homes by following the links below. Many of the homes also have alternate floor plans featuring custom designs and revisions."
        item['ElevationImage'] = ElevationImages
        item['PlanWebsite'] = response.url
        yield item


if __name__ == '__main__':
    execute("scrapy crawl hillcountry".split())