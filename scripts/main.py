import os
import sys

# магическое заклинание (без него не работает)
sys.path.append(os.getcwd())

import hashlib
from Crypto.Cipher import AES
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for
from cardsInfo import cardsInfoList
import datetime
from sqlalchemy import or_
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import RegisterForm, LoginForm, NFTCreationForm
from models import db_session
from models.users import User
from models.nfts import NFT
assert load_dotenv(), "Даня, ты забыл .env добавить"

app = Flask(
    import_name="NFT-Market-Offense",
    static_folder=os.path.join("client", "static"),
    template_folder=os.path.join("client", "templates")
)
app.secret_key = os.getenv("WEBSITE_SECRET_KEY_AA01")
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(hours=1)
enc_key = hashlib.sha256(app.secret_key.encode()).digest()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
@app.route("/home")
def home():
    return render_template("homepage.html")


@app.route("/market")
def market():
    db = db_session.create_session()
    entries = db.query(NFT).all()
    return render_template("marketpage.html", nfts=entries)


@app.route("/create", methods=["GET", "POST"])
@login_required
def nft_creation():
    form = NFTCreationForm()
    if form.validate_on_submit():
        file = form.image.data
        cipher = AES.new(enc_key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(file.read())

        newNFT = NFT(
            name=form.name.data,
            cost=form.cost.data,
            owner=current_user.id,
            image=ciphertext,
            token=tag
        )

        db = db_session.create_session()
        db.add(newNFT)
        db.commit()

        return redirect(url_for("nft_creation"))

    most_recent_error = None
    if form.errors:
        most_recent_error = tuple(form.errors.values())[0][-1]

    return render_template("createnftpage.html",
                           error=most_recent_error,
                           form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user.check_password(form.password.data):
            login_user(user)
            return redirect("/")

        return render_template("login.html",
                               error="Неправильный пароль",
                               form=form)

    most_recent_error = None
    if form.errors:
        most_recent_error = tuple(form.errors.values())[0][0]

    return render_template("login.html",
                           error=most_recent_error,
                           form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        user = User(
            login=form.login.data,
            email=form.email.data,
            crypto_wallet=form.wallet.data
        )

        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect("/")

    most_recent_error = None
    if form.errors:
        most_recent_error = tuple(form.errors.values())[0][0]
    return render_template("register.html", form=form, error=most_recent_error)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route('/filter')
def showFilter():
    return render_template('filter.html')


if __name__ == "__main__":
    db_session.global_init(os.path.join("db", "db.db"))
    # session = db_session.create_session()
    # user = session.query(User).first()
    # if user:
    #     print(user.nfts)
    app.run(host="127.0.0.1", port=5000, debug=True)
