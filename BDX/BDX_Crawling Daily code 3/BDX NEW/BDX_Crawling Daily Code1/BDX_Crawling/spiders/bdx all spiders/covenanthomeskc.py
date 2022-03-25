# -*- coding: utf-8 -*-
import hashlib
import re
import scrapy
import requests
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
import json
from w3lib.html import remove_tags


class AndersonhomesllcSpider(scrapy.Spider):
	name = 'covenanthomeskc'
	allowed_domains = []
	start_urls = ['https://www.covenanthomeskc.com/neighborhood?format=json-pretty']

	builderNumber = "49273"
	c = 1

	def parse(self, response):
		sub_list = []
		data_json = json.loads(response.text)
		subs = data_json['items']
		for sub in subs:
			try:
				url='https://www.covenanthomeskc.com'+sub['fullUrl']
			except:
				url = ''

			try:
				name=sub['title']
			except Exception as e:
				print(' Error in  name',e)
				name= ''
			try:
				street1=sub['location']['addressLine1']
			except Exception as e:
				print(' Error in street',e)
				street1= ''
			try:
				temadd = (sub['location']['addressLine2']).split(',')
			except Exception as e:
				print(' Error in ',e)
				temadd = ''
			if len(temadd) == 2:
				try:
					city=temadd[0].strip()
				except Exception as e:
					print(' Error in  city',e)
					city= ''
				try:
					zipcode=temadd[1].strip()
				except Exception as e:
					print(' Error in zipcode',e)
					zipcode= ''
			else:
				try:
					city=temadd[0].strip()
				except Exception as e:
					print(' Error in  city',e)
					city= ''
				try:
					state=temadd[1].strip()
				except Exception as e:
					print(' Error in state',e)
					state= ''
				try:
					zipcode=temadd[2].strip()
				except Exception as e:
					print(' Error in zipcode',e)
					zipcode= ''
			try:
				phone=str(sub['customContent']['contactNo']).split('-')
			except Exception as e:
				print(' Error in phone',e)
				phone= ''
			try:
				areacode = phone[0].strip()
			except Exception as e:
				print(' Error in areacode',e)
				areacode = ''
			try:
				prefix = phone[1].strip()
			except Exception as e:
				print(' Error in prefix',e)
				prefix = ''
			try:
				suffix = phone[2].strip()
			except Exception as e:
				print(' Error in suffix',e)
				suffix = ''
			try:
				email = sub['customContent']['email']
			except Exception as e:
				print(' Error in email',e)
				email = ''
			try:
				des = remove_tags(sub['excerpt']).replace('&nbsp;','')
			except Exception as e:
				print(' Error in des',e)
				des = ''
			try:
				image = sub['customContent']['bannerimage']['assetUrl']
			except Exception as e:
				print(' Error in image',e)
				image = ''

			subdivisonNumber = int(hashlib.md5(bytes(name, "utf8")).hexdigest(), 16) % (10 ** 30)
			sub_list.append(subdivisonNumber)
			# name = response.xpath('//div[@class="home-title"]/h1/text()').get().strip()


			item = BdxCrawlingItem_subdivision()
			item['sub_Status'] = "Active"
			item['SubdivisionNumber'] = subdivisonNumber
			item['BuilderNumber'] = self.builderNumber
			item['SubdivisionName'] = name
			item['BuildOnYourLot'] = 0
			item['OutOfCommunity'] = 0
			item['Street1'] = street1
			item['City'] = city
			item['State'] = state
			item['ZIP'] = zipcode
			item['AreaCode'] = areacode
			item['Prefix'] = prefix
			item['Suffix'] = suffix
			item['Extension'] = ""
			item['AmenityType'] = ""
			item['Email'] = email
			item['SubDescription'] = des
			item['SubImage'] = image
			item['SubWebsite'] = url
			print(name, subdivisonNumber,self.c)
			self.c+=1
			if zipcode != '':
				yield item

		yield scrapy.Request(url='https://chris-horsefield-28ca.squarespace.com/homesfloorplans?format=json-pretty',callback=self.floorplane,dont_filter=True,meta={'sub_list':sub_list})

	def floorplane(self,response):
		data_js1= json.loads(response.text)
		plan_data = data_js1['items']
		sub_list = response.meta['sub_list']
		#
		# # pdata = json.loads(response.text)
		# # subdivison = response.meta['subdivison']
		plan_names = []
		for pdata in plan_data:
			try:
				url1 = pdata['fullUrl']
				plan_url = 'https://www.covenanthomeskc.com' + url1
			except:
				plan_url = ''
			try:
				plan_name = pdata['title']
				Type = 'SingleFamily'
				PlanNotAvailable = 0
				PlanTypeName = 'Single Family'
				base_price = 0
			except:
				plan_name = ''
			try:
				full_bath = pdata['customContent']['bathFull']
			except:
				full_bath = ''
			try:
				half_bath = pdata['customContent']['bathHalf']
				if half_bath == "":
					half_bath = '0'
			except:
				half_bath = ''
			try:
				bed = pdata['customContent']['bedRooms']
			except:
				bed = ''
			try:
				garage = pdata['customContent']['garages']

			except:
				garage = ''
			try:
				sqft = pdata['customContent']['approxSqFt']
			except:
				sqft = ''
			try:
				desc = pdata['customContent']['description']
				# desc = remove_tags(desc)
			except:
				desc = ''

			image=[]

			try:
				flor_img=pdata['customContent']['floorplanGallery']
				for i in flor_img:#items[7].customContent.floorplanGallery[0].assetUrl
					img_url = i['assetUrl']
					image.append(img_url)
			except Exception as e:
				print("Error in flor_img", e)

			try:
				add_img = pdata['customContent']['additionalImages']
				for i in add_img:
					img_add = i['assetUrl']
					image.append(img_add)
			except Exception as e:
				print("Error in add_img", e)

			try:
				main_img = pdata['assetUrl']
				image.append(main_img)
			except Exception as e:
				print("Error in main_img", e)

			final_image = '|'.join(image)

			for j in sub_list:
				PlanNumber = int(hashlib.md5(bytes(plan_name + str(j), "utf8")).hexdigest(), 16) % (10 ** 30)
				unique = str(PlanNumber) + str(j)
				unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
				# PlanDetails[plan_name] = unique_number
				item = BdxCrawlingItem_Plan()
				item['Type'] = Type
				item['PlanNumber'] = PlanNumber
				item['unique_number'] = unique_number
				item['SubdivisionNumber'] = j
				item['PlanName'] = plan_name
				item['PlanNotAvailable'] = PlanNotAvailable
				item['PlanTypeName'] = PlanTypeName
				item['BasePrice'] = base_price
				item['BaseSqft'] = sqft
				item['Baths'] = full_bath
				item['HalfBaths'] = half_bath
				item['Bedrooms'] = bed
				item['Garage'] = garage
				item['Description'] = desc
				item['ElevationImage'] = final_image
				item['PlanWebsite'] = plan_url
				plan_names.append((plan_name, unique_number))
				yield item


