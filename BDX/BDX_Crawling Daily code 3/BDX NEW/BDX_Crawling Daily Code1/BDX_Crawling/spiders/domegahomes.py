import hashlib
import re
import scrapy
from scrapy.cmdline import execute
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan


class DomegahomesSpider(scrapy.Spider):
    name = 'domegahomes'
    allowed_domains = ['domegahomes.com']
    start_urls = ['http://domegahomes.com/']
    builderNumber = '30554'

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
        item['Street1'] = '952 Peachcrest Drive'
        item['City'] = 'Pueblo'
        item['State'] = 'CO'
        item['ZIP'] = '81005'
        item['AreaCode'] = '719'
        item['Prefix'] = '566'
        item['Suffix'] = '8245'
        item['Extension'] = ""
        item['Email'] = 'sales@domegahomes.com'
        item[
            'SubDescription'] = 'Over 40 years of AWARD WINNING EXPERIENCE Where lifestyle, design, and energy efficiency meet'
        item[
            'SubImage'] = 'https://static.wixstatic.com/media/2cccd9_ae676e4895e94121a278a6f7e5ff9115~mv2_d_3000_1804_s_2.jpg/v1/fill/w_1582,h_951,al_c,q_85,usm_0.66_1.00_0.01/2cccd9_ae676e4895e94121a278a6f7e5ff9115~mv2_d_3000_1804_s_2.jpg|https://static.wixstatic.com/media/2cccd9_7e3982b437d64fd68493388d6308f010~mv2_d_7080_3982_s_4_2.jpg/v1/fill/w_1583,h_890,al_c,q_85,usm_0.66_1.00_0.01/2cccd9_7e3982b437d64fd68493388d6308f010~mv2_d_7080_3982_s_4_2.jpg|https://static.wixstatic.com/media/2cccd9_68c44a25c3d448818218cf4747008813~mv2_d_7680_4320_s_4_2.jpg/v1/fill/w_1583,h_890,al_c,q_85,usm_0.66_1.00_0.01/2cccd9_68c44a25c3d448818218cf4747008813~mv2_d_7680_4320_s_4_2.jpg|https://static.wixstatic.com/media/2cccd9_8a3bf9da6c66466d96aeae2093287c52~mv2_d_7080_3982_s_4_2.jpg/v1/fill/w_1583,h_890,al_c,q_85,usm_0.66_1.00_0.01/2cccd9_8a3bf9da6c66466d96aeae2093287c52~mv2_d_7080_3982_s_4_2.jpg'
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''

        yield item

        planlink ='https://www.domegahomes.com/available'

        yield scrapy.Request(url=planlink, callback=self.plan_list,dont_filter=True)


    def plan_list(self,response):

        links = response.xpath('//*[contains(text(),"Learn More")]/parent::a/@href').getall()
        for link in links:
            print(link)
            # link = "http://domegahomes.com" + str(link)
            yield scrapy.Request(url=link, callback=self.plan_detail, dont_filter=True)

    def plan_detail(self,response):

        try:
            planname = response.xpath('//h3//*[@style="color:#000000;"]/text()').get()
        except:
            planname = ''

        try:
            sqft = response.xpath('//*[@class="font_8"]//*[contains(text(),"Sq. Ft")]/text()').get().replace(',','')
            sqft = re.findall(r'(\d+)',sqft)[0]
        except:
            sqft = 0

        try:
            bedrooms = response.xpath('//*[@class="font_8"]//*[contains(text(),"Bedroom")]/text()').get()
            bedrooms = re.findall(r'(\d+)', bedrooms)[0]
        except:
            bedrooms = 0

        try:
            bath = response.xpath('//*[@class="font_8"]//*[contains(text(),"Bath")]/text()').get()
            bath = re.findall(r'(\d+)', bath)[0]
        except:
            bath = 0

        try:
            garage = response.xpath('//*[@class="font_8"]//*[contains(text(),"Car ")]/text()').get()
            garage = re.findall(r'(\d+)', garage)[0]
        except:
            garage = 0

        try:
            # price = response.xpath('//h2[@class="font_2"]//text()').get().replace(',','')
            price = 0
            # price = re.findall(r'(\d+)', price)[0]
        except:
            price = 0

        try:
            image = "|".join(response.xpath('//div[@class="gallery-item-content image-item gallery-item-visible gallery-item gallery-item-preloaded  load-with-color  "]/picture/source/@srcset').extract())
        except:
            image = ''

        try:
            desc = response.xpath('//p[@class="font_8"]//*[@class="color_11"]//text()').get()
        except:
            desc = ''

        SubdivisionNumber = self.builderNumber  # if subdivision is not available

        PlanNumber = int(hashlib.md5(bytes(planname, "utf8")).hexdigest(), 16) % (10 ** 30)
        f = open("html/%s.html" % PlanNumber, "wb")
        f.write(response.body)
        f.close()
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber
        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = planname
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = price
        item['BaseSqft'] = sqft
        item['Baths'] = bath
        item['HalfBaths'] = 0
        item['Bedrooms'] = bedrooms
        item['Garage'] = garage
        item['Description'] = desc
        item['ElevationImage'] = '|'.join(image)
        item['PlanWebsite'] = response.url
        yield item

if __name__ == '__main__':
    execute("scrapy crawl domegahomes".split())