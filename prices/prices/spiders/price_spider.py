import time

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
        print("Running script........")
        print(f"Searching for {self.search_term}....")
        links = self.get_products_links()
        time.sleep(1)
        if not links:
            print("Stopped script")
            return
        print(f"Got {len(links)} links to products")
        products = self.get_products_info(links)
        self.driver.quit()

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
            results = result_list[0].find_element_by_xpath(
                '//html/body/div[1]/div[2]/div[1]/div[2]/div/span[3]/div[2]/div[7]/div/span/div/div/div[2]')
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

    def get_single_product_info(self, asin):
        print(f"product ID: {asin} - getting data..")
        product_short_url = self.shorten_url(asin)
        self.driver.get(f'{product_short_url}?language=en_GB')
        time.sleep(2)
        title = self.get_title(),
        price = self.get_price()

    def get_title(self):
        try:
            return self.driver.find_element_by_id('productTitle').text
        except Exception as e:
            print(e)
            print(f"Can't find product title....")
            return None

    def get_price(self):
       return '999'

    def shorten_url(self, asin):
        return self.base_url + '/dp' + asin

    def get_asins(self, links):
        return [self.get_asin(link) for link in links]

    def get_asin(self, product_link):
        return product_link[product_link.find('/dp/') + 4:product_link.find('/ref')]


class GenerateReport:
    def __init__(self):
        pass


if __name__ == '__main__':
    print('HEYYYYY!!')
    amazon = AmazonAPI(NAME, FILTERS, BASE_URL, CURRENCY)
    amazon.run()
