from datetime import datetime
import sqlalchemy
from models.db_session import SqlAlchemyBase


class Transaction(SqlAlchemyBase):
    __tablename__ = 'transactions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           unique=True,
                           autoincrement=True)

    date = sqlalchemy.Column(sqlalchemy.DateTime,
                             nullable=False,
                             default=datetime.now())

    transferred = sqlalchemy.Column(sqlalchemy.Float,
                                    nullable=False)

    sender = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("users.id"),
                               nullable=False)

    receiver = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("users.id"),
                                 nullable=False)
