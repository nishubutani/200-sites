import hashlib
import re
import scrapy

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class autumnhomeSpider(scrapy.Spider):
    name ='autumanhome'
    allowed_domains = []
    start_urls = ['https://www.autumnhomesinc.com/']

    builderNumber = "52526"

    def parse(self, response):
        # IF you do not have Communities and you are creating the one
        # ------------------- If No communities found ------------------- #

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
        item['Street1'] = '1015 Shimer Court'
        item['City'] = 'Naperville'
        item['State'] = 'IL'
        item['ZIP'] = '60565'
        item['AreaCode'] = '630'
        item['Prefix'] ='983'
        item['Suffix'] = '6220'
        item['Extension'] = ""
        item['Email'] ='Sales@AutumnHomesInc.com'
        item['SubDescription'] = "Autumn Homes, Builders of innovative custom homes, builds on decades of experience to provide our clients with not only the highest quality home, but also a great home building experience. We specialize in forming a partnership with our clients to bring their vision to reality. Our refined process, the diligence of our people and the dedication to our product sets us apart from the rest. Having served Naperville and the surrounding areas we are proud to have completed over 400 custom Homes. Contact Autumn for your next custom home build to see firsthand why our customers have made Autumn Homes their builder of choice."
        item['SubImage']= "https://www.autumnhomesinc.com/wp-content/uploads/2020/01/Slide-1-1.jpg|https://www.autumnhomesinc.com/wp-content/uploads/2020/01/slide-2.jpg|https://www.autumnhomesinc.com/wp-content/uploads/2020/01/slide-3.jpg|https://www.autumnhomesinc.com/wp-content/uploads/2020/01/slide-4.jpg|https://www.autumnhomesinc.com/wp-content/uploads/2020/01/slide-5.jpg"
        item['SubWebsite'] = response.url
        item['AmenityType'] = ''
        yield item

    #     home_link = 'https://www.autumnhomesinc.com/current-offerings/'
    #     yield scrapy.Request(url=home_link, callback=self.spec_links, dont_filter=True)
    #
    # def spec_links(self,response):
    #     links = response.xpath('//div[@class="elementor-widget-container"]/h2/a/@href').extract()[:3]
    #     for link in links:
    #         link = 'https://www.autumnhomesinc.com/current-offerings/' + link
    #         yield scrapy.Request(url=link, callback=self.home_data, dont_filter=True)
    #
    #
    # def home_data(self, response):
    #     unique = str("Plan Unknown") + str(self.builderNumber)  # < -------- Changes here
    #     unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
    #             10 ** 30)  # < -------- Changes here
    #     item = BdxCrawlingItem_Plan()
    #     item['unique_number'] = unique_number
    #     item['Type'] = "SingleFamily"
    #     item['PlanNumber'] = "Plan Unknown"
    #     item['SubdivisionNumber'] = self.builderNumber
    #     item['PlanName'] = "Plan Unknown"
    #     item['PlanNotAvailable'] = 1
    #     item['PlanTypeName'] = 'Single Family'
    #     item['BasePrice'] = 0
    #     item['BaseSqft'] = 0
    #     item['Baths'] = 0
    #     item['HalfBaths'] = 0
    #     item['Bedrooms'] = 0
    #     item['Garage'] = 0
    #     item['Description'] = ""
    #     item['ElevationImage'] = ""
    #     item['PlanWebsite'] = ""
    #     yield item


        # r=response.text
        # div=response.xpath('//div[@class="elementor-row"]//div[@class="elementor-widget-container"]//h2//a/@href').extract()
        # # data=response.xpath('//div[@class="elementor-container elementor-column-gap-default"]//section[@data-element_type="section"]')
        # # print(data)
        #
        # for i in div:
        #
        #     link= 'https://www.autumnhomesinc.com/current-offerings/'+i.xpath('//div[@class="elementor-row"]//div[@class="elementor-widget-wrap"]//h2[@class="elementor-heading-title elementor-size-default"]/a/@href').extract_first()
        #     print(link)
        #
        #     SpecCity='Naperville'
        #     SpecState='IL'
        #     SpecZIP='60540'
        #
        #     specstreet=re.findall('iwloc=near" title="(.*?),',response.text,re.DOTALL)
        #     print(specstreet)
        #     for j in specstreet:
        #         SpecStreet1=j.strip()
        #         if 'Naperville' in SpecStreet1:
        #             SpecStreet1=SpecStreet1.replace(' Naperville','')
        #         unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
        #         print(unique)
        #         SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        #
        #         f = open("html/%s.html" % SpecNumber, "wb")
        #         f.write(response.body)
        #         f.close()
        #
        #     descr=response.xpath('.//div[@role="tabpanel"]//p/text()').extract()
        #     if '\xa0' in descr:
        #         descr=descr.replace('\xa0','')
        #         print(descr)
        #
        #     try:
        #         Sft = re.findall('built to(.*?)square feet',descr)[0].strip()
        #         SpecSqft = ''.join(re.findall(r"(\d+)",Sft, re.DOTALL))
        #         print(SpecSqft)
        #     except:
        #         SpecSqft=0
        #
        #     try:
        #         SpecBedrooms = re.findall('square feet features(.*?)bedrooms',descr)[0].strip()
        #     except Exception as e:
        #         print(str(e))
        #
        #     try:
        #         SpecBaths = re.findall('bedrooms,(.*?)baths',descr)[0].strip()
        #     except Exception as e:
        #         print(str(e))
        #
        #     try:
        #         SpecGarage = re.findall('true(.*?)car garage',descr)[0].strip()
        #
        #     except Exception as e:
        #         SpecGarage=0.0
        #         print(str(e))
        #
        #     # ElevationImage = 'https://www.autumnhomesinc.com/wp-content/uploads' + '|https://www.autumnhomesinc.com/wp-content/uploads'
        #     elv=re.findall("href='https://www.autumnhomesinc.com/wp-content/uploads(.*?)'",response.text,re.DOTALL)
        #     if SpecStreet1=='730 Willow Rd':
        #         ElevationImage= 'https://www.autumnhomesinc.com/wp-content/uploads' + '|https://www.autumnhomesinc.com/wp-content/uploads'.join(elv[0:10])
        #         print(ElevationImage)
        #     elif SpecStreet1=='653 S Sleight St':
        #         ElevationImage = 'https://www.autumnhomesinc.com/wp-content/uploads' + '|https://www.autumnhomesinc.com/wp-content/uploads'.join(elv[10:20])
        #         print(ElevationImage)
        #     elif SpecStreet1 == '812 Wellner Rd':
        #         ElevationImage = 'https://www.autumnhomesinc.com/wp-content/uploads' + '|https://www.autumnhomesinc.com/wp-content/uploads'.join(elv[20:30])
        #         print(ElevationImage)
        #     elif SpecStreet1 == '806 S Julian St':
        #         ElevationImage = 'https://www.autumnhomesinc.com/wp-content/uploads' + '|https://www.autumnhomesinc.com/wp-content/uploads'.join(elv[30:40])
        #         print(ElevationImage)
        #     elif SpecStreet1 == '236 N Laird St':
        #         ElevationImage = 'https://www.autumnhomesinc.com/wp-content/uploads' + '|https://www.autumnhomesinc.com/wp-content/uploads'.join(elv[40:50])
        #         print(ElevationImage)
        #
        #     # ----------------------- Don't change anything here --------------------- #
        #     item = BdxCrawlingItem_Spec()
        #     item['SpecNumber'] = SpecNumber
        #     item['PlanNumber'] = response.meta['PN']
        #     item['SpecStreet1'] = SpecStreet1
        #     item['SpecCity'] = SpecCity
        #     item['SpecState'] = SpecState
        #     item['SpecZIP'] = SpecZIP
        #     item['SpecCountry'] = 'USA'
        #     item['SpecPrice'] = 0.00
        #     item['SpecSqft'] = SpecSqft
        #     item['SpecBaths'] = SpecBaths
        #     item['SpecHalfBaths'] = 0
        #     item['SpecBedrooms'] = SpecBedrooms
        #     item['MasterBedLocation'] = "Down"
        #     item['SpecGarage'] = SpecGarage
        #     item['SpecDescription'] =descr
        #     item['SpecElevationImage'] = ElevationImage
        #     item['SpecWebsite'] = link
        #     yield item

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl autumanhome".split())