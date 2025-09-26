from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import sqlite3
from scrape import Scrape

class Uniqlo(Scrape):
    def __init__(self):
        super().__init__("Uniqlo")

    def run(self):
        # Note: Need to whole brand in table before running or will be double ups
        self.scrape("men/tops", "Tops")
        self.scrape("women/tops", "Tops")
        self.scrape("men/bottoms", "Bottoms")
        self.scrape("women/bottoms", "Bottoms")

    def scrape(self, page, clothing_type):
        print("Running", page + "...")
        url = "https://www.uniqlo.com/au/en/" + page
        driver = webdriver.Chrome()
        driver.get(url)
        initial_soup = BeautifulSoup(driver.page_source, "html.parser")
        search_results = int(initial_soup.find("span", class_="fr-ec-body fr-ec-body--color-primary-dark fr-ec-body--standard fr-ec-text-align-left fr-ec-text-transform-normal").text.split()[1])
        search_count = len(initial_soup.find_all("div", class_="fr-ec-product-tile-resize-wrapper"))
      
        while search_count < search_results:
            print(search_results, search_count)

            # Move page
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_UP)
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_UP)
            time.sleep(2)
            check_soup = BeautifulSoup(driver.page_source, "html.parser")
            search_count = len(check_soup.find_all("div", class_="fr-ec-product-tile-resize-wrapper"))

        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = soup.find_all("div", class_="fr-ec-product-tile-resize-wrapper")
        items = []

        for product in products:
            item = {}
            item["title"] = product.find("img")["alt"]
            item["brand"] = self.brand
            item["link"] = "www.uniqlo.com" + product.find("a")["href"]
            item["img"] = product.find("img")["src"].split("?")[0]
            item["price"] = product.find("p", class_="fr-ec-price-text").text[1:]
            item["type"] = clothing_type
            
            if item not in items:
                items.append(item)

        for item in items:
            self.add_to_db(item)

uniqlo = Uniqlo()
uniqlo.run()