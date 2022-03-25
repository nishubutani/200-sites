from datetime import datetime

host = "localhost"
usernm = "root"
passwd = ""
dddd= str(datetime.strftime(datetime.now(),"%Y_%m_%d"))
# database = "bdx_crawling_{}"+"_"+(dddd)
database = "bdx_crawling_{}"

create_query = """CREATE TABLE IF NOT EXISTS Corporation_Table (CorporateBuilderNumber varchar(30) NOT NULL,
                                                  CorporateState varchar(2) NOT NULL,
                                                  CorporateName varchar(40) NOT NULL,
                                                  PRIMARY KEY (CorporateBuilderNumber));"""

create_query2 = """CREATE TABLE IF NOT EXISTS Builder_Table (BuilderNumber varchar(30) NOT NULL,
                                              CorporateBuilderNumber varchar(30) NOT NULL,
                                              BrandName varchar(30) NOT NULL,
                                              BrandLogo_Med varchar(500) NOT NULL,
                                              ReportingName varchar(75) NOT NULL,
                                              DefaultLeadsEmail varchar(100) NOT NULL,
                                              BuilderWebsite varchar(255) NOT NULL,
                                              PRIMARY KEY (BuilderNumber));"""

create_query3 = """CREATE TABLE IF NOT EXISTS Subdivision_Table (sub_Status varchar(20) NOT NULL DEFAULT 'Active',
                                                  SubdivisionNumber varchar(30) NOT NULL,
                                                  BuilderNumber varchar(30) NOT NULL,
                                                  SubdivisionName varchar(60) NOT NULL,
                                                  BuildOnYourLot bool NOT NULL,
                                                  OutOfCommunity bool NOT NULL,
                                                  Street1 varchar(100) NOT NULL,
                                                  City varchar(40) NOT NULL,
                                                  State varchar(2) NOT NULL,
                                                  ZIP varchar(10) NOT NULL,
                                                  AreaCode varchar(3) NOT NULL,
                                                  Prefix varchar(3) NOT NULL,
                                                  Suffix varchar(4) NOT NULL,
                                                  Extension varchar(7),
                                                  Email varchar(50) NOT NULL,
                                                  AmenityType longtext NOT NULL,
                                                  SubDescription varchar(2000),
                                                  SubImages longtext NOT NULL,
                                                  SubWebsite varchar(255) NOT NULL,
                                                  DownloadTime text NOT NULL,
                                                  PRIMARY KEY (SubdivisionNumber));"""

create_query4 = """CREATE TABLE IF NOT EXISTS Plan_Table (Type varchar(20) NOT NULL DEFAULT 'SingleFamily',
                                            unique_number varchar(100) NOT NULL,
                                            PlanNumber varchar(30) NOT NULL,
                                            SubdivisionNumber varchar(30) NOT NULL,
                                            PlanName varchar(50) NOT NULL,
                                            PlanNotAvailable bool NOT NULL,
                                            PlanTypeName varchar(40) NOT NULL DEFAULT 'Single Family',
                                            BasePrice DECIMAL(10, 2) NOT NULL,
                                            BaseSqft int NOT NULL,
                                            Baths int NOT NULL,
                                            HalfBaths int NOT NULL,
                                            Bedrooms int NOT NULL,
                                            Garage DECIMAL(4, 1) NOT NULL,
                                            Description varchar(1500) NOT NULL,
                                            ElevationImage longtext NOT NULL,
                                            PlanWebsite varchar(255) NOT NULL,
                                            DownloadTime text NOT NULL,
                                            PRIMARY KEY (unique_number));"""

create_query5 = """CREATE TABLE IF NOT EXISTS Spec_Table (SpecNumber varchar(30) NOT NULL,
                                            PlanNumber varchar(30) NOT NULL,
                                            SpacStreet1 varchar(100) NOT NULL,
                                            SpacCity varchar(40) NOT NULL,
                                            SpecState varchar(2) NOT NULL,
                                            SpecZip varchar(10) NOT NULL,
                                            SpecCountry varchar(3) NOT NULL DEFAULT 'USA',
                                            SpecPrice DECIMAL(10, 2) NOT NULL,
                                            SpecSqft int NOT NULL,
                                            SpecBaths int NOT NULL,
                                            SpecHalfBaths int NOT NULL,
                                            SpecBedrooms int NOT NULL,
                                            MasterBedLocation varchar(10) NOT NULL,
                                            SpecGarage DECIMAL(4, 1) NOT NULL,
                                            SpecDescription varchar(1500) NOT NULL,
                                            SpecElevationImage longtext NOT NULL,
                                            SpecWebsite varchar(255) NOT NULL,
                                            DownloadTime text NOT NULL,
                                            PRIMARY KEY (SpecNumber));"""

alt_table = """ALTER TABLE Builder_Table ADD CONSTRAINT Builder_Table_fk0 FOREIGN KEY (CorporateBuilderNumber) REFERENCES Corporation_Table(CorporateBuilderNumber);"""

alt_table2 = """ALTER TABLE Subdivision_Table ADD CONSTRAINT Subdivision_Table_fk0 FOREIGN KEY (BuilderNumber) REFERENCES Builder_Table(BuilderNumber);"""

alt_table3 = """ALTER TABLE Plan_Table ADD CONSTRAINT Plan_Table_fk0 FOREIGN KEY (SubdivisionNumber) REFERENCES Subdivision_Table(SubdivisionNumber);"""

alt_table4 = """ALTER TABLE Spec_Table ADD CONSTRAINT Spec_Table_fk0 FOREIGN KEY (PlanNumber) REFERENCES Plan_Table(unique_number);"""


countTableQry = """CREATE TABLE IF NOT EXISTS countTable (CorporateBuilderNumber varchar(30) DEFAULT NULL,
                                                        BuilderWebsite longtext DEFAULT NULL,
                                                        subdivisionCount longtext DEFAULT NULL,
                                                        planCount longtext DEFAULT NULL,
                                                        specCount longtext DEFAULT NULL,
                                                        LastUpdated longtext DEFAULT NULL,
                                                        unique (CorporateBuilderNumber))"""
