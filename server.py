# -*- coding:utf-8 -*-
import json
from flask import Flask, Response, request, jsonify
import persistence as p
from db import connexion

cnx = connexion

app = Flask(__name__)

pers = p.Persistence(cnx)


@app.route("/")
def headers():
    return '<br/>'.join(['%s => %s' % (key, value) for (key, value) in request.headers.items()])


@app.route("/user", methods=['GET'])
def get_users():
    page = request.args.get('page', default=0, type=int)
    users = pers.get_users(page)
    return jsonify(users)


@app.route('/user', methods=['PUT'])
def put_users():
    # TODO
    return


@app.route('/user', methods=['DELETE'])
def delete_users():
    # TODO
    return "OK", 200


if __name__ == "__main__":
    app.run()
    cnx.close()
