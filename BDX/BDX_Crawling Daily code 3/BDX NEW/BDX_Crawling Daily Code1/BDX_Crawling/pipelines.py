# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import time
from pprint import pprint
import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pymongo
import MySQLdb as pymysql
import os
from datetime import datetime
from elasticsearch import Elasticsearch
from BDX_Crawling.items import BdxCrawlingItem_subdivision, BdxCrawlingItem_Plan, BdxCrawlingItem_Spec
from BDX_Crawling import database_config as dbc
from BDX_Crawling.export_xml import genxml
from BDX_Crawling.validate import validate
from scrapy.exceptions import DropItem


class BdxCrawlingPipeline(object):
    subCount = planCount = specCount = 0
    initsub = 0

    # def __init__(self):

    def open_spider(self, spider):
        super(BdxCrawlingPipeline, self).__init__()
        self.xmlFolder = "xml/xml_%s" % datetime.now().strftime("%Y_%m_%d")

        if not os.path.exists(self.xmlFolder):
            os.makedirs(self.xmlFolder)
        if not os.path.exists("html"):
            os.makedirs("html")

        try:
            con = pymysql.connect(dbc.host, dbc.usernm, dbc.passwd)
            con.cursor().execute(f"DROP DATABASE IF EXISTS {dbc.database.format(spider.name)};")
            con.commit()
            con.close()
            print(f"{dbc.database.format(spider.name)} is Droped If Existed")
            # con.cursor().execute("CREATE DATABASE IF NOT EXISTS %s;" % (dbc.database))
        except Exception as e:
            print(e)
        time.sleep(3)
        try:
            con = pymysql.connect(dbc.host, dbc.usernm, dbc.passwd)
            con.cursor().execute(f"CREATE DATABASE IF NOT EXISTS {dbc.database.format(spider.name)};")
            con.commit()
            con.close()
            print(f"{dbc.database.format(spider.name)} is Created")
        except Exception as e:
            print(e)

        try:
            con = pymysql.connect(dbc.host, dbc.usernm, dbc.passwd, dbc.database.format(spider.name))
            con.cursor().execute(dbc.create_query)
            con.cursor().execute(dbc.create_query2)
            con.cursor().execute(dbc.create_query3)
            con.cursor().execute(dbc.create_query4)
            con.cursor().execute(dbc.create_query5)
            con.cursor().execute(dbc.alt_table)
            con.cursor().execute(dbc.alt_table2)
            con.cursor().execute(dbc.alt_table3)
            con.cursor().execute(dbc.alt_table4)
            con.close()
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        con = pymysql.connect(dbc.host, dbc.usernm, dbc.passwd, dbc.database.format(spider.name))
        con.commit()
        try:
            if isinstance(item, BdxCrawlingItem_subdivision):
                if self.initsub == 0:
                    values = get_details(item['BuilderNumber'])
                    if values != 0:
                        print("builder number matched")
                        try:
                            self.brandName = values['BrandName']
                            self.outputFileName = values['OutputFile']
                            self.number = values['CorporateBuilderNumber']
                            self.State = values['CorporateState']
                            self.Name = values['CorporateName']
                            self.builderwebsite = values['BuilderWebsite']
                        except Exception as e:
                            print("error in mongo data", e)

                        if values['BrandLogo_Med'] == None:
                            values['BrandLogo_Med'] = ""

                    try:
                        qry = "INSERT INTO Corporation_Table (CorporateBuilderNumber, CorporateState, CorporateName) VALUES (%s, %s, %s)"
                        con.cursor().execute(qry, (
                        values['CorporateBuilderNumber'], values['CorporateState'], values['CorporateName']))
                        con.commit()
                    except Exception as e:
                        print(e)

                    try:
                        qry1 = "INSERT INTO Builder_Table (BuilderNumber, CorporateBuilderNumber, BrandName, BrandLogo_Med, ReportingName, DefaultLeadsEmail, BuilderWebsite) VALUES (%s, %s, %s, %s, %s, %s, %s)"

                        con.cursor().execute(qry1, (
                        values['BuilderNumber'], values['CorporateBuilderNumber'], values['BrandName'],
                        values['BrandLogo_Med'], values['ReportingName'], values['DefaultLeadsEmail'],
                        values['BuilderWebsite']))
                        con.commit()
                    except Exception as e:
                        print(e)

                    self.init = 1

                time = datetime.now().strftime("%Y-%m-%d %I:%M:%S")
                if item['SubdivisionName'] == "No Sub Division":
                    qry = "INSERT INTO Subdivision_Table (sub_Status, SubdivisionNumber, BuilderNumber, SubdivisionName, BuildOnYourLot, OutOfCommunity, Street1, City, State, ZIP, AreaCode, Prefix, Suffix, Extension, Email,AmenityType  , SubDescription, SubImages, SubWebsite, DownloadTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    con.cursor().execute(qry, (
                        item['sub_Status'], item['BuilderNumber'], item['BuilderNumber'], self.brandName,
                        item['BuildOnYourLot'], item['OutOfCommunity'], item['Street1'], item['City'],
                        item['State'], item['ZIP'], item['AreaCode'], item['Prefix'], item['Suffix'], item['Extension'],
                        item['Email'], item['AmenityType'], item['SubDescription'], item['SubImage'],
                        self.builderwebsite, time))

                    con.commit()
                    print("Data Inserted ...")
                    self.subCount = self.subCount + 1

                else:

                    if item['SubdivisionName'] != "":
                        qry = "INSERT INTO Subdivision_Table (sub_Status, SubdivisionNumber, BuilderNumber, SubdivisionName, BuildOnYourLot, OutOfCommunity, Street1, City, State, ZIP, AreaCode, Prefix, Suffix, Extension, Email, AmenityType, SubDescription, SubImages, SubWebsite, DownloadTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        con.cursor().execute(qry, (
                        item['sub_Status'], item['SubdivisionNumber'], item['BuilderNumber'], item['SubdivisionName'],
                        item['BuildOnYourLot'], item['OutOfCommunity'], item['Street1'], item['City'], item['State'],
                        item['ZIP'], item['AreaCode'], item['Prefix'], item['Suffix'], item['Extension'], item['Email'],
                        item['AmenityType'], item['SubDescription'], item['SubImage'], item['SubWebsite'], time))
                        con.commit()
                        print("Data Inserted ...")
                        self.subCount = self.subCount + 1
                    else:
                        raise DropItem("SubdivisionName must not be Blank\nDropping Item: %s ..." % item['Street1'])

            if isinstance(item, BdxCrawlingItem_Plan):
                try:
                    try:
                        item['BaseSqft'] = int(item['BaseSqft'])
                    except Exception as e:
                        item['BaseSqft'] = 0
                    if (500 < item['BaseSqft'] < 14000) or (item['BaseSqft'] == 0):
                        if item['PlanName'] == "":
                            raise DropItem("PlanName must not be Blank\nDropping Item: %s ..." % item['PlanWebsite'])
                        else:
                            time = datetime.now().strftime("%Y-%m-%d %I:%M:%S")
                            qry = "INSERT INTO Plan_Table (Type, PlanNumber, SubdivisionNumber, PlanName, PlanNotAvailable, PlanTypeName, BasePrice, BaseSqft, Baths, HalfBaths, Bedrooms, Garage, Description, ElevationImage, PlanWebsite, unique_number, DownloadTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            con.cursor().execute(qry, (
                                item['Type'], item['PlanNumber'], item['SubdivisionNumber'], item['PlanName'],
                                item['PlanNotAvailable'], item['PlanTypeName'], item['BasePrice'], item['BaseSqft'],
                                item['Baths'], item['HalfBaths'], item['Bedrooms'], item['Garage'], item['Description'],
                                item['ElevationImage'], item['PlanWebsite'], item['unique_number'], time))
                            con.commit()
                            print("Data Inserted ...")
                            self.planCount = self.planCount + 1
                    else:
                        raise DropItem("SQFT Must be between 500 and 14000\nDropping Item: %s ..." % item['PlanName'])


                except Exception as e:
                    print(e)
                    pprint(item)

            if isinstance(item, BdxCrawlingItem_Spec):
                try:
                    try:
                        item['SpecSqft'] = int(item['SpecSqft'])
                    except Exception as e:
                        item['SpecSqft'] = 0

                    if 0 < int(float(item['SpecPrice'])) < 39999:
                        raise DropItem(
                            "Price Must be either 0 or Graterthan 39999\nDropping Item: %s ..." % item['SpecStreet1'])
                    elif (500 < item['SpecSqft'] < 14000) or (item['SpecSqft'] == 0):

                        time = datetime.now().strftime("%Y-%m-%d %I:%M:%S")
                        qry = "INSERT INTO Spec_Table (SpecNumber, PlanNumber, SpacStreet1, SpacCity, SpecState, SpecZIP, SpecCountry, SpecPrice, SpecSqft, SpecBaths, SpecHalfBaths, SpecBedrooms, MasterBedLocation, SpecGarage, SpecDescription, SpecElevationImage, SpecWebsite, DownloadTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        con.cursor().execute(qry, (
                            item['SpecNumber'], item['PlanNumber'], item['SpecStreet1'], item['SpecCity'],
                            item['SpecState'], item['SpecZIP'], item['SpecCountry'], item['SpecPrice'],
                            item['SpecSqft'],
                            item['SpecBaths'], item['SpecHalfBaths'], item['SpecBedrooms'], item['MasterBedLocation'],
                            item['SpecGarage'], item['SpecDescription'], item['SpecElevationImage'],
                            item['SpecWebsite'],
                            time))
                        con.commit()
                        print("Data Inserted ...")
                        self.specCount = self.specCount + 1
                    else:
                        raise DropItem(
                            "SQFT Must be between 500 and 14000\nDropping Item: %s ..." % item['SpecStreet1'])

                except Exception as e:
                    print(e)
                    pprint(item)

        except Exception as e:
            print(e)

        return item

    def close_spider(self, spider):

        # self.outputFileName = self.outputFileName.replace("Xbyte", datetime.strftime(datetime.now(),"%Y%m%d_%H%M"))
        self.outputFileName = "%s/%s" % (self.xmlFolder, self.outputFileName)
        print(self.outputFileName)

        # ----------------------- generating xml File ----------------------
        isXML = genxml(dbc.host, dbc.usernm, dbc.passwd, dbc.database.format(spider.name), self.number, self.State, self.Name,self.outputFileName)

        if isXML == 1:
            # ----------------------- validating xml File ------------------
            isValidate = validate(self.outputFileName)
            if isValidate[0] == 0:
                os.remove("%s" % self.outputFileName)
                xmlnotvalidatedmail(self.outputFileName, isValidate[1])

            # else:
            #     try:
            #         Today = str(datetime.strftime(datetime.now(),"%Y_%m_%d"))
            #         session = ftplib.FTP('builderftp.newhomesource.com', 'basicautomated', 'kem3Xas')
            #         f = open("xml/%s" % self.outputFileName, "rb")
            #         session.storbinary('STOR ' + self.outputFileName, f)
            #         f.close()
            #         session.quit()
            #         print("File uploaded Successfully ...")
            #         kibanacountupload(self.outputFileName)
            #     except Exception as e:
            #         print(e)
            #         print("File Not Uploaded On FTP ...")


