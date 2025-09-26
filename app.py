from flask import Flask, render_template, request, jsonify
import sqlite3
import math

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.jinja")

@app.route("/browse")
def browse():
    per_page = 12
    page = request.args.get("page", 1, type=int)
    conn = sqlite3.connect("product_data.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM Product")
    total_items = c.fetchone()[0]

    # Compute total pages
    total_pages = math.ceil(total_items / per_page) if total_items > 0 else 0

    # Pagination window: only needed if total_pages > 1
    if total_pages > 1:
        start_page = max(1, page - 1)
        end_page = min(total_pages, start_page + 2)
        # Ensure window has 3 pages if possible
        if (end_page - start_page) < 2:
            start_page = max(1, end_page - 2)
    else:
        start_page, end_page = 0, 0  # force empty loop in template

    # Fetch items for current page
    offset = (page - 1) * per_page
    c.execute("SELECT id, title, type, link, img, price FROM Product LIMIT ? OFFSET ?", (per_page, offset))
    items = c.fetchall()
    conn.close()

    # Convert tuples to dicts for Jinja
    items_list = [
        {"id": row[0], "title": row[1], "type": row[2], "link": row[3], "img": row[4], "price": row[5]}
        for row in items
    ]

    return render_template(
        "browse.jinja",
        items=items_list,
        page=page,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page
    )

if __name__ == "__main__":
    app.run(debug=True)