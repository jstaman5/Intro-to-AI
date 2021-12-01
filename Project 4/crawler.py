#Web Crawler
from bs4.element import Doctype
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from socket import timeout
import string
import re

class WebCrawler:

    #constructor
    def __init__(self, root = 'https://eecs.utk.edu/', verbose = 'F'):
        self.root = root
        self.verbose = verbose
        self.docs = []
        self.links = []

    #return list of cleaned documents
    def get_documents(self):
        #self.clean()
        return self.docs

    #sets the list of cleaned documents
    def set_documents(self, d):
        self.docs = d

    #returns the list of collected links
    def get_links(self):
        return self.links

    #sets the list of collected links
    def set_links(self, l):
        self.links = l

    #collects the list of links starting with site s and hopping depth "d"
    def collect(self, s, d):
        depth = d
        site = s
        parent_links = []
        parent_links.append(site)
        total_links = []
        total_links.append(site)
        total_link_count = 1

        count = 1
        if self.verbose == 'T':
            print("[VERBOSE] 1. COLLECTING LINKS - STARTED\n")
            print("[VERBOSE] COLLECTED: LINK ({})\n".format(count))
        for d in range(depth+1):
        
            for new_root in parent_links:
                
                links = []
                root = new_root
                #print("Root: " + str(root))
                hdr = {'User-Agent': 'Mozilla/5.0'}
                req = Request(root, headers=hdr)

                #add in a timeout except
                try:
                    page = urlopen(req, timeout=10)
                except HTTPError as err:
                    print(err.code)
                except timeout:
                    print("connction's timeout expired")
                except:
                    continue
                    

                soup = BeautifulSoup(page, 'html.parser')

                #paragraphs = []

                for j in soup.find_all('div', {'class': 'main-content'}):
                    # find each of the <a> elements to identify links.
                    for k in j.find_all('a', href=True):
                        #root = site
                        #print("k[href] " + str(k['href']))
                        if(k['href'].startswith('/')):
                            link = site + k['href'][1:]
                        else:
                            link = k['href']
                        #print (link)

                        #only care about links that start with http
                        if(link.startswith('http')):
                            #make sure there are no repeats
                            link2 = link[:4] + 's' + link[4:]
                            link3 = link[:4] + link[5:]
                            if link in total_links or link2 in total_links or link3 in total_links:
                                pass
                            else:
                                utk = "utk.edu"
                                if utk in link:
                                    if self.verbose == 'T':
                                        count += 1
                                        
                                        print("[VERBOSE] COLLECTED: LINK ({})".format(count))
                                    links.append(link)
                                    total_links.append(link)


            # print(paragraphs)
                #print(links)
            # print('Number of Paragraphs: ' + str(len(paragraphs)))
                #print('Number of Links: ' + str(len(links)))
                total_link_count += len(links)
                #print(total_link_count)
                parent_links = links
        if self.verbose == 'T':
            print("[VERBOSE] 1. COLLECTING LINKS - DONE\n")
        self.links = total_links

    #extracts and stores all relevant text from the list of collected links
    def crawl(self):
        #site = self.root
        hdr = {'User-Agent': 'Mozilla/5.0'}

        if self.verbose == 'T':
            print("[VERBOSE] 2. CRAWLING LINKS - STARTED\n")
        #loop through the list of links
        for index, s in enumerate(self.links):
            if self.verbose == 'T':
                print("[VERBOSE] CRAWLING: LINK ({}/{})".format( index, len(self.links)))
            req = Request(s, headers=hdr)

            try:
                page = urlopen(req, timeout=10)
            except HTTPError as err:
                print(err.code)
            except timeout:
                continue
            except:
                continue

            soup = BeautifulSoup(page, 'html.parser')
            
            paragraphs = []
            #self.docs = []
            #find paragraphs and links in <div>
            for j in soup.find_all('div', {'class': ['entry-content', 'people', 'person_content']}):
                for i in j.find_all('p'):
                    #print (i.text)
                    paragraphs.append(i.text)

            #find table content   
            for j in soup.find_all('table', {'class': 'table_default'}):
                paragraphs.append(j.text)

            #create a document from the list of paragraphs
            doc = ''
            for p in paragraphs:
                doc += p
            #print(doc)
            self.docs.append(doc)
        if self.verbose == 'T':
            print("[VERBOSE] 2. CRAWLING LINKS - DONE\n")
        
    #remove Unicode, puncuation, remove twitter handles, remove double spaces, convert chars to lowercase
    def clean(self):
        
        if self.verbose == 'T':
            print("[VERBOSE] 3. CLEANING TEXT - STARTED\n")
        #clean it
        for i,d in enumerate(self.docs):
            #lower case
            d = d.lower()
            #get rid of punctuation
            d = d.translate(str.maketrans('', '', string.punctuation))
            #get rid of extra spaces
            d = re.sub(' +', ' ', d)
            #get rid of twitter handles (strings that start with @)
            d = re.sub(r'(\s)@\w+', r'\1', d)
            #get rid of unicode characters
            d = d.encode("ascii", "ignore").decode()
            self.docs[i] = d

        if self.verbose == 'T':
            print("[VERBOSE] 3. CLEANING TEXT - DONE\n")
        return self.docs