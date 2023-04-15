import os
import sys

# магическое заклинание (без него не работает)
sys.path.append(os.getcwd())

from dotenv import load_dotenv
from flask import Flask, render_template, redirect
from cardsInfo import cardsInfoList
import datetime
from flask_login import LoginManager, login_user, login_required, logout_user
from forms import RegisterForm, LoginForm
from models import db_session
from models.users import User
from forms import RegisterForm
assert load_dotenv(), "Даня, ты забыл .env добавить"

app = Flask(
    import_name="NFT-Market-Offense",
    static_folder=os.path.join("client", "static"),
    template_folder=os.path.join("client", "templates")
)
app.secret_key = os.getenv("WEBSITE_SECRET_KEY_AA01")
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=365)


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
    return render_template("marketpage.html", cardsInfoList=cardsInfoList)


@app.route("/create")
def nft_creation():
    return render_template("createnftpage.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")

        return render_template("login.html", form=form, message="Неправильный логин или пароль")

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_repeat.data:
            return render_template("register.html", form=form, message="Пароли не совпадают")

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template("register.html", form=form, message="Такой пользователь уже есть")

        user = User(
            login=form.login.data,
            email=form.email.data
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


@app.route('/filter')
def showFilter():
    return render_template('filter.html')


if __name__ == "__main__":
    db_session.global_init(os.path.join("db", "db.db"))
    session = db_session.create_session()
    print(session.query(User).all())
    app.run(host="127.0.0.1", port=5000, debug=True)
