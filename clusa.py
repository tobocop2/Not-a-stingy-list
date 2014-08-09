import requests
from bs4 import BeautifulSoup
def search_all_cities():
    r = requests.get("http://geo.craigslist.org/iso/us/")
    html_text = r.text
    soup = BeautifulSoup(html_text)

    for child in soup.find_all(id='list'):
        for link in x.find_all('a'):
            print(link.get('href'))

