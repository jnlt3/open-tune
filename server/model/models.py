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
