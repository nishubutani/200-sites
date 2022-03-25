import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec


class westwindSpider(scrapy.Spider):

    name = 'westwindhomes123'
    allowed_domains = []
    start_urls = ['https://westwindhomes.com']

    builderNumber = "21812"

    def parse(self, response):
        links = response.xpath('//*[@class="wpb_wrapper"]//h3/a/@href').getall()

        for ind,link in enumerate(links):
            res = requests.get(link)
            try:
                response = HtmlResponse(url=res.url, body=res.content, encoding='utf-8')
            except Exception as e:
                print(e)

            subdivisonName = response.xpath('//h1/text()').get()
            subdivisonNumber = int(hashlib.md5(bytes(subdivisonName, "utf8")).hexdigest(), 16) % (10 ** 30)

            f = open("html/%s.html" % subdivisonNumber, "wb")
            f.write(response.body)
            f.close()

            try:
                add = response.xpath(f'//*[contains(text(),"Contact Us")]/../../following-sibling::div//p[{ind+1}]//text()').getall()
                add = [i.strip() for i in add if i.strip()!='']
                street = add[0]
                city = add[1].split(',')[0]
                state = add[1].split(',')[-1].split(' ')[1].replace('Texas','TX')
                zipcode1 = add[1].split(',')[-1].split(' ')[-1]
                if re.findall(r'\d+',zipcode1):
                    zipcode = zipcode1
                else:
                    zipcode = add[2]
                phn_no1 = add[3]
                if re.findall(r'\d{3}-\d{3}-\d{4}',phn_no1):
                    phn_no = phn_no1
                    m = re.search(r'(\d+)-(\d+)-(\d+)',phn_no)
                    areacode = m.group(1)
                    prefix = m.group(2)
                    suffix = m.group(3)

                else:
                    phn_no = add[4]
                    m = re.search(r'(\d+)-(\d+)-(\d+)', phn_no)
                    areacode = m.group(1)
                    prefix = m.group(2)
                    suffix = m.group(3)


            except Exception as e:
                print(e)
                street = ''
                city = ''
                state = ''
                zipcode = ''

            try:
                description = response.xpath('//*[@class="g-cols vc_row type_default valign_top"]//p/text()').get()
            except Exception as e:
                print(e)
                description = ''

            item2 = BdxCrawlingItem_subdivision()
            item2['sub_Status'] = "Active"
            item2['SubdivisionName'] = subdivisonName
            item2['SubdivisionNumber'] = subdivisonNumber
            item2['BuilderNumber'] = self.builderNumber
            item2['BuildOnYourLot'] = 0
            item2['OutOfCommunity'] = 0
            item2['Street1'] = street
            item2['City'] = city
            item2['State'] = state
            item2['ZIP'] = zipcode
            item2['AreaCode'] = areacode
            item2['Prefix'] = prefix
            item2['Suffix'] = suffix
            item2['Extension'] = ""
            item2['Email'] = ''
            item2['SubDescription'] = description
            item2['SubImage'] = ""
            item2['SubWebsite'] = response.url
            item2['AmenityType'] = ''
            yield item2

            try:
                links = response.xpath('//*[@class="cspml_details_title cspm_txt_hex_hover  cspm-col-lg-12 cspm-col-xs-12 cspm-col-sm-12 cspm-col-md-12"]/a/@href').getall()

                if links == []:
                    links = response.xpath('//*[contains(text(),"View Homes For Sale")]/../@href').getall()
                else:
                    pass
                PlanDetails = {}

                for link in links:
                    yield scrapy.Request(url=link, callback=self.plans_details,
                                         meta={'sbdn': self.builderNumber, 'PlanDetails': PlanDetails,'subdivisonNumber':subdivisonNumber,'zipcode':zipcode,'subdivisonName':subdivisonName}, dont_filter=True)
                # for link1 in home_links:
                #     yield scrapy.Request(url=link1, callback=self.home_details,
                #                          meta={'sbdn': self.builderNumber, 'HomeDetails': HomeDetails,'subdivisonNumber':subdivisonNumber,'home_links':home_links}, dont_filter=True)
            except Exception as e:
                print(e)


    def plans_details(self, response):
        plandetails = response.meta['PlanDetails']
        zipcode = response.meta['zipcode']
        subdivisonName = response.meta['subdivisonName']
        subdivisonNumber = response.meta['subdivisonNumber']

        plan_links = response.xpath('//*[contains(text(),"More Info")]/../@href').getall()
        home_links = response.xpath('//*[contains(text(),"Details")]/@href').getall()

        for plan_link in plan_links:
            plan_link = plan_link.replace('https://westwindhomes.com','')
            res1 = requests.get("https://westwindhomes.com" + str(plan_link))
            try:
                response1 = HtmlResponse(url=res1.url, body=res1.content, encoding='utf-8')
            except Exception as e:
                print(e)
            try:
                plan_name = response1.xpath('//*[@class="page-title notranslate"]/text()').get()
                Type = 'SingleFamily'
                PlanNotAvailable = 0
                PlanTypeName = 'Single Family'
                base_price = 0
            except Exception as e:
                print('Error in Planname',e)
                plan_name = ''



            all = response1.xpath('//*[@id="page-content"]//p//text()').getall()[0]
            try:
                bed1 = re.split(r'\s?(?:Bedrooms|Bedroom)\s?',all)
                bed = bed1[0]
                if '–' in bed:
                    bed = bed.split('–')[-1].strip()
            except Exception as e:
                print("Error in Bedroom",e)
                bed = ''
            try:
                temp_bath = re.split(r'\s?(?:Baths|Bath)\s?', bed1[-1])
                bath = temp_bath[0].replace('-1/2', '1/2').replace('1/2', '.5').replace('/', '').replace('–', '').replace(
                    ' ', '').replace('-1/2', '1/2')
                if '.5' in bath:
                    half_bath = 1
                    full_bath = bath.replace('.5','')
                else:
                    half_bath = 0
                    full_bath = bath
            except Exception as e:
                print("Error in Bedroom", e)
                full_bath = ''


            garage = '0'
            if temp_bath[-1] != '':
                try:
                    if 'Car Garage' in temp_bath[-1]:
                        garage = temp_bath[-1].replace(' Car Garage', '').replace('-1/2', '1/2').replace('1/2', '.5').replace(
                            '/', '').replace('–', '').replace(' ', '').replace('-1/2', '1/2')
                    elif 'Sq.Ft' or 'Sq.Ft.' or 'sq.ft' or 'sq.ft.' in temp_bath[-1]:
                        sqft = re.split(r'\s?(?:Sq.Ft.|sq.ft.|Sq.Ft|sq.ft)\s?', temp_bath[-1])
                        sq = [re.findall(r'[\d*][,]*\d{1,}', i) for i in sqft if i.strip() != '']
                        if (len(sq)) > 1:
                            sq1 = sq[0][0].replace(',', '')
                            sq2 = sq[1][0].replace(',', '')
                            if int(sq1) > int(sq2):
                                sqft1 = sq1
                            else:
                                sqft1 = sq2
                        else:
                            sqft1 = sq[0][0].replace(',', '')
                except Exception as e:
                    print("Error in temp_bath[-1]",e)


            try:
                all1 = response1.xpath('//*[@id="page-content"]//p//text()').getall()[1]
                if 'Car Garage' in all1:
                    garage = all1.split('Car Garage')[0].strip()
                else:
                    pass
                if 'Sq.Ft' or 'Sq.Ft.' or 'sq.ft' or 'sq.ft.' in all1:
                    # sqft = all1.split('Sq.Ft')
                    sqft = re.split(r'\s?(?:Sq.Ft.|sq.ft.|Sq.Ft|sq.ft)\s?', all1)
                    sq = [re.findall(r'[\d*][,]*\d{1,}',i) for i in sqft if i.strip()!='']
                    if (len(sq)) > 1 :
                        sq1 = sq[0][0].replace(',','')
                        sq2 = sq[1][0].replace(',','')
                        if int(sq1)>int(sq2):
                            sqft1 = sq1
                        else:
                            sqft1 = sq2
                    else:
                        sqft1 = sq[0][0].replace(',','')
                else:
                    pass
            except Exception as e:
                print("error in all1",e)

            try:
                PlanNumber = int(hashlib.md5(bytes(str(response1.url) + plan_name + str(bed) +str(full_bath) +str(response.url) , "utf8")).hexdigest(), 16) % (10 ** 30)
            except Exception as e:
                print("error in Plannumber",e)

            SubdivisionNumber = subdivisonNumber  # if subdivision is there
            unique = str(PlanNumber) + str(SubdivisionNumber)
            unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            plandetails[plan_name] = unique_number
            item = BdxCrawlingItem_Plan()
            item['Type'] = Type
            item['PlanNumber'] = PlanNumber
            item['unique_number'] = unique_number
            item['SubdivisionNumber'] = SubdivisionNumber
            item['PlanName'] = plan_name
            item['PlanNotAvailable'] = PlanNotAvailable
            item['PlanTypeName'] = PlanTypeName
            item['BasePrice'] = base_price
            item['BaseSqft'] = sqft1
            item['Baths'] = full_bath
            item['HalfBaths'] = half_bath
            item['Bedrooms'] = bed
            item['Garage'] = garage
            item['Description'] = ''
            item['ElevationImage'] = ''
            item['PlanWebsite'] = response1.url
            yield item

        for home_link in home_links:
            yield scrapy.FormRequest(url=home_link, callback=self.Home_Details, meta={'PlanNumber': unique_number,'subdivisonNumber':SubdivisionNumber,'zipcode':zipcode,'plan_name':plan_name})


    def Home_Details(self,response):

        subdivisonNumber = response.meta['subdivisonNumber']
        zipcode = response.meta['zipcode']
        plan_name = response.meta['plan_name']
        PlanNumber = response.meta['PlanNumber']

        try:
            status = response.xpath('//*[contains(text(),"Status")]/..//a/text()').get().strip()
            print(status)
        except Exception as e:
            print("Error in Status",e)
            status = ''
        try:
            home_zipcode1 = ''.join(response.xpath('//*[@class="es-tabbed-item es-description"]//text()').getall())
            home_zip = re.findall(r'\d{5,}', home_zipcode1)[0]
        except Exception as e:
            print("Erron in home_zipcode1",e)


        if 'Sold' not in status:
            if int(home_zip) == int(zipcode):
                home_name = response.xpath('//*[@class="w-post-elm post_title us_custom_e51b94ea align_center entry-title color_link_inherit"]/text()').get().strip()
                home_plan_name = response.xpath('//*[@class="es-property-fields"]//*[contains(text(),"Floor Plan")]/../text()').get().strip()


                address = response.xpath('//*[@class="es-tabbed-item es-description"]//text()').getall()
                add1 = [(index, i) for index, i in enumerate(address) if re.findall(r'\d{5,}', i) != []]
                index = add1[0][0]
                SpecStreet1 = address[index - 1]
                s = list(add1)[1]
                SpecCity = s.split(',')[0]
                SpecState = re.findall(r'[A-Z]{2}',s.split(',')[-1])
                try:
                    Bed = response.xpath('//*[contains(text(),"Bedrooms")]/../text()').get().strip()
                    if '-' in Bed:
                        Bed = Bed.split('-')[-1]
                        Bedrooms = re.findall(r'(\d+)', Bed)[0]
                    else:
                        Bedrooms = re.findall(r'(\d+)', Bed)[0]
                except Exception as e:
                    print("Error in bed",e)

                try:
                    bath = response.xpath('//*[contains(text(),"Bathrooms")]/../text()').get().strip()
                    bath = bath.replace('-1/2', '1/2').replace('1/2', '.5').replace('/', '').replace('–','').replace(' ', '').replace('-1/2', '1/2')
                    if '.5' in bath:
                        half_bath = 1
                        full_bath = bath.replace('.5', '')
                    else:
                        half_bath = 0
                        full_bath = bath
                except Exception as e:
                    print('Error in Bathroom',e)

                try:
                    garage1 = response.xpath('//*[contains(text(),"Garage")]/../text()').get().strip()
                    garage = garage1.replace('One','1').replace('ONE','1').replace('one','1').replace('Two','2').replace('TWO','2').replace('two','2').replace('Three','3').replace('THREE','3').replace('three','3').replace('Car','').replace('car','').replace('CAR','')
                except Exception as e:
                    print("Error in garage",e)
                    garage = 0

                try:
                    Sqft = response.xpath('//*[contains(text(),"Total Sq Ft")]/../text()').get().strip()
                    if '-' in Sqft:
                        Sqft = Sqft.split('-')[-1]
                        Sqft = Sqft.replace(',', '')
                        BaseSqft = re.findall(r'\d+', Sqft)[0]
                    else:
                        Sqft = Sqft.replace(',', '')
                        BaseSqft = re.findall(r'\d+', Sqft)[0]
                except Exception as e:
                    print("error in sqft",e)
                    BaseSqft = 0

                unique = SpecStreet1 + SpecCity + SpecState + home_zip + str(response.url)
                SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

                PlanNumber = int(hashlib.md5(bytes(home_plan_name, "utf8")).hexdigest(), 16) % (10 ** 30)

                try:

                    item = BdxCrawlingItem_Spec()
                    item['SpecNumber'] = SpecNumber
                    item['PlanNumber'] = PlanNumber
                    item['SpecStreet1'] = SpecStreet1
                    item['SpecCity'] = SpecCity
                    item['SpecState'] = SpecState
                    item['SpecZIP'] = home_zip
                    item['SpecCountry'] = "USA"
                    item['SpecPrice'] = 0
                    item['SpecSqft'] = BaseSqft
                    item['SpecBaths'] = full_bath
                    item['SpecHalfBaths'] = half_bath
                    item['SpecBedrooms'] = Bedrooms
                    item['MasterBedLocation'] = "Down"
                    item['SpecGarage'] = garage
                    item['SpecDescription'] = ''
                    item['SpecElevationImage'] = ''
                    item['SpecWebsite'] = response.url
                    yield item
                except:
                    print("*******************Home*****************")



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl westwindhomes123".split())


