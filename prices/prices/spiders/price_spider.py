import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from amazon_config import (
    get_web_driver_options,
    get_chrome_web_driver,
    set_browser_as_incognito,
    set_ignore_certificate_error,
    DIRECTORY,
    NAME, CURRENCY,
    FILTERS,
    BASE_URL,
    MAX_PRICE,
    MIN_PRICE
)


class AmazonAPI:
    def __init__(self, search_term, filters, base_url, currency):
        self.base_url = base_url
        self.search_term = search_term
        options = get_web_driver_options()
        set_browser_as_incognito(options)
        set_ignore_certificate_error(options)
        self.driver = get_chrome_web_driver(options)
        self.currency = currency
        self.price_filter = f"&rh=p_36%3A{filters['min']}00-{filters['max']}00"

    def run(self):
        links = self.get_products_links()
        time.sleep(1)
        if not links:
            print("Stopped script")
            return
        print(f"Got {len(links)} links to products")
        products = self.get_products_info(links)
        self.driver.quit()
        return products

    def get_products_links(self):
        links = []
        self.driver.get(self.base_url)
        element = self.driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
        element.send_keys(self.search_term)
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        self.driver.get(f'{self.driver.current_url}{self.price_filter}')
        time.sleep(2)
        result_list = self.driver.find_elements_by_class_name('s-result-list')

        try:
            results = result_list[0].find_elements_by_xpath(
                '//div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a')
            links = [link.get_attribute('href') for link in results]
            return links
        except Exception as e:
            print("No results....")
            print(e)
            return links

    def get_products_info(self, links):
        asins = self.get_asins(links)
        products = []
        for asin in asins:
            product = self.get_single_product_info(asin)
            if product:
                products.append(product)
        return products

    def get_single_product_info(self, asin):
        print(f"product ID: {asin} - getting data..")
        product_short_url = self.shorten_url(asin)
        self.driver.get(f'{product_short_url}?language=en_GB')
        time.sleep(2)
        title = self.get_title(),
        price = self.get_price(),
        old_price = self.get_old_price()
        discount = self.calculate_discount()
        if title and price:
            product_info = {
                'asin': asin,
                'url': product_short_url,
                'title': title,
                'price': price,
                'old_price': old_price,
                'discount': discount
            }
            return product_info
        return None

    def get_title(self):
        try:
            return self.driver.find_element_by_id('productTitle').text
        except Exception as e:
            print(e)
            print(f"Can't find product title....")
            return None

    def get_price(self):
        price = None
        try:
            price = self.driver.find_element_by_xpath('//*[@id="priceblock_ourprice"]').text
            price = self.convert_price(price)
        except NoSuchElementException:
            try:
                availability = self.driver.find_element_by_id('availability').text
                if "Available" in availability:
                    price = self.driver.find_elements_by_class_name('olp-padding-right').text
                    price = price[price.find(self.currency):]
                    price = self.convert_price(price)
            except Exception as e:
                print(e)
                print(f"Can't get price product - {self.driver.current_url}")
                return None
        except Exception as e:
            print(e)
            print(f"Can't get price product - {self.driver.current_url}")
            return None
        return price

    def get_old_price(self):

        try:
            old_price = self.driver.find_element_by_xpath('//*[@id="price"]/table/tbody/tr[1]/td[2]/span[1]').text
            old_price = self.convert_price(old_price)
        except NoSuchElementException:
            try:
                discount_price = old_price
                if discount_price:
                    old_price = self.convert_price(old_price)
            except:
                old_price = self.get_price()
        return old_price

    def calculate_discount(self):
        # price = self.get_price()
        # old_price = self.get_old_price()
        # percent_price = old_price-price
        discount = None
        return discount

    def convert_old_price(self, old_price):
        old_price = old_price.split(self.currency)[1]
        try:
            old_price = old_price.split("\n")[0] + "." + old_price.split("\n")[1]
        except:
            Exception()
        return float(old_price)

    def convert_price(self, price):
        price = price.split(self.currency)[1]
        try:
            price = price.split("\n")[0] + "." + price.split("\n")[1]
        except:
            Exception()
        return float(price)

    def shorten_url(self, asin):
        return self.base_url + 'dp/' + asin

    def get_asins(self, links):
        return [self.get_asin(link) for link in links]

    @staticmethod
    def get_asin(product_link):
        return product_link[product_link.find('/dp/') + 4:product_link.find('/ref')]


class GenerateReport:
    def __init__(self):
        pass


if __name__ == '__main__':
    amazon = AmazonAPI(NAME, FILTERS, BASE_URL, CURRENCY)
    data = amazon.run()
    print(data)
