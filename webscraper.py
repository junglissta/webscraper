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

# Scrape proxy list from free-proxy-list.net
def get_proxies(url):
    global proxy_list, clean_list
    # Make a request to the url
    web = requests.get(url)
    # Create a BeautifulSoup object from the HTML of the page
    soup = BeautifulSoup(web.text, 'lxml' )
    # Find the table element on the page
    table = soup.find('table')
    # Find all of the rows in the table
    rows = soup.find_all('tr')
    # Extract the headers from the first row
    headers = [i.text for i in rows[0]]
    # Add all of the rows to the proxy list
    for i in rows:
        proxy_list.append([y.text for y in i])
    # Iterate through the rows and add the valid proxies to the clean list
    for row in proxy_list[1:-17]:
        # if row[4] == 'elite proxy' and row[6] == 'yes':
            clean_list.append(row[0] + ':' + row[1])
    return 

# Test the scraped proxies to see which ones are working
def try_proxies(url):
    global clean_list
    # Initialize the index counter
    index = 0
    # Iterate through the list of proxies
    while index < len(clean_list):
        try:
            print(f'trying {clean_list[index]}')
            # Make a request to the url using the current proxy
            web = requests.get(url, proxies={'https': clean_list[index]}, timeout=5
            # Create a BeautifulSoup object from the HTML of the page
            soup = BeautifulSoup(web.content, 'html.parser')
            # The request was successful, so set the good_proxy variable to the current proxy
            good_proxy = 'https://' + clean_list[index]
            print('passed')
            print('Loading page...')
            # Sleep for 5 seconds to avoid overloading the server
            time.sleep(5)
            # Scrape the data from the website using the good_proxy
            # scrape_web('http://books.toscrape.com/', good_proxy)
            return good_proxy
        except:
            # The request failed, so print a message and move on to the next proxy
            print('Bad proxy...')
            index += 1
            print(index)
    return 
# get_proxies(site)
# try_proxies('http://books.toscrape.com/')

proxy = '80.48.119.28:8080'
url = 'http://books.toscrape.com'

def scrape_web(url,proxy):
    # Make a request to the website using the given proxy
    web = requests.get(url, proxies={'https': proxy})
    # Create a BeautifulSoup object from the HTML of the page
    soup = BeautifulSoup(web.content, 'html.parser')
    # Find all of the list elements with the specified class
    lists = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
    # Open a file for writing in append mode, with utf8 encoding and a newline character between rows
    with open('scraped_data.csv', 'a+', encoding='utf8', newline='') as file:
        # Store the filename as a variable
        f = 'scraped_data.csv'
        # Create a CSV writer object
        thewriter = csv.writer(file)
        # Create a CSV reader object
        thereader = csv.reader(file)
        # Set the header row
        header = ['Title', 'Price']
        # If the file is empty, write the header row
        if os.stat(f).st_size == 0:
            thewriter.writerow(header)
        
        # Iterate through the list elements
        for i in lists:
            # Extract the title, price, and link from the list element
            title = i.find('h3').text.replace('\n','')
            # year = i.find('span', class_= 'listitem-info-year').text.replace('\n','')
            # power = i.find('a', class_= 'listitem-info-kw').text.replace('\n','')
            price = i.find('p', class_='price_color').text.replace('\n','')
            # link = i.find('a', class_= 'listitem-link')['href'].replace('\n','')
            # Create a list of the data to be written to the CSV
            info = [title, price]
            # Write the data to the CSV
            thewriter.writerow(info)
    # Return the BeautifulSoup object
    return soup

# Function for finding the link to the next page on the website
def next_page(soup):
    # Find the element containing the pagination links
    page = soup.find('ul', class_='pager')
    # If there is a 'next' button in the pagination element
    if page.find('li', class_='next'):
        # If the next page is the second page
        if page.find('li', class_='next').a['href'] == 'catalogue/page-2.html':
            # Set the URL to the second page
            url = 'http://books.toscrape.com/' + str(page.find('li', class_='next').a['href'])
        # If the next page is not the second page
        else:
            # Set the URL to the next page
            url = 'http://books.toscrape.com/catalogue/' + str(page.find('li', class_='next').a['href'])
        print(url)
        # Return the URL of the next page
        return url
    else:
        # If there is no 'next' button, return nothing
        return

# Scrape the list of proxies from free-proxy
get_proxies(site)
# Test the scraped proxies and get a working proxy
try_proxies('http://books.toscrape.com/')

# Scrape the pages of the website until there are no more pages
while True:
    # Scrape the current page of the website
    soup = scrape_web(url, good_proxy)
    # Get the URL of the next page
    url = next_page(soup)
    # If there is no URL for the next page, break the loop
    if not url:
        break



 
