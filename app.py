from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.jinja")

@app.route("/browse")
def browse():
    return render_template("browse.jinja")

if __name__ == "__main__":
    app.run(debug=True)