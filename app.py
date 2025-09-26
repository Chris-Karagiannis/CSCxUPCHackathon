from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/Cart")
def Cart():
    return render_template("cart.html")

if __name__ == '__main__':
    app.run(debug=True)