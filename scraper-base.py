import requests
from bs4 import BeautifulSoup
import random
from fractions import Fraction
import time


def sleep():
    # Generate a random timeout between 10 and 100 seconds as a Fraction
    timeout = Fraction(random.randint(10, 100), 1)

    # Convert the fraction to a decimal value in seconds
    timeout_in_seconds = timeout.numerator / timeout.denominator

    # Pause the program for the specified timeout
    time.sleep(timeout_in_seconds)


def scrape(company_names):
    for name in company_names:
        query = "contact information linkedin"

        query = query.replace(" ", "+")

        url = f"https://www.google.com/search?q={name}+{query}"

        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        results = soup.find_all("div", class_="BNeawe vvjwJb AP7Wnd")
        for result in results:
            title = result.text
            link = result.find_parent('a')['href']
            content = result.find("div", class_="BNeawe s3v9rd AP7Wnd").get_text()
            print(title)
            print("URL: " + link)
            print("Content: " + content)

        sleep()




def readFile():
    path_to_file = 'data/charity_email_list.txt'
    with open(path_to_file, 'r') as f:
        emails = f.readlines()
        f.close()

    return emails


def writeFile():
    with open('./data/output.txt', 'w') as f:



def getCompanyName(company_emails):
    names = [email.split('@')[1].split('.')[0].lower() for email in company_emails]
    unwanted_names = ('yahoo','hotmail','gmail', 'outlook', 'icloud', 'aol', 'live')
    clean_names = [name for name in names if name not in unwanted_names]
    return clean_names


def main():
    company_emails = readFile()
    company_names = getCompanyName(company_emails)
    scrape(company_names)

