import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision,BdxCrawlingItem_Plan,BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header

class westwickbuilderSpider(scrapy.Spider):
    name = 'westwick_builder'
    allowed_domains = []
    start_urls = ['http://www.westwickbuilders.com/index.php']

    builderNumber = "21806"

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
        item['Street1'] = '701 North Loop 336 East Conroe'
        item['City'] = 'Texas'
        item['State'] = 'TX'
        item['ZIP'] = '77303'
        item['AreaCode'] = ''
        item['Prefix'] =''
        item['Suffix'] = ''
        item['Extension'] = ""
        item['Email'] =''
        item['SubDescription'] ='Welcome to Westwick Builders, a company you can count on. A family owned and operated business with strong family values, Westwick has built over 1,000 new homes in several communities throughout the Montgomery County area alone, with the utmost quality in each one.Our focus on family extends to our clients as we treat each of you as if you are a member of our family. At Westwick Builders, we not only remove the stress from building a home, we make the process easy and enjoyable.Our modern, innovative floor plans fit any price range, from starter homes on quaint wooded lots to large beautiful lakefront homes. Westwick Homes has the right floor plan for you,and the experience to put it all together.'
        item['SubImage']= ''
        item['SubWebsite'] = response.url
        yield item
        url = 'http://www.westwickbuilders.com/floor_plans.php'
        yield scrapy.Request(url=url, callback=self.Plandetail, meta={'sbdn': self.builderNumber})

    def Plandetail(self,response):
        item = BdxCrawlingItem_Plan()
        # PlanNames = response.xpath('//div[@style="margin-left:20px;"]/table/tbody/tr[2]/td[1]/p/text()').get()
        divs=response.xpath('//*[@style="color:#000;"]')
        for div in divs:
            PlanName = div.xpath('.//td[1]/p/text()').extract_first()
        # for PlanName in PlanNames:
        #     PlanName = PlanName
        #     PlanName = re.sub('<[^<]+?>', '', str(PlanName))

            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % PlanNumber, "wb")
            f.write(response.body)
            f.close()

            Basesqft = div.xpath('.//td[4]/p/text()').extract_first()
        # for Basesqft in Basesqfts:
        #     Basesqft = Basesqft
            Basesqft = Basesqft.replace('sq. ft.', '')
            Basesqft = re.findall(r"(\d+)", Basesqft)[0]

            planbed = div.xpath('.//td[3]/p/text()').extract_first()
        # for planbed in planbeds:
        #     planbed = planbed
            planbeds = planbed.split('/')[0]
            planbeds = planbeds.replace(' bed', '')
            planbeds = re.findall(r"(\d+)", planbeds)[0]

            planbath = div.xpath('.//td[3]/p/text()').extract_first()
        # for planbath in planbaths:
        #     planbath = planbath
            planbath = planbath.split('/')[1]
            planbath = planbath.replace(' bath', '')
            tmp = re.findall(r"(\d+)", planbath)
            planbath = tmp[0]
            if len(tmp) > 1:
                planHalfBaths = 1
            else:
                planHalfBaths = 0


            SubdivisionNumber = response.meta['sbdn']
            PlanImages = response.xpath('//td[@rowspan="2"]/a/img/@src').extract()
            for PlanImage in PlanImages:
                PlanImage = 'http://www.westwickbuilders.com/'+str(PlanImage)
                item['ElevationImage'] = PlanImage

            unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (
                        10 ** 30)  # < -------- Changes here

            item['PlanName'] = PlanName
            item['BaseSqft'] = Basesqft
            item['Type'] = 'SingleFamily'
            item['PlanNumber'] = PlanNumber
            item['unique_number'] = unique_number  # < -------- Changes here
            item['SubdivisionNumber'] = SubdivisionNumber
            item['PlanNotAvailable'] = 0
            item['PlanTypeName'] = 'Single Family'
            item['Baths'] = planbath
            item['HalfBaths'] = planHalfBaths
            item['Bedrooms'] = planbeds
            item['BasePrice'] = 0
            item['Garage'] = 0
            item['Description'] = 'Welcome to Westwick Builders, a company you can count on. A family owned and operated business with strong family values, Westwick has built over 1,000 new homes in several communities throughout the Montgomery County area alone, with the utmost quality in each one.Our focus on family extends to our clients as we treat each of you as if you are a member of our family. At Westwick Builders, we not only remove the stress from building a home, we make the process easy and enjoyable.Our modern, innovative floor plans fit any price range, from starter homes on quaint wooded lots to large beautiful lakefront homes. Westwick Homes has the right floor plan for you,and the experience to put it all together.'
            item['ElevationImage'] = PlanImage
            item['PlanWebsite'] = response.url
            yield item
            url = 'http://www.westwickbuilders.com/find_home.php'
            yield scrapy.FormRequest(url=url,callback=self.homedetail,dont_filter=True,meta={'pn':PlanName})
    #
    def homedetail(self,response):
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
            for i in range(1,29):
                # PlanName = response.meta['pn']
                if i == 1 :
                    Street1 = '4376 County Road 447'
                    City = 'Anderson'
                    State = 'TX'
                    Zip = '77830'
                    Price = '329890'
                    sqft = '2482'
                    bath = '2'
                    HalfBaths = '1'
                    bed = '4'
                    garage = '3'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/24/4376%20CR%20447.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=24'
                    Description = 'Great 2 story home on 10.80 acres. Fireplace, Formal Dining Room, Gameroom, Ceramic Tile throughout, Granite countertops in Kitchen. Downstairs Master Suite has large walk-in closet and Garden Tub in Master Bath. Great floorplan and great views'
                    # unique = str("Plan Unknown")+str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 2 :
                    Street1 = '4318 County Road 447'
                    City = 'Anderson'
                    State = 'TX'
                    Zip = '77830'
                    Price = '289500'
                    sqft = '2050'
                    bath = '2'
                    HalfBaths = '0'
                    bed = '4'
                    garage = '3'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/23/Front.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=23'
                    Description = 'Beautiful home on 10.91 acres. Open living and dining areas. Optional 4th bedroom or study. Fireplace, Tile Flooring throughout, Granite countertops in Kitchen, Very light and bright with lots of windows.'
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 3 :
                    Street1 = '4428 County Road 447'
                    City = 'Anderson'
                    State = 'TX'
                    Zip = '77830'
                    Price = '310000'
                    sqft = '2350'
                    bath = '2'
                    HalfBaths = '0'
                    bed = '3'
                    garage = '3'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/25/Front.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=25'
                    Description = 'Great view from a great home on 10.70 acres. One story has family room with fireplace, formal living and dining, ceramic tile throughout. Large Master suite has sitting room. Master Bath has Whirlpool tub, marble shower surround and double walk in closets. Kitchen has granite countertops and tumbled backsplash. Custom color selections throughout.'
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 4:
                    Street1 = '4506 County Road 447'
                    City = 'Anderson'
                    State = 'TX'
                    Zip = '77830'
                    Price = '305000'
                    sqft = '2134'
                    bath = '2'
                    HalfBaths = '0'
                    bed = '4'
                    garage = '3'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/26/Front.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=26'
                    Description = 'Great 4/2 home with attached side entry garage. Extra large kitchen cabinets and Granite countertops. Very open floor plan includes Formal Dinig Room and Study. Tile throughout. Huge Master Suite with breathtaking views. Master Bath has Garden Tub and Marble Surround Shower.'
                    # unique = str("Plan Unknown") + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 5:
                    Street1 = '5014 County Road 447'
                    City = 'Anderson'
                    State = 'TX'
                    Zip = '77830'
                    Price = '305000'
                    sqft = '2134'
                    bath = '2'
                    HalfBaths = '0'
                    bed = '3'
                    garage = '2'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/27/Front.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=27'
                    Description = 'You will love the views of this beautiful one story home on 11.61 acres. Very open floor plan, Family Room with Fireplace, Formal Dining, Optional 4th bedroor or Study, Master Bath has a Garden Tub, Tile throughout. Kitchen has Granite countertops and a large bay window. 12\' celings and many built-ins'
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 6:
                    Street1 = '5084 County Road 447'
                    City = 'Anderson'
                    State = 'TX'
                    Zip = '77830'
                    Price = '339500'
                    sqft = '2574'
                    bath = '2'
                    HalfBaths = '1'
                    bed = '4'
                    garage = '3'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/28/Front.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=28'
                    Description = 'Beautiful Two Story home on 77.74 acres. 3 bedrooms and gameroom up. Large Master Suite down with Whirlpool Tub in Master Bath. Family Room with fireplace, Formal Dining, Garage is detached, ovresized and has a breezwayl Unfinished studio above Garage. Upgraded Carpet, Light Fixtures, Hardware and large open porch'
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 7:
                    Street1 = '5853 County Road 405'
                    City = 'Navasota'
                    State = 'TX'
                    Zip = '77868'
                    Price = '363900'
                    sqft = '2460'
                    bath = '2'
                    HalfBaths = '0'
                    bed = '4'
                    garage = '3'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/29/5853%20County%20Road%20405.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=29'
                    Description = 'Your dream home sits on 10.67 acres with plenty of porches to look at your fantastic view. This home comes with many amenities. 9\' ceilings throughout, Formal Dining, Tile flooring, Granite Countertops in Kitchen, Marble shower walls in all baths. Additional square footage upstairs that can be finished later.'
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 8:
                    Street1 = '5977 County Road 405'
                    City = 'Navasota'
                    State = 'TX'
                    Zip = '77868'
                    Price = '321750'
                    sqft = '2722'
                    bath = '3'
                    HalfBaths = '0'
                    bed = '4'
                    garage = '3'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/30/Houses%20on%20County%20Road%20405%20004.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=30'
                    Description = '10.67 acres surround this one of a kind, must see home. One story, very open floor plan, stone fireplace in family room, granite countertop in kitchen, tile flooring, marble shower walls. Front and rear covered porches. Second floor has 576 sp ft. of unfinished space for future use. Approx. sq. ft. downstairs is 2273.'
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 9:
                    Street1 = '5997 County Road 405'
                    City = 'Navasota'
                    State = 'TX'
                    Zip = '77868'
                    Price = '414190'
                    sqft = '2810'
                    bath = '2'
                    HalfBaths = '1'
                    bed = '4'
                    garage = '3'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/22/Houses%20on%20County%20Road%20405%20002.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=22'
                    Description = 'Your dream home awaits on 10.67 rolling acres. Beautiful two story home with almost 1000 sq. ft. of porches, a two story stone fireplace in family room with handscraped wood floors. Large country kitchen with island, granite countertops, stainless steel appliances and lots of cabinets. Large master suite with sitting room and designer carpet. Master bath has tile floors, granite countertops, oversized custom tiled shower with two shower heads and grand walk in closet. Many upgrades including oil rubbed bronze light fixtures and hardware. Custom interior paint throughout. Don\'t miss this stunning home !!'
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 10:
                    Street1 = '1010 Arbor Way'
                    City = 'Conroe'
                    State = 'TX'
                    Zip = '77303'
                    Price = '150000'
                    sqft = '1885'
                    bath = '2'
                    HalfBaths = '0'
                    bed = '3'
                    garage = '2'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/43/1010%20Arbor%20Way%20003.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=43'
                    Description = 'Great one story home with very open floor plan. Large family room, formal dining room, breakfast and hearth room. Covered porch in fenced back yard.'
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    # unique = str(PlanNumber)+str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 11 :
                    Street1 = '985 Arbor Crossing'
                    City = 'Conroe'
                    State = 'TX'
                    Zip = '77303'
                    Price = '176000'
                    sqft = '1973'
                    bath = '2'
                    HalfBaths = '0'
                    bed = '3'
                    garage = '2'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/44/985%20Arbor%20Crossing%202.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=44'
                    Description = 'Great one story home located in a cul-de-sac on a quiet street. Great floor plan. Fenced back yard.'
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 12 :
                    Street1 = '991 Arbor Way'
                    City = 'Conroe'
                    State = 'TX'
                    Zip = '77303'
                    Price = '165900'
                    sqft = '2231'
                    bath = '2'
                    HalfBaths = '1'
                    bed = '3'
                    garage = '2'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/8/991%20Arbor%20Way%204.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=8'
                    Description = 'Unique 2 story combining formal dining room, formal living room and family room. Spacious kitchen with cabinets galore, powder bath and oversized utility room on the first floor. Master suite with 2 additional bedrooms upstairs, game room loft that overlooks the family room. All bedrooms have large walk in closets. The master bathroom includes separate tub and shower. Large fenced back yard'
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 13 :
                    Street1 = '991 Arbor Crossing'
                    City = 'Conroe'
                    State = 'TX'
                    Zip = '77303'
                    Price = '204600'
                    sqft = '2712'
                    bath = '2'
                    HalfBaths = '1'
                    bed = '5'
                    garage = '2'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/4/Arbor%20Place%20Model%20-%20991%20Arbor%20001.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=4'
                    Description = 'Unique 2 story combining formal dining room, formal living room and family room. Spacious kitchen with cabinets galore, powder bath and oversized utility room on the first floor. Master suite with 2 additional bedrooms upstairs, game room loft that overlooks the family room. All bedrooms have large walk in closets. The master bathroom includes separate tub and shower. Large fenced back yard'
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 14 :
                    Street1 = '993 Arbor Crossing'
                    City = 'Conroe'
                    State = 'TX'
                    Zip = '77303'
                    Price = '177000'
                    sqft = '2030'
                    bath = '2'
                    HalfBaths = '0'
                    bed = '4'
                    garage = '2'
                    MasterBedLocation = "Down"
                    image = 'westwickbuilders.com/archive/res/9/993%20Arbor%20Crossing%203.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=9'
                    Description = 'One story home with 4 bedrooms, 2 baths, formal dining room, formal living room and a family room with fireplace. Kitchen opens to family room with rear porch deck. Master bedroom has vaulted ceiling and master bath features a separate tub and shower. Treed front and rear yard. Lot size 65\' x 114\'.'
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 15 :
                    Street1 = '983 Arbor Way'
                    City = 'Conroe'
                    State = 'TX'
                    Zip = '77303'
                    Price = '148900'
                    sqft = '1720'
                    bath = '2'
                    HalfBaths = '0'
                    bed = '3'
                    garage = '2'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/10/Front%202.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=10'
                    Description = "One story home with 3 bedrooms, 2 baths and a 2 car attached garage. Very spacious family room, formal dining with decorative openings and high ceilings in the entry, family room and master suite. Home features a split bedroom design and a fully fenced yard. Lot size 50\\\' x 125\\\'"
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 16:
                    Street1 = '9633 Canyon Park Drive'
                    City = 'Willis'
                    State = 'TX'
                    Zip = '77318'
                    Price = '138000'
                    sqft = '1747'
                    bath = '2'
                    HalfBaths = '1'
                    bed = '4'
                    garage = '2'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/33/9633%20Canyon%20Park%202.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=33'
                    Description = "Two story home with extra large family room for entertaining. All bedrooms are up, including master suite with large master bath and walk in closet."
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 17:
                    Street1 = '12565 Canyon Hill Drive'
                    City = 'Willis'
                    State = 'TX'
                    Zip = '77318'
                    Price = '169990'
                    sqft = '2391'
                    bath = '2'
                    HalfBaths = '1'
                    bed = '4'
                    garage = '2'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/13/Front%203.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=13'
                    Description = "A great family home featuring formal dining room, big kitchen with breakfast area and breakfast bar, large family room and master suite downstairs. 3 bedrooms upstairs with loft/game room that over looks the foyer. Fenced back yard with plenty of room for the kids. Great flow to this floor plan."
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 18:
                    Street1 = '12569 Canyon Hill Drive'
                    City = 'Willis'
                    State = 'TX'
                    Zip = '77318'
                    Price = '155990'
                    sqft = '1944'
                    bath = '2'
                    HalfBaths = '0'
                    bed = '3'
                    garage = '2'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/13/Front%203.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=14'
                    Description = 'A great home for entertaining. This 1 story home features an open concept to the formal dining, family room and breakfast area that\\\'s connected to a covered back porch. This home offers a split bedroom design, high ceilings and lots of windows.'
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 19:
                    Street1 = '12552 Canyon Hill Drive'
                    City = 'Willis'
                    State = 'TX'
                    Zip = '77318'
                    Price = '145500'
                    sqft = '1688'
                    bath = '2'
                    HalfBaths = '0'
                    bed = '3'
                    garage = '2'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/31/12552%20CANYON%20HILL.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=31'
                    Description = 'Great one story home with extra large family room. Nice kitchen with breakfast area and formal dining room. Master suite has huge walk in closet.'
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 20:
                    Street1 = '12649 Maggie Lane'
                    City = 'Willis'
                    State = 'TX'
                    Zip = '77318'
                    Price = '330900'
                    sqft = '2722'
                    bath = '3'
                    HalfBaths = '0'
                    bed = '4'
                    garage = '3'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/21/12649%20Maggie%20Lane.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=21'
                    Description = 'Great location. Country setting on 3 acres, close to I-45 and Lake Conroe. One story floor plan with custom features throughout. Very open, spacious kitchen with granite countertops and stainless steel appliances. Upgraded flooring throughout, including tile, wood and carpet. 576 sq. ft. un-finished bonus room and front and rear covered porches. A must see!'
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 21:
                    Street1 = '954 Oak Terrace'
                    City = 'Willis'
                    State = 'TX'
                    Zip = '77378'
                    Price = '145900'
                    sqft = '1854'
                    bath = '2'
                    HalfBaths = '1'
                    bed = '3'
                    garage = '2'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/34/954%20Oak%20Terrace%208.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=34'
                    Description = 'Two story home with large family room. Breakfast area and formal dining room. All bedrooms are upstairs including nice master suite.'
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 22:
                    Street1 = '958 Oak Terrace'
                    City = 'Willis'
                    State = 'TX'
                    Zip = '77378'
                    Price = '153900'
                    sqft = '1807'
                    bath = '2'
                    HalfBaths = '0'
                    bed = '4'
                    garage = '2'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/16/Front.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=16'
                    Description = 'Great house located on a fantastic lot. This home offers 4 bedrooms, spacious family room, large kitchen with tons of cabinets and a great eating space. Volume ceilings, tile floors. Master bath has separate tub and shower with cultured marble walls. Covered front and rear porches. This house has it all!'
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 23:
                    Street1 = '965 Oak Lynn Drive'
                    City = 'Willis'
                    State = 'TX'
                    Zip = '77378'
                    Price = '168900'
                    sqft = '2297'
                    bath = '2'
                    HalfBaths = '1'
                    bed = '4'
                    garage = '2'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/19/Front.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=19'
                    Description = 'This 2 story home has it all. Master suite on the first floor, offers a luxurious master bath suite. Large family room with sloped ceilings and fireplace, formal dining room, great island kitchen with tile counter tops and backsplash. Three bedrooms up with a huge game room. Fantastic curb appeal, fenced and landscaped yard.'
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 24:
                    Street1 = '9647 Cypress Drive'
                    City = 'Willis'
                    State = 'TX'
                    Zip = '77318'
                    Price = '83500'
                    sqft = '1269'
                    bath = '2'
                    HalfBaths = '0'
                    bed = '3'
                    garage = '1'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/37/9647%20Cypress%20-%20Exterior.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=37'
                    Description = 'Great starter home. All appliances included. Complete with all blinds and a fenced back yard.'
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 25:
                    Street1 = '9643 Cypress Drive'
                    City = 'Willis'
                    State = 'TX'
                    Zip = '77318'
                    Price = '89500'
                    sqft = '1361'
                    bath = '2'
                    HalfBaths = '0'
                    bed = '4'
                    garage = '1'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/35/9643%20Cypress%20-%20Exterior.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=35'
                    Description = 'Great starter home. All appliances included. Complete with all blinds and a fenced back yard.'
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 26:
                    Street1 = '211 Boulder Drive'
                    City = 'Navasota'
                    State = 'TX'
                    Zip = '77868'
                    Price = '141900'
                    sqft = '1367'
                    bath = '2'
                    HalfBaths = '0'
                    bed = '3'
                    garage = '2'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/40/Front.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=40'
                    Description = 'Amazing home, priced to sell. Kitchen has natural Maple cabinets, tile flooring in all wet areas. Separate tub and shower in Master bath and cultured marble surrounds.'
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 27:
                    Street1 = '213 Boulder Drive'
                    City = 'Navasota'
                    State = 'TX'
                    Zip = '77868'
                    Price = '143000'
                    sqft = '1456'
                    bath = '2'
                    HalfBaths = '0'
                    bed = '3'
                    garage = '2'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/41/Front.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=41'
                    Description = 'Great floor plan in new planned community. Large family room. Open kitchen with granite countertops.'
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()
                elif i == 28:
                    Street1 = '3512 White Oak Point Drive'
                    City = 'Conroe'
                    State = 'TX'
                    Zip = '77304'
                    Price = '187990'
                    sqft = '2464'
                    bath = '2'
                    HalfBaths = '1'
                    bed = '4'
                    garage = '2'
                    MasterBedLocation = "Down"
                    image = 'http://www.westwickbuilders.com/archive/res/7/Front.jpg'
                    website = 'http://www.westwickbuilders.com/res_property.php?id=7'
                    Description = 'Large family home with spacious kitchen, breakfast area including an eating bar, family room, formal dining room, utility room and 1/2 bath on the first floor. 4 bedrooms up including the master suite and a large game room for the kids. Master suite also has a sitting area for relaxing or a small home office.'
                    # unique = str(PlanNumber) + str(self.builderNumber)
                    # unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    unique = str(Street1) + str(City) + str(State) + str(Zip)
                    SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
                    f = open("html/%s.html" % SpecNumber, "wb")
                    f.write(response.body)
                    f.close()


                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = unique_number
                item['SpecStreet1'] = Street1
                item['SpecCity'] = City
                item['SpecState'] = State
                item['SpecZIP'] = Zip
                item['SpecCountry'] = 'USA'
                item['SpecPrice'] = Price
                item['SpecSqft'] = sqft
                item['SpecBaths'] = bath
                item['SpecHalfBaths'] = HalfBaths
                item['SpecBedrooms'] = bed
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = garage
                item['SpecDescription'] = Description
                item['SpecElevationImage'] = image
                item['SpecWebsite'] = website
                yield item


# execute("scrapy crawl westwick_builder".split())