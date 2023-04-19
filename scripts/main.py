from operator import or_
import os
import sys

# магическое заклинание (без него не работает)
sys.path.append(os.getcwd())

import hashlib
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash, abort
import datetime
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import RegisterForm, LoginForm, NFTCreationForm
from models import db_session
from sqlalchemy import or_
from models.users import User
from models.nfts import NFT
assert load_dotenv(), "Даня, ты забыл .env добавить"
from security import decrypt_image, encrypt_image, get_recent_error

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
    entries = db.query(NFT).filter(NFT.on_sale == 1).all()
    images = [decrypt_image(entry.image) for entry in entries]
    print(images)
    return render_template("marketpage.html", data=zip(entries, images))


@app.route("/create", methods=["GET", "POST"])
@login_required
def nft_creation():
    form = NFTCreationForm()
    if form.validate_on_submit():
        file = form.image.data
        image = encrypt_image(file.read())

        newNFT = NFT(
            name=form.name.data,
            cost=form.cost.data,
            owner=current_user.id,
            description=form.description.data,
            on_sale=form.is_selling.data,
            image=image
        )

        db = db_session.create_session()
        db.add(newNFT)
        db.commit()

        return redirect(url_for("nft_creation"))

    error = get_recent_error(form)
    return render_template("createnftpage.html",
                           error=error,
                           form=form, hint="Здесь будет отображаться ваша NFT")


@app.route("/buy/<int:nft_id>")
@login_required
def nft_buy(nft_id):
    return f"page for {nft_id}"


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")

        return render_template("login.html", form=form, error="Неправильный логин или пароль")

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        db_sess = db_session.create_session()
        entry = db_sess.query(User).filter(
            or_(
                User.email == form.email.data,
                User.login == form.login.data
            )
        ).first()

        if entry:
            error = "Такой логин уже есть"
            if entry.email == form.email.data:
                error = "Такая почта уже зарегистрирована"

            return render_template("register.html",
                                   error=error,
                                   form=form)

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

    return render_template("register.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/profile/<int:id>")
def profile(id):
    db = db_session.create_session()
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        return abort(404)

    entries = db.query(NFT).filter(NFT.owner == user.id).all()
    images = [decrypt_image(entry.image) for entry in entries]

    print(user)
    return render_template("profile.html", profile_user=user, data=zip(entries, images))


@app.route("/nft/edit/<int:nft_id>", methods=["GET", "POST"])
@login_required
def nft_edit(nft_id):
    form = NFTCreationForm()
    db = db_session.create_session()
    nft = db.query(NFT).filter(NFT.id == nft_id).first()

    if nft is None:
        return abort(404)

    if form.is_submitted():
        # // Скип валидации при изменении (иначе требует файл)
        form.image.data = b"d"

    if form.validate_on_submit():
        nft.name = form.name.data
        nft.cost = form.cost.data
        nft.description = form.description.data
        nft.on_sale = form.is_selling.data
        db.commit()

        flash("Успешно изменено!")
        return redirect(url_for("nft_edit", nft_id=nft_id))

    form.name.data = nft.name
    form.cost.data = nft.cost
    form.description.data = nft.description
    form.submit.label.text = "Сохранить"
    form.is_selling.data = nft.on_sale

    if nft is None:
        return abort(404)

    if nft.owner != current_user.id and current_user.id != 1:
        return abort(401)

    error = get_recent_error(form)
    return render_template("updatenftpage.html",
                           nft=nft, form=form,
                           image=decrypt_image(nft.image),
                           hint="Изображение NFT",
                           error=error)


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