def get_details(builder_number):
    try:

        # print(builder_number)
        # master_con = pymongo.MongoClient('mongodb://nishant.b:Nishant#123@51.161.13.140:27017/?authSource=admin')
        # master_data = master_con["bdx_daily"].all_phase.find_one({'BuilderNumber': str(builder_number)})
        # # master_data = master_con["bdx_daily"].bdx_388site_trial2.find_one({'CorporateBuilderNumber': str(builder_number)})
        #
        # # temp_nishu = list(master_data)
        # # print(temp_nishu)
        #
        # results = master_data
        # return results

        url = 'https://0344c0c954b148c4a412c7cc64c80f00.us-east-1.aws.found.io:9243'
        user = 'elastic'
        password = "vhr4byyTWPcS9TYUN4vqUiYi"
        data_table = 'bdxstaticdata_2'

        es = Elasticsearch([url], http_auth=(user, password))

        search = {
            "query": {
                "match": {
                    "BuilderNumber": builder_number
                }
            }
        }
        print(search)

        results = es.search(index=data_table, body=search)
        # print(results)

        # results = {'BrandLogo_Med': 'http://www.busterbuilt.com/wp-content/uploads/2017/10/logomain.png', 'BrandName': 'Busterbuilt', 'BuilderNumber': '169997824428359468527692220082', 'BuilderWebsite': 'http://www.busterbuilt.com/', 'CorporateBuilderNumber': '347583766290227853564476213359', 'CorporateName': 'Busterbuilt', 'CorporateState': 'MT', 'DefaultLeadsEmail': 'leads@thebdx.com', 'OutputFile': 'Busterbuilt_Xbyte.xml', 'Phase': 'Phase-2', 'ReportingName': 'Busterbuilt'}
        return results['hits']['hits'][0]["_source"]

    except Exception as e:
        print("BuilderNumber Not Valid ...")
        return 0


