import requests
from bs4 import BeautifulSoup
import smtplib
import  credentials

URL = 'https://www.amazon.de/-/en/Labists-Raspberry-Ultimate-Class10-switching/dp/B07W7Q6ZC9/ref=sr_1_4?dchild=1&keywords=raspberry+pi&qid=1613641182&s=ce-de&sr=1-4'
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'
}
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

def check_price():
    try:
        title = soup.find(id="productTitle").get_text()
        price = soup.find(id="priceblock_dealprice").get_text()
    except:
        print('ERROR')
    converted_price = float(price[1:])
    if(converted_price > 51.00):
        send_mail()

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(credentials.email_from, credentials.password)
    subject = "PRICE REDUCED"
    body = 'check the link https://www.amazon.de/-/en/Labists-Raspberry-Ultimate-Class10-switching/dp/B07W7Q6ZC9/ref=sr_1_4?dchild=1&keywords=raspberry+pi&qid=1613641182&s=ce-de&sr=1-4 '
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        credentials.email_from,
        credentials.email_to,
        msg
    )

    print('EMAIL SENT')
    server.quit()

check_price()