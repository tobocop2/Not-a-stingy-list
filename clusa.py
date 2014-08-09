import requests
from bs4 import BeautifulSoup

#test query
query = "9c1";

#result paring
result = {}

def search_all_cities():

    req = requests.get("http://geo.craigslist.org/iso/us/")
    html_text = req.text
    soup = BeautifulSoup(html_text)

    for child in soup.find_all(id='list'):
        for link in child.find_all('a'):
            # do some stuff with each link
            #print(link.get('href'))
            get_results(link.get('href'))

    req.close

def get_results(link):

    reqx = requests.get(link+"/search/sss?query="+query+"&sort=rel")
    html_textx = reqx.text
    soupx = BeautifulSoup(html_textx)
    soupx.find_all("div",class_="content")

    for child in soupx.find_all("div",class_="content"):
        for result_link in child.find_all("a",class_="hdrlnk"):
            if "html" in result_link.get('href'):
                full_link = link+result_link.get('href')
                link_desc = link.get_text()
                #the link/value
                #print link+result_link.get('href')
                #the key
                #print (link.get_text())
                print "\n"+link+result_link.get('href')+": \n"+link.get_text()
                if not result[link_text]:
                   result[link_text] = full_link

    reqx.close

    for key in result:
        print key+":\n"+result[key]+"\n"
#Will include price later 
#for result_link in child.find_all("a",class_="hdrlnk"):

search_all_cities()
