import datetime
import sqlalchemy
import secrets
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship
from models.db_session import SqlAlchemyBase
from models.transactions import Transaction
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
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

    api_key = sqlalchemy.Column(sqlalchemy.String(32),
                                unique=True,
                                default=secrets.token_hex(32))

    nfts = relationship("NFT", backref="owned_nfts")

    # // Не протестировано. Может и не работать собсна =)
    sent_transactions = relationship("Transaction",
                                     backref="sent_transactions",
                                     order_by=sqlalchemy.desc("Transaction.date"),
                                     foreign_keys=[Transaction.sender],
                                     viewonly=True)

    received_transactions = relationship("Transaction",
                                         backref="received_transactions",
                                         order_by=sqlalchemy.desc("Transaction.date"),
                                         foreign_keys=[Transaction.receiver],
                                         viewonly=True)

    all_transactions = relationship("Transaction",
                                    primaryjoin="or_(User.id==Transaction.sender, User.id==Transaction.receiver)", 
                                    order_by=sqlalchemy.desc("Transaction.date"),
                                    viewonly=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
