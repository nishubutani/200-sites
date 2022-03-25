import hashlib
import random

import scrapy
from w3lib.http import basic_auth_header

from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
proxy = [
    'lum-customer-xbyte-zone-zone_us-country-us|0gi0pioy3oey',
    'lum-customer-xbyte-zone-zone_india-country-in|w6zj0g4ikjy3',
]

current_proxy = random.choice(proxy).split("|")
proxy_host = "zproxy.lum-superproxy.io"
proxy_port = "22225"
proxy_auth = str(current_proxy[0])+":"+str(current_proxy[1])
proxies = {"https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
      "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}


class GraniteridgebuildersSpider(scrapy.Spider):
    name = 'graniteridgebuilders'
    allowed_domains = ['graniteridgebuilders.com']
    # start_urls = ['http://graniteridgebuilders.com/']
    builderNumber = '26924'
    def start_requests(self):
        url = 'http://graniteridgebuilders.com/'
        header = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            # "cookie": "dd_device_id=dx_c3721ea525514e01a8b4d7bf5029fb2e; dd_device_id_2=dx_14568fb17dc84c1f81c7590daf91be08; ajs_anonymous_id=%22310b4c0c-3526-485f-bf4b-a4405322ca18%22; _fbp=fb.1.1590061279532.105558481; __cfduid=d148cf56b70337c864e29f26d227bc09d1590061279; dd_login_id=lx_74985db089e54b8b94ee7dd76fbba922; optimizelyEndUserId=oeu1590061280857r0.18117935485753045; ajs_group_id=null; amplitude_idundefineddoordash.com=eyJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGwsImxhc3RFdmVudFRpbWUiOm51bGwsImV2ZW50SWQiOjAsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjowfQ==; _gcl_au=1.1.622846915.1590061281; _ga=GA1.2.147978338.1590061282; _gid=GA1.2.736786608.1590061282; _scid=127b19ac-f4bb-484e-a251-9645ed783136; _sctr=1|1589999400000; csrf_token=KG11zHXchxydjc8NCCAGfaViKAGHIT99WFZQ8KvKx5RS7SfEsuAeBcWDpBEqx6mN; sessionid=peo2v6gntgi46l4pvzkwdishs0lg5lsh; dd_submarket_id=23; dd_district_id=564; dd_zip_code=30303; ajs_user_id=%22302269637%22; __ssid=cbcd1c0e6fdc1e61e07b5dc7c51cfe2; _pin_unauth=NGM4NmVlOTQtMDI0Zi00ZjkwLWFlYTYtMWExYmZhZGY3Nzcy; dd_session_id_2=sx_2a9d8ef1603c42eea7a67385bff124e1; dd_session_id=sx_c0d257e74c394a0abd0fec58130b2603; doordash_attempt_canary=0; _dpm_ses.4dc2=*; _gat_UA-36201829-6=1; __cf_bm=92fb4800563695be7c0e98fb3b49f50aca6d25e8-1590210041-1800-AWQK3rKj2zC/x+VzwOt7pQTuJ5vYfxvVQPd3fpicPC5Id2thXFhCpqMD6N6maH/hvQBOssA8M5qOhZdampwcdYs=; amplitude_id_8a4cf5f3981e8b7827bab3968fb1ad2bdoordash.com=eyJkZXZpY2VJZCI6ImFlZGVjYjZiLWE2MjktNGVlMS05ZmUxLWU4OTA4NWE3NDQ3NVIiLCJ1c2VySWQiOiIzMDIyNjk2MzciLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE1OTAyMDk5NDI2MTAsImxhc3RFdmVudFRpbWUiOjE1OTAyMTAwNDQ2OTMsImV2ZW50SWQiOjEyMywiaWRlbnRpZnlJZCI6MTMsInNlcXVlbmNlTnVtYmVyIjoxMzZ9; _uetsid=ad769752-70fd-3c88-2392-d832f89f4ec6; _dpm_id.4dc2=5d74af7e-4535-4107-9cd7-82c3c9d6bbb2.1590061284.7.1590210045.1590153954.3c67949c-974d-4b25-a610-b885d5fae435",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            # "Proxy-Authorization": basic_auth_header(current_proxy[0], current_proxy[1])
        }
        yield scrapy.Request(url=url, headers=header, callback=self.parse, dont_filter=True)

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
        item['Street1'] = '1020 Woodland Plaza Run'
        item['City'] = 'Fort Wayne'
        item['State'] = 'IN'
        item['ZIP'] = '46825'
        item['AreaCode'] = '260'
        item['Prefix'] = '490'
        item['Suffix'] = '1417'
        item['Extension'] = ""
        item['Email'] = 'info@graniteridgebuilders.com'
        item[
            'SubDescription'] = "We’re here to bring your dream home to life while providing the best experience possible throughout the new home construction process."
        item[
            'SubImage'] = 'https://assets.graniteridgebuilders.com/uploads/banners/_it2000x640/harbour-villas-3-parade-home.JPG|https://assets.graniteridgebuilders.com/uploads/banners/_it2000x/kitchen-harbourwood-grey-oaks-villas-45.jpg'
        item['SubWebsite'] = response.url
        yield item

        planlink = 'https://graniteridgebuilders.com/build-your-home/floor-plans'
        header = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            # "cookie": "dd_device_id=dx_c3721ea525514e01a8b4d7bf5029fb2e; dd_device_id_2=dx_14568fb17dc84c1f81c7590daf91be08; ajs_anonymous_id=%22310b4c0c-3526-485f-bf4b-a4405322ca18%22; _fbp=fb.1.1590061279532.105558481; __cfduid=d148cf56b70337c864e29f26d227bc09d1590061279; dd_login_id=lx_74985db089e54b8b94ee7dd76fbba922; optimizelyEndUserId=oeu1590061280857r0.18117935485753045; ajs_group_id=null; amplitude_idundefineddoordash.com=eyJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGwsImxhc3RFdmVudFRpbWUiOm51bGwsImV2ZW50SWQiOjAsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjowfQ==; _gcl_au=1.1.622846915.1590061281; _ga=GA1.2.147978338.1590061282; _gid=GA1.2.736786608.1590061282; _scid=127b19ac-f4bb-484e-a251-9645ed783136; _sctr=1|1589999400000; csrf_token=KG11zHXchxydjc8NCCAGfaViKAGHIT99WFZQ8KvKx5RS7SfEsuAeBcWDpBEqx6mN; sessionid=peo2v6gntgi46l4pvzkwdishs0lg5lsh; dd_submarket_id=23; dd_district_id=564; dd_zip_code=30303; ajs_user_id=%22302269637%22; __ssid=cbcd1c0e6fdc1e61e07b5dc7c51cfe2; _pin_unauth=NGM4NmVlOTQtMDI0Zi00ZjkwLWFlYTYtMWExYmZhZGY3Nzcy; dd_session_id_2=sx_2a9d8ef1603c42eea7a67385bff124e1; dd_session_id=sx_c0d257e74c394a0abd0fec58130b2603; doordash_attempt_canary=0; _dpm_ses.4dc2=*; _gat_UA-36201829-6=1; __cf_bm=92fb4800563695be7c0e98fb3b49f50aca6d25e8-1590210041-1800-AWQK3rKj2zC/x+VzwOt7pQTuJ5vYfxvVQPd3fpicPC5Id2thXFhCpqMD6N6maH/hvQBOssA8M5qOhZdampwcdYs=; amplitude_id_8a4cf5f3981e8b7827bab3968fb1ad2bdoordash.com=eyJkZXZpY2VJZCI6ImFlZGVjYjZiLWE2MjktNGVlMS05ZmUxLWU4OTA4NWE3NDQ3NVIiLCJ1c2VySWQiOiIzMDIyNjk2MzciLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE1OTAyMDk5NDI2MTAsImxhc3RFdmVudFRpbWUiOjE1OTAyMTAwNDQ2OTMsImV2ZW50SWQiOjEyMywiaWRlbnRpZnlJZCI6MTMsInNlcXVlbmNlTnVtYmVyIjoxMzZ9; _uetsid=ad769752-70fd-3c88-2392-d832f89f4ec6; _dpm_id.4dc2=5d74af7e-4535-4107-9cd7-82c3c9d6bbb2.1590061284.7.1590210045.1590153954.3c67949c-974d-4b25-a610-b885d5fae435",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Proxy-Authorization": basic_auth_header(current_proxy[0], current_proxy[1])
        }
        yield scrapy.Request(url=planlink, headers = header,callback=self.parse_planlink, dont_filter=True)

    def parse_planlink(self,response):
        plandetail = {}
        links = response.xpath('//*[@class="floor-plans-listing-detail"]/@href').getall()
        for link in links:
            header = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                # "cookie": "dd_device_id=dx_c3721ea525514e01a8b4d7bf5029fb2e; dd_device_id_2=dx_14568fb17dc84c1f81c7590daf91be08; ajs_anonymous_id=%22310b4c0c-3526-485f-bf4b-a4405322ca18%22; _fbp=fb.1.1590061279532.105558481; __cfduid=d148cf56b70337c864e29f26d227bc09d1590061279; dd_login_id=lx_74985db089e54b8b94ee7dd76fbba922; optimizelyEndUserId=oeu1590061280857r0.18117935485753045; ajs_group_id=null; amplitude_idundefineddoordash.com=eyJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGwsImxhc3RFdmVudFRpbWUiOm51bGwsImV2ZW50SWQiOjAsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjowfQ==; _gcl_au=1.1.622846915.1590061281; _ga=GA1.2.147978338.1590061282; _gid=GA1.2.736786608.1590061282; _scid=127b19ac-f4bb-484e-a251-9645ed783136; _sctr=1|1589999400000; csrf_token=KG11zHXchxydjc8NCCAGfaViKAGHIT99WFZQ8KvKx5RS7SfEsuAeBcWDpBEqx6mN; sessionid=peo2v6gntgi46l4pvzkwdishs0lg5lsh; dd_submarket_id=23; dd_district_id=564; dd_zip_code=30303; ajs_user_id=%22302269637%22; __ssid=cbcd1c0e6fdc1e61e07b5dc7c51cfe2; _pin_unauth=NGM4NmVlOTQtMDI0Zi00ZjkwLWFlYTYtMWExYmZhZGY3Nzcy; dd_session_id_2=sx_2a9d8ef1603c42eea7a67385bff124e1; dd_session_id=sx_c0d257e74c394a0abd0fec58130b2603; doordash_attempt_canary=0; _dpm_ses.4dc2=*; _gat_UA-36201829-6=1; __cf_bm=92fb4800563695be7c0e98fb3b49f50aca6d25e8-1590210041-1800-AWQK3rKj2zC/x+VzwOt7pQTuJ5vYfxvVQPd3fpicPC5Id2thXFhCpqMD6N6maH/hvQBOssA8M5qOhZdampwcdYs=; amplitude_id_8a4cf5f3981e8b7827bab3968fb1ad2bdoordash.com=eyJkZXZpY2VJZCI6ImFlZGVjYjZiLWE2MjktNGVlMS05ZmUxLWU4OTA4NWE3NDQ3NVIiLCJ1c2VySWQiOiIzMDIyNjk2MzciLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE1OTAyMDk5NDI2MTAsImxhc3RFdmVudFRpbWUiOjE1OTAyMTAwNDQ2OTMsImV2ZW50SWQiOjEyMywiaWRlbnRpZnlJZCI6MTMsInNlcXVlbmNlTnVtYmVyIjoxMzZ9; _uetsid=ad769752-70fd-3c88-2392-d832f89f4ec6; _dpm_id.4dc2=5d74af7e-4535-4107-9cd7-82c3c9d6bbb2.1590061284.7.1590210045.1590153954.3c67949c-974d-4b25-a610-b885d5fae435",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                "Proxy-Authorization": basic_auth_header(current_proxy[0], current_proxy[1])
            }
            yield scrapy.Request(url=link,headers=header, callback=self.plan_detail, dont_filter=True,meta={'plandetail':plandetail})
        next = response.xpath('//*[@class="rd-button primary lazy-load-link"]/@href').get()
        if next:
            header = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                # "cookie": "dd_device_id=dx_c3721ea525514e01a8b4d7bf5029fb2e; dd_device_id_2=dx_14568fb17dc84c1f81c7590daf91be08; ajs_anonymous_id=%22310b4c0c-3526-485f-bf4b-a4405322ca18%22; _fbp=fb.1.1590061279532.105558481; __cfduid=d148cf56b70337c864e29f26d227bc09d1590061279; dd_login_id=lx_74985db089e54b8b94ee7dd76fbba922; optimizelyEndUserId=oeu1590061280857r0.18117935485753045; ajs_group_id=null; amplitude_idundefineddoordash.com=eyJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGwsImxhc3RFdmVudFRpbWUiOm51bGwsImV2ZW50SWQiOjAsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjowfQ==; _gcl_au=1.1.622846915.1590061281; _ga=GA1.2.147978338.1590061282; _gid=GA1.2.736786608.1590061282; _scid=127b19ac-f4bb-484e-a251-9645ed783136; _sctr=1|1589999400000; csrf_token=KG11zHXchxydjc8NCCAGfaViKAGHIT99WFZQ8KvKx5RS7SfEsuAeBcWDpBEqx6mN; sessionid=peo2v6gntgi46l4pvzkwdishs0lg5lsh; dd_submarket_id=23; dd_district_id=564; dd_zip_code=30303; ajs_user_id=%22302269637%22; __ssid=cbcd1c0e6fdc1e61e07b5dc7c51cfe2; _pin_unauth=NGM4NmVlOTQtMDI0Zi00ZjkwLWFlYTYtMWExYmZhZGY3Nzcy; dd_session_id_2=sx_2a9d8ef1603c42eea7a67385bff124e1; dd_session_id=sx_c0d257e74c394a0abd0fec58130b2603; doordash_attempt_canary=0; _dpm_ses.4dc2=*; _gat_UA-36201829-6=1; __cf_bm=92fb4800563695be7c0e98fb3b49f50aca6d25e8-1590210041-1800-AWQK3rKj2zC/x+VzwOt7pQTuJ5vYfxvVQPd3fpicPC5Id2thXFhCpqMD6N6maH/hvQBOssA8M5qOhZdampwcdYs=; amplitude_id_8a4cf5f3981e8b7827bab3968fb1ad2bdoordash.com=eyJkZXZpY2VJZCI6ImFlZGVjYjZiLWE2MjktNGVlMS05ZmUxLWU4OTA4NWE3NDQ3NVIiLCJ1c2VySWQiOiIzMDIyNjk2MzciLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE1OTAyMDk5NDI2MTAsImxhc3RFdmVudFRpbWUiOjE1OTAyMTAwNDQ2OTMsImV2ZW50SWQiOjEyMywiaWRlbnRpZnlJZCI6MTMsInNlcXVlbmNlTnVtYmVyIjoxMzZ9; _uetsid=ad769752-70fd-3c88-2392-d832f89f4ec6; _dpm_id.4dc2=5d74af7e-4535-4107-9cd7-82c3c9d6bbb2.1590061284.7.1590210045.1590153954.3c67949c-974d-4b25-a610-b885d5fae435",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                "Proxy-Authorization": basic_auth_header(current_proxy[0], current_proxy[1])
            }
            yield scrapy.Request(url=next,headers=header, callback=self.parse_planlink, dont_filter=True)

    def plan_detail(self,response):

        plandetail = response.meta['plandetail']
        planname = response.xpath('//header/h1/text()').get()
        price = response.xpath('//header/div[@class="price"]/text()').get().replace('$','').replace(',','')
        sqft = response.xpath('//div[contains(text(),"Square Feet")]/following-sibling::div/text()').get()
        bedroom = response.xpath('//div[contains(text(),"Bedrooms")]/following-sibling::div/text()').get()
        bathroom = response.xpath('//div[contains(text(),"Bathrooms")]/following-sibling::div/text()').get()
        halfbaths = response.xpath('//div[contains(text(),"Half Baths")]/following-sibling::div/text()').get()
        garage = response.xpath('//div[contains(text(),"Garage")]/following-sibling::div/text()').get()

        image = response.xpath('//*[@id="main-content"]//img/@src').getall()

        PlanNumber = int(hashlib.md5(bytes(response.url, "utf8")).hexdigest(), 16) % (10 ** 30)
        f = open("html/%s.html" % PlanNumber, "wb")
        f.write(response.body)
        f.close()

        SubdivisionNumber = self.builderNumber  # if subdivision is not available
        unique = str(PlanNumber) + str(SubdivisionNumber)
        unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)

        item = BdxCrawlingItem_Plan()
        item['Type'] = 'SingleFamily'
        item['PlanNumber'] = PlanNumber

        item['unique_number'] = unique_number
        item['SubdivisionNumber'] = SubdivisionNumber
        item['PlanName'] = planname
        plandetail[planname] = unique_number
        item['PlanNotAvailable'] = 0
        item['PlanTypeName'] = 'Single Family'
        item['BasePrice'] = price
        item['BaseSqft'] = sqft
        item['Baths'] = bathroom
        item['HalfBaths'] = halfbaths
        item['Bedrooms'] = bedroom
        item['Garage'] = garage
        item['Description'] = response.xpath('//*[@class="description"]/p/text()').get()
        item['ElevationImage'] = "|".join(image)
        item['PlanWebsite'] = response.url
        yield item

        homelinks = 'https://graniteridgebuilders.com/find-your-home/available-homes'
        header = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            # "cookie": "dd_device_id=dx_c3721ea525514e01a8b4d7bf5029fb2e; dd_device_id_2=dx_14568fb17dc84c1f81c7590daf91be08; ajs_anonymous_id=%22310b4c0c-3526-485f-bf4b-a4405322ca18%22; _fbp=fb.1.1590061279532.105558481; __cfduid=d148cf56b70337c864e29f26d227bc09d1590061279; dd_login_id=lx_74985db089e54b8b94ee7dd76fbba922; optimizelyEndUserId=oeu1590061280857r0.18117935485753045; ajs_group_id=null; amplitude_idundefineddoordash.com=eyJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGwsImxhc3RFdmVudFRpbWUiOm51bGwsImV2ZW50SWQiOjAsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjowfQ==; _gcl_au=1.1.622846915.1590061281; _ga=GA1.2.147978338.1590061282; _gid=GA1.2.736786608.1590061282; _scid=127b19ac-f4bb-484e-a251-9645ed783136; _sctr=1|1589999400000; csrf_token=KG11zHXchxydjc8NCCAGfaViKAGHIT99WFZQ8KvKx5RS7SfEsuAeBcWDpBEqx6mN; sessionid=peo2v6gntgi46l4pvzkwdishs0lg5lsh; dd_submarket_id=23; dd_district_id=564; dd_zip_code=30303; ajs_user_id=%22302269637%22; __ssid=cbcd1c0e6fdc1e61e07b5dc7c51cfe2; _pin_unauth=NGM4NmVlOTQtMDI0Zi00ZjkwLWFlYTYtMWExYmZhZGY3Nzcy; dd_session_id_2=sx_2a9d8ef1603c42eea7a67385bff124e1; dd_session_id=sx_c0d257e74c394a0abd0fec58130b2603; doordash_attempt_canary=0; _dpm_ses.4dc2=*; _gat_UA-36201829-6=1; __cf_bm=92fb4800563695be7c0e98fb3b49f50aca6d25e8-1590210041-1800-AWQK3rKj2zC/x+VzwOt7pQTuJ5vYfxvVQPd3fpicPC5Id2thXFhCpqMD6N6maH/hvQBOssA8M5qOhZdampwcdYs=; amplitude_id_8a4cf5f3981e8b7827bab3968fb1ad2bdoordash.com=eyJkZXZpY2VJZCI6ImFlZGVjYjZiLWE2MjktNGVlMS05ZmUxLWU4OTA4NWE3NDQ3NVIiLCJ1c2VySWQiOiIzMDIyNjk2MzciLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE1OTAyMDk5NDI2MTAsImxhc3RFdmVudFRpbWUiOjE1OTAyMTAwNDQ2OTMsImV2ZW50SWQiOjEyMywiaWRlbnRpZnlJZCI6MTMsInNlcXVlbmNlTnVtYmVyIjoxMzZ9; _uetsid=ad769752-70fd-3c88-2392-d832f89f4ec6; _dpm_id.4dc2=5d74af7e-4535-4107-9cd7-82c3c9d6bbb2.1590061284.7.1590210045.1590153954.3c67949c-974d-4b25-a610-b885d5fae435",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Proxy-Authorization": basic_auth_header(current_proxy[0], current_proxy[1])
        }
        yield scrapy.Request(url=homelinks,headers=header, callback=self.homelinks, dont_filter=True,meta={'PN':plandetail})

    def homelinks(self, response):

        PN = response.meta['PN']
        links = response.xpath('//*[@class="homes-listing-detail"]/@href').getall()
        for link in links:
            header = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                # "cookie": "dd_device_id=dx_c3721ea525514e01a8b4d7bf5029fb2e; dd_device_id_2=dx_14568fb17dc84c1f81c7590daf91be08; ajs_anonymous_id=%22310b4c0c-3526-485f-bf4b-a4405322ca18%22; _fbp=fb.1.1590061279532.105558481; __cfduid=d148cf56b70337c864e29f26d227bc09d1590061279; dd_login_id=lx_74985db089e54b8b94ee7dd76fbba922; optimizelyEndUserId=oeu1590061280857r0.18117935485753045; ajs_group_id=null; amplitude_idundefineddoordash.com=eyJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGwsImxhc3RFdmVudFRpbWUiOm51bGwsImV2ZW50SWQiOjAsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjowfQ==; _gcl_au=1.1.622846915.1590061281; _ga=GA1.2.147978338.1590061282; _gid=GA1.2.736786608.1590061282; _scid=127b19ac-f4bb-484e-a251-9645ed783136; _sctr=1|1589999400000; csrf_token=KG11zHXchxydjc8NCCAGfaViKAGHIT99WFZQ8KvKx5RS7SfEsuAeBcWDpBEqx6mN; sessionid=peo2v6gntgi46l4pvzkwdishs0lg5lsh; dd_submarket_id=23; dd_district_id=564; dd_zip_code=30303; ajs_user_id=%22302269637%22; __ssid=cbcd1c0e6fdc1e61e07b5dc7c51cfe2; _pin_unauth=NGM4NmVlOTQtMDI0Zi00ZjkwLWFlYTYtMWExYmZhZGY3Nzcy; dd_session_id_2=sx_2a9d8ef1603c42eea7a67385bff124e1; dd_session_id=sx_c0d257e74c394a0abd0fec58130b2603; doordash_attempt_canary=0; _dpm_ses.4dc2=*; _gat_UA-36201829-6=1; __cf_bm=92fb4800563695be7c0e98fb3b49f50aca6d25e8-1590210041-1800-AWQK3rKj2zC/x+VzwOt7pQTuJ5vYfxvVQPd3fpicPC5Id2thXFhCpqMD6N6maH/hvQBOssA8M5qOhZdampwcdYs=; amplitude_id_8a4cf5f3981e8b7827bab3968fb1ad2bdoordash.com=eyJkZXZpY2VJZCI6ImFlZGVjYjZiLWE2MjktNGVlMS05ZmUxLWU4OTA4NWE3NDQ3NVIiLCJ1c2VySWQiOiIzMDIyNjk2MzciLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE1OTAyMDk5NDI2MTAsImxhc3RFdmVudFRpbWUiOjE1OTAyMTAwNDQ2OTMsImV2ZW50SWQiOjEyMywiaWRlbnRpZnlJZCI6MTMsInNlcXVlbmNlTnVtYmVyIjoxMzZ9; _uetsid=ad769752-70fd-3c88-2392-d832f89f4ec6; _dpm_id.4dc2=5d74af7e-4535-4107-9cd7-82c3c9d6bbb2.1590061284.7.1590210045.1590153954.3c67949c-974d-4b25-a610-b885d5fae435",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                "Proxy-Authorization": basic_auth_header(current_proxy[0], current_proxy[1])
            }
            yield scrapy.Request(url=link,headers=header, callback=self.home_detail, dont_filter=True,meta={'PN':PN})

    def home_detail(self, response):
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
        PN = response.meta['PN']
        SpecStreet1 = response.xpath('//header/h1/text()').get()
        detail = response.xpath('//header/h1/span/text()').get()
        SpecCity = detail.split(',')[0].strip()
        SpecState = detail.split(',')[1].split()[0].strip()
        SpecZIP = detail.split(',')[1].split()[1].strip()
        SpecPrice = response.xpath('//header/div[@class="price"]/text()').get().replace('$','').replace(',','')
        SpecSqft = response.xpath('//div[contains(text(),"Square Feet")]/following-sibling::div/text()').get()
        SpecBedrooms = response.xpath('//div[contains(text(),"Bedrooms")]/following-sibling::div/text()').get()
        SpecBaths = response.xpath('//div[contains(text(),"Bathrooms")]/following-sibling::div/text()').get()
        SpecHalfBaths = response.xpath('//div[contains(text(),"Half Baths")]/following-sibling::div/text()').get()
        SpecGarage = response.xpath('//div[contains(text(),"Garage")]/following-sibling::div/text()').get()

        SpecElevationImage = response.xpath('//*[@id="main-content"]//img/@src').getall()

        planName = response.xpath('//div[contains(text(),"Floor Plan")]/following-sibling::div/text()').get()
        if planName != 'N/A':
            try:
                PlanNumber = PN[planName]
            except Exception as e:
                pass
        else:
            PlanNumber = unique_number

        try:
            unique = SpecStreet1 + SpecCity + SpecState + SpecZIP
            SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
            f = open("html/%s.html" % SpecNumber, "wb")
            f.write(response.body)
            f.close()
        except Exception as e:
            print(e)
            SpecNumber = ''

        item = BdxCrawlingItem_Spec()
        item['SpecNumber'] = SpecNumber
        item['PlanNumber'] = PlanNumber
        item['SpecStreet1'] = SpecStreet1
        item['SpecCity'] = SpecCity
        item['SpecState'] = SpecState
        item['SpecZIP'] = SpecZIP
        item['SpecCountry'] = 'USA'
        item['SpecPrice'] = SpecPrice
        item['SpecSqft'] = SpecSqft
        item['SpecBaths'] = SpecBaths
        item['SpecHalfBaths'] = SpecHalfBaths
        item['SpecBedrooms'] = SpecBedrooms
        item['MasterBedLocation'] = "Down"
        item['SpecGarage'] = SpecGarage
        item['SpecDescription'] = response.xpath('//*[@class="description"]/p/text()').get()
        item['SpecElevationImage'] = '|'.join(SpecElevationImage)
        item['SpecWebsite'] = response.url
        yield item

from scrapy.cmdline import execute
# execute("scrapy crawl graniteridgebuilders".split())
