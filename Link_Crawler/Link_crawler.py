# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 16:21:22 2018

@author: Ashwin Dhakaita
"""
#import the required libraries
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
from urllib.parse import urlparse
import os

#function to get the base url and relinquish the extra parameters from a url
def get_base_url(url):
    try:
        res = urlparse(url).netloc
        res = res.split('.')
        res = res[-2] + '.' + res[-1]
        return res
    except:
        return ''

#function to write the values to a file given by its path    
def write_to_file(path , value):
    if os.path.isfile(path):
        f = open(path,'a')
    else:
        f = open(path,'w')
    f.write(value+'\n')
    f.close()

#Extracts link from a given HTML code segment and adds to the list of the web_crawler
class Extractor(HTMLParser):
    def __init__(self,url,base_url,path):
        super().__init__()
        self.base_url = base_url
        self.path = path
        self.url = url
        
    def handle_starttag(self,tag,attrib):
        for (attr,value) in attrib:
            if attr == 'href':
                value = parse.urljoin(self.url,value)
               
                if get_base_url(value)==self.base_url:
                    if value not in web_crawler.url_master:
                        write_to_file(self.path,value)
                        web_crawler.url_list_sec.add(value)
                        web_crawler.url_master.add(value)
                    
    def error(self):
        pass

#the web crawler class which governs all the processes 
#all methods are static and no objects of the class are therefore created
class web_crawler:
    url_list = set()
    url_list_sec = set()
    url_master = set()
    
    @staticmethod
    def get_response(url):
        try:
            response = urlopen(url)
            if 'text/html' in response.getheader('Content-Type'):
                response = response.read()
                response = response.decode('utf-8')
                ext = Extractor(url,get_base_url(url),"H://results.txt")
                ext.feed(response)
        except:
            return
    
    #starts the web crawler
    @staticmethod
    def start_crawler():
        for url in web_crawler.url_list:
            web_crawler.get_response(url)
        else:
            web_crawler.url_list = web_crawler.url_list_sec
            web_crawler.url_list_sec = set()
            if len(web_crawler.url_list)>0:
                web_crawler.start_crawler()
            else:
                return

#assigning values to the crawler and starting it    
web_crawler.url_list.add("https://www.kaggle.com")
web_crawler.url_master.add("https://www.kaggle.com")
web_crawler.start_crawler()