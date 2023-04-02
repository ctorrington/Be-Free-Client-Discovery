import csv
import sys
import requests
from bs4 import BeautifulSoup
import re


run = False

# with open('company_house_data.csv', newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#     for row in spamreader:
#         print(', '.join(row))
#         input()


i = 0
j = 0

print("runninig run")
def run():
    with open('company_house_data.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # print(row)
            if row['RegAddress.PostTown'] == 'LIVERPOOL':
                # print(row['CompanyName'])
                # print(row['RegAddress.PostTown'])
                print(row)
                break
                # i+= 1
            # print(i)
            # j+=1


# cookies = {"CONSENT": "YES+cb.20210720-07-p0.en+FX+410"}
           
cookies = {
    "__Secure-3PSIDCC" :"AFvIBn-mowv1SkFptQkQvi9TMphLCFWv8oJHGwA_Y5lK2og_TqUtbc82ZEKQEu1pVt-VsKiEquc",
    "__Secure-1PSIDCC" :"AFvIBn88wdKIGKEwRPFCNETUWI8czNgZNDLwa5eXvzRpzUKPRmhvXiAHNtTRywGNVgbw6JnnSxpG",
    "SIDCC" :"AFvIBn_Ap6L4LG2_7XSlWIr30wqtz0hnC0muxM3x1LNR7lb6xKfa77-2OZaGOeA6qn2LDDbgqAw",
    "__Secure-3PAPISID" :"GX9HOoNDPZtpMTS7/AvJrOvH103T9VnAsJ",
    "SSID" :"AIGnTREjnjLQoxVtc",
    "__Secure-1PAPISID" :"GX9HOoNDPZtpMTS7/AvJrOvH103T9VnAsJ",
    "HSID" :"Ao6sNvp6sfQraY1eQ",
    "__Secure-1PSID" :"TwjfOLPhIAYYikn0NkjDxJ93NTsQKinT589XMGRc9T_yZNUePbOCMU7IvPsOdOK0UBJa3A.",
    "SID" :"TwjfOLPhIAYYikn0NkjDxJ93NTsQKinT589XMGRc9T_yZNUetH6Z773C-oiWJadTvPrKaQ.",
    "__Secure-3PSID" :"TwjfOLPhIAYYikn0NkjDxJ93NTsQKinT589XMGRc9T_yZNUeSHaQ_7RUY3lk1FUq3roOtg.",
    "SAPISID" :"GX9HOoNDPZtpMTS7/AvJrOvH103T9VnAsJ",
    "APISID" :"3XyZhGSEgf5eL0_1/AqvTMZ7BOboP3yYOR",
    "1P_JAR" :"2023-3-28-16",
    "AEC" :"AUEFqZcjzke7ckwRkBDNwBOp_vinUazwz2TcKUqLzJvN2wG2DuxXRWnvEw",
    "NID" :"511=j2LjNxB0TYjnBotkZ8SvyCTnZj4GfxVZz_n84ktFgCLKRSOxkBm699NxkaMlswJLEhHceKEq24K2nyAA6pega72wHhd7N0N4oc1huLX9_ZW6Gmr8BMbDd4dcbtrDRo7Tn7flgDrbwCC5Tj1egzIvwVeH8LWEiMnRe0ikKjjn_rpiCx181kYRNYUTNP61-fUE5sX5okRQW5DRMdJ7crhpucBs8_vuT7JEBUhkSiAOSm1OufVa7hec_UU7Zn0BL7OO9jgQ0FE-7Ah9ib9bka6BonOygj8LVQ",
    "OTZ" :"6953323_56_56_123900_52_436380",
    "SEARCH_SAMESITE" :"CgQI8pcB",
    "CONSENT" :"PENDING+201",
    "DV" :"Y68L4ZO3aeJQACJ-bZgLX56NwZqSchgijpdIBVqZxgEAACAcuD9TMkTrwAAAABhFrO4c0K_MSAAAACZXk6Owkfa-GwAAAA",
    "SOCS" :"CAISHAgCEhJnd3NfMjAyMzAyMTUtMF9SQzEaAmVuIAEaBgiA8MqfBg", 
    "OGPC" :"1151720448-1:19022622-1:"
}
URL = "https://www.google.com/search?q=the+liverpool+recruitment+company+contact+information+linkedin"
page = requests.get(URL, cookies=cookies)

results = BeautifulSoup(page.content, "html.parser")

# print(results.body.div.children)

# searched = results.find("div", {'id':'main'})
searched = results.findAll("div", {'class':'BNeawe s3v9rd AP7Wnd'}, recursive=True)
# children = searched.findChildren("div", recursive=False)
# print(children[3])
print(results)

#rso > div:nth-child(1) > div > div > div > div > div:nth-child(2) > div


if __name__ == "__main__":

    # terminal arguements
    # print(sys.argv)
    for i in sys.argv:
        # print(i)
        match i:
            case "run":
                print("running")
                run()

    # for i, arg in enumerate(sys.argv):
    #     print(f"Argument {i:>6}: {arg}")

# if sys.argv[1] == "run":
#     print("yo")

# print(i)
# print(j)