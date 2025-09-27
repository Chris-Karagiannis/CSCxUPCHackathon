from abc import ABC, abstractmethod
import sqlite3

class Scrape(ABC):
    def __init__(self, brand):
        self.brand = brand

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def scrape(self, page, clothing_type):
        pass

    def add_to_db(self, item):
        conn = sqlite3.connect('product_data.db')
        sql =   "INSERT INTO Product (title, type, link, img, price, brand) " \
                "VALUES (?, ?, ?, ?, ?, ?) "
        
        conn.execute(sql, (item["title"], item["type"], item["link"], item["img"], item["price"], item["brand"]))
        
        conn.commit()
        conn.close()
