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

pers = p.Persistence(cnx)


@app.route("/")
def headers():
    return '<br/>'.join(['%s => %s' % (key, value) for (key, value) in request.headers.items()])


@app.route("/user", methods=['GET'])
def get_users():
    users = pers.get_users()
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


