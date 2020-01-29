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
    return '<h1>BONJOUR</h1>'


@app.route("/user", methods=['GET'])
def get_users():
    page = request.args.get('page', default=0, type=int)
    users = persistence.get_users(page)
    if type(users) == dict:
        users = [users]
    return jsonify(users)


@app.route("/user/age", methods=['GET'])
def get_users_age():
    gt = request.args.get('gt', default=0, type=int)
    eq = request.args.get('eq', default=0, type=int)
    page = request.args.get('page', default=0, type=int)

    if not isinstance(gt, int) and not isinstance(eq, int):
        return "Bad Request", 400

    if gt < 0 or eq < 0:
        return "Bad Request", 400

    if gt > 0:
        users = persistence.get_users_age_greater(gt, page)
    elif eq > 0:
        users = persistence.get_users_age_equal(eq, page)
    else:
        users = persistence.get_users(page)
    return jsonify(users), 200


@app.route("/user/search", methods=['GET'])
def get_user_search():
    filter = request.args.get('term', default="", type=str)
    page = request.args.get('page', default=0, type=int)

    if not isinstance(filter, str):
        return "Bad Request", 400
    
    users = persistence.get_users_search(filter, page)
    return jsonify(users), 200


@app.route("/user/<uid>", methods=['GET'])
def get_user(uid):
    user = persistence.get_user(uid)
    if not user:
        return "BAD", 404
    else:
        return jsonify(user)


@app.route('/user', methods=['PUT'])
def put_users():
    if type(request.json) == dict:
        data = [request.json]
    else:
        data = request.json

    try:
        _ = data[0]['id']
    except KeyError:
        for i in range(len(data)):
            data[i]['id'] = str(i)

    user_list = [
        [
            u['id'],
            u['firstName'],
            u['lastName'],
            u['birthDay']
        ]
        for u in data
    ]
    if persistence.put_users(user_list):
        return user_list, 201
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
        return "OK", 200
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
    user = request.json
    new_id  = persistence.post_user(user)
    if new_id:
        user['id'] = new_id
        return jsonify(user)
    else:
        return "Server error", 500


if __name__ == "__main__":
    app.run()
    cnx.close()
