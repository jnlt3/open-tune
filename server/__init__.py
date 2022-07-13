from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql://root@127.0.0.1/open_tune"  # name and address of where the database will be
# created (this means that the machine has to have mysql installed)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "jfhnifhjwieotjhf7847f5ee4eqws"
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "loginPage"
login_manager.login_message_category = "info"

from server.model import models

# Create database if it does not exist
if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    create_database(app.config["SQLALCHEMY_DATABASE_URI"])
    with app.app_context():
        db.create_all()
else:
    with app.app_context():
        db.create_all()

# import routes to allow for the redirects (otherwise you can't use app.py as an empty entrpoiny)
from server import routes
