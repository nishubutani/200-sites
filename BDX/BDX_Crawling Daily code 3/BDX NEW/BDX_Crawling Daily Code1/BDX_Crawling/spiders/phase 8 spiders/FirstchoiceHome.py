import hashlib
import re
import scrapy
import json

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class firstSpider(scrapy.Spider):
    name ='firstchoice'
    allowed_domains = []
    start_urls = ['http://www.firstchoicehomebuilders.com']

    builderNumber = 15654

    def parse(self, response):
            url='https://www.firstchoicehomebuilders.com/communities'
            yield scrapy.FormRequest(url=url, callback=self.page, dont_filter=True)

    def page(self,response):

            comn='https://www.firstchoicehomebuilders.com/API/communities.json'
            yield scrapy.FormRequest(url=comn, callback=self.community, dont_filter=True)

    def community(self, response):
        r=response.url
        print(r)
        s=json.loads(response.text)

        for i in range(0,6):
            try:
                SubdivisionName = s[i]['com_name']
                print(SubdivisionName)
            except Exception as e:
                print(e)

            try:
                SubdivisionNumber = int(hashlib.md5(bytes(SubdivisionName, "utf8")).hexdigest(), 16) % (10 ** 30)
                print(SubdivisionNumber)
            except Exception as e:
                print(e)

            try:
                data=''.join(s[i]['com_description'])
                clean = re.compile('<.*?>')
                desc=re.sub(clean, '', data)
                print(desc)
            except:
                desc="NEW HOME COMMUNITIES. First Choice Home Builders offer new homes in Columbia County's top communities located near high ranking schools, each with varying neighborhood amenities and conveniences, styles, designs, and price points. Explore our list of new home communities below."

            link=s[i]['url']
            url= 'https://www.firstchoicehomebuilders.com'+ str(link)

            try:
                street=s[i]['com_street1']
                print(street)
            except:
                print('street not define----------->')
                street=''

            ct=s[i]['city_name']
            sat=s[i]['state_code']
            zp=s[i]['com_zip']
            img=s[i]['photos'][0]['imageSource']
            image='https://www.firstchoicehomebuilders.com/' +img

            area='410'
            prefix='775'
            sufix='0688'


            f = open("html/%s.html" % self.builderNumber, "wb")
            f.write(response.body)
            f.close()


            item = BdxCrawlingItem_subdivision()
            item['sub_Status'] = "Active"
            item['SubdivisionNumber'] = SubdivisionNumber
            item['BuilderNumber'] = self.builderNumber
            item['SubdivisionName'] = SubdivisionName
            item['BuildOnYourLot'] = 0
            item['OutOfCommunity'] = 0
            item['Street1'] = street
            item['City'] = ct
            item['State'] = sat
            item['ZIP'] = zp
            item['AreaCode'] = area
            item['Prefix'] = prefix
            item['Suffix'] = sufix
            item['Extension'] = ""
            item['Email'] = ''
            item['SubDescription'] = desc
            item['SubImage']=image
            item['SubWebsite'] = url
            yield item

            plan_link = 'https://www.firstchoicehomebuilders.com/API/models.json'
            yield scrapy.Request(url=plan_link, callback=self.plan_link_page,meta={'sbdn':SubdivisionNumber,'name':SubdivisionName})

    def plan_link_page(self, response):

        a=json.loads(response.text)
        print(a)
        for i in range(0,73):


            name= a[i]['mod_name']
            url= a[i]['url']
            url='https://www.firstchoicehomebuilders.com' + str(url)
            PlanNumber = int(hashlib.md5(bytes(url, "utf8")).hexdigest(), 16) % (10 ** 30)

            BaseSqft = a[i]['mod_sqft']
            print(BaseSqft)

            try:
                BasePrice = a[i]['mod_basePrice']
            except:
                BasePrice=0.00

            bed= a[i]['mod_beds']

            bath=a[i]['mod_baths']

            garage=a[i]['mod_garages']

            try:
                desc=a[i]['mod_description']
                cleanr = re.compile('<.*?>')
                desc = re.sub(cleanr, '', desc)
                print(desc)
            except:
                desc="First Choice Home Builders offer new homes in Columbia County's top communities located near high ranking schools, each with varying neighborhood amenities and conveniences, styles, designs, and price points. Explore our list of new home communities below."

            halfbath=a[i]['mod_halfBaths']
            try:
                image=a[i]['mod_image']
                img2=a[i]['imageSource']
                pic= image+img2
                images= 'https://www.firstchoicehomebuilders.com/'+'|https://www.firstchoicehomebuilders.com/'.join(pic)
            except:
                images="https://www.firstchoicehomebuilders.com/images/uploaded/46865950338542_010_52927637.jpg"


            SubdivisionNumber = self.builderNumber  # if subdivision is not available
            unique = str(PlanNumber) + str(SubdivisionNumber)
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

            item = BdxCrawlingItem_Plan()
            item['Type'] = 'SingleFamily'
            item['PlanNumber'] = PlanNumber
            item['unique_number'] = unique_number
            item['SubdivisionNumber'] = SubdivisionNumber
            item['PlanName'] = name
            item['PlanNotAvailable'] = 0
            item['PlanTypeName'] = 'Single Family'
            item['BasePrice'] = BasePrice
            item['BaseSqft'] = BasePrice
            item['Baths'] = bath
            item['HalfBaths'] =halfbath
            item['Bedrooms'] = bed
            item['Garage'] = garage
            item['Description'] = desc
            item['ElevationImage'] =images
            item['PlanWebsite'] = url
            yield item

            home_link = 'https://www.firstchoicehomebuilders.com/API/homes.json'
            print('--------------')
            yield scrapy.Request(url=home_link, callback=self.home_link_page,
                                 dont_filter=True)


    def home_link_page(self, response):
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
        item[
            'Description'] = "First Choice Home Builders offer new homes in Columbia County's top communities located near high ranking schools, each with varying neighborhood amenities and conveniences, styles, designs, and price points. Explore our list of new home communities below."
        item[
            'ElevationImage'] = "ttps://www.firstchoicehomebuilders.com/images/uploaded/288460118230432_908_ellis_ln_evans_ga_30809-large-014-66-dining_room-1500x987-72dpi.jpg"
        item['PlanWebsite'] = "https://www.firstchoicehomebuilders.com/plans"
        yield item

        l=json.loads(response.text)
        mainlink = 'https://www.firstchoicehomebuilders.com/API/homes.json'
        for i in range(0,32):
            home_links = 'https://www.firstchoicehomebuilders.com'+ l[i]['url']
            print(home_links)
            yield scrapy.Request(url=mainlink, callback=self.home_details, meta={'PN':item['unique_number'],'homelink':home_links},dont_filter=True)

    def home_details(self, response):
        s = json.loads(response.text)
        print(s)
        for i in range(0,32):
            stu= s[i]['inv_status']

            if stu !='Sold':

                try:
                    SpecStreet1 = s[i]['inv_street1']
                    print(SpecStreet1)

                    SpecCity = s[i]['city_name']
                    print(SpecCity)

                    SpecState = s[i]['state_code']
                    SpecZIP =  s[i]['inv_zip']

                    try:
                        SpecPrice = s[i]['inv_price']

                    except Exception as e:
                        SpecPrice=0.00
                        print(str(e))

                    unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
                    print(unique)
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
                    SpecBedrooms = s[i]['inv_beds']
                except Exception as e:
                    print(str(e))

                try:
                    SpecBaths = s[i]['inv_baths']

                except Exception as e:
                    print(str(e))

                try:
                    halfbath=s[i]['inv_halfBaths']
                except:
                    halfbath=0

                try:
                    SpecGarage =  s[i]['inv_garages']

                except Exception as e:
                    print(str(e))


                SpecSqft =  s[i]['inv_sqft']
                print(SpecSqft)

                try:
                    MasterBedLocation = "Down"
                except Exception as e:
                    print(e)

                try:
                    SpecDes =  s[i]['inv_description']
                    cleanr = re.compile('<.*?>')
                    SpecDescription= re.sub(cleanr, '', SpecDes)
                    print(SpecDescription)
                except Exception as e:
                    SpecDescription="First Choice Home Builders offer new homes in Columbia County's top communities located near high ranking schools, each with varying neighborhood amenities and conveniences, styles, designs, and price points. Explore our list of new home communities below."

                try:
                    # image = s[i]['photos'][i]['imageSource']
                    image=s[i]['inv_image']
                    images= 'https://www.firstchoicehomebuilders.com/'+image
                    ElevationImage = images
                except:
                    ElevationImage="https://www.firstchoicehomebuilders.com/images/uploaded/46865950338542_010_52927637.jpg"


                try:
                    SpecWebsite = response.meta['homelink']
                except Exception as e:
                    print(e)

                # ----------------------- Don't change anything here --------------------- #
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
                item['SpecHalfBaths'] = halfbath
                item['SpecBedrooms'] = SpecBedrooms
                item['MasterBedLocation'] = MasterBedLocation
                item['SpecGarage'] = SpecGarage
                item['SpecDescription'] = SpecDescription
                item['SpecElevationImage'] = ElevationImage
                item['SpecWebsite'] = SpecWebsite
                yield item


# from scrapy.cmdline import execute
# execute("scrapy crawl firstchoice".split())