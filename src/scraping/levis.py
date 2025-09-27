from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from scrape import Scrape

class Levis(Scrape):
    def __init__(self):
        super().__init__(3)

    def run(self):
        self.scrape("men-tees-polos", "Tops")
        self.scrape("men-shirts", "Tops")
        self.scrape("men-jeans", "Bottoms")
        self.scrape("women-jeans", "Bottoms")
        self.scrape("women-tees", "Tops")
        self.scrape("women-shirts", "Tops")


    def scrape(self, page, clothing_type):
        url = "https://levis.com.au/collections/" + page
        driver = webdriver.Chrome()
        driver.get(url)
        items = []
        
        while True:
            try:
                soup = BeautifulSoup(driver.page_source, "html.parser")
                products = soup.find_all("li", class_="grid__item")
                
                for product in products:
                    item = {}
                    item["title"] = product["data-cnstrc-item-name"]
                    item["brand"] = self.brand
                    item["link"] = "https://levis.com.au/" + product.find("a", class_="sa-handler")["href"]
                    item["img"] = product.find("img")["src"]
                    item["price"] = product["data-cnstrc-item-price"]
                    item["type"] = clothing_type

                    if item not in items:
                        items.append(item)

                button = driver.find_element(By.CSS_SELECTOR, "a[aria-label='Next page']")
                button.click()
                time.sleep(2) 
                
            except Exception as e:
                print(f"An error occurred: {e}")
                break
        
            
        for item in items:
            self.add_to_db(item)

Levis().run()