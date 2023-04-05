from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import force_auto_coercion
from model_loader import load_models

__all__ = ('db', 'init_db')


db = SQLAlchemy()
query = db.session.query


def init_db(app=None, db=None):
    """Инициализирую общий объект бд, используемый приложением"""
    if isinstance(app, Flask) and isinstance(db, SQLAlchemy):
        force_auto_coercion()
        load_models()
        db.init_app(app)
    else:
        raise ValueError('Аргументы `app` и `db` не были переданы')