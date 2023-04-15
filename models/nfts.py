from datetime import datetime
import sqlalchemy
from models.db_session import SqlAlchemyBase


class NFT(SqlAlchemyBase):
    __tablename__ = 'nfts'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           unique=True,
                           autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.VARCHAR(100),
                             unique=True,
                             nullable=False)

    cost = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    publish_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     nullable=False,
                                     default=datetime.now())

    owner = sqlalchemy.Column(sqlalchemy.ForeignKey("users.id"),
                              nullable=False)