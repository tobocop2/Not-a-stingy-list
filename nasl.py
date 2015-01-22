import requests
import grequests
import random
import time
from user_agents import user_agents
from bs4 import BeautifulSoup

def search_all_cities():
    #list for all request urls
    url_list = []

    print "Enter your query here: \n"
    query = raw_input().replace(' ','+')

    #random user agent taken from the list of user agents
    rand_user_agent = random.choice(user_agents)
    user_agent = {'User-Agent': rand_user_agent}
    cities = ['http://geo.craigslist.org/iso/us/','http://geo.craigslist.org/iso/ca/']
    responses = [requests.get(url,headers=user_agent) for url in cities]
    for res in responses:
        html_text = res.text
        soup = BeautifulSoup(html_text)
        for child in soup.find_all(id='list'):
            for link in child.find_all('a'):
                search_link = link.get('href')+"/search/cta?query="+query+"&sort=rel"
                city_res = requests.get(search_link)
                soup = BeautifulSoup(city_res.text)
                print soup.select('.totalcount')
                if len(soup.select('.totalcount')) > 0:
                    count = int(soup.select('.totalcount')[0].text)
                    print 'The item count %d' % count
                    url_list.append(search_link)
                    for i in range(100,count,100):
                        next_link = "%s/search/cta?s=%d&query=%s&sort=rel" % (link.get('href'),i,query)
                        print search_link
                        print next_link
                        url_list.append(next_link)
                else:
                    url_list.append(search_link)
                    print search_link
            city_res.close()
        res.close()

    get_results(query,url_list)


#The div with the "content" class contains all of the results. Each "hdrlnk" class contains the
#description as well as the url, which is why it's convenient to use this class.

def get_results(query,url_list):
    #result paring
    result = {}
    #sorted by time
    result2 = {}

    rand_user_agent = user_agents[random.randint(0,len(user_agents)-1)]
    user_agent = {'User-Agent': rand_user_agent}

    rs = (grequests.get(link,stream=False) for link in url_list)
    responses = grequests.map(rs,size=10)

    for req in responses:
        link = req.url.split('search')[0]
        print "searching: "+link+"\nfor "+query+"."
        html_text = req.text
        soup = BeautifulSoup(html_text)
        print link
        for child in soup.find_all("div",class_="content"):
            for result_link in child.find_all("a",class_="hdrlnk"):
                #If a link exists  must check if the result is local to prepend the full link
                if "html" in result_link.get('href'):
                    if "http" not in result_link.get('href'):
                        full_link = link+result_link.get('href')
                    else:
                        full_link = result_link.get('href')

                    link_desc = result_link.get_text()
                    try:
                       link_desc.decode('ascii')
                    except UnicodeError:
                       link_desc = link_desc.encode('utf-8',"replace")
                    page_res = requests.get(full_link)
                    page_soup = BeautifulSoup(page_res.text)
                    try:
                        post_time_text = page_soup.find('time').text
                        post_time = str(post_time_text[:-2])
                        time_of_day = str(post_time_text[-2:])
                        post_time_struct = time.strptime(post_time, "%Y-%m-%d %H:%M")
                        unix_post_time = time.mktime(post_time_struct)
                    except AttributeError:
                        unix_post_time = 1149552000

                    if not link_desc in result:
                       result[link_desc] = full_link
                       result2[link_desc] = {full_link: unix_post_time}
        req.close()

    print_result(result,result2)

def print_result(result,result2):
    sorted_result = sorted([pair[::-1] for pair in (result.items())])
    sorted_result2 = sorted(result2.items(), key=lambda pair: pair[1].values(),reverse=True)

    with open('result0.html', 'w') as f1, open('result1.html', 'w') as f2:
        f1.write("<!DOCTYPE_HTML>\n <html>\n<head>\n<title>Not a stingy List</title>\n</head>\n<body>\n")
        for pair in sorted_result:
            #f.write("<br>"+str(pair[1])+"<a href="""+str(pair[0])+"<br>")
            desc = str(pair[1])
            url = str(pair[0])
            f1.write("<br>\n%s\n<br>\n<a href=\"%s\">%s</a><br>" % (desc,url,url))
            print"\n"+str(pair[1])+"\n"+str(pair[0])+"\n"
        f1.write("<br></body>\n</html>")

        f2.write("<!DOCTYPE_HTML>\n <html>\n<head>\n<title>Not a stingy List</title>\n</head>\n<body>\n")
        for pair in sorted_result2:
            desc = pair[0]
            post_time = pair[1][pair[1].keys()[0]]
            post_time = time.ctime(post_time)
            url = pair[1].keys()[0]
            try:
                f2.write(("<br>\n%s\n<br>\nPosted at: %s\n<br><a href=\"%s\">%s</a><br>" % (desc,post_time,url,url)))
            except UnicodeDecodeError:
                f2.write(("<br>\nCannot Load Description\n<br>\nPosted at: %s\n<br><a href=\"%s\">%s</a><br>" % (post_time,url,url)))

            print"\n"+str(pair[1])+"\n"+str(pair[0])+"\n"
        f2.write("<br></body>\n</html>")

search_all_cities()
