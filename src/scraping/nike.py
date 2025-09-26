from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import sqlite3
from scrape import Scrape

class Nike(Scrape):
    def __init__(self):
        super().__init__("Nike")

    def run(self):
        # Note: Need to whole brand in table before running or will be double ups
        self.scrape("tops-t-shirts-9om13", "Tops")
        self.scrape("trousers-tights-2kq19", "Bottoms")

    def scrape(self, page, clothing_type):
        url = "https://www.nike.com/au/w/" + page

        driver = webdriver.Chrome()
        driver.get(url)

        initial_soup = BeautifulSoup(driver.page_source, "html.parser")
        search_results = int(initial_soup.find("span", class_="wall-header__item_count").text[1:-1])
        last_position = 1

        print(search_results)

        while last_position < search_results:

            # Move page
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_UP)
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_UP)

            # Check soup
            check_soup = BeautifulSoup(driver.page_source, "html.parser")
            last_position = int(check_soup.find_all("div", class_="product-card")[-1]["data-product-position"])
            print(last_position)
            time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        figures = soup.find_all("div", class_="product-card")
        items = []

        for figure in figures:
            item = {}
            item["title"] = figure.find("a", class_="product-card__link-overlay").text
            item["brand"] = self.brand
            item["link"] = figure.find("a", class_="product-card__link-overlay")["href"]
            item["img"] = figure.find("img")["src"]

            try:
                item["price"] = float(figure.find("div", attrs={"data-testid":"product-price-reduced"}).text[1:])
            except:
                item["price"] = float(figure.find("div", attrs={"data-testid":"product-price"}).text[1:])

            item["type"] = clothing_type

            if item not in items:
                items.append(item)
        
        for item in items:
            self.add_to_db(item)


            