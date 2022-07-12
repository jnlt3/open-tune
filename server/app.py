import sys

sys.path.append("../")

from dataclasses import asdict
import json
from flask import Flask, request
import server.tune as tune
from server.tune import push_result_json, push_test_json

app = Flask(__name__)


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
