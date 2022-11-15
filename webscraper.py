from re import I
import requests
from bs4 import BeautifulSoup
import csv
import time
import os

# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
# 'Accept':'	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
# }

# proxy = '193.122.71.184:3128'
# url = 'https://httpbin.org/ip'

# web = requests.get(url , proxies={'https':proxy})
# print(web.json())


proxy_list = []
clean_list = []
site = 'https://free-proxy-list.net/'
good_proxy = ''

# function, that connect to free-proxy-list.net and scrape proxies from it.
def get_proxies(url):
    global proxy_list, clean_list
    web = requests.get(url)
    soup = BeautifulSoup(web.text, 'lxml' )
    table = soup.find('table')
    rows = soup.find_all('tr')
    headers = [i.text for i in rows[0]]
    for i in rows:
        proxy_list.append([y.text for y in i])
    for row in proxy_list[1:-17]:
        # if row[4] == 'elite proxy' and row[6] == 'yes':
            clean_list.append(row[0] + ':' + row[1])
    return 

# function for testing if scraped proxies work.
def try_proxies(url):
    global clean_list
    index = 0
    while index < len(clean_list):
        try:
            print(f'trying {clean_list[index]}')
            web = requests.get(url, proxies={'https': clean_list[index]}, timeout=5)
            soup = BeautifulSoup(web.content, 'html.parser')
            # print(web.json())
            print('passed')
            print('Loading page...')
            time.sleep(5)
            good_proxy = 'https://' + clean_list[index]
            
            # scrape_web('http://books.toscrape.com/', good_proxy)
            return good_proxy
        except:
            print('Bad proxy...')
            index += 1
            print(index)
    return 
# get_proxies(site)
# try_proxies('http://books.toscrape.com/')

proxy = '80.48.119.28:8080'
url = 'http://books.toscrape.com'

# function for scraping specific url
def scrape_web(url,proxy):
    web = requests.get(url, proxies={'https': proxy})
    soup = BeautifulSoup(web.content, 'html.parser')
    lists = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
    with open('scraped_data.csv', 'a+', encoding='utf8', newline='') as file:
        f = 'scraped_data.csv'
        thewriter = csv.writer(file)
        thereader = csv.reader(file)
        header = ['Title', 'Price']
        if os.stat(f).st_size == 0:
            thewriter.writerow(header)
        
        for i in lists:
            title = i.find('h3').text.replace('\n','')
            # year = i.find('span', class_= 'listitem-info-year').text.replace('\n','')
            # power = i.find('a', class_= 'listitem-info-kw').text.replace('\n','')
            price = i.find('p', class_='price_color').text.replace('\n','')
            # link = i.find('a', class_= 'listitem-link')['href'].replace('\n','')
            info = [title, price]
            thewriter.writerow(info)
    return soup

# for changing pages on selected url
def next_page(soup):
    page = soup.find('ul', class_='pager')
    if page.find('li', class_='next'):
        if page.find('li', class_='next').a['href'] == 'catalogue/page-2.html':
            url = 'http://books.toscrape.com/' + str(page.find('li', class_='next').a['href'])
        else:
            url = 'http://books.toscrape.com/catalogue/' + str(page.find('li', class_='next').a['href'])
        print(url)
        return url
    else:
        return
get_proxies(site)
try_proxies('http://books.toscrape.com/')
while True:
    soup = scrape_web(url, good_proxy)
    url = next_page(soup)
    if not url:
        break




 