def xmlnotvalidatedmail(filename, e):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))
    local_ip_address = s.getsockname()[0]
    today = datetime.strftime(datetime.now(), "%m/%d/%Y %I:%M %p")
    filename = filename.split('/')[-1]
    # emailId = "alerts.xbyteio@gmail.com"
    # emailpass = "Xbytealerts1234"

    emailId = "bdx.xbyte@gmail.com"
    emailpass = "Xbyte*1234"

    # send_to = ['maulik.kotadiya.xbyte@gmail.com']
    # cc = []

    send_to = [
        'nishantb.xbyte@gmail.com',

    ]

    cc = [
        # 'hiral.trivedi.xbyte@gmail.com',
        # 'alpesh.khalas.xbyte@gmail.com'
    ]

    body = """<!DOCTYPE html>
                <html>
                <head>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
                <style>
                #customers {
                  font-family: Arial, Helvetica, sans-serif;
                  border-collapse: collapse;
                  width: 100%;
                }

                #customers td, #customers th {
                  border: 1px solid #ddd;
                  padding: 8px;
                }

                #customers tr:nth-child(even){background-color: #f2f2f2;}

                #customers tr:hover {background-color: #ddd;}

                #customers th {
                  padding-top: 12px;
                  padding-bottom: 12px;
                  text-align: left;
                  background-color: #FF0000;
                  color: white;
                }
                .btn {
                  background-color: DodgerBlue;
                  border: none;
                  color: white;
                  padding: 12px 30px;
                  cursor: pointer;
                  font-size: 20px;
                }

                / Darker background on mouse-over /
                .btn:hover {
                  background-color: RoyalBlue;
                }
                </style>
                </head>
                <body>

                <table id="customers">
                  <tr>
                    <th colspan=2>BDX Error In File filenamex</th>
                  </tr>
                   <tr>
                    <td>FileName:</th>
                    <td>filenamex</th>
                  </tr>
                  <tr>
                    <td>Error:</th>
                    <td>errorx</th>
                  </tr>
                  <tr>
                    <td colspan=2>
                        <center>
                            <h2>File Not Generated...</h2>
                        </center>
                    </td>
                  </tr>
                </table>
                </body>
                </html>"""

    try:
        body = body.replace('filenamex', filename).replace('errorx', str(e))
        msg = MIMEMultipart()
        msg['From'] = emailId
        msg['To'] = ",".join(send_to)
        msg['CC'] = ",".join(cc)
        msg['Subject'] = "Bdx Not Validated File: %s" % str(today)
        msg.attach(MIMEText(body, 'html'))
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(emailId, emailpass)
        text = msg.as_string()
        s.sendmail(emailId, send_to + cc, text)
        print("Mail Sent ...")
        s.quit()
    except Exception as e:
        print(e)