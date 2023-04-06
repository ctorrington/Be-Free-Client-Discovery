# Scrape the given address, or addresses from a given file, for the given keywords, or keywords from a given file.

import requests
import re
import time
import random

# tmp
import csv
import argparse

from bs4 import BeautifulSoup

LIMIT = 265

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
        rows = read_file.readlines()

        split_num = 0
        start_range = 265 * split_num
        end_range = 265 * split_num + 264

        for row in range(start_range, end_range):
            # print(rows[row])
            # input()
            try:
                charity_email_contact_info[rows[row].split('@')[1].split('.')[0]] = None
            except:
                continue

        # for row in reader:
        #     try:
        #         # this gets the company name from the email. name@companyname.com
        #         charity_email_contact_info[row[0].split('@')[1].split('.')[0]] = None
        #     except:
        #         continue




        read_file.close()

    counter = 0

    for charity_name in charity_email_contact_info:
        random_page_urls = [
            "https://www.google.com/search?q=youtube&oq=youtube+&aqs=chrome..69i57j0i67i650l2j0i67i131i433i650j0i131i433i512j0i512j0i131i433i512j69i60.1682j0j7&sourceid=chrome&ie=UTF-8",
            "https://www.youtube.com/",
            "https://www.google.com/search?q=twitter&oq=twitter+&aqs=chrome..69i57j0i67i131i433i650l2j0i131i433i512j0i131i433i650j0i131i433i512j69i60l2.1930j0j4&sourceid=chrome&ie=UTF-8",
            "https://twitter.com/?lang=en",
            "https://www.google.com/search?q=why+are+dogs+wolfs&oq=why+are+dogs+wolfs&aqs=chrome..69i57j0i22i30l3j0i10i22i30i625j0i10i22i30j0i8i13i30l2j0i390i395i650l2.4433j1j9&sourceid=chrome&ie=UTF-8",
            "https://www.google.com/search?q=teapots&oq=teapots&aqs=chrome..69i57j0i512j46i175i199i512j0i512l5j46i175i199i512j0i512.1285j0j9&sourceid=chrome&ie=UTF-8",
            "https://www.google.com/search?q=hiking+shoes&oq=hiking+shoes&aqs=chrome..69i57j0i131i433i512j0i512l8.1584j0j9&sourceid=chrome&ie=UTF-8",
            "https://www.google.com/search?q=books+to+read+before+you+die&oq=books+to+read&aqs=chrome.2.69i57j0i512l9.4472j0j9&sourceid=chrome&ie=UTF-8",
            "https://www.google.com/search?q=how+to+cook+noodles&oq=how+to+cook+noodles&aqs=chrome..69i57j0i512l9.3189j0j9&sourceid=chrome&ie=UTF-8",
            "https://www.google.com/search?q=is+face+book+down%3F&oq=is+face+book+down%3F&aqs=chrome..69i57j0i10i512l9.3885j0j9&sourceid=chrome&ie=UTF-8",
            "https://www.google.com/search?q=can+you+drink+london+tap+water&oq=can+you+drink+london+tap&aqs=chrome.0.0i512j69i57j0i22i30l6j0i390i395i650l2.5567j1j9&sourceid=chrome&ie=UTF-8",
            "https://www.google.com/search?q=are+kettles+worth+it%3F&oq=are+kettles+worth+it%3F&aqs=chrome..69i57j0i22i30l9.6727j0j9&sourceid=chrome&ie=UTF-8",
            "https://www.google.com/search?q=alternative+ways+to+boil+water&oq=alternative+ways+to+boil+water&aqs=chrome..69i57j0i22i30l5j0i15i22i30l2j0i390i395i650l2.4356j1j9&sourceid=chrome&ie=UTF-8",
            "https://www.google.com/search?q=why+does+water+boil%3F&oq=why+does+water+boil%3F&aqs=chrome..69i57j0i512l9.5990j0j9&sourceid=chrome&ie=UTF-8",
            "https://www.google.com/search?q=where+does+water+come+from%3F&oq=where+does+water+come+from%3F&aqs=chrome..69i57j0i512j0i20i263i512j0i512l7.3115j0j9&sourceid=chrome&ie=UTF-8",
            "https://www.google.com/search?q=nasa&oq=nasa&aqs=chrome.0.0i271j46i199i340i433i465i512j0i433i512j0i131i433i650j0i131i433i512j46i131i175i199i433i512j0i512j0i131i433i512j0i433i512j0i131i433i512.1189j0j9&sourceid=chrome&ie=UTF-8",
            "https://www.nasa.gov/",
            "https://www.google.com/search?q=cool+space+stuff&oq=cool+space+stuff&aqs=chrome..69i57j0i512l3j0i22i30l6.2484j1j4&sourceid=chrome&ie=UTF-8",
            "https://www.google.com/search?q=why+is+pluto+not+a+planet+nasa&oq=why+is+pluto+not+a+planet+nasa&aqs=chrome..69i57j0i22i30l2j0i390i395i650l3.6989j1j9&sourceid=chrome&ie=UTF-8",
            "https://www.google.com/search?q=when+is+pluto+not+a+planet&oq=when+is+pluto+not+a+planet&aqs=chrome..69i57j0i22i30l8j0i10i22i30.4298j1j9&sourceid=chrome&ie=UTF-8",
        ]

        random_page_chance = 0.4

        if random.random() > random_page_chance:
            url = random_page_urls[random.randint(0, len(random_page_urls) - 1)]
        else:
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

        # Python dictionary with all charity information
        charity_email_contact_info[charity_name] = {charity_name: unique_regex_matches}

        # print(f"\nFOUND CONTACT DETAILS\n{charity_email_contact_info}")

        # I AM A HUMAN. I AM A HUMAN MALE.
        time.sleep(random.randint(5, 60))


        counter += 1
        if counter >= LIMIT:
            break

    # Write the charity contact information into a new file.
    with open('./data/charity_contact_information.csv', 'w', newline = '') as write_file:

        print(f"writing to file {write_file}")
        print(f"charity email info {charity_email_contact_info}")
        print(f"dict keys {charity_email_contact_info.keys()}")

        writer = csv.DictWriter(write_file, fieldnames=charity_email_contact_info.keys())

        # writer.writeheader()

        # for row in charity_email_contact_info:
        #     writer.writerow(row)

        writer.writerow(charity_email_contact_info)

# This is the value of the class property of the div tags that encompass the description of the resultant links
# VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('file_name', type=str, help='The name of the file to get the company contact information from.')
    args = parser.parse_args()

    main(args.file_name)
