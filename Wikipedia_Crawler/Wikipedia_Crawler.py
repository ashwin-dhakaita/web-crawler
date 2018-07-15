import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

print("Enter the Topic: ")
name = input()

url = 'https://en.wikipedia.org/wiki/Main_Page'

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu') 
chrome_Handle = webdriver.Chrome('H://chromedriver.exe', chrome_options=options) 
chrome_Handle.get(url)

search_bar = chrome_Handle.find_element_by_name('search')
search_bar.send_keys(name)
search_button = chrome_Handle.find_element_by_name('go')
search_button.click()

os.system('cls')

required_url = chrome_Handle.current_url
soup = bs4.BeautifulSoup(chrome_Handle.page_source, 'lxml')

html = str(soup)
for tag in soup.findAll('sup'):
    try:
        lis = html.split(str(tag))
        html = lis[0]+lis[1]
    except:
        continue

refined_soup = bs4.BeautifulSoup(html , 'lxml')       

screen_clear_flag = 0

for p in refined_soup.findAll('p'):
    if screen_clear_flag==0:
        os.system('cls')
        screen_clear_flag = 1
    print(p.text)

chrome_Handle.quit()