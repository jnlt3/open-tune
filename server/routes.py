# routes in a separate file just for them
from datetime import timedelta
from pathlib import Path

from flask_login import login_user, logout_user

from server import app, db
from model.models import User
import sys

from dataclasses import asdict
import json
from flask import Flask, request, render_template, flash
import server.tune as tune
from server.tune import push_result_json, push_test_json

sys.path.append("../")


@app.route("/test", methods=["POST"])
def submit_test():
    content = request.get_json()
    push_test_json(content)
    return ""


@app.route("/result", methods=["POST"])
def submit_result():
    content = request.get_json()
    push_result_json(content)
    return ""


@app.route("/get")
def get_test():
    test = tune.get_test()
    if test is not None:
        return json.dumps(asdict(test))
    return ""


@app.route("/params/<test_id>")
def get_params(test_id):
    test = tune.get_test_by_id(test_id)
    if test is not None:
        return json.dumps(test)
    return ""


@app.route("/")
def index():
    return ""


@app.route('/loginPage')
def login():
    return render_template('login.html')


@app.route("/signupPage")
def registrationPage():
    return render_template("sign_up.html")


@app.route('/signup', methods=['POST'])
def signup():
    """
                      Reads the user credentials from a http request and adds him to the project database
                          :return: redirect to index page
                      """
    email = request.form.get("email")
    password = request.form.get("password")
    username = request.form.get("username")
    user = User.query.filter_by(username=username).first()
    if user:
        flash("Username is invalid or already taken", "error")
        return render_template("registration.html")

    utente = User(
        email=email,
        password=password,
        username=username
    )

    db.session.add(utente)
    db.session.commit()

    login_user(utente, duration=timedelta(days=365), force=True)
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def Login():
    """
           reads a user login credentials from a http request and if they are valid logs the user in with those same
           credentials,changing his state from anonymous  user to logged user
           :return: redirect to index page
           """
    email = request.form.get("email")
    password = request.form.get("password")
    attempted_user: User = User.query.filter_by(email=email).first()
    if not attempted_user:
        print(attempted_user.__class__)
        flash("User doesn't exist", "error")
        return render_template("login.html")

    if attempted_user.password == password:
        login_user(attempted_user, duration=timedelta(days=365), force=True)
    else:
        flash("wrong password ", "error")
        return render_template("login.html")
    return render_template("index.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    """
          logs a user out, changing his state from logged user to anonymous user
              :return:redirect to index page
          """
    logout_user()
    return render_template("index.html")
