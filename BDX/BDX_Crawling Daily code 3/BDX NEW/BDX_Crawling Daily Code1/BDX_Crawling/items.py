# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BdxCrawlingItem_Corporation(scrapy.Item):
    CorporateBuilderNumber = scrapy.Field()
    CorporateState = scrapy.Field()
    CorporateName = scrapy.Field()

class BdxCrawlingItem_Builder(scrapy.Item):

    BuilderNumber = scrapy.Field()
    BrandName = scrapy.Field()
    BrandLogo_Med = scrapy.Field()
    ReportingName = scrapy.Field()
    DefaultLeadsEmail = scrapy.Field()
    BuilderWebsite = scrapy.Field()
    CorporateBuilderNumber = scrapy.Field()

class BdxCrawlingItem_subdivision(scrapy.Item):
    sub_Status = scrapy.Field()
    SubdivisionNumber = scrapy.Field()
    BuilderNumber = scrapy.Field()
    SubdivisionName = scrapy.Field()
    BuildOnYourLot = scrapy.Field()
    OutOfCommunity = scrapy.Field()
    Street1 = scrapy.Field()
    City = scrapy.Field()
    State = scrapy.Field()
    ZIP = scrapy.Field()
    AreaCode = scrapy.Field()
    Prefix = scrapy.Field()
    Suffix = scrapy.Field()
    Extension = scrapy.Field()
    Email = scrapy.Field()
    AmenityType = scrapy.Field()
    SubDescription = scrapy.Field()
    SubImage = scrapy.Field()
    SubWebsite = scrapy.Field()

class BdxCrawlingItem_Plan(scrapy.Item):
    Type = scrapy.Field()
    PlanNumber = scrapy.Field()
    SubdivisionNumber = scrapy.Field()
    PlanName = scrapy.Field()
    PlanNotAvailable = scrapy.Field()
    PlanTypeName = scrapy.Field()
    BasePrice = scrapy.Field()
    BaseSqft = scrapy.Field()
    Baths = scrapy.Field()
    HalfBaths = scrapy.Field()
    Bedrooms = scrapy.Field()
    Garage = scrapy.Field()
    Description = scrapy.Field()
    ElevationImage = scrapy.Field()
    PlanWebsite = scrapy.Field()
    unique_number = scrapy.Field()


class BdxCrawlingItem_Spec(scrapy.Item):

    SpecNumber = scrapy.Field()
    PlanNumber = scrapy.Field()
    SpecStreet1 = scrapy.Field()
    SpecCity = scrapy.Field()
    SpecState = scrapy.Field()
    SpecZIP = scrapy.Field()
    SpecCountry = scrapy.Field()
    SpecPrice = scrapy.Field()
    SpecSqft = scrapy.Field()
    SpecBaths = scrapy.Field()
    SpecHalfBaths = scrapy.Field()
    SpecBedrooms = scrapy.Field()
    MasterBedLocation = scrapy.Field()
    SpecGarage = scrapy.Field()
    SpecDescription = scrapy.Field()
    SpecElevationImage = scrapy.Field()
    SpecWebsite = scrapy.Field()
    unique_number = scrapy.Field()