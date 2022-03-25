import hashlib
import json
import re

import requests
import scrapy
from scrapy.selector import Selector
from BDX_Crawling.items import BdxCrawlingItem_Builder, BdxCrawlingItem_Corporation, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec, BdxCrawlingItem_subdivision

class HillcrestbuildersSpider(scrapy.Spider):
    name = 'hillcrest'
    allowed_domains = []
    start_urls = ['http://www.hillcrestbuilders.com/communities']
    builderNumber = "32698"

    def parse(self,response):
        url = 'http://www.hillcrestbuilders.com/API/communities.json'

        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.parse1)

    def parse1(self,response):
        data = response.text
        data1 = json.loads(data)
        l_json = len(data1)
        for i in range(0,l_json):
            try:
                # x = data1[i]["com_street1"]

            # if x != None:
                com_status = data1[i]["com_status"]
                if 'Active' in com_status:
                    subdivisonName = data1[i]["com_name"]
                    subdivisonNumber = int(hashlib.md5(bytes(str(subdivisonName) + str(self.builderNumber), "utf8")).hexdigest(), 16) % (10 ** 30)
                    try:
                        Street1 = data1[i]["com_street1"]
                        City = data1[i]["city_name"]
                        State = data1[i]["state_code"]
                        ZIP = data1[i]["com_zip"]
                        phone = str(data1[i]["com_phone"])
                        if '(' in phone:
                            AreaCode = phone.split(')')[0].replace('(','').strip()
                            Prefix = phone.split(')')[-1].split('-')[0].strip()
                            if Prefix == '':
                                Prefix = '526'
                            else:
                                Prefix = Prefix
                            Suffix = phone.split('-')[-1].strip()

                        else:
                            AreaCode = phone.split('-')[0]
                            Prefix = phone.split('-')[1]
                            if Prefix == '':
                                Prefix = '526'
                            else:
                                Prefix = Prefix
                            Suffix = phone.split('-')[-1]


                        Email = data1[i]["com_email"]
                        link = 'http://www.hillcrestbuilders.com' + str(data1[i]["url"]).replace('\\','')
                        try:
                            desc = str(data1[i]["com_description"]).replace("<p class='lead'><strong><strong>","").replace('<strong>','').replace('<\/strong><br \/>','').replace('<\/p>','').replace('<span>','').replace('<\/span>','').replace('<br \/>','').replace('<\/p>','').replace('<p>','').replace('</p>','').replace("<span style='text-decoration: underline;'>","").replace('<strong>','').replace('</span>','').replace('</h2>','').replace("<iframe src='","").replace('</li>','').replace('<li>','').replace('</ul>','').replace('<ul>','').replace("<p class='lead'>","").replace('<h3>','').replace('</h3>','')
                        except:
                            desc = '''Thank you for your interest in Hillcrest Builders and Construction, Inc! We invite you to browse our website to get a first glance at our capabilities. We would love the opportunity to set up a consultation with you to understand the goals for your new home. Let us share with you our outstanding home plans, and a plethora of locations to build (or review a home for your lot).  We will also explain our design, quality and value proposition. I am personally involved with every project and hope to have the opportunity to review with you how we make the process of building clear, simple and exciting.'''
                        img = 'http://www.hillcrestbuilders.com/' + str(data1[i]["imageSource"]).replace('\\','')

                        item = BdxCrawlingItem_subdivision()
                        item['sub_Status'] = "Active"
                        item['SubdivisionNumber'] = subdivisonNumber
                        item['BuilderNumber'] = self.builderNumber
                        item['SubdivisionName'] = subdivisonName
                        item['BuildOnYourLot'] = 0
                        item['OutOfCommunity'] = 1
                        item['Street1'] = Street1
                        item['City'] = City
                        item['State'] = State
                        item['ZIP'] = ZIP
                        item['AreaCode'] = AreaCode
                        item['Prefix'] = Prefix
                        item['Suffix'] = Suffix
                        item['Extension'] = ""
                        item['Email'] = Email
                        item['SubDescription'] = desc
                        item['SubImage'] = img
                        item['SubWebsite'] = link
                        yield item
                    except:
                        print('address not found')

            except:
                print('address not found')

        item1 = BdxCrawlingItem_subdivision()
        item1['sub_Status'] = "Active"
        item1['SubdivisionNumber'] = ''
        item1['BuilderNumber'] = self.builderNumber
        item1['SubdivisionName'] = "No Sub Division"
        item1['BuildOnYourLot'] = 0
        item1['OutOfCommunity'] = 0
        item1['Street1'] = '124 South Swift St'
        item1['City'] = 'Glenbeulah'
        item1['State'] = 'WI'
        item1['ZIP'] = '53023'
        item1['AreaCode'] = '920'
        item1['Prefix'] = '526'
        item1['Suffix'] = '3600'
        item1['Extension'] = ""
        item1['Email'] = 'solvang@hillcrestbuilders.com'
        item1['SubDescription'] = '''Thank you for your interest in Hillcrest Builders and Construction, Inc! We invite you to browse our website to get a first glance at our capabilities. We would love the opportunity to set up a consultation with you to understand the goals for your new home. Let us share with you our outstanding home plans, and a plethora of locations to build (or review a home for your lot).  We will also explain our design, quality and value proposition. I am personally involved with every project and hope to have the opportunity to review with you how we make the process of building clear, simple and exciting.'''
        item1['SubImage'] = 'http://www.hillcrestbuilders.com/images/uploaded/231872182339429_home-cta1.jpg|http://www.hillcrestbuilders.com/images/uploaded/87684105150401_home-cta-2.jpg|http://www.hillcrestbuilders.com/images/uploaded/781225086655467_p1010047.jpg|'
        item1['SubWebsite'] = 'http://www.hillcrestbuilders.com'
        yield item1

        url = 'http://www.hillcrestbuilders.com/planssinglefamily'

        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.plan_link1)

    def plan_link1(self,response):
        url = 'http://www.hillcrestbuilders.com/API/models.json'
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.plan_data1)

    def plan_data1(self,response):
        data = response.text
        data1 = json.loads(data)
        l_json = len(data1)
        for i in range(0,l_json):
            PlanName = data1[i]['mod_name']
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
            SubdivisionNumber = self.builderNumber
            PlanNotAvailable = 0
            PlanTypeName = 'Single Family'
            Type = 'SingleFamily'
            BaseSqft = data1[i]['mod_sqft']
            Bedrooms = data1[i]['mod_beds']
            Baths = data1[i]['mod_baths']
            HalfBaths = data1[i]['mod_halfBaths']
            Garage = data1[i]['mod_garages']
            BasePrice = data1[i]['mod_basePrice']
            URL = 'http://www.hillcrestbuilders.com' + str(data1[i]['url']).replace('\\','')
            try:
                Desc1 = data1[i]['mod_description']
            except:
                Desc1 = ''
            try:
                # Desc2 = data1[i]['features']
                l_d = len(data1[i]['features'])
                des2 = []
                for k in range(0,l_d):
                    desc2 = data1[i]['features'][k]['mfeat_name']
                    des2.append(desc2)
                Desc2 = ''.join(des2)
            except:
                Desc2 = ''

            description = str(Desc1) + ' ' + str(Desc2)
            try:
                l_p = len(data1[i]['photos'])
                image1 = []
                for j in range(1,l_p):
                    img1 = 'http://www.hillcrestbuilders.com/' + str(data1[i]['photos'][j]['imageSource']).replace('\\','')
                    image1.append(img1)
                imgs1 = '|'.join(image1)
            except:
                imgs1= ''
            try:
                l_p2 = len(data1[i]['elevations'])
                image2 = []
                for j in range(1, l_p2):
                    img2 = 'http://www.hillcrestbuilders.com/' + str(data1[i]['elevations'][j]['imageSource']).replace('\\', '')
                    image2.append(img2)
                imgs2 = '|'.join(image2)
            except:
                imgs2 = ''
            try:
                l_p3 = len(data1[i]['floorplans'])
                image3 = []
                for j in range(1, l_p3):
                    img3 = 'http://www.hillcrestbuilders.com/' + str(data1[i]['floorplans'][j]['imageSource']).replace('\\', '')
                    image3.append(img3)
                imgs3 = '|'.join(image3)
            except:
                imgs3 = ''

            ElevationImage = str(imgs1) + '|' + str(imgs2) + '|' +str(imgs3)

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
            item['Description'] = description.replace('<p>','').replace('</p>','').replace('\r\n','').replace("<span style='text-decoration: underline;'>","").replace('<strong>','').replace('</span>','').replace('</h2>','').replace("<iframe src='","").replace('</li>','').replace('<li>','').replace('</ul>','').replace('<ul>','')
            item['ElevationImage'] = ElevationImage
            item['PlanWebsite'] = URL
            yield item

        url = 'http://www.hillcrestbuilders.com/planscondos'
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.plan_link2)

    def plan_link2(self,response):
        url = 'http://www.hillcrestbuilders.com/API/models.json'
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.plan_data2)

    def plan_data2(self,response):
        data = response.text
        data1 = json.loads(data)
        l_json = len(data1)
        for i in range(0, l_json):
            PlanName = data1[i]['mod_name']
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
            SubdivisionNumber = self.builderNumber
            PlanNotAvailable = 0
            PlanTypeName = 'Single Family'
            Type = 'SingleFamily'
            BaseSqft = data1[i]['mod_sqft']
            Bedrooms = data1[i]['mod_beds']
            Baths = data1[i]['mod_baths']
            HalfBaths = data1[i]['mod_halfBaths']
            Garage = data1[i]['mod_garages']
            BasePrice = data1[i]['mod_basePrice']
            URL = 'http://www.hillcrestbuilders.com' + str(data1[i]['url']).replace('\\', '')
            try:
                Desc1 = data1[i]['mod_description']
            except:
                Desc1 = ''
            try:
                # Desc2 = data1[i]['features']
                l_d = len(data1[i]['features'])
                des2 = []
                for k in range(1, l_d):
                    desc2 = data1[i]['features'][k]['mfeat_name']
                    des2.append(desc2)
                Desc2 = ''.join(des2)
            except:
                Desc2 = ''

            description = str(Desc1) + ' ' + str(Desc2)
            try:
                l_p = len(data1[i]['photos'])
                image1 = []
                for j in range(1, l_p):
                    img1 = 'http://www.hillcrestbuilders.com/' + str(data1[i]['photos'][j]['imageSource']).replace('\\',
                                                                                                                   '')
                    image1.append(img1)
                imgs1 = '|'.join(image1)
            except:
                imgs1 = ''
            try:
                l_p2 = len(data1[i]['elevations'])
                image2 = []
                for j in range(1, l_p2):
                    img2 = 'http://www.hillcrestbuilders.com/' + str(data1[i]['elevations'][j]['imageSource']).replace(
                        '\\', '')
                    image2.append(img2)
                imgs2 = '|'.join(image2)
            except:
                imgs2 = ''
            try:
                l_p3 = len(data1[i]['floorplans'])
                image3 = []
                for j in range(1, l_p3):
                    img3 = 'http://www.hillcrestbuilders.com/' + str(data1[i]['floorplans'][j]['imageSource']).replace(
                        '\\', '')
                    image3.append(img3)
                imgs3 = '|'.join(image3)
            except:
                imgs3 = ''

            ElevationImage = str(imgs1) + '|' + str(imgs2) + '|' + str(imgs3)

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
            item['Baths'] = Baths
            item['HalfBaths'] = HalfBaths
            item['Bedrooms'] = Bedrooms
            item['Garage'] = Garage
            item['Description'] = description.replace('<p>','').replace('</p>','').replace('\r\n','').replace("<span style='text-decoration: underline;'>","").replace('<strong>','').replace('</span>','').replace('</h2>','').replace("<iframe src='","").replace('</li>','').replace('<li>','').replace('</ul>','').replace('<ul>','').replace("</strong>9'","").replace('<h2>','').replace('</h2>','').replace('<span>','').strip()
            item['ElevationImage'] = ElevationImage
            item['PlanWebsite'] = URL
            yield item

        unique1 = str("Plan Unknown") + str(self.builderNumber)
        unique_number1 = int(hashlib.md5(bytes(unique1, "utf8")).hexdigest(), 16) % (10 ** 30)
        item1 = BdxCrawlingItem_Plan()
        item1['unique_number'] = unique_number1
        item1['Type'] = "SingleFamily"
        item1['PlanNumber'] = "Plan Unknown"
        item1['SubdivisionNumber'] = self.builderNumber
        item1['PlanName'] = "Plan Unknown"
        item1['PlanNotAvailable'] = 1
        item1['PlanTypeName'] = "Single Family"
        item1['BasePrice'] = 0
        item1['BaseSqft'] = 0
        item1['Baths'] = 0
        item1['HalfBaths'] = 0
        item1['Bedrooms'] = 0
        item1['Garage'] = 0
        item1['Description'] = ""
        item1['ElevationImage'] = ""
        item1['PlanWebsite'] = ""
        yield item1

        url2 = 'http://www.hillcrestbuilders.com/homes'
        yield scrapy.FormRequest(url=url2, dont_filter=True, callback=self.home_link,meta={'PN':unique_number1})

    def home_link(self,response):
        PN = response.meta['PN']
        url = 'http://www.hillcrestbuilders.com/API/homes.json'
        yield scrapy.FormRequest(url=url, dont_filter=True, callback=self.home_data,meta={'PN':PN})

    def home_data(self,response):
        data = response.text
        data1 = json.loads(data)
        l_h = len(data1)
        for i in range(0, l_h):
            status = str(data1[i]["inv_status"])
            if status == 'Active':
                SpecStreet1 = data1[i]["inv_street1"]
                SpecCity = data1[i]["city_name"]
                SpecState = data1[i]["state_code"]
                SpecZIP = data1[i]["inv_zip"]
                if SpecZIP == '':
                    continue
                unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
                # print(unique)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

                f = open("html/%s.html" % SpecNumber, "wb")
                f.write(response.body)
                f.close()

                try:
                    PlanNumber = response.meta['PN']
                except Exception as e:
                    print(e)

                try:
                    SpecCountry = "USA"
                except Exception as e:
                    print(e)

                try:
                    MasterBedLocation = "Down"
                except Exception as e:
                    print(e)
                try:
                    SpecSqft = data1[i]["inv_sqft"]
                except Exception as e:
                    SpecSqft = 0
                try:
                    SpecBaths = data1[i]["inv_baths"]
                except Exception as e:
                    SpecBaths = 0
                try:
                    SpecHalfBaths = data1[i]["inv_halfBaths"]
                except Exception as e:
                    SpecHalfBaths = 0
                try:
                    SpecBedrooms = data1[i]["inv_beds"]
                except Exception as e:
                    SpecBedrooms = e
                try:
                    SpecGarage = data1[i]["inv_garages"]
                except Exception as e:
                    SpecGarage  = 0
                try:
                    SpecPrice = data1[i]["inv_price"]
                except Exception as e:
                    SpecPrice = 0

                try:
                    des1 = data1[i]["inv_description"]
                except:
                    des1 = ''
                try:
                    des2 = data1[i]["inv_description150"]
                except:
                    des2 = ''
                try:
                    des3 = data1[i]["inv_description300"]
                except:
                    des3 = ''
                try:
                    des4 = data1[i]["inv_description600"]
                except:
                    des4 = ''

                Des = str(des1)+str(des2)+str(des3)+str(des4)
                try:
                    IMAGE = len(data1[i]["photos"])
                    images = []
                    for r in range(0,IMAGE):
                        img1 = 'http://www.hillcrestbuilders.com/' + data1[i]["photos"][r]["imageSource"]
                        images.append(img1)
                    spec_image = '|'.join(images)
                except:
                    spec_image = 'http://www.hillcrestbuilders.com/images/uploaded/438911271747201_aa_final_result.jpg'

                SpecWebsite = 'http://www.hillcrestbuilders.com' + str(data1[i]["url"])
                item = BdxCrawlingItem_Spec()
                item['SpecNumber'] = SpecNumber
                item['PlanNumber'] = PlanNumber
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
                item['SpecDescription'] = (Des.replace('<p>','').replace('</p>','').replace('\r\n','').replace('<ul>','').replace('<li>','').replace('</li>','').replace('</ul>','').replace('\xa0','').replace('</h3>','').replace('<h3>','').replace('<span>','').replace('</span>','').replace('<h4>','').replace('</h4>','').replace('<h2>','').replace('</h2>',''))[0:1500]
                item['SpecElevationImage'] = spec_image
                item['SpecWebsite'] = SpecWebsite
                yield item

            else:
                pass
# from scrapy.cmdline import execute
# execute("scrapy crawl hillcrest".split())


