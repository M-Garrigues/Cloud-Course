# -*- coding:utf-8 -*-
import json
from flask import Flask, make_response, request, jsonify
import persistence as p
from db import connexion

cnx = connexion
print(connexion)

app = Flask(__name__)

persistence = p.Persistence(cnx)


# TODO: Remove ?
@app.route("/")
def headers():
    return '<br/>'.join(['%s => %s' % (key, value) for (key, value) in request.headers.items()])


@app.route("/user", methods=['GET'])
def get_users():
    page = request.args.get('page', default=0, type=int)
    users = persistence.get_users(page)
    return jsonify(users)


@app.route("/user/<uid>", methods=['GET'])
def get_user(uid):
    user = persistence.get_user(uid)
    return jsonify(user)


@app.route('/user', methods=['PUT'])
def put_users():
    # TODO: vérifier qu'il a bien un id ? vérifier que c'est bien une list ?
    user_list = [
        [
            u['id'],
            u['firstName'],
            u['lastName'],
            u['birthDay']
        ]
        for u in list(request.json)
    ]
    if persistence.put_users(user_list):
        return "OK", 201
    else:
        return "BAD", 500


@app.route('/user/<uid>', methods=['PUT'])
def put_user(uid):
    user = request.json
    try:
        _ = user['id']
    except KeyError:
        user['id'] = uid
    if persistence.put_user(user):
        return "OK", 201
    else:
        return "BAD", 500


@app.route('/user', methods=['DELETE'])
def delete_users():
    persistence.delete_users()
    return "OK", 200


@app.route('/user/<uid>', methods=['DELETE'])
def delete_user(uid):
    if persistence.delete_user(uid):
        return "OK", 200
    else:
        return "BAD", 500


@app.route("/user", methods=['POST'])
def post_user():
    persistence.post_user(request.json)
    return "OK", 200


if __name__ == "__main__":
    app.run()
    cnx.close()
