import os
from dotenv import load_dotenv
from flask import Flask, render_template
assert load_dotenv(), "Даня, ты забыл .env добавить"

app = Flask(
    import_name="NFT-Market-Offense",
    static_folder=os.path.join("client", "static"),
    template_folder=os.path.join("client", "templates")
)
app.secret_key = os.getenv("WEBSITE_SECRET_KEY_AA01")


@app.route("/")
@app.route("/home")
def home():
    return render_template("base.html")


@app.route("/market")
def market():
    return render_template("base.html")


@app.route("/create")
def nft_creation():
    return render_template("base.html")


@app.route("/login")
def login():
    return render_template("base.html")


@app.route("/register")
def register():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)