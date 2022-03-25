import hashlib
import re
import scrapy
import json

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class Everviewhome(scrapy.Spider):
    name ='everviewhome'
    allowed_domains = []
    start_urls = []

    builderNumber = 53411

    def start_requests(self):
        # url='https://www.everviewhomes.com/communities'
        link='https://www.powr.io/wix/map/public.json?instance=-cpo2HsitBN1tAk1tiznl3mYf4TGg5o1DubEJZVOOCI.eyJpbnN0YW5jZUlkIjoiOTY1Mzk4NzAtMmFlOC00MDQ2LWEyMmMtOTQyNTYzYTQ2YzYzIiwiYXBwRGVmSWQiOiIxMzQwYzVlZC1hYWM1LTIzZWYtNjkzYy1lZDIyMTY1Y2ZkODQiLCJzaWduRGF0ZSI6IjIwMjAtMDktMjlUMDk6MTE6MTcuNDIxWiIsInZlbmRvclByb2R1Y3RJZCI6ImJ1c2luZXNzIiwiZGVtb01vZGUiOmZhbHNlLCJhaWQiOiI0OTg0YzAyNS1mYzBiLTRkNGQtYmY0Mi0zYjI3NGY2NGNjZmYiLCJzaXRlT3duZXJJZCI6IjUxZWFkZjY1LTVjYjAtNGJlMy05NGU5LWViMjM0MGM5M2ZlMyJ9&pageId=fxziq&compId=comp-k6cti52m&viewerCompId=comp-k6cti52m&siteRevision=938&viewMode=site&deviceType=desktop&locale=en&commonConfig=%7B%22brand%22%3A%22wix%22%2C%22bsi%22%3A%2218bb456e-6810-4c3c-a238-b1c274f8ffb6%7C1%22%2C%22consentPolicy%22%3A%7B%22essential%22%3Atrue%2C%22functional%22%3Atrue%2C%22analytics%22%3Atrue%2C%22advertising%22%3Atrue%2C%22dataToThirdParty%22%3Atrue%7D%2C%22consentPolicyHeader%22%3A%7B%7D%7D&tz=America%2FChicago&vsi=32c419e9-c79a-4b87-905c-766bc2169bcf&currency=USD&currentCurrency=USD&width=1810&height=842&url=https://www.everviewhomes.com/communities'
        yield scrapy.Request(url=link, callback=self.parse, dont_filter=True)

    def parse(self, response):
       a=response.text
       for i in range(0,10):
            try:

                SubdivisionName=re.findall('"name":"(.*?)"',a)[i]
                print(SubdivisionName)
            except Exception as e:
                print(e)

            try:
                SubdivisionNumber = int(hashlib.md5(bytes(SubdivisionName, "utf8")).hexdigest(), 16) % (10 ** 30)
            except Exception as e:
                print(e)


            url = "https://www.everviewhomes.com/communities"

            try:
                street = re.findall('"address":"(.*?)"',a)[i]

                print(street)
            except:
                street = ''

            try:
                cty = street.split(',')
                street=cty[0]
                ct=cty[1].strip()
            except:
                ct=''

            try:
                sat = cty[2].strip()
                stu=sat.split(' ')
                sat=stu[0]
            except:
                sat=''


            if SubdivisionName=='Mountain Springs Ranch':
                zp='78133'
                street='1929 Split Mountai'
            elif SubdivisionName=='Katy Way':
                zp='78220'
            elif SubdivisionName=="Rockin' J Ranch":
                zp='78606'
            elif SubdivisionName=='Horseshoe Bay':
                zp='78657'
            elif SubdivisionName=='Cascada at Canyon Lake':
                zp='78070'
            elif SubdivisionName=='Tivoli Hills':
                zp='78260'
            elif SubdivisionName=='Comanche Ridge':
                street=''
                zp=None
            elif SubdivisionName=='Selma Park Estates':
                street=''
                zp = None
            elif SubdivisionName=='Mystic Shores':
                street=''
                zp = None
            else:
                zp='00000'

            img = 'https://static.wixstatic.com/media/3e48e4_df424ad75ade486fbd3012e31db3738f~mv2.jpg/v1/fill/w_144,h_96,al_c,q_80,usm_0.66_1.00_0.01/3e48e4_df424ad75ade486fbd3012e31db3738f~mv2.jpg'

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
            item['AreaCode'] = '210'
            item['Prefix'] = '496'
            item['Suffix'] = '7555'
            item['Extension'] = ""
            item['Email'] = ''
            item['SubDescription'] = "We would love to provide you more information about our beautiful homes and how we can properly serve you and your family’s needs for your new home. Learn more about Everview homes, our communities, ‘Build On Your Lot’ custom homes, and future developments in San Antonio, New Braunfels, Bulverde, Schertz, Selma, and surrounding areas."
            item['SubImage'] = img
            item['SubWebsite'] = url
            yield item

       link = ['https://www.everviewhomes.com/production-homes','https://www.everviewhomes.com/semi-custom-homes','https://www.everviewhomes.com/custom-home-floorplans']
       for i in link:
            link=i
            print(link)
            yield scrapy.Request(url=link, callback=self.plan_link,dont_filter=True)


    def plan_link(self,response):
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
        item['Street1'] = '18410 US Hwy 281 N #109'
        item['City'] = 'San Antonio'
        item['State'] = 'TX'
        item['ZIP'] = '78259'
        item['AreaCode'] = '210'
        item['Prefix'] = '496'
        item['Suffix'] = '7555'
        item['Extension'] = ""
        item['Email'] = ''
        item['SubDescription'] = "We build new homes in great communities, as well as semi-custom homes and custom homes on your land or ours.One of them is the perfect home for you and your family ... Explore"
        item['SubImage'] = "https://static.wixstatic.com/media/3e48e4_df424ad75ade486fbd3012e31db3738f~mv2.jpg/v1/fill/w_144,h_96,al_c,q_80,usm_0.66_1.00_0.01/3e48e4_df424ad75ade486fbd3012e31db3738f~mv2.jpg"
        item['SubWebsite'] = 'https://www.everviewhomes.com/communities'
        yield item

        div=response.xpath('//div[@role="gridcell"]')
        for k in div:
            plink=k.xpath('.//a/@href').extract_first()
            image=k.xpath('.//img/@src').extract_first()
            name=k.xpath('.//div//h4//text()').extract_first()
            try:
                if 'SF' in name:
                    if response.url=='https://www.everviewhomes.com/cranesmill-custom-floorplan':
                        print('---')
                    sqft = re.findall('(.*?)SF', name)[0].strip()
                    sqft = ''.join(re.findall(r"(\d+)", sqft, re.DOTALL))
                    print(sqft)
                else:
                    sq=name.split(' ')
                    sqft=sq[0]
            except:
                sqft=0

            yield scrapy.Request(url=plink, callback=self.plan_data,dont_filter=True,meta={'plink':plink,'image':image,'name':name,'sqft':sqft})

    def plan_data(self,response):

            data=response.xpath('//p[@class="font_7"]//text()').extract()

            dt=''.join(data)
            try:
                if 'Garage' in dt:
                    gr=re.findall('Bath(.*?)Car',dt)[0]
                    grg=''.join(re.findall(r"(\d+)", gr, re.DOTALL))
                    garage=grg+ '.0'
                else:
                    garage=0.0
            except:
                garage=0.0

            info=data[:2]
            PlanName = response.meta['name']


            try:

                dts=''.join(data[1])

                if '|' in dts:
                    b = dts.split('|')
                    be=b[0]
                    bed = ''.join(re.findall(r"(\d+)", be, re.DOTALL))
                    bth=b[1]
                    if '.' in bth:
                        bth=bth.split('.')
                        baths=bth[0].strip()
                        halfbath=1
                    else:
                        baths = ''.join(re.findall(r"(\d+)", bth, re.DOTALL)).strip()
                        halfbath=0

                else :
                    if ',' in dts:
                        b=dts.split(',')
                        be=b[0]
                        bed = ''.join(re.findall(r"(\d+)", be, re.DOTALL))
                        bth=b[1]
                        if '.' in bth:
                            bth = bth.split('.')
                            baths = bth[0]
                            halfbath = 1
                        else:
                            baths = ''.join(re.findall(r"(\d+)", bth, re.DOTALL))
                            halfbath = 0

            except:
                dts2= ''.join(data[4])
                dts3=''.join(data[3])
                if 'BD' in dts3:
                    print(dts3)
                    if '|' in dts2 or dts3:
                        b = dts2.split('|')
                        be = b[0]
                        bed = ''.join(re.findall(r"(\d+)", be, re.DOTALL))
                        bth=b[1]
                        if '.' in bth:
                            bth=bth.split('.')
                            baths=bth[0]
                            halfbath=1
                        else:
                            baths = ''.join(re.findall(r"(\d+)", bth, re.DOTALL))
                            halfbath=0

                else:
                    try:
                        if ',' in dts2:
                            b= dts2.split(',')
                            be = b[0]
                            bed = ''.join(re.findall(r"(\d+)", be, re.DOTALL))
                            bth = b[1]
                            if '.' in bth:
                                bth = bth.split('.')
                                baths = bth[0]
                                halfbath = 1
                            else:
                                baths = ''.join(re.findall(r"(\d+)", bth, re.DOTALL))
                                halfbath = 0
                    except:
                        dts2=''.join(data[4])
                        print(dts2)


            try:
                PlanNumber = int(hashlib.md5(bytes(PlanName + str(response.url), "utf8")).hexdigest(), 16) % (10 ** 30)
            except Exception as e:
                print(str(e))

            # if response.url == 'https://www.everviewhomes.com/cascada-custom-floorplan':
            #     baths = '2'
            #     halfbath = '0'
            #     bed = '4'
            # elif response.url == 'https://www.everviewhomes.com/price-custom-floorplan':
            #     baths = '2'
            #     halfbath = '0'
            #     bed = '3'
            # elif response.url == 'https://www.everviewhomes.com/campestres-custom-floorplan':
            #     baths = '2'
            #     halfbath = '0'
            #     bed = '3'
            # elif response.url=='https://www.everviewhomes.com/coneflower-custom-floorplan':
            #     PlanName='2877 SF Coneflower Plan'
            #     baths = '2'
            #     halfbath = '0'
            #     bed = '3'
            # else:
            #     pass

            SubdivisionNumber = self.builderNumber  # if subdivision is not available
            unique = str(PlanNumber) + str(SubdivisionNumber)
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            item = BdxCrawlingItem_Plan()
            item['Type'] = 'SingleFamily'
            item['PlanNumber'] = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
            item['unique_number'] = unique_number
            item['SubdivisionNumber'] = SubdivisionNumber
            item['PlanName'] = PlanName
            item['PlanNotAvailable'] = 0
            item['PlanTypeName'] = 'Single Family'
            item['BasePrice'] = 0.00
            item['BaseSqft'] = response.meta['sqft']
            item['Baths'] =  baths
            item['HalfBaths'] = halfbath
            item['Bedrooms'] = bed
            item['Garage'] =  garage
            item['Description'] = "We build new homes in great communities, as well as semi-custom homes and custom homes on your land or ours.One of them is the perfect home for you and your family ... Explore"
            item['ElevationImage'] = response.meta['image']
            item['PlanWebsite'] = response.url
            yield item

#
# from scrapy.cmdline import execute
# execute("scrapy crawl everviewhome".split())
#
