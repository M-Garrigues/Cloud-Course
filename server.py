# -*- coding:utf-8 -*-
import json
import platform
import subprocess
from flask import Flask, Response, request, jsonify

app = Flask(__name__)

@app.route("/")
def headers():
    return '<br/>'.join(['%s => %s' % (key, value) for (key, value) in request.headers.items()])

@app.route("/favicon.ico")
def favicon():
    resp = Response(status=200, mimetype='image/png')
    return resp

@app.route("/pyver")
def pyver():
    return platform.python_version()

@app.route("/tag")
def tag():
    p = subprocess.Popen(['git', 'describe', '--tags', '--abbrev=0'], stdout=subprocess.PIPE)
    p.wait()
    return p.stdout.read()

@app.route("/user")
def user():
    with open('static/users.json', 'r') as f:
        d = json.load(f)
    return jsonify(d)

if __name__ == "__main__":
    app.run()

