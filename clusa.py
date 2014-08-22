import requests
import random
import time
import Queue
import threading
import multiprocessing
from bs4 import BeautifulSoup

#user_agent = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0'}

#test query
query = "9c1"

#result paring
result = {}

#Queue used for request urls
url_queue = Queue.Queue()

#number of cpu coresu
num_cores = multiprocessing.cpu_count()

#resulting output file
f=open('result.log', 'w')

def get_link(url_queue):
    if not url_queue.empty():
        link = url_queue.get()
        url_queue.put(link)

    return link

def search_all_cities():

    req = requests.get("http://geo.craigslist.org/iso/us/")
    html_text = req.text
    soup = BeautifulSoup(html_text)

    for child in soup.find_all(id='list'):
        for link in child.find_all('a'):
            #get_results((link.get('href')))
            url_queue.put(link.get('href'))

    req.close

#The div with the "content" class contains all of the results. Each "hdrlnk" class contains the
#description as well as the url, which is why it's convenient to use this class.

def get_results():
    print 'start'

    while True:
        #link = get_link(url_queue)
        if not url_queue.empty():
            link = url_queue.get()
        print "searching: "+link+"\nfor "+query+"."
        req_link = link+"search/sss?query="+query+"&sort=rel"
        #sleep_time = random.random()
        #time.sleep(sleep_time)
        reqx = requests.get(req_link)
        html_textx = reqx.text
        soupx = BeautifulSoup(html_textx)

        for child in soupx.find_all("div",class_="content"):
            for result_link in child.find_all("a",class_="hdrlnk"):
                #If a link exists  must check if the result is local to prepend the full link
                if "html" in result_link.get('href'):
                    if "http" not in result_link.get('href'):
                        full_link = link+result_link.get('href')
                    else:
                        full_link = result_link.get('href')

                    link_desc = result_link.get_text()
                    '''try:
                       link_desc.decode('ascii')
                    except UnicodeError:
                       link_desc = unicode(link_desc, "utf-8")
                    '''
                    if not link_desc in result:
                       result[link_desc] = full_link
                       #print_result()
        reqx.close
        print 'finishing task'
        url_queue.task_done()


#Will include price later
#for result_link in child.find_all("a",class_="i"):
#get text from this child

def threaded_search():

    print("Creating %d threads" % num_cores)
    for i in range(num_cores):
         t = threading.Thread(target=get_results)
         t.daemon = True
         t.start()

def print_result():
    for key in result:
        f.write("\n"+key+"\n"+result[key]+"\n")
        print "\n"+key+"\n"+result[key]+"\n"

search_all_cities()
threaded_search()
url_queue.join()
print_result()
f.close
