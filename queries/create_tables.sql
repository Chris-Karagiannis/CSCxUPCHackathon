DROP TABLE Product;

CREATE TABLE Product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    type TEXT,
    link TEXT,
    img TEXT,
    price REAL,
    brand TEXT
);