import requests
from bs4 import BeautifulSoup

#test query
query = "9c1";

def search_all_cities(query):

    r = requests.get("http://geo.craigslist.org/iso/us/")
    html_text = r.text
    soup = BeautifulSoup(html_text)

    for child in soup.find_all(id='list'):
        for link in child.find_all('a'):
            # do some stuff with each link
            print(link.get('href'))
            get_results(link.get('href'),query)

    r.close

def get_results(link):
    r = requests.get(link+"/search/sss?query="+query+"&sort=rel")
    html_text = r.text
    soup = BeautifulSoup(html_text)
    soup.find_all("div",class_="content")



