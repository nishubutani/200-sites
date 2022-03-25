# # import hashlib
# # from urllib import response
# #
# # planname = "ajhjha"
# # communityfromplan = "jdjdf"
# #
# #
# # try:
# #     PlanNumber = int(hashlib.md5(bytes(planname , "utf8")).hexdigest(), 16) % (10 ** 30)
# #     f = open("html/%s.html" % PlanNumber, "wb")
# #     print(PlanNumber)
# #     # f.write(response.body)
# #     f.close()
# # except Exception as e:
# #     print(e)
# #
#
# address = '  2667 H. Bullard Road Hope Mills, NC 28348 '
# if 'Hope Mills' in address:
#     SpecCity = address.split(',')[0].strip().split()[-1:-4].strip()
#     print(SpecCity)
#     SpecStreet1 = address.split(SpecCity)[0].strip()
#     print(SpecStreet1)
#     SpecState = address.split(',')[1].strip().split(" ")[0].strip()
#     print(SpecState)
#     SpecZIP = address.split(',')[1].strip().split(" ")[1].strip()
#     print(SpecZIP)
#
