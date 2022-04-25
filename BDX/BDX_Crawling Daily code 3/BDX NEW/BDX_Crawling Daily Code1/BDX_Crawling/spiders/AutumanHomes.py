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

        unique = str("Plan Unknown") + str(self.builderNumber)  # < -------- Changes here
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        item = BdxCrawlingItem_Plan()
        item['unique_number'] = unique_number
        item['Type'] = "SingleFamily"
        item['PlanNumber'] = "Plan Unknown"
        item['SubdivisionNumber'] = self.builderNumber
        item['PlanName'] = "Plan Unknown"
        item['PlanNotAvailable'] = 1
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = 0
        item['BaseSqft'] = 0
        item['Baths'] = 0
        item['HalfBaths'] = 0
        item['Bedrooms'] = 0
        item['Garage'] = 0
        item['Description'] = ""
        item['ElevationImage'] = ""
        item['PlanWebsite'] = ""
        yield item

        home_link = 'https://www.autumnhomesinc.com/current-offerings/'
        yield scrapy.Request(url=home_link, callback=self.spec_links, dont_filter=True,meta={'unique_number':unique_number})

    def spec_links(self,response):
        unique_number1 = response.meta['unique_number']
        divs = response.xpath('//div[@class="elementor-column-wrap elementor-element-populated"]/div[@class="elementor-widget-wrap"]/div/div/h2/a[@target="_blank"]/../../../..')
        for div in divs:
            try:
                address = div.xpath('.//h2/a/text()').extract_first('')
                print(address)
            except Exception as e:
                print(e)
                address = ''

            if address == '417 BAYBERRY - $1,550,000 - 2022 CAVALCADE HOME!':
                SpecStreet1 = '417 Bayberry Ln'
                SpecCity = 'Naperville'
                SpecState = 'IL'
                SpecZIP = '60563'
            elif address == '618 HIGHLAND - $1,375,000':
                SpecStreet1 = '618 Highland Ave'
                SpecCity = 'Naperville'
                SpecState = 'IL'
                SpecZIP = '60540'
            else:
                SpecStreet1 = '235 W Benton Ave'
                SpecCity = 'Naperville'
                SpecState = 'IL'
                SpecZIP = '60540'

            unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
                        10 ** 30)  # < -------- Changes here
            SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

            f = open("html/%s.html" % SpecNumber, "wb")
            f.write(response.body)
            f.close()

            try:
                SpecSqft = div.xpath(".//*[contains(text(),'square feet')]/text()").extract_first('').replace(",","")
                SpecSqft = re.findall(r'(\d+)', SpecSqft)[0]
                print(SpecSqft)
            except:
                SpecSqft=0

            try:
                SpecBedrooms = div.xpath(".//*[contains(text(),'Bedrooms')]/text()").extract_first('')
                if '-' in SpecBedrooms:
                    SpecBedrooms = SpecBedrooms.split("-")[1]
                    SpecBedrooms = re.findall(r'(\d+)', SpecBedrooms)[0]
                else:
                    SpecBedrooms = re.findall(r'(\d+)', SpecBedrooms)[0]

            except Exception as e:
                print(str(e))
                SpecBedrooms = ""

            try:
                SpecBaths = div.xpath(".//*[contains(text(),'Bath')]/text()").extract_first('')
                if '-' in SpecBaths:
                    SpecBaths = SpecBaths.split("-")[1]

                SpecBaths = re.findall(r'(\d+)', SpecBaths)[0]
            except Exception as e:
                print(str(e))
                SpecBaths = ""

            try:
                SpecGarage = div.xpath(".//*[contains(text(),'Car ')]/text()").extract_first('')
                if 'option' in SpecGarage:
                    SpecGarage = re.findall(r'(\d+)', SpecGarage)[1]
                else:
                    if '.' in SpecGarage:
                        SpecGarage = ".".join(re.findall(r'(\d+)', SpecGarage))
                    else:
                        SpecGarage = re.findall(r'(\d+)', SpecGarage)[0]
            except Exception as e:
                SpecGarage=0.0
                print(str(e))

            try:
                price = div.xpath('.//h2/a/text()').extract_first('')
                price = price.split("$")[1]
                price = price.split("-")[0].replace(",","")
                price = re.findall(r'(\d+)', price)[0]
            except Exception as e:
                print(e)
                price = ''


            try:
                image  = div.xpath('.//div[@class="gallery-icon landscape"]/a/@href').extract()
                SpecElevationImage= "|".join(image)
            except Exception as e:
                print(e)
                SpecElevationImage = ''

            try:
                Specdesc = div.xpath('.//div[@class="elementor-widget-container"]//p/text()').extract_first('')
                print(Specdesc)
            except Exception as e:
                print(e)
                Specdesc = ''

            #----------------------- Don't change anything here --------------------- #
            item = BdxCrawlingItem_Spec()
            item['SpecNumber'] = SpecNumber
            item['PlanNumber'] = unique_number1
            item['SpecStreet1'] = SpecStreet1
            item['SpecCity'] = SpecCity
            item['SpecState'] = SpecState
            item['SpecZIP'] = SpecZIP
            item['SpecCountry'] = 'USA'
            item['SpecPrice'] = price
            item['SpecSqft'] = SpecSqft
            item['SpecBaths'] = SpecBaths
            item['SpecHalfBaths'] = 0
            item['SpecBedrooms'] = SpecBedrooms
            item['MasterBedLocation'] = "Down"
            item['SpecGarage'] = SpecGarage
            item['SpecDescription'] = Specdesc
            item['SpecElevationImage'] = SpecElevationImage
            item['SpecWebsite'] = 'https://www.autumnhomesinc.com/current-offerings/'
            yield item

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl autumanhome".split())