#<- ---------------------------------------------PRIYANKA'S CODE ---------------------------------------------------- ->


	# 		yield scrapy.Request(url='https://www.covenanthomeskc.com/homes-lots-for-sale?format=json-pretty',callback=self.spec_data,dont_filter=True,meta={'plan_names':plan_names})
	#
	# def spec_data(self, response):
	# 	plan_names = response.meta['plan_names']
	# 	# unique_number = response.meta['unique_number']
	#
	# 	sdata = json.loads(response.text)
	# 	for i in range(len(sdata)):
	# 		status = sdata[i]['inv_status']
	# 		if 'Under Construction' in status:
	# 			continue
	# 		try:
	# 			spec_street = sdata[i]['inv_street1']
	# 		except:
	# 			spec_street = ''
	# 		try:
	# 			spec_city = sdata[i]['city_name']
	# 		except:
	# 			spec_city = ''
	# 		try:
	# 			spec_state = sdata[i]['state_code']
	# 		except:
	# 			spec_state = ''
	# 		try:
	# 			spec_zip = sdata[i]['inv_zip']
	# 		except:
	# 			spec_zip = ''
	# 		try:
	# 			spec_price = sdata[i]['inv_price']
	# 		except:
	# 			spec_price = ''
	# 		try:
	# 			spec_sqft = sdata[i]['inv_sqft']
	# 		except:
	# 			spec_sqft = ''
	# 		try:
	# 			s_bed = sdata[i]['inv_beds']
	# 		except:
	# 			s_bed = ''
	# 		try:
	# 			s_full_bath = sdata[i]['inv_baths']
	# 		except:
	# 			s_full_bath = ''
	# 		try:
	# 			s_half_bath = sdata[i]['inv_halfBaths']
	# 		except:
	# 			s_half_bath = ''
	# 		try:
	# 			s_garage = sdata[i]['inv_garages']
	# 		except:
	# 			s_garage = ''
	# 		try:
	# 			s_desc = sdata[i]['inv_description']
	# 			s_desc = remove_tags(s_desc)
	# 		except:
	# 			s_desc = ''
	# 		try:
	# 			spec_url = sdata[i]['url']
	# 			spec_url = 'https://www.encorehomesinc.com' + spec_url
	# 		except:
	# 			spec_url = ''
	# 		try:
	# 			plan_name1 = sdata[i]['mod_name']
	# 		except:
	# 			plan_name1 = ''
	#
	# 		img_url1 = []
	# 		try:
	# 			photos = sdata[i]['photos']
	# 			for j in range(len(photos)):
	# 				img_url = photos[j]['imageSource']
	# 				img_url = 'https://www.encorehomesinc.com/' + img_url
	# 				img_url1.append(img_url)
	# 			img_url1 = '|'.join(img_url1)
	# 		except Exception as e:
	# 			print("Error in Spec_image", e)
	#
	# 		unique = spec_street + spec_city + spec_state + spec_zip
	# 		SpecNumber = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)
	#
	# 		for p in plan_names:
	# 			if p[0] == plan_name1:
	# 				PlanNumber = p[1]
	#
	# 			# PlanNumber = int(hashlib.md5(bytes(, "utf8")).hexdigest(), 16) % (10 ** 30)
	#
	# 			try:
	# 				item = BdxCrawlingItem_Spec()
	# 				item['SpecNumber'] = SpecNumber
	# 				item['PlanNumber'] = PlanNumber
	# 				item['SpecStreet1'] = spec_street
	# 				item['SpecCity'] = spec_city
	# 				item['SpecState'] = spec_state
	# 				item['SpecZIP'] = spec_zip
	# 				item['SpecCountry'] = "USA"
	# 				item['SpecPrice'] = spec_price
	# 				item['SpecSqft'] = spec_sqft
	# 				item['SpecBaths'] = s_full_bath
	# 				item['SpecHalfBaths'] = s_half_bath
	# 				item['SpecBedrooms'] = s_bed
	# 				item['MasterBedLocation'] = "Down"
	# 				item['SpecGarage'] = s_garage
	# 				item['SpecDescription'] = s_desc
	# 				item['SpecElevationImage'] = img_url1
	# 				item['SpecWebsite'] = spec_url
	# 				yield item
	# 			except:
	# 				print("*******************Home*****************")


#<- ---------------------------------------------PRIYANKA'S CODE ---------------------------------------------------- ->



		# links =[ i for i in set(response.xpath('//*[@class="sqs-block-content"]/div[@id="neighborhoods"]/div//a/@href').getall()) if 'http' not in i]
		# for i in links:
		# 	yield scrapy.Request(url=i,callback=self.parse2,dont_filter=True)

		# IF you do not have Communities and you are creating the one
		# ------------------- If No communities found ------------------- #

		# f = open("html/%s.html" % self.builderNumber, "wb")
		# f.write(response.body)
		# f.close()
if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl covenanthomeskc".split())