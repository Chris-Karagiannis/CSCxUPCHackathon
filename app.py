from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.jinja")

@app.route("/browse")
def browse():
    conn = sqlite3.connect("product_data.db")
    c = conn.cursor()
    c.execute("SELECT id, title, type, link, img, price FROM Product")
    items = c.fetchall()
    conn.close()

    # Convert to list of dicts (Jinja friendly)
    items_list = [
        {"id": row[0], "title": row[1], "type": row[2], "link": row[3], "img": row[4], "price": row[5]}
        for row in items
    ]

    return render_template("browse.jinja", items=items_list)

if __name__ == "__main__":
    app.run(debug=True)