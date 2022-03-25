import hashlib
import re
import scrapy
import requests
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from w3lib.http import basic_auth_header

class DavelargentHomesSpider(scrapy.Spider):
    name = 'DaveLargentHomes'
    allowed_domains = []
    start_urls = ['https://www.davelargenthomes.com/']
    builderNumber = 37684

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
        item['Street1'] = '1402 N. River Vista Street'
        item['City'] = 'Spokane'
        item['State'] = 'WA'
        item['ZIP'] = '99224'
        item['AreaCode'] = '509'
        item['Prefix'] ='999'
        item['Suffix'] = '9794'
        item['Extension'] = ""
        item['Email'] ='dlhomes@comcast.net'
        item['SubDescription'] ="Dave and his crews made the experience very enjoyable and we would highly recommend him to anyone!"
        item['SubImage']= 'https://static.wixstatic.com/media/e05021_d83b8e9eeffa46ffabbdc2c697379168.png/v1/fill/w_945,h_500,al_c,q_90/e05021_d83b8e9eeffa46ffabbdc2c697379168.webp|https://static.wixstatic.com/media/e05021_e9dafefe7bcb4d87b4f810bc3e1a3228.png/v1/fill/w_945,h_500,al_c,q_90/e05021_e9dafefe7bcb4d87b4f810bc3e1a3228.webp|https://static.wixstatic.com/media/e05021_a4f21e135ae1bae7eb8066222906d3a3.png/v1/fill/w_945,h_500,al_c,q_90/e05021_a4f21e135ae1bae7eb8066222906d3a3.webp|https://static.wixstatic.com/media/e05021_9856bace3b0c72d3ff34d2db76ab6334.png/v1/fill/w_945,h_500,al_c,q_90/e05021_9856bace3b0c72d3ff34d2db76ab6334.webp'
        item['SubWebsite'] = response.url
        yield item

        planlinks = ['https://www.davelargenthomes.com/the-chelan','https://www.davelargenthomes.com/copy-of-the-chelan','https://www.davelargenthomes.com/dresden','https://www.davelargenthomes.com/taylor-creek','https://www.davelargenthomes.com/rosewood','https://www.davelargenthomes.com/ashley','https://www.davelargenthomes.com/river-ridge']
        for planlink in planlinks:
            # a = 'https://www.davelargenthomes.com/the-chelan'
            yield scrapy.FormRequest(url=planlink,callback=self.planDetail)

    def planDetail(self,response):
        print(response.url)
        # if response.url == 'https://www.davelargenthomes.com/the-chelan':
        #     PlanName = str(response.url).split('/')[-1].replace('-', ' ')
        #     PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        #     SubdivisionNumber = self.builderNumber
        #     unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        #     unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        #     item = BdxCrawlingItem_Plan()
        #     item['Type'] = 'SingleFamily'
        #     item['PlanNumber'] = PlanNumber
        #     item['unique_number'] = unique_number  # < -------- Changes here
        #     item['SubdivisionNumber'] = SubdivisionNumber
        #     item['PlanName'] = PlanName
        #     item['PlanNotAvailable'] = '0'
        #     item['PlanTypeName'] = 'Single Family'
        #     item['BasePrice'] = '0'
        #     item['BaseSqft'] = '3570'
        #     item['Baths'] = '3'
        #     item['HalfBaths'] = '0'
        #     item['Bedrooms'] = '5'
        #     item['Garage'] = '3'
        #     item[
        #         'Description'] = 'Vaulted covered back deck,Large covered front porch,Vaulted ceiling in great room,Floor-to-ceiling stone fireplace,Large kitchen with island, pantry, & double ovens,Large master suite with soaking tub & walk-in shower'
        #     item['ElevationImage'] = "https://static.wixstatic.com/media/a3b9ec_138b994919bc4440983501c36c17d3f1~mv2.jpg/v1/fill/w_610,h_370,al_c,q_80,usm_0.66_1.00_0.01/a3b9ec_138b994919bc4440983501c36c17d3f1~mv2.webp|https://static.wixstatic.com/media/a3b9ec_8ac70bd6ad7b413aaade5d4c60e9d84f~mv2.jpeg/v1/fill/w_319,h_323,al_c,q_80,usm_0.66_1.00_0.01/a3b9ec_8ac70bd6ad7b413aaade5d4c60e9d84f~mv2.webp|https://static.wixstatic.com/media/a3b9ec_596a171089af47ab885001ce8e1a32a1~mv2.jpeg/v1/fill/w_318,h_323,al_c,q_80,usm_0.66_1.00_0.01/a3b9ec_596a171089af47ab885001ce8e1a32a1~mv2.webp"
        #     item['PlanWebsite'] = response.url
        #     yield item
        #
        # elif response.url == 'https://www.davelargenthomes.com/copy-of-the-chelan':
        #     PlanName = str(response.url).split('/')[-1].replace('-', ' ')
        #     PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        #     SubdivisionNumber = self.builderNumber
        #     unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        #     unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        #     item = BdxCrawlingItem_Plan()
        #     item['Type'] = 'SingleFamily'
        #     item['PlanNumber'] = PlanNumber
        #     item['unique_number'] = unique_number  # < -------- Changes here
        #     item['SubdivisionNumber'] = SubdivisionNumber
        #     item['PlanName'] = PlanName
        #     item['PlanNotAvailable'] = '0'
        #     item['PlanTypeName'] = 'Single Family'
        #     item['BasePrice'] = '0'
        #     item['BaseSqft'] = '3295'
        #     item['Baths'] = '3'
        #     item['HalfBaths'] = '0'
        #     item['Bedrooms'] = '5'
        #     item['Garage'] = '3'
        #     item['Description'] = "Oversized master suite with double vanity, walk-in shower, modern free standing soaking tub and walk-in closet,Custom chef's kitchen with solid surface countertops and stainless steel appliances,Large vaulted covered back deck with gorgeous views,11 tall great room with box beam ceiling, modern fireplace and 12 sliding glass door, Partially staged"
        #     item['ElevationImage'] = "https://static.wixstatic.com/media/a3b9ec_36ba27cc961246b2bf2766a913734104~mv2.jpg/v1/fill/w_829,h_553,al_c,q_90,usm_0.66_1.00_0.01/a3b9ec_36ba27cc961246b2bf2766a913734104~mv2.webp|https://static.wixstatic.com/media/a3b9ec_c3054ba7ecb04bb7a7535b1b363a52f9~mv2.jpg/v1/fill/w_829,h_553,al_c,q_90,usm_0.66_1.00_0.01/a3b9ec_c3054ba7ecb04bb7a7535b1b363a52f9~mv2.webp|https://static.wixstatic.com/media/a3b9ec_50d76ef901654d4e9ea3444c90430178~mv2.jpg/v1/fill/w_829,h_553,al_c,q_90,usm_0.66_1.00_0.01/a3b9ec_50d76ef901654d4e9ea3444c90430178~mv2.webp|https://static.wixstatic.com/media/a3b9ec_8d3251b768e9474e8f9ffbfa892fa93e~mv2.jpg/v1/fill/w_829,h_553,al_c,q_90,usm_0.66_1.00_0.01/a3b9ec_8d3251b768e9474e8f9ffbfa892fa93e~mv2.webp|https://static.wixstatic.com/media/a3b9ec_73a7393ccf894a1db9ef515b220e582b~mv2.jpg/v1/fill/w_829,h_553,al_c,q_90,usm_0.66_1.00_0.01/a3b9ec_73a7393ccf894a1db9ef515b220e582b~mv2.webp|https://static.wixstatic.com/media/a3b9ec_b3297f362e774395b9a3ef9eb63ebdc2~mv2.jpg/v1/fill/w_319,h_323,al_c,q_80,usm_0.66_1.00_0.01/a3b9ec_b3297f362e774395b9a3ef9eb63ebdc2~mv2.webp|https://static.wixstatic.com/media/a3b9ec_5dc415dee34644f49814397cb6274a5d~mv2.jpg/v1/fill/w_318,h_323,al_c,q_80,usm_0.66_1.00_0.01/a3b9ec_5dc415dee34644f49814397cb6274a5d~mv2.webp"
        #     item['PlanWebsite'] = response.url
        #     yield item
        #
        # elif response.url == 'https://www.davelargenthomes.com/dresden':
        #     PlanName = str(response.url).split('/')[-1].replace('-', ' ')
        #     PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        #     SubdivisionNumber = self.builderNumber
        #     unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        #     unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        #     item = BdxCrawlingItem_Plan()
        #     item['Type'] = 'SingleFamily'
        #     item['PlanNumber'] = PlanNumber
        #     item['unique_number'] = unique_number  # < -------- Changes here
        #     item['SubdivisionNumber'] = SubdivisionNumber
        #     item['PlanName'] = PlanName
        #     item['PlanNotAvailable'] = '0'
        #     item['PlanTypeName'] = 'Single Family'
        #     item['BasePrice'] = '0'
        #     item['BaseSqft'] = '3212'
        #     item['Baths'] = '3'
        #     item['HalfBaths'] = '0'
        #     item['Bedrooms'] = '4'
        #     item['Garage'] = '4'
        #     item['Description'] = "Spacious great room w/ vaulted ceiling Hardwood floors in entry, kitchen, dining room and hall Island kitchen w/ granite countertops walk-in pantry & stainless steel appliances Large master suite with walk-in shower,soaking tub, and walk-in closet Fully finished basement with 4 beds and large Rec Room,Vaulted covered deck off of dining room,Front yard landscaping included"
        #     item['ElevationImage'] = "https://static.wixstatic.com/media/e05021_15352e2c94133ec7bd770c8560e7d131.png/v1/fill/w_610,h_370,al_c,q_85/e05021_15352e2c94133ec7bd770c8560e7d131.webp|https://static.wixstatic.com/media/e05021_c1c3e4120744f9619ede176ed84f207a.png/v1/fill/w_618,h_321,al_c,q_85,usm_0.66_1.00_0.01/e05021_c1c3e4120744f9619ede176ed84f207a.webp"
        #     item['PlanWebsite'] = response.url
        #     yield item
        #
        # elif response.url == 'https://www.davelargenthomes.com/taylor-creek':
        #     PlanName = str(response.url).split('/')[-1].replace('-', ' ')
        #     PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        #     SubdivisionNumber = self.builderNumber
        #     unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        #     unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        #     item = BdxCrawlingItem_Plan()
        #     item['Type'] = 'SingleFamily'
        #     item['PlanNumber'] = PlanNumber
        #     item['unique_number'] = unique_number  # < -------- Changes here
        #     item['SubdivisionNumber'] = SubdivisionNumber
        #     item['PlanName'] = PlanName
        #     item['PlanNotAvailable'] = '0'
        #     item['PlanTypeName'] = 'Single Family'
        #     item['BasePrice'] = '0'
        #     item['BaseSqft'] = '3204'
        #     item['Baths'] = '3'
        #     item['HalfBaths'] = '0'
        #     item['Bedrooms'] = '4'
        #     item['Garage'] = '3'
        #     item['Description'] = "Spacious Great Room w/ vaulted ceiling Hardwood floors in entry, kitchen, dining room and hall Island Kitchen w/ granite countertops walk-in pantry & double ovens Large Master Suite with walk-in shower,granite vanity, and walk-in closet Fully finished basement with 2 bedrooms and large family room Covered front porch and back deck,Front yard landscaping included"
        #     item['ElevationImage'] = "https://static.wixstatic.com/media/e05021_b779ac90ccb54a57a8e4993d131f547e.png/v1/fill/w_610,h_370,al_c,q_95/e05021_b779ac90ccb54a57a8e4993d131f547e.webp|https://static.wixstatic.com/media/e05021_4f2a224f116e8062504b23c973040d2f.png/v1/fill/w_610,h_370,al_c,q_95/e05021_4f2a224f116e8062504b23c973040d2f.webp|https://static.wixstatic.com/media/e05021_020ee1e5e8294075a2e8232a8ef04830.png/v1/fill/w_610,h_370,al_c,q_95/e05021_020ee1e5e8294075a2e8232a8ef04830.webp|https://static.wixstatic.com/media/e05021_7fc88e50993572892e6edc0de3480949.png/v1/fill/w_610,h_370,al_c,q_95/e05021_7fc88e50993572892e6edc0de3480949.webp|https://static.wixstatic.com/media/e05021_321c34a41c0398a94d9e528ebdb5d48a.png/v1/fill/w_615,h_313,al_c,q_85,usm_0.66_1.00_0.01/e05021_321c34a41c0398a94d9e528ebdb5d48a.webp"
        #     item['PlanWebsite'] = response.url
        #     yield item
        #
        # elif response.url == 'https://www.davelargenthomes.com/rosewood':
        #     PlanName = str(response.url).split('/')[-1].replace('-', ' ')
        #     PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        #     SubdivisionNumber = self.builderNumber
        #     unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        #     unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        #     item = BdxCrawlingItem_Plan()
        #     item['Type'] = 'SingleFamily'
        #     item['PlanNumber'] = PlanNumber
        #     item['unique_number'] = unique_number  # < -------- Changes here
        #     item['SubdivisionNumber'] = SubdivisionNumber
        #     item['PlanName'] = PlanName
        #     item['PlanNotAvailable'] = '0'
        #     item['PlanTypeName'] = 'Single Family'
        #     item['BasePrice'] = '0'
        #     item['BaseSqft'] = '3426'
        #     item['Baths'] = '3'
        #     item['HalfBaths'] = '0'
        #     item['Bedrooms'] = '5'
        #     item['Garage'] = '3'
        #     item['Description'] = "Spacious Great Room with natural stone fireplace Custom Chef's Kitchen with granite counters and stainless steel appliances Large Master Suite with large soaker tub in the bathroom and walk-in closet"
        #     item['ElevationImage'] = "https://static.wixstatic.com/media/e05021_203f123e3556e0d1178e1b443c7f0a67.png/v1/fill/w_610,h_370,al_c,q_95/e05021_203f123e3556e0d1178e1b443c7f0a67.webp|https://static.wixstatic.com/media/e05021_3a1023aa5836a07aa8f7054bf86876b4.png/v1/fill/w_610,h_370,al_c,q_95/e05021_3a1023aa5836a07aa8f7054bf86876b4.webp|https://static.wixstatic.com/media/e05021_8704a9ba0215578779d90a5dd327770c.png/v1/fill/w_610,h_370,al_c,q_95/e05021_8704a9ba0215578779d90a5dd327770c.webp|https://static.wixstatic.com/media/e05021_50c8853c8597117e6fc2a024fde780db.png/v1/fill/w_610,h_370,al_c,q_95/e05021_50c8853c8597117e6fc2a024fde780db.webp|https://static.wixstatic.com/media/e05021_ca70f09e745b05ab4fdfa49786bebe10.png/v1/fill/w_610,h_370,al_c,q_95/e05021_ca70f09e745b05ab4fdfa49786bebe10.webp|https://static.wixstatic.com/media/e05021_365c6fef4505ba5ea0ced6b50fcab45e.png/v1/fill/w_612,h_400,al_c,q_85,usm_0.66_1.00_0.01/e05021_365c6fef4505ba5ea0ced6b50fcab45e.webp"
        #     item['PlanWebsite'] = response.url
        #     yield item
        #
        # elif response.url == 'https://www.davelargenthomes.com/ashley':
        #     PlanName = str(response.url).split('/')[-1].replace('-', ' ')
        #     PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        #     SubdivisionNumber = self.builderNumber
        #     unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        #     unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        #     item = BdxCrawlingItem_Plan()
        #     item['Type'] = 'SingleFamily'
        #     item['PlanNumber'] = PlanNumber
        #     item['unique_number'] = unique_number  # < -------- Changes here
        #     item['SubdivisionNumber'] = SubdivisionNumber
        #     item['PlanName'] = PlanName
        #     item['PlanNotAvailable'] = '0'
        #     item['PlanTypeName'] = 'Single Family'
        #     item['BasePrice'] = '0'
        #     item['BaseSqft'] = '3718'
        #     item['Baths'] = '3'
        #     item['HalfBaths'] = '0'
        #     item['Bedrooms'] = '5'
        #     item['Garage'] = '4'
        #     item['Description'] = "Spacious Great Room w/ vaulted ceiling Hardwood floors in entry, kitchen, dining room and hall Island Kitchen w/ granite countertops walk-in pantry & double ovens Large Master Suite with walk-in shower,granite vanity, and walk-in closet Fully finished basement with 2 bedrooms and large family room Covered front porch and back deck,Front yard landscaping included"
        #     item['ElevationImage'] = "https://static.wixstatic.com/media/e05021_ea15baef361c138e9d8f6347224cdc9f.png/v1/fill/w_610,h_370,al_c,q_95/e05021_ea15baef361c138e9d8f6347224cdc9f.webp|https://static.wixstatic.com/media/e05021_1d5da7b1a247572464ab5f335d6c1800.png/v1/fill/w_610,h_370,al_c,q_95/e05021_1d5da7b1a247572464ab5f335d6c1800.webp|https://static.wixstatic.com/media/e05021_a91ee64d792ba998e1408f62b0d78aa0.png/v1/fill/w_610,h_370,al_c,q_95/e05021_a91ee64d792ba998e1408f62b0d78aa0.webp|https://static.wixstatic.com/media/e05021_9ea574af7cb6b0d7d0b878bc4cf0e6b8.png/v1/fill/w_610,h_370,al_c,q_95/e05021_9ea574af7cb6b0d7d0b878bc4cf0e6b8.webp|https://static.wixstatic.com/media/e05021_b8e04a5b46a0ad9fd7254a6f2d96b7bf.png/v1/fill/w_610,h_370,al_c,q_95/e05021_b8e04a5b46a0ad9fd7254a6f2d96b7bf.webp|https://static.wixstatic.com/media/e05021_a9556480d716694fa614d69f050f17ff.png/v1/fill/w_610,h_370,al_c,q_95/e05021_a9556480d716694fa614d69f050f17ff.webp|https://static.wixstatic.com/media/e05021_189f79314e3cbfcfc326e5b96f8dbb28.png/v1/fill/w_612,h_393,al_c,q_85,usm_0.66_1.00_0.01/e05021_189f79314e3cbfcfc326e5b96f8dbb28.webp"
        #     item['PlanWebsite'] = response.url
        #     yield item
        #
        # elif response.url == 'https://www.davelargenthomes.com/river-ridge':
        #     PlanName = str(response.url).split('/')[-1].replace('-', ' ')
        #     PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        #     SubdivisionNumber = self.builderNumber
        #     unique = str(PlanNumber) + str(SubdivisionNumber)  # < -------- Changes here
        #     unique_number = int(hashlib.md5(bytes(unique, "utf8")).hexdigest(), 16) % (10 ** 30)  # < -------- Changes here
        #     item = BdxCrawlingItem_Plan()
        #     item['Type'] = 'SingleFamily'
        #     item['PlanNumber'] = PlanNumber
        #     item['unique_number'] = unique_number  # < -------- Changes here
        #     item['SubdivisionNumber'] = SubdivisionNumber
        #     item['PlanName'] = PlanName
        #     item['PlanNotAvailable'] = '0'
        #     item['PlanTypeName'] = 'Single Family'
        #     item['BasePrice'] = '0'
        #     item['BaseSqft'] = '3724'
        #     item['Baths'] = '2'
        #     item['HalfBaths'] = '1'
        #     item['Bedrooms'] = '5'
        #     item['Garage'] = '3'
        #     item['Description'] = "Spacious Great Room w/ vaulted ceiling Hardwood floors in entry, kitchen, dining room and hall Island Kitchen w/ granite countertops walk-in pantry & double ovens Large Master Suite with walk-in shower,granite vanity, and walk-in closet Fully finished basement with 2 bedrooms and large family room Covered front porch and back deck,Front yard landscaping included"
        #     item['ElevationImage'] = "https://static.wixstatic.com/media/e05021_3093ff4271a4c47f2d86e03edf82baba.png/v1/fill/w_610,h_370,al_c,q_95/e05021_3093ff4271a4c47f2d86e03edf82baba.webp|https://static.wixstatic.com/media/e05021_0f946508e7100630745bcf3e943891d7.png/v1/fill/w_610,h_370,al_c,q_95/e05021_0f946508e7100630745bcf3e943891d7.webp|https://static.wixstatic.com/media/e05021_bd02de5ccd6d422d17a6372ee668cbc4.png/v1/fill/w_610,h_370,al_c,q_95/e05021_bd02de5ccd6d422d17a6372ee668cbc4.webp|https://static.wixstatic.com/media/e05021_a6419fc5e7eac5647d5d7d0bb3bf6e82.png/v1/fill/w_610,h_370,al_c,q_95/e05021_a6419fc5e7eac5647d5d7d0bb3bf6e82.webp|https://static.wixstatic.com/media/e05021_e0e205fe5bd309050bd5780f017b07e5.png/v1/fill/w_610,h_370,al_c,q_95/e05021_e0e205fe5bd309050bd5780f017b07e5.webp|https://static.wixstatic.com/media/e05021_629186c12351c7bc3e7c88b3d7012c72.png/v1/fill/w_610,h_370,al_c,q_95/e05021_629186c12351c7bc3e7c88b3d7012c72.webp|https://static.wixstatic.com/media/e05021_158c616c3647cbce8bb79f877c34365b.png/v1/fill/w_610,h_370,al_c,q_95/e05021_158c616c3647cbce8bb79f877c34365b.webp|https://static.wixstatic.com/media/e05021_9e35ff86fa50b9900319f305243d8842.png/v1/fill/w_610,h_370,al_c,q_95/e05021_9e35ff86fa50b9900319f305243d8842.webp|https://static.wixstatic.com/media/e05021_89ee9865e685e5509badf88ceb067536.png/v1/fill/w_625,h_642,al_c,q_90/e05021_89ee9865e685e5509badf88ceb067536.webp"
        #     item['PlanWebsite'] = response.url
        #     yield item


        try:
            PlanName = str(response.url).split('/')[-1].replace('-',' ')
            if PlanName == None:
                PlanName = response.xpath('//*[@class="txtNew"]/h2/span/text()').extract_first()
                if PlanName == None:
                    PlanName = response.xpath('//*[@class="c24sd_hjizu7wainlineContent"]/div/h2/text()').extract_first()
            print(PlanName)
        except Exception as e:
            print("PlanName: ", e)
        try:
            Type = 'SingleFamily'
        except Exception as e:
            print(e)

        try:
            PlanNumber = int(hashlib.md5(bytes(PlanName, "utf8")).hexdigest(), 16) % (10 ** 30)
        except Exception as e:
            print(e)

        try:
            SubdivisionNumber = self.builderNumber
            print(SubdivisionNumber)
        except Exception as e:
            print(str(e))

        try:
            PlanNotAvailable = 0
        except Exception as e:
            print(e)

        try:
            PlanTypeName = 'Single Family'
        except Exception as e:
            print(e)

        try:
            BasePrice = 0
        except Exception as e:
            print(str(e))

        try:
            PlanWebsite = response.url
        except Exception as e:
            print(e)
        try:
            Bedroo = response.xpath(
                '//*[contains(text(),"bedrooms")]/text()').extract_first()
            Bedroom = Bedroo.split('&')[0]
            Bedrooms = re.findall(r"(\d+)",Bedroom)[0]
            if PlanName == 'the chelan':
                Bedrooms = '5'
        except Exception as e:
            Bedrooms = 0
            print("Bedrooms: ", e)

        try:
            Bathroo = response.xpath(
                '//*[contains(text(),"bathrooms")]/text()').extract_first().strip()
            if PlanName == 'Chelan':
                Baths = '3'
                HalfBaths = 0
            Bathroom = Bathroo.split('&')[1]
            Baths = Bathroom.split('bed')[0]
            tmp = re.findall(r"(\d+)", Baths)
            Baths = tmp[0]
            if len(tmp) > 1:
                HalfBaths = 1
            else:
                HalfBaths = 0

        except Exception as e:
            Baths = 0
            print("Baths: ", e)

        try:
            Garage = response.xpath('//*[contains(text(),"-car")]/text()').extract_first()
            if PlanName == 'the chelan':
                Garage = '3'
            Garage = Garage.split('-car')[0]
        except Exception as e:
            Garage = 0
        try:
            # if PlanName == '':
            #     BaseSqft = "a"
            # elif PlanName == '':
            BaseSqft = response.xpath('//*[contains(text(),"Total Square Feet:")]/../../div[6]/p[3]/text()').extract_first()
            if BaseSqft == None or BaseSqft == '':
                BaseSqft = response.xpath('//*[contains(text(),"Total Square Feet:")]/../../../../div[5]/p[3]/text()').extract_first()
            if PlanName == 'dresden':
                BaseSqft = '3212'
            if PlanName == 'taylor creek':
                BaseSqft = '3204'
            if PlanName == 'the chelan':
                BaseSqft = '3570'
            BaseSqft = BaseSqft.replace(',', '').strip()
            BaseSqft = re.findall(r"(\d+)", BaseSqft)[0]
            BaseSqft = BaseSqft.strip()
            print(BaseSqft)
        except Exception as e:
            BaseSqft = 0
            print("BaseSQFT: ", e)

        try:
            ElevationImages = []
            e1 = response.xpath('//*[@itemprop="image"]/@src').getall()
            e2 = response.xpath('//div[@class="ssg1itemsContainer"]/div/a/@href').getall()
            ElevationImage = e1 + e2
            if PlanName == 'Chelan':
                ElevationImages = 'https://static.wixstatic.com/media/a3b9ec_138b994919bc4440983501c36c17d3f1~mv2.jpg/v1/fill/w_610,h_370,al_c,q_80,usm_0.66_1.00_0.01/a3b9ec_138b994919bc4440983501c36c17d3f1~mv2.webp|https://static.wixstatic.com/media/a3b9ec_596a171089af47ab885001ce8e1a32a1~mv2.jpeg/v1/fill/w_318,h_323,al_c,q_80,usm_0.66_1.00_0.01/a3b9ec_596a171089af47ab885001ce8e1a32a1~mv2.webp|https://static.wixstatic.com/media/a3b9ec_8ac70bd6ad7b413aaade5d4c60e9d84f~mv2.jpeg/v1/fill/w_319,h_323,al_c,q_80,usm_0.66_1.00_0.01/a3b9ec_8ac70bd6ad7b413aaade5d4c60e9d84f~mv2.webp'
            for ElevationImag in ElevationImage:
                # print(ElevationImage)
                ElevationImages.append(ElevationImag)
            ElevationImages = "|".join(ElevationImages)
        except Exception as e:
            print(str(e))

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
        item[
            'Description'] = 'We have access to building sites, in nearly every development in the area! Bring us your custom home plans or choose from one of the many popular plans in our library. Click one of the thumbnails below for a PDF sheet with full details.'
        item['ElevationImage'] = ElevationImages
        item['PlanWebsite'] = PlanWebsite
        yield item

if __name__ == '__main__':
    execute("scrapy crawl DaveLargentHomes".split())