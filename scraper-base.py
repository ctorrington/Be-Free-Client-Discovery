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


def scrape():
    query = "Enter search terms here"

    query = query.replace(" ", "+")

    url = f"https://www.google.com/search?q={query}"

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


def readFile():
    path_to_file = 'data/charity_email_list.txt'
    with open(path_to_file, 'r') as f:
        emails = f.readlines()
        f.close()

    return emails

def getCompanyName(company_emails):
    naems

    return names


def main():
    company_emails = readFile()
    company_names = getCompanyName(company_emails)
    scrape()
