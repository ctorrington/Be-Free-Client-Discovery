import requests

from bs4 import BeautifulSoup


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


