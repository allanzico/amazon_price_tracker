import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pandas as pd
import smtplib
import credentials

# search term separated with a + sign for two words (samsung+tv)
searchTerm = 'tv'
session = HTMLSession()
deals_list = []
url = f'https://www.amazon.de/s?k={searchTerm}&i=electronics&ref=nb_sb_noss'
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'
}
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')


def get_data(url):
    r = session.get(url)
    r.html.render(sleep=1)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup


def get_deals(soup):
    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    for product in products:
        title = product.find('a', {'class': 'a-link-normal a-text-normal'}).text.strip()
        short_title = product.find('a', {'class': 'a-link-normal a-text-normal'}).text.strip()[:25]
        link = product.find('a', {'class': 'a-link-normal a-text-normal'})['href']
        try:
            sale_price = float(
                product.find_all('span', {'class': 'a-offscreen'})[0].text.replace('€', '').replace(',', '').strip())
            old_price = float(
                product.find_all('span', {'class': 'a-offscreen'})[1].text.replace('€', '').replace(',', '').strip())
        except:
            old_price = float(
                product.find('span', {'class': 'a-offscreen'}).text.replace('€', '').replace(',', '').strip())
        try:
            reviews = float(product.find('span', {'class': 'a-size-base'}).text.strip())
        except:
            reviews = 0

        sale_item = {
            'title': title,
            'short_title': short_title,
            'link': link,
            'sale_price': sale_price,
            'old_price': old_price
        }
        deals_list.append(sale_item)
    return

def get_next_page(soup):
    pages = soup.find('ul', {'class': 'a-pagination'})
    if not pages.find('li', {'class': 'a-disabled a-last'}):
        url = 'https://www.amazon.de/' + str(pages.find('li', {'class': 'a-last'}).find('a')['href'])
        return url
    else:
        return


while True:
    soup = get_data(url)
    get_deals(soup)
    url = get_next_page(soup)
    if not url:
        break
    else:
        print(len(deals_list))

# headers = {
#     "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'
# }
# page = requests.get(url, headers=headers)
# soup = BeautifulSoup(page.content, 'html.parser')

# def check_price():
#
#     title = soup.find(id="productTitle").get_text()
#     price = soup.find(id="priceblock_dealprice").get_text()
#     converted_price = float(price[1:])
#
#     if(converted_price > 51.00):
#         send_mail()
#
# def send_mail():
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.ehlo()
#     server.starttls()
#     server.ehlo()
#
#     server.login(credentials.email_from, credentials.password)
#     subject = "PRICE REDUCED"
#     body = 'check the link https://www.amazon.de/-/en/Labists-Raspberry-Ultimate-Class10-switching/dp/B07W7Q6ZC9/ref=sr_1_4?dchild=1&keywords=raspberry+pi&qid=1613641182&s=ce-de&sr=1-4 '
#     msg = f"Subject: {subject}\n\n{body}"
#     server.sendmail(
#         credentials.email_from,
#         credentials.email_to,
#         msg
#     )
#
#     print('EMAIL SENT')
#     server.quit()

# check_price()
