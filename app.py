from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.jinja")

@app.route("/browse")
def browse():
    search_query = request.args.get("query", "", type=str).strip()

    conn = sqlite3.connect("product_data.db")
    c = conn.cursor()
    if search_query:
        like_pattern = f"%{search_query}%"
        c.execute(
            "SELECT id, title, type, link, img, price FROM Product "
            "WHERE title LIKE ? OR type LIKE ?",
            (like_pattern, like_pattern)
        )
    else:
        c.execute("SELECT id, title, type, link, img, price FROM Product")
    rows = c.fetchall()
    conn.close()

    items_list = [
        {"id": row[0], "title": row[1], "type": row[2], "link": row[3], "img": row[4], "price": row[5]}
        for row in rows
    ]

    return render_template("browse.jinja", items=items_list, search_query=search_query)


if __name__ == "__main__":
    app.run(debug=True)