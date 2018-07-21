#IMDB web scrapper written in python
#import the required modules
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import os

#feed the imdb homepage to give a starting point for the crawling process
imdb_link = 'https://www.imdb.com/'

#take user input in the form of query that is to be performed
print('Enter the name of the movie or tv-series')
query = input()

#set options to have google chrome operate in headless mode
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu') 
chrome_Handle = webdriver.Chrome('H://chromedriver.exe', chrome_options=options) 
chrome_Handle.get(imdb_link)

#get handle over search bar of imdb homepage and generate search query
search_bar = chrome_Handle.find_element_by_id('navbar-query')
search_bar.send_keys(query)
search_button = chrome_Handle.find_element_by_css_selector('#navbar-submit-button')
search_button.click()

#crawl on the page which is most likely to be the page desired by the user
req_link = chrome_Handle.find_element_by_css_selector('table.findList a')
chrome_Handle.get(req_link.get_attribute('href'))

sauce = chrome_Handle.page_source

#convert required  page html code into beautifulsoup object for better html processing 
os.system('cls')
soup = bs4.BeautifulSoup( sauce , 'lxml')

#scrape required information from the page in prettify accordingly to be displayed on the  screen
print(soup.find('h1').text)
print('IMDB Rating: '+soup.select('.ratingValue > strong')[0]['title'])
cast_list = pd.read_html(sauce)
cast_list[0].drop(columns=[2],inplace = True)
cast_list[0].fillna('',inplace=True)
print(cast_list[0])
print("StoryLine: ")
print(soup.select('#titleStoryLine > .canwrap > p')[0].text)
s = soup.select('#titleDetails')[0].text
print('\n')
for i in ['Edit','See more\xa0»','Official Sites:\nOfficial Facebook\n|\nOfficial site','See more on IMDbPro\xa0»',' See full technical specs\xa0»','\n\n','\n  Show more on\n  IMDbPro\xa0»','|']:
    stf = s.split(i)
    s = ''
    for j in stf:
        s += j
else:
    print(s)


