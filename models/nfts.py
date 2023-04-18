from datetime import datetime
import sqlalchemy
from models.db_session import SqlAlchemyBase


NFT_DEFAULT_DESCRIPTION = """
    Коллекция NFT c чем-то внутри.
    Это очень интересно покупать кота в мешке
    и думать о чем-то приятном!!!
"""


class NFT(SqlAlchemyBase):
    __tablename__ = 'nfts'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           unique=True,
                           autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.VARCHAR(100),
                             unique=True,
                             nullable=False)

    description = sqlalchemy.Column(sqlalchemy.VARCHAR(300),
                                    default=NFT_DEFAULT_DESCRIPTION)

    cost = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    publish_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     nullable=False,
                                     default=datetime.now)

    image = sqlalchemy.Column(sqlalchemy.LargeBinary(),
                              nullable=False)

    owner = sqlalchemy.Column(sqlalchemy.Integer,
                              sqlalchemy.ForeignKey("users.id"),
                              nullable=False)

    on_sale = sqlalchemy.Column(sqlalchemy.Boolean,
                                default=False,
                                nullable=False)