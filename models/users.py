import datetime
import sqlalchemy
from models.db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           unique=True,
                           autoincrement=True)

    login = sqlalchemy.Column(sqlalchemy.VARCHAR(50),
                              nullable=False)

    email = sqlalchemy.Column(sqlalchemy.VARCHAR(255),
                              index=True,
                              unique=True,
                              nullable=False)

    hashed_password = sqlalchemy.Column(sqlalchemy.String,
                                        nullable=False)

    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now,
                                     nullable=False)

    crypto_wallet = sqlalchemy.Column(sqlalchemy.VARCHAR(75),
                                      nullable=False)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
