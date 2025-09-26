from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from scrape import Scrape

class CottonOn(Scrape):
    def __init__(self):
        super().__init__("Cotton On")

    def run(self):
        self.scrape("men/mens-clothing/mens-tops/", "Tops")
        self.scrape("women/womens-clothing/womens-tops/", "Tops")
        self.scrape("men/men-denim/mens-jeans-1/", "Bottoms")
        self.scrape("men/mens-clothing/mens-pants/", "Bottoms")
        self.scrape("women/womens-clothing/womens-pants/", "Bottoms")
        self.scrape("women/womens-clothing/womens-jeans/", "Bottoms")

    def scrape(self, page, clothing_type):
        url = "https://cottonon.com/AU/co/" + page
        driver = webdriver.Chrome()
        driver.get(url)

        while True:
            try:
                button = driver.find_element(By.CLASS_NAME, "load-more-btn")
                button.click()
                time.sleep(1) 
                
            except Exception as e:
                print(f"An error occurred: {e}")
                break
        
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = soup.find_all("div", class_="product-tile")
        items = []

        for product in products:
            item = {}
            item["title"] = product.find("a", class_="name-link").text.replace("\n", "")
            item["brand"] = self.brand
            item["link"] = product.find("a", class_="thumb-link")["href"]
            item["img"] = product.find("img")["src"]
            item["price"] = product.find("span", class_="product-sales-price").text.replace("\n", "").replace(" ", "")[1:]
            item["type"] = clothing_type

            if item not in items:
                items.append(item)
            
        for item in items:
            self.add_to_db(item)


CottonOn().run()
