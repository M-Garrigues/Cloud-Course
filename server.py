# -*- coding:utf-8 -*-
import json
import platform
import subprocess
from flask import Flask, Response, request, jsonify

app = Flask(__name__)


@app.route("/")
def headers():
    return '<br/>'.join(['%s => %s' % (key, value) for (key, value) in request.headers.items()])


@app.route("/user")
def user():
    with open('../static/users.json', 'r') as f:
        d = json.load(f)
    return jsonify(d)


if __name__ == "__main__":
    app.run()

