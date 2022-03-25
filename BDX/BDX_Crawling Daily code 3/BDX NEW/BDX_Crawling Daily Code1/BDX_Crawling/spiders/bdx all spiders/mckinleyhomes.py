import hashlib
import re
import json
import scrapy
# from scrapy.utils.response import open_in_browser
from scrapy.http.response.html import HtmlResponse
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
import requests
# from scrapy.http import HtmlResponse

def get_response(url):
    try:
        res = requests.request("GET", url)
        res = HtmlResponse(url=url, body=res.content)
        return res
    except Exception as e:
        print("Isse in response", e)


class mckinleyhomesSpider(scrapy.Spider):
    name = 'mckinleyhomes'
    allowed_domains = ['mckinleyhomes.com']
    start_urls = ['https://www.mckinleyhomes.com/']

    builderNumber = 63677

    uniquenumberlist = []

    def parse(self, response, **kwargs):
        Urls=['https://www.mckinleyhomes.com/new-homes-in/georgia/','https://www.mckinleyhomes.com/new-homes-in/new-york/']
        for url in Urls:
            yield scrapy.FormRequest(url=url,callback=self.community_link,dont_filter=True)
            
    def community_link(self,response):        
        communitylinks=response.xpath('//h2[@class="serif"]/a/@href').getall()
        for lnk in communitylinks:
            yield scrapy.Request(url=lnk,callback=self.communities,dont_filter=True)

    def communities(self,response):
        try:
            communitysite=response.url
        except Exception as e:
            communitysite=''
            print(e)
            communityname=''
            
        try:
            communityname=response.xpath('//h1//text()').get().strip()
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber1 = int(hashlib.md5(bytes(communityname, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % SubdivisionNumber1, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
            SubdivisionNumber1=0
            print(e)

        try:
            status=response.xpath('//h2[@class="sans_serif uppercase"]/text()').get()
        except Exception as e:
            status = "Sold Out"
            print(e)

        try:
            #------------------------------addresss----------------------------------
            addresstemp=response.xpath('//*[@class="comm_overview_location grid-70 prefix-15 suffix-15 bold flex tablet-prefix-5 tablet-suffix-5 tablet-grid-90"]//span[2]//text()').getall()
            addressstreet=addresstemp[0]
            city=addresstemp[1].split(",")[0]
            state=addresstemp[1].split(",")[1].split( )[0]
            zipcode=addresstemp[1].split(",")[1].split( )[1]
        except Exception as e:
            addressstreet=city=state=zipcode=0
            print(e)

        try:
            subdescription="".join(response.xpath('//h2[@class="textcenter inset_tb"]/following-sibling::p//text()').getall())[0:1500]
            subdescription = " ".join(subdescription.split())
        except Exception as e:
            subdescription=''
            print(e)

        try:
            phonetemp=response.xpath('//div[@class="comm_overview_phone grid-70 prefix-15 suffix-15 bold flex tablet-prefix-5 tablet-suffix-5 tablet-grid-90"]//span[2]//text()').get().replace("\t","").split("-")
            try:
                AreaCode=phonetemp[0]
                Prefix=phonetemp[1]
                Suffix=phonetemp[2]
            except:
                phonetemp = response.xpath('//div[@class="comm_overview_phone grid-70 prefix-15 suffix-15 bold flex tablet-prefix-5 tablet-suffix-5 tablet-grid-90"]//span[2]//text()').get().replace("\t", "").split(".")
                AreaCode = phonetemp[0]
                Prefix = phonetemp[1]
                Suffix = phonetemp[2]
        except Exception as e:
            AreaCode=Suffix=Prefix=000
            print(e)

        try:
            subimagelist=[]
            subimage1=response.xpath('//*[@id="comm_hero"]/@style').get()
            subimage3=re.findall('\:[ ]url(.*)',subimage1)[0].replace("(","").replace(")","")
            if subimage3:
                subimagelist.append(subimage3)
            subimage2=response.xpath('//span[@id="comm_siteplan_img"]/img/@src').get()
            if subimage2:
                subimagelist.append(subimage2)
        except Exception as e:
            print(e)

        if "Sold Out" in status:
            pass
        else:
            item = BdxCrawlingItem_subdivision()
            item['sub_Status'] = "Active"
            item['SubdivisionNumber'] = SubdivisionNumber1
            item['BuilderNumber'] = self.builderNumber
            item['SubdivisionName'] = communityname
            item['BuildOnYourLot'] = 0
            item['OutOfCommunity'] = 0
            item['Street1'] = addressstreet
            item['City'] = city
            item['State'] = state
            item['ZIP'] = zipcode
            item['AreaCode'] = AreaCode
            item['Prefix'] = Prefix
            item['Suffix'] = Suffix
            item['Extension'] = ""
            item['Email'] = ""
            item['SubDescription'] = subdescription
            item['SubImage'] = "|".join(subimagelist)
            item['SubWebsite'] = communitysite
            item['AmenityType'] = ''
            yield item

    #         Planlinks=response.xpath('//div[@class="grid-100 grid-parent card_inset white_bg inset_tb"]/a/@href').getall()
    #         for link2 in Planlinks:
    #             yield scrapy.FormRequest(url=link2,callback=self.plan_detail,dont_filter=True)
    #
    # def plan_detail(self,response):
    #     communityfromplan=''
    #     try:
    #         community=response.xpath('//h4[@class="grid-100 textcenter inset_b"]//text()').get().split("-")[1].strip()
    #         communityfromplan = int(hashlib.md5(bytes(community, "utf8")).hexdigest(), 16) % (10 ** 30)
    #     except Exception as e:
    #         print("community in plan not given")
    #         print(e)
    #         community =''
    #     try:
    #         Plansite=response.url
    #     except Exception as e:
    #         Plansite=''
    #         print(e)
    #     planname=''
    #     try:
    #         planname=response.xpath('//h1[@class="object_title grid-100 textcenter inset_t"]//text()').get().strip()
    #         print("******")
    #     except Exception as e:
    #         print(e)
    #
    #     PlanNumber=''
    #     try:
    #         PlanNumber = int(hashlib.md5(bytes(planname+community, "utf8")).hexdigest(), 16) % (10 ** 30)
    #         f = open("html/%s.html" % PlanNumber, "wb")
    #         f.write(response.body)
    #         f.close()
    #     except Exception as e:
    #         print(e)
    #
    #     Baths=HalfBaths=''
    #     Sqft=''
    #     Beds=''
    #     Garage=''
    #     try:
    #         Temp=response.xpath('//div[@class="flex grid-100 grid-parent inset_tb single_details textcenter"]/div/text()').getall()
    #         if len(Temp)==4:
    #             Beds=Temp[0]
    #             Sqft = Temp[2]
    #             Garage = Temp[3]
    #             Baths1=Temp[1]
    #             try:
    #                 tmp = re.findall(r"(\d+)", Baths1)
    #                 Baths = tmp[0]
    #                 if len(tmp) > 1:
    #                     HalfBaths = 1
    #                 else:
    #                     HalfBaths = 0
    #             except Exception as e:
    #                 Baths=HalfBaths=0
    #                 print(e)
    #         if len(Temp)==3:
    #             Beds = Temp[0]
    #             Sqft = Temp[2]
    #             Garage = 0
    #             Baths1 = Temp[1]
    #             try:
    #                 tmp = re.findall(r"(\d+)", Baths1)
    #                 Baths = tmp[0]
    #                 if len(tmp) > 1:
    #                     HalfBaths = 1
    #                 else:
    #                     HalfBaths = 0
    #             except Exception as e:
    #                 Baths = HalfBaths = 0
    #                 print(e)
    #     except Exception as e:
    #         Sqft=Beds=Garage=0
    #         print(e)
    #
    #     try:
    #         Description="".join(response.xpath('//h5[@class="p1"]//text()').getall()).replace(" ","")
    #         print("*****")
    #     except Exception as e:
    #         Description=''
    #         print(e)
    #
    #     Imglist=''
    #     try:
    #         Imglist = []
    #         try:
    #             img1=response.xpath('//*[@class="plan_single_feature image_contain_height grid-100"]/img/@src').get()
    #             Imglist.append(img1)
    #         except:
    #             img1=''
    #         img2 = response.xpath('//div[@class="rvadv_switcher_heading_container flex textcenter"]/div/@data-image').getall()
    #         try:
    #             Img3=img2[0]
    #             Imglist.append(Img3)
    #         except:
    #             Img3=''
    #         try:
    #             Img4=img2[1]
    #             Imglist.append(Img4)
    #         except:
    #             Img4=''
    #         try:
    #             Img5=img2[2]
    #             Imglist.append(Img5)
    #         except:
    #             Img5=''
    #     except Exception as e:
    #         print(e)
    #
    #     unique = str(PlanNumber) + str(community)
    #     print(unique)
    #     unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
    #     self.uniquenumberlist.append(unique_number)
    #     print("******",self.uniquenumberlist)
    #     item = BdxCrawlingItem_Plan()
    #     item['Type'] = 'SingleFamily'
    #     item['PlanNumber'] = PlanNumber
    #     item['unique_number'] = unique_number
    #     item['SubdivisionNumber'] = communityfromplan
    #     item['PlanName'] = planname
    #     item['PlanNotAvailable'] = 0
    #     item['PlanTypeName'] = 'Single Family'
    #     item['BasePrice'] = 0
    #     item['BaseSqft'] = Sqft
    #     item['Baths'] = Baths
    #     item['HalfBaths'] = HalfBaths
    #     item['Bedrooms'] = Beds
    #     item['Garage'] = Garage
    #     item['Description'] = Description
    #     item['ElevationImage'] = "|".join(Imglist)
    #     item['PlanWebsite'] = Plansite
    #     yield item
    #
    #
    #
    #     homelinks =response.xpath('//div[@class="grid-100 textcenter"]/a[1]/@href').getall()
    #     for hmlnk in homelinks:
    #         yield scrapy.FormRequest(url=hmlnk,callback=self.home_link,dont_filter=True)
    #
    #
    # def home_link
    #
    #                 Homelink='https://www.mckinleyhomes.com'+hmlnk
    #                 res3=get_response(Homelink)
    #
    #                 try:
    #                     Homeurl=res3.url
    #                     print("*****")
    #                 except Exception as e:
    #                     Homeurl=''
    #                     print(e)
    #
    #                 planename=''
    #                 try:
    #                     planename=res3.xpath('//div[@class="grid-parent plan_desc mobile-grid-90 mobile-prefix-5"]/p/text()').get().strip()
    #                 except Exception as e:
    #                     print(e,response.url)
    #
    #                 try:
    #                     plannumberforspec=int(hashlib.md5(bytes(planename, "utf8")).hexdigest(), 16) % (10 ** 30)
    #                     # plannumberforspec= unique_number
    #                     print(plannumberforspec)
    #                     print("Hahid of spec",plannumberforspec)
    #                 except Exception as e:
    #                     plannumberforspec=''
    #
    #                 specaddressstreet=''
    #                 speccity=''
    #                 specstate=''
    #                 speczipcode=''
    #                 try:
    #                     addresstemp1=res3.xpath('//h3[@class="grid-100 inset_t mobile-grid-100 textcenter"]//text()').getall()
    #                     try:
    #                         specaddressstreet = addresstemp1[0].strip()
    #                     except:
    #                         specaddressstreet=0
    #                     try:
    #                         speccity = addresstemp1[1].split(",")[0]
    #                     except:
    #                         speccity=0
    #                     try:
    #                         specstate = addresstemp1[1].split(",")[1].split()[0]
    #                     except:
    #                         specstate=0
    #                     try:
    #                         speczipcode = addresstemp1[1].split(",")[1].split()[1]
    #                     except:
    #                         speczipcode=0
    #                 except Exception as e:
    #                     print(e)
    #
    #                 specBaths=specHalfBaths=''
    #                 try:
    #                     tempforbedbathsqft=res3.xpath('//div[@class="grid-25 mobile-grid-25 textcenter borderright"]/text()').getall()
    #                     specBed=tempforbedbathsqft[0]
    #                     specsqft=tempforbedbathsqft[2].replace(",","").strip()
    #                     Baths2 = tempforbedbathsqft[1]
    #                     try:
    #                         tmp = re.findall(r"(\d+)", Baths2)
    #                         specBaths = tmp[0]
    #                         if len(tmp) > 1:
    #                             specHalfBaths = 1
    #                         else:
    #                             specHalfBaths = 0
    #                     except Exception as e:
    #                         specBaths = specHalfBaths = 0
    #                         print(e)
    #                 except Exception as e:
    #                     specBed=specsqft=0
    #                     print(e)
    #
    #                 try:
    #                     garage = res3.xpath('//div[@class="grid-25 mobile-grid-25 textcenter"]/text()').get().strip()
    #                 except Exception as e:
    #                     garage=0
    #                     print(e)
    #
    #                 try:
    #                     specImage=res3.xpath('//*[@class="grid-60 push-5 grid-parent"]/div/img/@src').get()
    #                 except Exception as e:
    #                     specImage=''
    #                     print(e)
    #
    #                 SpecNumber=''
    #                 try:
    #                     unique1 = specaddressstreet + speccity + specstate + speczipcode
    #                     SpecNumber = int(hashlib.md5(bytes(unique1, "utf8")).hexdigest(), 16) % (10 ** 30)
    #                     f = open("html/%s.html" % SpecNumber, "wb")
    #                     f.write(response.body)
    #                     f.close()
    #                 except Exception as e:
    #                     print(e)
    #
    #                 if unique_number in self.uniquenumberlist:
    #                     item = BdxCrawlingItem_Spec()
    #                     item['PlanNumber'] = unique_number
    #                     item['SpecStreet1'] = specaddressstreet
    #                     item['SpecCity'] = speccity
    #                     item['SpecState'] = specstate
    #                     item['SpecZIP'] = speczipcode
    #                     item['SpecNumber'] = SpecNumber
    #                     item['SpecCountry'] = 'USA'
    #                     item['SpecPrice'] = 0
    #                     item['SpecSqft'] = specsqft
    #                     item['SpecBaths'] = specBaths
    #                     item['SpecHalfBaths'] = specHalfBaths
    #                     item['SpecBedrooms'] = specBed
    #                     item['MasterBedLocation'] = 'Down'
    #                     item['SpecGarage'] = garage
    #                     item['SpecDescription'] = ''
    #                     item['SpecElevationImage'] = specImage
    #                     item['SpecWebsite'] = Homeurl
    #                     yield item
    #                 else:
    #                     unique = str(SubdivisionNumber1)  # < -------- Changes here
    #                     unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
    #                     item = BdxCrawlingItem_Plan()
    #                     item['unique_number'] = unique_number
    #                     item['Type'] = "SingleFamily"
    #                     item['PlanNumber'] = "Plan Unknown"
    #                     item['SubdivisionNumber'] = SubdivisionNumber1
    #                     item['PlanName'] = "Plan Unknown"
    #                     item['PlanNotAvailable'] = 1
    #                     item['PlanTypeName'] = 'Single Family'
    #                     item['BasePrice'] = 0
    #                     item['BaseSqft'] = 0
    #                     item['Baths'] = 0
    #                     item['HalfBaths'] = 0
    #                     item['Bedrooms'] = 0
    #                     item['Garage'] = 0
    #                     item['Description'] = ""
    #                     item['ElevationImage'] = ""
    #                     item['PlanWebsite'] = ""
    #                     yield item
    #                     print("*****Error in fakeplan*******spec")
    #                     item = BdxCrawlingItem_Spec()
    #                     item['PlanNumber'] = unique_number
    #                     item['SpecStreet1'] = specaddressstreet
    #                     item['SpecCity'] = speccity
    #                     item['SpecState'] = specstate
    #                     item['SpecZIP'] = speczipcode
    #                     item['SpecNumber'] = SpecNumber
    #                     item['SpecCountry'] = 'USA'
    #                     item['SpecPrice'] = 0
    #                     item['SpecSqft'] = specsqft
    #                     item['SpecBaths'] = specBaths
    #                     item['SpecHalfBaths'] = specHalfBaths
    #                     item['SpecBedrooms'] = specBed
    #                     item['MasterBedLocation'] = 'Down'
    #                     item['SpecGarage'] = garage
    #                     item['SpecDescription'] = ''
    #                     item['SpecElevationImage'] = specImage
    #                     item['SpecWebsite'] = Homeurl
    #                     yield item

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl mckinleyhomes".split())


