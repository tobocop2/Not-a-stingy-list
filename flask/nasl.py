import requests
import random
import time
import Queue
import threading
import multiprocessing
from user_agents import user_agents
from bs4 import BeautifulSoup

#Currently set up for multithreading. Will look into asynchronous request handling


#test query
#print "Enter your query here: \n"
#query = raw_input().replace(' ','+')
#query = '9c1'

#result paring
result = {}

#Queue used for request urls
url_queue = Queue.Queue()

#number of cpu coresu
num_cores = multiprocessing.cpu_count()

#resulting output file
#f=open('result.log', 'w')

def search_all_cities(query):

    #random user agent taken from the list of user agents
    rand_user_agent = user_agents[random.randint(0,len(user_agents)-1)]
    user_agent = {'User-Agent': rand_user_agent}
    req = requests.get("http://geo.craigslist.org/iso/us/",headers=user_agent)
    html_text = req.text
    soup = BeautifulSoup(html_text)

    for child in soup.find_all(id='list'):
        for link in child.find_all('a'):
            #get_results((link.get('href')))
            url_queue.put(link.get('href')+"search/sss?query="+query+"&sort=rel"
)

    req.close

#The div with the "content" class contains all of the results. Each "hdrlnk" class contains the
#description as well as the url, which is why it's convenient to use this class.

def get_results():

    rand_user_agent = user_agents[random.randint(0,len(user_agents)-1)]
    user_agent = {'User-Agent': rand_user_agent}

    while True:
        if not url_queue.empty():
            link = url_queue.get()
        #print "searching: "+link+"\nfor "+query+"."
        #req_link = link+"search/sss?query="+query+"&sort=rel"
        req_link = link

        sleep_time = random.random()
        #time.sleep(sleep_time)

        req = requests.get(req_link,headers=user_agent)
        html_text = req.text
        soup = BeautifulSoup(html_text)

        for child in soup.find_all("div",class_="content"):
            for result_link in child.find_all("a",class_="hdrlnk"):
                #If a link exists  must check if the result is local to prepend the full link
                if "html" in result_link.get('href'):
                    if "http" not in result_link.get('href'):
                        link = req_link.split('search')[0]
                        full_link = link+result_link.get('href')
                    else:
                        full_link = result_link.get('href')

                    link_desc = result_link.get_text().decode('utf-8')
                    '''try:
                       link_desc.decode('ascii')
                    except UnicodeError:
                       link_desc = str(link_desc.encode('utf-8',"replace"))
                       '''
                    if not link_desc in result:
                       result[link_desc] = full_link
                       #print_result()
        req.close
        url_queue.task_done()


#Will include price later
#for result_link in child.find_all("a",class_="i"):
#get text from this child

def threaded_search():

    #print("Creating %d threads" % num_cores)
    for i in range(0,10):
         t = threading.Thread(target=get_results)
         t.daemon = True
         t.start()
    url_queue.join()
    return result

'''def print_result():
    for key in result:
        f.write("\n"+str(key)+"\n"+str(result[key])+"\n")
        print "\n"+str(key)+"\n"+str(result[key])+"\n"
'''

#search_all_cities()
#threaded_search()
#get_results()
