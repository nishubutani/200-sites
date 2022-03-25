from lxml import etree
import datetime
import pymysql

def genxml(host, usernm, passwd, database, CorporateBuilderNumber, CorporateState, CorporateName, output_file_name):

    try:

        con = pymysql.connect(host=host, user=usernm, passwd=passwd, database=database)
        crsr = con.cursor()

        now = datetime.datetime.now()
        res = now.strftime("%Y-%m-%dT%H:%M:%S")

        # ---------------------- Root Element -------------
        root = etree.Element('Builders', DateGenerated=res)

        # ---------------------- Corporation --------------
        corp = etree.SubElement(root, "Corporation")
        cbn = etree.SubElement(corp, "CorporateBuilderNumber")
        cbn.text = str(CorporateBuilderNumber)
        cst = etree.SubElement(corp, "CorporateState")
        cst.text = CorporateState
        cnm = etree.SubElement(corp, "CorporateName")
        cnm.text = CorporateName

        # ----------------------- Builder ------------------
        retrive = "select BuilderNumber, BrandName, BrandLogo_Med, ReportingName, DefaultLeadsEmail, BuilderWebsite From Builder_Table where CorporateBuilderNumber='%s'"% str(cbn.text)
        crsr.execute(retrive)
        valuse = crsr.fetchall()

        builder = etree.SubElement(corp, "Builder")
        bldrNum = etree.SubElement(builder, "BuilderNumber")
        bldrNum.text = valuse[0][0]
        bldrName = etree.SubElement(builder, "BrandName")
        bldrName.text = valuse[0][1]
        bldrLogo = etree.SubElement(builder, "BrandLogo_Med", ReferenceType="URL")
        bldrLogo.text = valuse[0][2]
        bldrRname = etree.SubElement(builder, "ReportingName")
        bldrRname.text = valuse[0][3]
        bldrDemail = etree.SubElement(builder, "DefaultLeadsEmail", LeadsPerMessage="All")
        bldrDemail.text = valuse[0][4]
        bldrweb = etree.SubElement(builder, "BuilderWebsite")
        bldrweb.text = valuse[0][5]


        # ------------------------ Subdivision --------------
        subretive = "select sub_Status, SubdivisionNumber, SubdivisionName, BuildOnYourLot, OutOfCommunity, Street1, City, State, ZIP, AreaCode, Prefix, Suffix, Extension, Email,AmenityType, SubDescription, SubImages, SubWebsite from Subdivision_Table where BuilderNumber = '%s'"%str(bldrNum.text)
        crsr.execute(subretive)
        subresult = crsr.fetchall()

        for sub in subresult:

            if sub[2] != "":
                subdiv = etree.SubElement(builder, "Subdivision", Status="%s" % str(sub[0]))
                subdivNum = etree.SubElement(subdiv, "SubdivisionNumber")
                subdivNum.text = str(sub[1])
                subdivName = etree.SubElement(subdiv, "SubdivisionName")
                subdivName.text = sub[2]
                subdivBoyl = etree.SubElement(subdiv, "BuildOnYourLot")
                subdivBoyl.text = str(sub[3])
                subdivSales = etree.SubElement(subdiv, "SalesOffice")

                salesAddress = etree.SubElement(subdivSales, "Address", OutOfCommunity='0')
                if sub[5] != "":
                    salesAddressStreet = etree.SubElement(salesAddress, "Street1")
                    salesAddressStreet.text = sub[5]
                if sub[6] != "":
                    salesAddressCity = etree.SubElement(salesAddress, "City")
                    salesAddressCity.text = sub[6]
                if sub[7] != "":
                    salesAddressState = etree.SubElement(salesAddress, "State")
                    salesAddressState.text = sub[7].upper()
                if sub[8] != "":
                    salesAddressZip = etree.SubElement(salesAddress, "ZIP")
                    salesAddressZip.text = sub[8]

                # if sub[9] != "":
                #     salesPhone = etree.SubElement(subdivSales, "Phone")
                #     salesPhoneAreaCode = etree.SubElement(salesPhone, "AreaCode")
                #     salesPhoneAreaCode.text = sub[9]
                #     salesPhonePrefix = etree.SubElement(salesPhone, "Prefix")
                #     salesPhonePrefix.text = sub[10]
                #     salesPhoneSuffix = etree.SubElement(salesPhone, "Suffix")
                #     salesPhoneSuffix.text = sub[11]
                #
                # if sub[13] != "":
                #     salesEmail = etree.SubElement(subdivSales, "Email")
                #     salesEmail.text = sub[13]

                amenity_list = ["Pool", "Playground", "GolfCourse", "Tennis", "Soccer", "Volleyball", "Basketball", "Baseball", "Views", "Lake", "Pond", "Marina", "Beach", "WaterfrontLots", "Park", "Trails", "Greenbelt", "Clubhouse", "CommunityCenter"]
                # amenity_list = ["Pool",  "GolfCourse", "Tennis", "Soccer", "Volleyball", "Basketball", "Baseball", "Views", "Lake", "Pond", "Marina", "Beach", "WaterfrontLots", "Park", "Trails", "Greenbelt", "Clubhouse", "CommunityCenter"]

                if sub[14] != "":
                    if "|" in str(sub[14]):
                        tmp = str(sub[14]).split("|")
                        for amenity in tmp:
                            for Default_amenity in amenity_list:
                                if Default_amenity in amenity:
                                    print(amenity)
                                    Amenity = etree.SubElement(subdiv, "SubAmenity", Type=str(Default_amenity))
                                    Amenity.text = "1"

                    else:
                        if sub[14] in amenity_list:
                            Amenity = etree.SubElement(subdiv, "SubAmenity", Type=str(sub[14]))
                            Amenity.text = "1"

                # amenity_list = ["Pool", "Playground", "GolfCourse", "Tennis", "Soccer", "Volleyball", "Basketball",
                #                 "Baseball", "Views", "Lake", "Pond", "Marina", "Beach", "WaterfrontLots", "Park",
                #                 "Trails", "Greenbelt", "Clubhouse", "CommunityCenter"]
                # if sub[14] != "":
                #     if "|" in str(sub[14]):
                #         tmp = str(sub[14]).split("|")
                #         for amenity in tmp:
                #             if amenity in amenity_list:
                #                 Amenity = etree.SubElement(subdiv, "SubAmenity", Type=str(amenity))
                #                 Amenity.text = '1'
                #     else:
                #         if sub[14] in amenity_list:
                #             Amenity = etree.SubElement(subdiv, "SubAmenity", Type=str(sub[14]))
                #             Amenity.text = "1"





                if sub[15] != "":
                    subDesc = etree.SubElement(subdiv, "SubDescription")
                    subDesc.text = sub[15]

                if str(sub[16]) != "":
                    if "|" in str(sub[16]):
                        tmp = str(sub[16]).split("|")
                        for i in range(len(tmp)):
                            if tmp[i].startswith('http'):
                                subdivImage = etree.SubElement(subdiv, "SubImage", SequencePosition=str(i + 1),Title="House1", ReferenceType="URL")
                                subdivImage.text = tmp[i]
                    else:
                        if sub[16].startswith('http'):
                            subdivImage = etree.SubElement(subdiv, "SubImage", SequencePosition="1", Title="House1",ReferenceType="URL")
                            subdivImage.text = sub[16]

                subdivweb = etree.SubElement(subdiv, "SubWebsite")
                subdivweb.text = sub[17]

                # --------------------------- Plan --------------------

                planRetrive = "select Type, PlanNumber, PlanName, PlanNotAvailable, PlanTypeName, BasePrice, BaseSqft, Baths, HalfBaths, Bedrooms, Garage, Description, ElevationImage, PlanWebsite, unique_number From Plan_Table  where " \
                              "SubdivisionNumber = '%s'" % str(subdivNum.text)
                crsr.execute(planRetrive)
                planResult = crsr.fetchall()

                if len(planResult) > 0:

                    for plan1 in planResult:
                        plan1 = list(plan1)
                        if plan1[2] != "":
                            if plan1[5] == 0 or plan1[5] > 39999:

                                if plan1[2] == "Plan Unknown":
                                    plan1[9] = plan1[7] = 1

                                if plan1[9] != 0 and plan1[7] != 0:
                                    if (500 < plan1[6] < 14000) or (plan1[6] == 0):

                                        plan = etree.SubElement(subdiv, "Plan", Type="%s" % plan1[0])

                                        planNum = etree.SubElement(plan, "PlanNumber")
                                        planNum.text = plan1[1]
                                        planName = etree.SubElement(plan, "PlanName")
                                        planName.text = plan1[2]
                                        planPna = etree.SubElement(plan, "PlanNotAvailable")
                                        planPna.text = str(plan1[3])
                                        planPtn = etree.SubElement(plan, "PlanTypeName")
                                        planPtn.text = plan1[4]
                                        planBp = etree.SubElement(plan, "BasePrice")
                                        planBp.text = str(plan1[5])
                                        planBsft = etree.SubElement(plan, "BaseSqft")
                                        planBsft.text = str(plan1[6])
                                        planBath = etree.SubElement(plan, "Baths")
                                        planBath.text = str(plan1[7])
                                        planHbath = etree.SubElement(plan, "HalfBaths")
                                        planHbath.text = str(plan1[8])
                                        planbedr = etree.SubElement(plan, "Bedrooms", MasterBedLocation="Down")
                                        planbedr.text = str(plan1[9])
                                        planGrage = etree.SubElement(plan, "Garage")
                                        planGrage.text = str(plan1[10])
                                        if plan1[11] != "":
                                            planDesc = etree.SubElement(plan, "Description")
                                            planDesc.text = plan1[11]

                                        planImages = etree.SubElement(plan, "PlanImages")
                                        if "|" in str(plan1[12]):
                                            pImages = str(plan1[12]).split("|")
                                            for i in range(len(pImages)):
                                                if pImages[i].startswith('http'):
                                                    planImagesElvationImage = etree.SubElement(planImages,"ElevationImage",SequencePosition="%s" % str(i + 1),ReferenceType="URL")
                                                    planImagesElvationImage.text = pImages[i]
                                        else:
                                            if plan1[12].startswith('http'):
                                                planImagesElvationImage = etree.SubElement(planImages, "ElevationImage",SequencePosition="%s" % str(1), ReferenceType="URL")
                                                planImagesElvationImage.text = plan1[12]

                                        planweb = etree.SubElement(plan, "PlanWebsite")
                                        planweb.text = plan1[13]

                                        # ------------------------- Spec ----------------------

                                        SpecRetive = "select SpecNumber, SpacStreet1, SpacCity, SpecState, SpecZIP, SpecCountry, SpecPrice, SpecSqft, SpecBaths, SpecHalfBaths, SpecBedrooms, MasterBedLocation, SpecGarage, " \
                                                     "SpecDescription, SpecElevationImage, SpecWebsite from Spec_Table where PlanNumber = '%s'" %str(plan1[14])
                                        crsr.execute(SpecRetive)
                                        SpecResults = crsr.fetchall()

                                        for SpecResult in SpecResults:

                                            if SpecResult[6] == 0 or SpecResult[6] > 39999:

                                                if SpecResult[8] != 0 and SpecResult[10] != 0:
                                                    if (500 < SpecResult[7] < 14000) or (SpecResult[7] == 0):
                                                        spec = etree.SubElement(plan, "Spec", Type="%s" % "SingleFamily")
                                                        specNum = etree.SubElement(spec, "SpecNumber")
                                                        specNum.text = SpecResult[0]

                                                        specAddress = etree.SubElement(spec, "SpecAddress")
                                                        specAddressStreet = etree.SubElement(specAddress, "SpecStreet1")
                                                        specAddressStreet.text = SpecResult[1]
                                                        specAddressCity = etree.SubElement(specAddress, "SpecCity")
                                                        specAddressCity.text = SpecResult[2]
                                                        specAddressState = etree.SubElement(specAddress, "SpecState")
                                                        specAddressState.text = SpecResult[3].upper()
                                                        specAddressZip = etree.SubElement(specAddress, "SpecZIP")
                                                        specAddressZip.text = SpecResult[4]
                                                        specAddressContry = etree.SubElement(specAddress, "SpecCountry")
                                                        specAddressContry.text = SpecResult[5]

                                                        SpecPrice = etree.SubElement(spec, "SpecPrice")
                                                        SpecPrice.text = str(SpecResult[6])
                                                        SpecSqft = etree.SubElement(spec, "SpecSqft")
                                                        SpecSqft.text = str(SpecResult[7])
                                                        SpecBaths = etree.SubElement(spec, "SpecBaths")
                                                        SpecBaths.text = str(SpecResult[8])
                                                        SpecHalfBaths = etree.SubElement(spec, "SpecHalfBaths")
                                                        SpecHalfBaths.text = str(SpecResult[9])
                                                        SpecBedrooms = etree.SubElement(spec, "SpecBedrooms", MasterBedLocation="Down" )
                                                        SpecBedrooms.text = str(SpecResult[10])
                                                        SpecGarage = etree.SubElement(spec, "SpecGarage")
                                                        SpecGarage.text = str(SpecResult[12])
                                                        SpecDescription = etree.SubElement(spec, "SpecDescription")
                                                        SpecDescription.text = str(SpecResult[13])
                                                        SpecImages = etree.SubElement(spec, "SpecImages")
                                                        if "|" in str(SpecResult[14]):
                                                            tmp2 = str(SpecResult[14]).split("|")
                                                            for j in range(len(tmp2)):
                                                                if tmp2[j].startswith('http'):
                                                                    SpecElevationImage = etree.SubElement(SpecImages,"SpecElevationImage",SequencePosition="%s" % str(j + 1),Title="",ReferenceType="URL")
                                                                    SpecElevationImage.text = tmp2[j]
                                                        else:
                                                            if str(SpecResult[14]).startswith('http'):
                                                                SpecElevationImage = etree.SubElement(SpecImages,"SpecElevationImage",SequencePosition="1",Title="",ReferenceType="URL")
                                                                SpecElevationImage.text = str(SpecResult[14])

                                                        SpecWebsite = etree.SubElement(spec, "SpecWebsite")
                                                        SpecWebsite.text = str(SpecResult[15])

        doc = etree.ElementTree(root)
        doc.write(output_file_name)
        print("Genrated XML %s"%(output_file_name))
        return 1
    except Exception as e:
        print("XML Not Genrated ....")
        print(e)
        return 0
