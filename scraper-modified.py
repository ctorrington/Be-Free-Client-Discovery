# Scrape the given address, or addresses from a given file, for the given keywords, or keywords from a given file.

import requests
import re
import time
import random

# tmp
import csv
import argparse

from bs4 import BeautifulSoup


def main(scrape_file: str):
    # I AM A HUMAN. I AM A HUMAN MALE.
    cookies = {
        "__Secure-3PSIDCC": "AFvIBn-mowv1SkFptQkQvi9TMphLCFWv8oJHGwA_Y5lK2og_TqUtbc82ZEKQEu1pVt-VsKiEquc",
        "__Secure-1PSIDCC": "AFvIBn88wdKIGKEwRPFCNETUWI8czNgZNDLwa5eXvzRpzUKPRmhvXiAHNtTRywGNVgbw6JnnSxpG",
        "SIDCC": "AFvIBn_Ap6L4LG2_7XSlWIr30wqtz0hnC0muxM3x1LNR7lb6xKfa77-2OZaGOeA6qn2LDDbgqAw",
        "__Secure-3PAPISID": "GX9HOoNDPZtpMTS7/AvJrOvH103T9VnAsJ",
        "SSID": "AIGnTREjnjLQoxVtc",
        "__Secure-1PAPISID": "GX9HOoNDPZtpMTS7/AvJrOvH103T9VnAsJ",
        "HSID": "Ao6sNvp6sfQraY1eQ",
        "__Secure-1PSID": "TwjfOLPhIAYYikn0NkjDxJ93NTsQKinT589XMGRc9T_yZNUePbOCMU7IvPsOdOK0UBJa3A.",
        "SID": "TwjfOLPhIAYYikn0NkjDxJ93NTsQKinT589XMGRc9T_yZNUetH6Z773C-oiWJadTvPrKaQ.",
        "__Secure-3PSID": "TwjfOLPhIAYYikn0NkjDxJ93NTsQKinT589XMGRc9T_yZNUeSHaQ_7RUY3lk1FUq3roOtg.",
        "SAPISID": "GX9HOoNDPZtpMTS7/AvJrOvH103T9VnAsJ",
        "APISID": "3XyZhGSEgf5eL0_1/AqvTMZ7BOboP3yYOR",
        "1P_JAR": "2023-3-28-16",
        "AEC": "AUEFqZcjzke7ckwRkBDNwBOp_vinUazwz2TcKUqLzJvN2wG2DuxXRWnvEw",
        "NID": "511=j2LjNxB0TYjnBotkZ8SvyCTnZj4GfxVZz_n84ktFgCLKRSOxkBm699NxkaMlswJLEhHceKEq24K2nyAA6pega72wHhd7N0N4oc1huLX9_ZW6Gmr8BMbDd4dcbtrDRo7Tn7flgDrbwCC5Tj1egzIvwVeH8LWEiMnRe0ikKjjn_rpiCx181kYRNYUTNP61-fUE5sX5okRQW5DRMdJ7crhpucBs8_vuT7JEBUhkSiAOSm1OufVa7hec_UU7Zn0BL7OO9jgQ0FE-7Ah9ib9bka6BonOygj8LVQ",
        "OTZ": "6953323_56_56_123900_52_436380",
        "SEARCH_SAMESITE": "CgQI8pcB",
        "CONSENT": "PENDING+201",
        "DV": "Y68L4ZO3aeJQACJ-bZgLX56NwZqSchgijpdIBVqZxgEAACAcuD9TMkTrwAAAABhFrO4c0K_MSAAAACZXk6Owkfa-GwAAAA",
        "SOCS": "CAISHAgCEhJnd3NfMjAyMzAyMTUtMF9SQzEaAmVuIAEaBgiA8MqfBg",
        "OGPC": "1151720448-1:19022622-1:"
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    }

    with open(scrape_file, 'r', newline='', encoding='utf-8') as read_file:
        reader = csv.reader(read_file)

        charity_email_contact_info = dict()

        for row in reader:
            try:
                # this gets the company name from the email. name@companyname.com
                charity_email_contact_info[row[0].split('@')[1].split('.')[0]] = None
            except:
                continue
        read_file.close()

    for charity_name in charity_email_contact_info:
        # The url of the page to scrape.
        url = f"https://www.google.com/search?q={charity_name}+contact+information+linkedin"
        page = requests.get(url, cookies=cookies, headers=headers)

        # Entire page scrape results.
        results = BeautifulSoup(page.content, "html.parser")
        # All text blurbs under link results.
        searched = results.findAll("div", {'class': 'BNeawe s3v9rd AP7Wnd'}, recursive=True)

        regrets_matches = []
        # List of regular expressions searching the selected HTML elements. 
        regrets = [
            r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',  # email regex
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # ten digit phone number regex
            r'\+(?:[0-9] ?){6,14}[0-9]'  # international phone number regex
        ]
        for regex in regrets:
            regrets_matches.append(re.findall(regex, str(searched)))

        # print(regrets_matches)

        # TODO Figure out how to make this a one liner.
        # TODO This could replace the above regrets_matches. Im not sure if re.findall works with sets
        unique_regex_matches = set()
        for i in regrets_matches:
            for j in i:
                unique_regex_matches.add(j)

        if len(unique_regex_matches) > 0:
            print(f"{charity_name}: {unique_regex_matches}")

        charity_email_contact_info[charity_name] = unique_regex_matches

        # print(f"\nFOUND CONTACT DETAILS\n{charity_email_contact_info}")

        # I AM A HUMAN. I AM A HUMAN MALE.
        time.sleep(random.randint(5, 7))


# This is the value of the class property of the div tags that encompass the description of the resultant links
# VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('file_name', type=str, help='The name of the file to get the company contact information from.')
    args = parser.parse_args()

    main(args.file_name)
