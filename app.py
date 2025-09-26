from flask import Flask, render_template, jsonify, session, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.jinja")


@app.route("/browse")
def browse():
    search_query = request.args.get("search", "")
    conn = sqlite3.connect("product_data.db")
    c = conn.cursor()

    # -- Product Search --
    like_pattern = f"%{search_query}%"
    c.execute(
        "SELECT Product.id, title, type, Product.link, Product.img, price, Brand.img, Brand.name FROM Product "\
        "Join Brand ON Product.brand = Brand.id "\
        "WHERE title LIKE ? OR type LIKE ?",
        (like_pattern, like_pattern)
    )
    rows = c.fetchall()
    
    items_list = [
        {"id": row[0], "title": row[1], "type": row[2], "link": row[3], "img": row[4], "price": row[5], "brand_logo": row[6], "brand_name": row[7]}
        for row in rows
    ]

    # -- Brand List --
    c.execute("SELECT id, name, img FROM Brand")
    brands_rows = c.fetchall()

    brands_list = [
        {"id": row[0], "name": row[1], "img": row[2]} for row in brands_rows
    ]

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
            rows = db.execute(f"SELECT id, title, price, img, link FROM Product WHERE id IN ({placeholders})", ids).fetchall()
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
                "qty": qty,
                "line_total": line_total
            })
    return render_template("cart.html", items=products, subtotal=subtotal)

def cart_add():
    data = request.get_json(silent=True) or request.form
    try:
        pid = int(data.get("product_id"))
        qty = int(data.get("qty", 1))
        if qty < 1:
            qty = 1
    except (TypeError, ValueError):
        return jsonify({"ok": False, "error": "Invalide product/qty"}), 400
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
    cart = ensure_cart()
    if qty <= 0:
        cart.pop(str(pid), None)
    else:
        cart[str(pid), None]
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


if __name__ == "__main__":
    app.run(debug=True)