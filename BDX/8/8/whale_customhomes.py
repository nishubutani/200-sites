import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class whaleandcustomhomesSpider(scrapy.Spider):
    name = 'whale_customhomes'
    allowed_domains = []
    start_urls = ['https://whalencustomhomes.com/']
    builderNumber = 21844

    def parse(self, response):
        for i in range(1, 6):
            if i == 1:
                subdivisonName = 'Bridlewood'
                subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
                Street1 = 'Bridleridge Crossing Spur'
                City = 'Fenton'
                State = 'MO'
                ZIP = '63049'
                SubImage = "https://whalencustomhomes.com/wp-content/uploads/2018/01/BridlewoodCoverPhoto.jpg"
                SubDescription = 'Nestled in the rolling hills of Southwest St. Louis County, these 49 home sites are situated on a single street with two cul-de-sacs in the highly desirable Rockwood School District. Choose from ridge top sites offering a panoramic vista which can take your breath away or cozier, tree lined perimeter in the valley below, providing privacy to each as the well planned, ample common ground buffers neighboring rear yards. Bridlewood is the ideal location to feature our new floor models which include the sprawling Alsing ranch with nearly 2800 square feet and two 1.5 stories with standard three car garage, the Stevenson with up to 4,185 square feet and the Stratford with 3,200 square feet. The wider, ninety foot frontage will provide a striking street scape with larger separations between homes and we have enhanced our generous features to compliment the brick and stone exteriors to include paver stone driveways, walks and patios as well as built-in irrigation systems to minimize exterior maintenance and preserve the neighborhood’s long term value. Bridlewood is located in Fenton just minutes from I-44 and Rte. 141, a short three mile drive past horse stables and the Golf Club at Paradise Valley beneath a treed canopy reminiscent of a British countryside and you have arrived at your new home! Drive slowly, or you may miss the occasional deer and wild turkey crossing the picturesque entrance.'
                SubWebsite = 'https://whalencustomhomes.com/communities/bridlewood/'

            elif i == 2:
                subdivisonName = 'Alexander Pointe'
                subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
                Street1 = '1515 Flora Del Drive'
                City = 'Fenton'
                State = 'MO'
                ZIP = '63026'
                SubImage = ""
                SubDescription = 'Nestled on a quiet established street in Fenton, MO, Alexander Pointe offers 4 lovely ½ acre custom home building sites in the highly desirable Rockwood School District. Alexander Pointe is located off of Hwy 141 and Hawkins Rd. with easy access to I-44.   These sprawling level lots back to gorgeous mature trees offering both beautiful views and plenty of privacy.  Whalen Custom Homes has hundreds of floor plans for you to consider or we can custom design a plan for you. Do not miss your opportunity to build your dream home in this incredible location.'
                SubWebsite = 'https://whalencustomhomes.com/communities/alexander-pointe/'

            elif i == 3:
                subdivisonName = 'Stone Mill'
                subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
                Street1 = 'Falstone Mill Court'
                City = 'Wildwood'
                State = 'MO'
                ZIP = '63040'
                SubImage = ""
                SubDescription = " "
                SubWebsite = 'https://whalencustomhomes.com/communities/stone-mill/'

            elif i == 4:
                subdivisonName = 'Old Towne Parc'
                subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)
                Street1 = '17026 Manchester Road'
                City = 'Wildwood'
                State = 'MO'
                ZIP = '63040'
                SubImage = ""
                SubDescription = 'Old Towne Parc is the most recent luxury home development by Whalen Custom Homes. If you are considering Wildwood for your new home, Old Towne Parc is a wonderful representation of the quality craftmanship, design, and character Whalen Custom Homes will be bringing to Wildwood with new developments in the near future. Old Towne Parc is located in the City of Wildwood, near the intersection of Highway 109 and Old Manchester Road and located within walking distance of Wildwood Towne Centre, shopping, restaurants, and recreation facilities. Our home plans are designed to meet your specific needs You can choose from one of our many custom plans or we can develop a plan just for you. Either way you will enjoy limitless features and elegant exteriors. Pricing will start in the $500s. If you want to live in the Rockwood School District, with an amazing home site and a distinctive, elegant home design, then please call Mike Whalen at 314-575-7645 to set up your consultation. If you would like any additional information, please send request to mike@whalencustomhomes.com.'
                SubWebsite = 'https://whalencustomhomes.com/communities/old-towne-parc/'

            item2 = BdxCrawlingItem_subdivision()
            item2['sub_Status'] = "Active"
            item2['SubdivisionName'] = subdivisonName
            item2['SubdivisionNumber'] = subdivisonNumber
            item2['BuilderNumber'] = self.builderNumber
            item2['BuildOnYourLot'] = 0
            item2['OutOfCommunity'] = 0
            item2['Street1'] = Street1
            item2['City'] = City
            item2['State'] = State
            item2['ZIP'] = ZIP
            item2['AreaCode'] = ''
            item2['Prefix'] = ''
            item2['Suffix'] = ''
            item2['Extension'] = ""
            item2['Email'] = ""
            item2[
                'SubDescription'] = SubDescription
            item2['SubImage'] = SubImage
            item2['SubWebsite'] = SubWebsite
            yield item2


            specs_link = 'https://whalencustomhomes.com/custom-home-design-gallery/'
            yield scrapy.Request(url=specs_link, callback=self.HomesLink)

    def HomesLink(self, response):
        divs = response.xpath('//div[@class="work-info"]/a/@href').extract()
        # unique = str("Plan Unknown") + str(self.builderNumber)
        # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
        # print(len(divs))
        for link in divs:
            yield scrapy.FormRequest(url=str(link), callback=self.HomeDetail, dont_filter=True)

    def HomeDetail(self, response):
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
        # PN = response.meta['PN']
        try:
            SpecStreet1 = response.xpath('//*[@class="col span_6 section-title no-date"]/div/h1/text()').extract_first()
            print(SpecStreet1)
            # SpecStreet1 = SpecStreet1.replace(",", "")
            SpecCity = response.xpath('//*[@class="col span_6 section-title no-date"]/div/span/text()').extract_first()
            print(SpecCity)
            SpecState = 'MO'
            SpecZIP = "00000"
            # SpecState = SpecCity.split(',')[-1]
            # if SpecState == 'Missouri':
            #     SpecState = 'MO'
            unique = str(SpecStreet1) + str(SpecCity) + str(SpecState) + str(SpecZIP)
            SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % SpecNumber, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
            print(e)

        try:
            PlanNumber = response.meta['PN']
        except Exception as e:
            print(e)

        try:
            SpecCountry = "USA"
        except Exception as e:
            print(e)

        try:
            # SpecPrice = str(response.xpath('normalize-space(//span[@itemprop="price"]//text())').extract_first(
            #     default='0').strip()).replace(",", "")
            # SpecPrice = re.findall(r"(\d+)", SpecPrice)[0]
            SpecPrice = 0
        except Exception as e:
            print(e)

        try:
            # SpecSqft = str(response.xpath(
            #     'normalize-space(//ul[@class="property-meta list-horizontal list-style-disc list-spaced"]//li[@data-label="property-meta-sqft"]//span/text())').extract_first(
            #     default='0').strip()).replace(",", "")
            # SpecSqft = re.findall(r"(\d+)", SpecSqft)[0]
            SpecSqft = 0
        except Exception as e:
            SpecSqft = 0

        try:
            # SpecBaths = str(response.xpath(
            #     'normalize-space(//ul[@class="property-meta list-horizontal list-style-disc list-spaced"]//li[@data-label="property-meta-bath"]//span/text())').extract_first(
            #     default='0').strip()).replace(",", "")
            SpecBaths = 0
            tmp = re.findall(r"(\d+)", SpecBaths)
            SpecBaths = tmp[0]
            if len(tmp) > 1:
                SpecHalfBaths = 1
            else:
                SpecHalfBaths = 0
        except Exception as e:
            SpecBaths = 0
            SpecHalfBaths = 0

        try:
            # SpecBedrooms = str(response.xpath(
            #     'normalize-space(//ul[@class="property-meta list-horizontal list-style-disc list-spaced"]//li[@data-label="property-meta-beds"]//span/text())').extract_first(
            #     default='0').strip()).replace(",", "")
            # SpecBedrooms = re.findall(r"(\d+)", SpecBedrooms)[0]
            SpecBedrooms = 0
        except Exception as e:
            SpecBedrooms = 0

        try:
            MasterBedLocation = "Down"
        except Exception as e:
            print(e)

        try:
            # SpecGarage = response.xpath(
            #     '//div[@class="load-more-features load-more-trigger"]/div[@class="row"]/div[@class
            #     ="col-sm-6"]/ul[@class="list-default"]/li[contains(text(),"Number of Garage Spaces:")]').get()
            SpecGarage = 0
        except Exception as e:
            SpecGarage = 0

        try:
            # SpecDescription = response.xpath('//*[@id="ldp-detail-romance"]//text()').extract()
            # SpecDescription = str(''.join(SpecDescription)).strip()
            # SpecDescription = SpecDescription.replace("\n", "").replace("  ", "")
            SpecDescription = ''
        except Exception as e:
            print(e)

        try:
            SpecElevationImage = '|'.join(response.xpath('//*[@class="envira-gallery-item-inner jg-entry"]/a/@href').extract())
            # ElevationImage = "|".join(ElevationImage)
            # SpecElevationImage = ElevationImage
        except Exception as e:
            print(e)
        # if ElevationImage == "":
        #     try:
        #         ElevationImage = response.xpath(
        #             '//*[@class="modal-body"]/div[@id="ldpPhotoGallery"]/div[@class="photo-item"]//img//@data-src').extract()
        #         ElevationImage = "|".join(ElevationImage)
        #         SpecElevationImage = ElevationImage
        #     except Exception as e:
        #         print(e)

        try:
            SpecWebsite = response.url
        except Exception as e:
            print(e)

            # ----------------------- Don't change anything here ---------------- #
        try:
            item = BdxCrawlingItem_Spec()
            item['SpecNumber'] = SpecNumber
            item['PlanNumber'] = unique_number
            item['SpecStreet1'] = SpecStreet1
            item['SpecCity'] = SpecCity
            item['SpecState'] = SpecState
            item['SpecZIP'] = SpecZIP
            item['SpecCountry'] = SpecCountry
            item['SpecPrice'] = SpecPrice
            item['SpecSqft'] = SpecSqft
            item['SpecBaths'] = SpecBaths
            item['SpecHalfBaths'] = SpecHalfBaths
            item['SpecBedrooms'] = SpecBedrooms
            item['MasterBedLocation'] = MasterBedLocation
            item['SpecGarage'] = SpecGarage
            item['SpecDescription'] = SpecDescription
            item['SpecElevationImage'] = SpecElevationImage
            item['SpecWebsite'] = SpecWebsite
            yield item
        except Exception as e:
            print(e)
    #     # --------------------------------------------------------------------- #


from scrapy.cmdline import execute

# execute("scrapy crawl whale_customhomes".split())