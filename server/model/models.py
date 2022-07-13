# database models in a separate file just for them
from flask_login import UserMixin
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.util import text_type

from server import db, login_manager


class User(db.Model, UserMixin):
    """
    code representation of the User table of the database
    """

    email = db.Column(db.VARCHAR(255), primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    def get_id(self):
        try:
            return text_type(self.email)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`")


@login_manager.user_loader
def load_user(user_email):
    return User.query.get(str(user_email))


class Param(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    lowest = db.Column(db.Float)
    highest = db.Column(db.Float)
    step = db.Column(db.Float)


class SpsaParam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    max_iter = db.Column(db.Integer)
    a = db.Column(db.Float)
    c = db.Column(db.Float)
    _A = db.Column(db.Float)
    alpha = db.Column(db.Float)
    gamma = db.Column(db.Float)


class SpsaTest(db.Model):
    test_id = db.Column(db.String(50), primary_key=True)
    engine = db.Column(db.String(50))
    branch = db.Column(db.String(50))
    book = db.Column(db.String(50))
    hash_size = db.Column(db.Integer)
    tc = db.Column(db.Float)
