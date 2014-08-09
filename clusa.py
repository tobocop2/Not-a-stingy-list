import requests
from bs4 import BeautifulSoup

#test query
query = "9c1"
print query

#result paring
result = {}

#resulting output file
f=open('./result.log', 'w+')

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
    print "searching: "+link+"\nfor "+query+"."

    reqx = requests.get(link+"search/sss?query="+query+"&sort=rel")
    html_textx = reqx.text
    soupx = BeautifulSoup(html_textx)
    #print html_textx
    #print soupx.text

    for child in soupx.find_all("div",class_="content"):
        for result_link in child.find_all("a",class_="hdrlnk"):
            if "html" in result_link.get('href'):
                full_link = result_link.get('href')
                link_desc = result_link.get_text()
                #the link/value
                #print link+result_link.get('href')
                #the key
                #print (link.get_text())
                #print "\n"+link+result_link.get('href')+": \n"+result_link.get_text()
                if not link_desc in result:
                   #print 'hello'
                   result[link_desc] = full_link
                   #print result[link_desc]

    reqx.close

#Will include price later
#for result_link in child.find_all("a",class_="i"):
#get text from this child

def print_result():
    for key in result:
        #print >> f, key+":\n"+result[key]+"\n"

        print key+":\n"+result[key]+"\n"

print_result()
search_all_cities()
print_result()
