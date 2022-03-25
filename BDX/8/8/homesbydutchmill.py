# import hashlib
# import re
# import scrapy
# from scrapy.cmdline import execute
#
# from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan
#
#
# class HomesbydutchmillSpider(scrapy.Spider):
#     name = 'homesbydutchmill'
#     allowed_domains = ['homesbydutchmill.com']
#     start_urls = ['http://homesbydutchmill.com/']
#     builderNumber = '31190'
#
#     def parse(self,response):
#         f = open("html/%s.html" % self.builderNumber, "wb")
#         f.write(response.body)
#         f.close()
#         item = BdxCrawlingItem_subdivision()
#         item['sub_Status'] = "Active"
#         item['SubdivisionNumber'] = self.builderNumber
#         item['BuilderNumber'] = self.builderNumber
#         item['SubdivisionName'] = "No Sub Division"
#         item['BuildOnYourLot'] = 0
#         item['OutOfCommunity'] = 0
#         item['Street1'] = '14795 W 101st Ave. Suite C'
#         item['City'] = 'Dyer'
#         item['State'] = 'IN'
#         item['ZIP'] = '46311'
#         item['AreaCode'] = '219'
#         item['Prefix'] = '365'
#         item['Suffix'] = '5699'
#         item['Extension'] = ""
#         item['Email'] = 'sales@domegahomes.com'
#         item[
#             'SubDescription'] = 'With Homes By Dutch Mill, you truly get what you want. We built our home with Dutch Mill due to their reputation and quality workmanship. That was the easiest decision and by far the best decision that we could have made. We absolutely love our home and so does everyone who comes to visit. The continuous compliments from others verifies our decision to build with Homes By Dutch Mill. Lori Burgans is an accomplished Design Specialist who was patient, kind, and above all knowledgeable and open-minded to our likes and dislikes in a home. She had an eye for detail and the budget friendly outlook gave us the peace of mind needed to commit to building our dream home. Many family members were less than supportive cautioning us to hidden costs, allowances, and “headaches” that are entailed in building. There were no hidden costs and Dutch Mill far exceeded our expectations and wildest dreams from start to finish.Each craftsman that made our house come to life treated us with respect, dignity, and kept an open line of communication with us on site throughout the build. With Dutch Mill you truly get what you want, as there is nothing standard or cookie cutter about our home. SERIOUSLY, we have house stalkers!" Susan & John – Schererville, IN “Our home is even more beautiful than I imagined”All I can say is WOW! Our home is even more beautiful than I imagined. You won’t be disappointed with the quality of their work. Dave and Lori are a pleasure to work with. Thank you Dutch Mill for creating our dream home." -JoAnna – St. John, IN  ”Thank you for making our Dream Home a reality. Your attention to details made all the difference. We could not have ever put all the pieces together without you. When we first met with you, we knew you were the ones to handle this project. We had a vision of what we were looking for in a home and you guided us through the many steps. From the first drafts to breaking ground to choosing every detail: too many decisions to even comprehend. Your ideas for the stone, the granite, the fixtures, the colors; Lori, you are an artist and each home is your palette.We would also like to add that your crews, the framing team, Decor Tile, etc. they were outstanding. We loved working with them. Not many people are happy after the process of building. We are extremely happy. This would not have been possible had we not made the right decision to work with you. It is with gratitude that our good friends recommended you. Also, seeing a Dutch Mill Home alongside others in The Parade of Homes and other Open Houses: no comparison as to who had the better home. While this thank you is long overdue, our feelings have not wavered. We are thrilled with our new home. With Love and Thanks, Diane and Marijo – Crown Point, IN '
#         item[
#             'SubImage'] = 'http://homesbydutchmill.com/wp-content/uploads/2017/07/edenscovemap.jpg'
#         item['SubWebsite'] = response.url
#         yield item
#
#         planlinks = ['http://homesbydutchmill.com/single-family-homes/','http://homesbydutchmill.com/town-home-living/']
#         for planlink in planlinks:
#             yield scrapy.Request(url=planlink, callback=self.plan_list, dont_filter=True)
#
#     def plan_list(self,response):
#         if response.url == 'http://homesbydutchmill.com/single-family-homes/':
#
#             for i in range(3,20):
#
#                 path = response.xpath(f'//*[@class="et_pb_section  et_pb_section_{i} et_pb_with_background et_section_regular"]')
#                 path1 = path.extract()
#                 planname = path.xpath('.//p/text()').get()
#
#                 try:
#                     bedrooms = re.findall('(\d.\d) Bathrooms',path1)[0]
#                 except:
#                     try:
#                         bathroom = re.findall('(\d) Bathrooms',path1)[0]
#                     except:
#                         bathroom = 0
#
#                 try:
#                     bedrooms = re.findall('(\d) Bedrooms',path1)[0]
#                 except:
#                     bedrooms = 0
#
#                 try:
#                     garage = re.findall('(\d) Car',path1)[0]
#                 except:
#                     garage = 0
#
#                 try:
#                     sqft = path.xpath('//strong[contains(text(),"Total Sq. Ft")]/text()').get()
#                     if not sqft :
#                         sqft = path.xpath('//strong[contains(text(),"//strong[contains(text(),"Main Floor Sq. Ft")]/text()")]/text()').get()
#                         if not sqft:
#                             sqft = path.xpath('//strong[contains(text(),"Total Sq. Ft")]/text()').get()
#                     sqft = re.findall('(\d+)',sqft.replace(',',''))[0]
#                 except:
#                     sqft = 0
#
#                 try:
#                     image = path.xpath('//*[@class="et_pb_gallery_image landscape"]//@src').getall()
#                 except:
#                     image = ''
#
#                 if image != '':
#                     elevation = '|'.join(image)
#
#                 try:
#                     price = path.xpath('//h2/strong[contains(text(),"$")]/text()').get()
#                     price = re.findall('(\d+)',price)[0]
#                 except:
#                     price = 0
#
#                 SubdivisionNumber = self.builderNumber  # if subdivision is not available
#                 try:
#                     PlanNumber = int(hashlib.md5(bytes(planname, "utf8")).hexdigest(), 16) % (10 ** 30)
#                 except:
#                     PlanNumber = ''
#                 f = open("html/%s.html" % PlanNumber, "wb")
#                 f.write(response.body)
#                 f.close()
#                 unique = str(PlanNumber) + str(SubdivisionNumber)
#                 unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
#
#                 item = BdxCrawlingItem_Plan()
#                 item['Type'] = 'SingleFamily'
#                 item['PlanNumber'] = PlanNumber
#                 item['unique_number'] = unique_number
#                 item['SubdivisionNumber'] = SubdivisionNumber
#                 item['PlanName'] = planname
#                 item['PlanNotAvailable'] = 0
#                 item['PlanTypeName'] = 'Single Family'
#                 item['BasePrice'] = price
#                 item['BaseSqft'] = sqft
#                 item['Baths'] = bathroom
#                 item['HalfBaths'] = 0
#                 item['Bedrooms'] = bedrooms
#                 item['Garage'] = garage
#                 item['Description'] = 'The basis for our philosophy is rooted from many decades of experience in construction in the Chicagoland area and Northwest Indiana. Years of knowledge brings out exquisite attention to detail.'
#                 item['ElevationImage'] = elevation
#                 item['PlanWebsite'] = response.url
#                 yield item
#
#         else:
#
#
# # execute("scrapy crawl homesbydutchmill".split())
#
#
