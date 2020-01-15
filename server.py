# -*- coding:utf-8 -*-
import json
from flask import Flask, Response, request, jsonify
import persistence as p
import mysql.connector

cnx = mysql.connector.connect(user='uxmafubcms8efnkd',
                              password='uKyZrSTyH2NCsjaqxq7U',
                              host='bwku7xxv8kkyfmuzbjf9-mysql.services.clever-cloud.com',
                              database='bwku7xxv8kkyfmuzbjf9',
                              port=3306)

app = Flask(__name__)


@app.route("/")
def headers():
    return '<br/>'.join(['%s => %s' % (key, value) for (key, value) in request.headers.items()])


@app.route("/user", methods=['GET'])
def get_users():
    with open('static/users.json', 'r') as f:
        d = json.load(f)
    return jsonify(d)


@app.route('/user', methods=['PUT'])
def put_users():
    # TODO
    return


@app.route('/user', methods=['DELETE'])
def delete_users():
    # TODO
    return "OK", 200


if __name__ == "__main__":
    p.H = 1
    print(p.get_user(15))

    app.run()
    cnx.close()


