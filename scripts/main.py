import os
import sys

# магическое заклинание (без него не работаит)
sys.path.append(os.getcwd())

from dotenv import load_dotenv
from flask import Flask, render_template
from cardsInfo import cardsInfoList
from models import db_session
from models.users import User
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
    return render_template("homepage.html")


@app.route("/market")
def market():
    cil = cardsInfoList
    return render_template("marketpage.html", cardsInfoList=cardsInfoList)


@app.route("/create")
def nft_creation():
    return render_template("createnftpage.html")


@app.route("/login")
def login():
    return render_template("base.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route('/filter')
def showFilter():
    return render_template('filter.html')


if __name__ == "__main__":
    db_session.global_init(os.path.join("db", "db.db"))
    session = db_session.create_session()
    print(session.query(User).all())
    app.run(host="127.0.0.1", port=5000, debug=True)
