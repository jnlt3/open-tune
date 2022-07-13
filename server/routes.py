# routes in a separate file just for them
import hashlib
from datetime import timedelta

from flask_login import login_user, logout_user, login_required

from server import app, db

import sys

from dataclasses import asdict
import json
from flask import request, render_template, flash, url_for
import server.tune as tune
from server.model.models import User, SpsaParam, SpsaTest
from server.tune import push_result_json, push_test_json

sys.path.append("/")


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
    return render_template("index.html")


@app.route("/loginPage")
def login():
    return render_template("login.html")


@app.route("/signupPage")
def registrationPage():
    return render_template("sign_up.html")


@app.route("/signup", methods=["POST"])
def signup():
    """
    Reads the user credentials from a http request and adds him to the project database
        :return: redirect to index page
    """
    email = request.form.get("email")
    password = request.form.get("password")
    hashed_password = hashlib.sha512(password.encode()).hexdigest()
    username = request.form.get("username")
    user = User.query.filter_by(username=username).first()
    if user:
        flash("Username is invalid or already taken", "error")
        return render_template("sign_up.html")

    utente = User(email=email, password=hashed_password, username=username)

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
    hashed_password = hashlib.sha512(password.encode()).hexdigest()
    attempted_user: User = User.query.filter_by(email=email).first()
    if not attempted_user:
        print(attempted_user.__class__)
        flash("User doesn't exist", "error")
        return render_template("login.html")

    if attempted_user.password == hashed_password:
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


@app.route("/addTest", methods=["GET", "POST"])
@login_required
def addTest():
    spsa_test = SpsaTest(
        test_id=request.form.get('test_id'),
        engine=request.form.get('engine'),
        branch=request.form.get('branch'),
        book=request.form.get('book'),
        hash_size=request.form.get('hash_size'),
        tc=request.form.get('tc'),
    )
    db.session.add(spsa_test)
    db.session.commit()

    param = SpsaParam(
        max_iter=request.form.get("max_iter"),
        a=request.form.get("a"),
        c=request.form.get("c"),
        _A=request.form.get("_A"),
        alpha=request.form.get("alpha"),
        gamma=request.form.get("gamma"),
    )
    db.session.add(param)
    db.session.commit()


