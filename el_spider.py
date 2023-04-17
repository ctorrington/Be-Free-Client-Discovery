import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import random
import typing
import csv

# from bs4 import BeautifulSoup
import bs4

class WebCrawlingSpider:
    def __init__(self):
        self.LIMIT = 265
        self.RANDOM_PAGE_CHANCE = 0.5
        self.target_city_list = ['Manchester', 'Liverpool', 'Blackpool', 'Chester', 'Northwich', 'Bolton', 'Warrington']
        self.target_city_list = ['Lancashire UK', 'Manchester']
        self.company_bcorp_data_dict = {}
        self.cookie_dict = {
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
        self.header_dict = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
            "Accept-Encoding": "gzip, deflate, br", 
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8", 
            "Sec-Ch-Ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"", 
            "Sec-Ch-Ua-Mobile": "?0", 
            "Sec-Ch-Ua-Platform": "\"Windows\"", 
            "Sec-Fetch-Dest": "document", 
            "Sec-Fetch-Mode": "navigate", 
            "Sec-Fetch-Site": "none", 
            "Sec-Fetch-User": "?1", 
            "Upgrade-Insecure-Requests": "1", 
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36", 
            "X-Amzn-Trace-Id": "Root=1-64343086-010389f337d23c2f0e81fc67"
        }
        self.user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
        ]
        self.random_page_url_list = [
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
            "https://www.google.com/search?q=when+is+pluto+not+a+planet&oq=when+is+pluto+not+a+planet&aqs=chrome..69i57j0i22i30l8j0i10i22i30.4298j1j9&sourceid=chrome&ie=UTF-8"
        ]
        
    def spider_sleep(self) -> None:
        """Prevent getting captchad.
        
        Should be called after every time the webdriver is closed."""
        
        time.sleep(random.randint(2, 5))
        
        
    def write_dict_to_file(self, file_path: str, data: dict[str, str]) -> None:
        """Write the given dictionary to the given file."""
        
        with open(file_path, 'w', newline='', encoding='utf-8') as write_file:
            writer = csv.DictWriter(write_file, fieldnames=data.keys())
            writer.writerow(data)
        
        print(f"{data.keys()} data written to {file_path}")
        
        
    def get_element_contents(self, page_html: bs4.BeautifulSoup, element: str, element_property: str, element_property_value: str) -> str:
        """Get the page content within the given element tag."""
        
        # found_data = page_html.findAll(element, {element_property, element_property_value})
        print(page_html)
        found_data = page_html.findAll('span')
        
        print(f"found data:\n{found_data}\n")
        
        
    
    
    def get_page_html(self, page_url: str) -> bs4.BeautifulSoup:
        """Get the page html for the given page url.
        NOT CURRENTLY IN USE WITH SELENIUM.
        WILL BE USED FOR MODULE LATER.
        """
        
        # Randomise the user agent to reduce chances of being captchad.
        random_user_agent_header = self.header_dict
        random_user_agent_header['User-Agent'] = self.user_agent_list[random.randint(0, len(self.user_agent_list) - 1)]
        
        # page = requests.get(page_url, cookies=self.cookie_dict)
        # results = bs4.BeautifulSoup(page.content, "html.parser")
        
        # print(re.findall('Bold Bean Co', str(results)))
        
        
        # Get element with tag name 'div'
        # elements = driver.find_elements(By.CLASS_NAME, 'text-xl font-medium text-black')
        # e = driver.find_element(By.XPATH, "//span[@class='text-xl font-medium text-black']")
        # e = driver.find_elements(By.XPATH, "//span[@class='text-xl font-medium text-black']")
        
        

        # e = driver.find_element(By.XPATH, "//span[@class='text-xl font-medium text-black']")
        
        
    def get_company_names_and_links(self, page_url: str) -> dict[str, str]:
        """Return the bcorp company names & their corresponding links to their bcorp info page"""
        
        company_name_link_dict = {}
        
        driver = webdriver.Chrome()
        driver.get(page_url)
        wait = WebDriverWait(driver, 10)
        
        # Get a list of all span elements with the class below. These are the company names.
        company_names = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//span[@class='text-xl font-medium text-black']")))
        
        # Get the link to each company's individual page.
        for company in company_names:
            print(f"found company with name: {company.text}")
            link_element = company.find_element(By.XPATH, "./ancestor::a")
            company_link = link_element.get_attribute("href")
            print(f"company has link: {company_link}\n")
            
            company_name_link_dict[company.text] = company_link
            
            # Update the global dictionary will all company names and data
            print(f"adding company information for: {company.text}\n")
            self.get_specific_company_bcorp_information(company_link)
            
        driver.quit()
        self.spider_sleep()
        
        return company_name_link_dict
        
        
        
    def get_number_of_pages(self, page_url: str) -> int:
        """Return the number of pages that list bcorp companies for a certain query"""
        
        driver = webdriver.Chrome()
        driver.get(page_url)
        wait = WebDriverWait(driver, 10)
        
        j = driver.find_elements(By.XPATH, "//button[@class='outline-none flex items-center justify-center w-10 h-10 border border-surface-variant-light-outline rounded-lg text-fiber-neutral-500 border-fiber-neutral-500 hover:bg-white hover:border-fiber-grey-900 focus:bg-white focus:border-fiber-grey-900']")
        driver.quit()
        self.spider_sleep()
        
        return len(j)
        
    
    def get_target_city_list_urls(self) -> list[str]:
        """Return the urls of the queries for the target cities"""
        
        return [f"https://www.bcorporation.net/en-us/find-a-b-corp?query={city.lower().replace(' ', '%20')}" for city in self.target_city_list]
    
    def get_specific_company_bcorp_information(self, company_page_url: str) -> dict[str, str]:
        """Return the company's bcorp information from the given company url.
        UNDER CONSTRUCTION
        """
        
        driver = webdriver.Chrome()
        driver.get(company_page_url)
        wait = WebDriverWait(driver, 10)
        
        # Get the overview div.
        overview_div = driver.find_element(By.XPATH, "//div[@class='lg:hidden flex flex-col bg-gray-light p-4 space-y-4']")
        print(f"found overview div:\n{overview_div}\n")
        
        section_div_list = overview_div.find_elements(By.XPATH, "./div")
        # section_div_list = overview_div.find_elements(By.TAG_NAME, 'div')
        print(f"\nfound section div:\n{section_div_list}\n") 
        
        for section in section_div_list:
            print(f"section:\n{section}\n\n")
            heading = section.find_element(By.XPATH, "span").text
            # heading = section.find_element(By.TAG_NAME, 'span')
            print(f"found heading:\n{heading}\n")
            
            info_div = section.find_element(By.XPATH, "./div")
            # info_div = section.find_element(By.TAG_NAME, 'div')
            print(f"found info div:\n{info_div}\n")
            
            info_text = info_div.find_element(By.XPATH, "./p").text
            # info_text = info_div.find_element(By.TAG_NAME, 'p').text
            print(f"found info text:\n{info_text}\n")
            self.company_bcorp_data_dict[heading] = info_text
            
            print(f"\n\n\nCOMPANY BCORP DATA DICT:\n{self.company_bcorp_data_dict}\n")
        
        
        
        
        driver.quit()
        self.spider_sleep()
        
        
    def write_bcorp_company_information(self):
        """Write the bcorp properties of the companies to the JSON file"""
        
        # Get all queries for the cities to search for bcorps in.
        target_city_urls = self.get_target_city_list_urls()
        print(f"\ntarget_city_urls:\n{target_city_urls}")
        
        # Get the data for each target city.
        for target_city_url in target_city_urls:
            # TODO this whole block should probably be a function.
            # Get the number of pages listing bcorps for each query in the bcorp page.
            number_of_pages = self.get_number_of_pages(target_city_url) + 1
            print(f"target city url:\n{target_city_url}\n")
            print(f"number of pages for query: {number_of_pages}\n")
            
            # Augment url if the number of pages for the company is greater than one.
            for page_number in range(number_of_pages):
                all_target_city_company_name_link_dict = {}
                
                print(f"currently searching page number {page_number + 1}.\n")
                if number_of_pages > 1:
                    target_city_url += f"&page={page_number}"    
                
                # Get the company and specific company information page.
                # TODO the line below could be incorpated into the update statement underneath.
                target_city_company_name_link_dictionary = self.get_company_names_and_links(target_city_url)
                print(f"updating cumulative company list with the following companies and links:\n{target_city_company_name_link_dictionary.keys()}.\n")
                all_target_city_company_name_link_dict.update(target_city_company_name_link_dictionary)
                
                # Get the specific data for each of those companies
                
                
                
        print(f"cumulative company names with all of their links.")
        print(all_target_city_company_name_link_dict)
            
        # page_url = 'https://www.bcorporation.net/en-us/find-a-b-corp?query=manchester'
        # self.get_company_names_and_links(page_url)
        
        
def main() -> None:
    page_url = 'https://www.bcorporation.net/en-us/find-a-b-corp?query=manchester'
    page_element = 'span'
    element_property = 'class'
    property_value = 'text-xl font-medium text-black'
    
    itsy_bitsy = WebCrawlingSpider()
    # page_html = itsy_bitsy.get_page_html(page_url)
    itsy_bitsy.write_bcorp_company_information()
    # itsy_bitsy.get_element_contents(page_html, page_element, element_property, property_value)
        
        
if __name__ == '__main__':
    main()