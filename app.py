from flask import Flask, render_template, jsonify, session, request
import sqlite3

app = Flask(__name__)
app.secret_key = "mySecret"

@app.route("/")
def index():
    return render_template("index.jinja")


@app.route("/browse")
def browse():
    search_query = request.args.get("search", "")
    sort_by = request.args.get("sortBy", "")
    brand_filter = request.args.get("brandFilter", "")

    page = int(request.args.get("page", 1))  # default to page 1
    items_per_page = 15
    offset = (page - 1) * items_per_page


    conn = sqlite3.connect("product_data.db")
    c = conn.cursor()

    # Sorting logic
    sort_options = {
        "price_asc": "price ASC",
        "price_desc": "price DESC",
        "title_asc": "title ASC",
        "title_desc": "title DESC",
        "type_asc": "type ASC",
        "type_desc": "type DESC",
    }
    order_clause = sort_options.get(sort_by, "Product.id ASC")

    # Base query
    query = """
        SELECT Product.id, title, type, Product.link, Product.img, price, Brand.img, Brand.name, Brand.link
        FROM Product
        JOIN Brand ON Product.brand = Brand.id
        WHERE (title LIKE ? OR type LIKE ?)
    """
    params = [f"%{search_query}%", f"%{search_query}%"]

    # Brand filter
    if brand_filter:
        query += " AND Brand.id = ?"
        params.append(brand_filter)

    query += f" ORDER BY {order_clause} LIMIT 200"
    c.execute(query, params)
    rows = c.fetchall()

    items_list = [
        {
            "id": row[0],
            "title": row[1],
            "type": row[2],
            "link": row[3],
            "img": row[4],
            "price": row[5],
            "brand_logo": row[6],
            "brand_name": row[7],
            "brand_link": row[8],
        }
        for row in rows
    ]

    # Brand list for dropdown
    c.execute("SELECT id, name, img FROM Brand")
    brands_rows = c.fetchall()
    brands_list = [{"id": row[0], "name": row[1], "img": row[2]} for row in brands_rows]

    conn.close()
    return render_template("browse.jinja", items=items_list, brands=brands_list)

    

@app.route("/Cart")
def Cart():
    cart = ensure_cart()
    ids = [int(pid) for pid in cart.keys()]
    products = []
    subtotal = 0.0

    if ids:
        placeholders = ",".join(["?"]*len(ids))
        with get_db() as db:
            rows = db.execute(f"SELECT p.id as id, title as title, price, p.img as img, p.link as link, p.brand as brand, b.img as brand_logo FROM Product as p JOIN Brand as b ON p.brand = b.id WHERE p.id IN ({placeholders})", ids).fetchall()
        for row in rows:
            qty = int(cart.get(str(row["id"]), 0))
            line_total = row["price"] * qty
            subtotal += line_total
            products.append({
                "id": row["id"],
                "title": row["title"],
                "img": row["img"],
                "link": row["link"],
                "price": row["price"],
                "brand": row["brand"],
                "brand_logo": row["brand_logo"],
                "qty": qty,
                "line_total": line_total
            })
    return render_template("cart.jinja", items=products, subtotal=subtotal)

@app.post("/cart/add")
def cart_add():
    data = request.get_json(silent=True) or request.form
    pid = int(data.get("product_id"))
    qty = int(data.get("qty", 1))
    if qty < 1:
        qty = 1

    with get_db() as db:
        if not db.execute("SELECT 1 FROM Product WHERE id = ?", (pid,)).fetchone():
            return jsonify({"ok": False, "error": "Product not found"}), 404

    cart = ensure_cart()
    cart[str(pid)] = cart.get(str(pid), 0) + qty
    session["cart"] = cart

    return jsonify({"ok": True, "cartCount": sum(int(v) for v in cart.values())})


@app.post("/cart/update")
def cart_update():
    data = request.get_json(silent=True) or request.form
    try:
        pid = int(data.get("product_id"))
        qty = int(data.get("qty", 1))
    except (TypeError, ValueError):
        return jsonify({"ok": False, "error": "invalid product"}), 400
    qty = max(0, qty)
    cart = ensure_cart()
    if qty <= 0:
        cart.pop(str(pid), None)
    else:
        cart[str(pid)] = qty

    session["cart"] = cart
    return jsonify({"ok": True, "cartCount": sum(int(v) for v in cart.values())})

@app.post("/cart/clear")
def cart_clear():
    session["cart"] = {}
    return jsonify({"ok": True, "cartCount": 0})

def get_db():
    conn = sqlite3.connect("product_data.db")
    conn.row_factory = sqlite3.Row
    return conn

def ensure_cart():
    if "cart" not in session:
        session["cart"] = {}
    return session["cart"]

@app.post("/mockups/save")
def mockup_save():
    data = request.get_json()
    with get_db() as db:
        mid = db.insert("INSERT INTO mockups (title, template) VALUES (?, ?)", (data["title"], data["template"]))
    for s in data["slots"]:
        with get_db() as db:
            db.insert("""INSERT INTO mockup_slots (mockup_id, slot_key, product_id, x, y, w, h) VALUES (?,?,?,?,?,?)""",
                    (mid, s["slot"], s.get("product_id"), None, None, None, None))
    return jsonify({"ok": True, "id": mid})


if __name__ == "__main__":
    app.run(debug=True)