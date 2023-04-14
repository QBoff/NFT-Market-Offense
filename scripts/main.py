import os
import sys

# магическое заклинание (без него не работаит)
sys.path.append(os.getcwd())

from dotenv import load_dotenv
from flask import Flask
from models import db_session
from models.users import User
assert load_dotenv(), "Даня, ты забыл .env добавить"

app = Flask(
    import_name="NFT-Market-Offense",
    static_folder=os.path.join("client", "static")
)
app.secret_key = os.getenv("WEBSITE_SECRET_KEY_AA01")


@app.route("/")
def index():
    return "<body><h2>Даня пока ничего не сделал =)</h2></body>"


if __name__ == "__main__":
    db_session.global_init(os.path.join("db", "db.db"))
    session = db_session.create_session()
    print(session.query(User).all())
    # app.run(host="127.0.0.1", port=5000, debug=True)