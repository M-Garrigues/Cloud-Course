import pytest
from datetime import datetime
from server import app

VALID_USER_ID = "0"
UNKNOWN_USER_ID = "-1"
AVAILABLE_USER_ID = "5000"

def test_get_users():
    response = app.test_client().get("/user")
    assert response.status_code == 200

    response_json = response.json
    assert len(response_json) >= 1

    assert 'birthDay' in response_json[0].keys()
    assert type(response_json[0]['birthDay']) == str
    datetime.strptime(response_json[0]['birthDay'], '%d/%m/%Y')

    assert 'id' in response_json[0].keys()
    assert type(response_json[0]['id']) == str

    assert 'firstName' in response_json[0].keys()
    assert type(response_json[0]['firstName']) == str

    assert 'lastName' in response_json[0].keys()
    assert type(response_json[0]['lastName']) == str

def test_delete_users():
    response = app.test_client().delete("/user")
    assert response.status_code == 200
    response = app.test_client().get("/user")
    assert response.status_code == 200
    assert len(response.json) == 0

def test_get_user():
    response = app.test_client().get("/user" + VALID_USER_ID)
    assert response.status_code == 200

    response_json = response.json
    assert len(response_json) == 1
    assert 'id' in response_json[0].keys()
    assert type(response_json[0]['id']) == str

    assert 'firstName' in response_json[0].keys()
    assert type(response_json[0]['firstName']) == str

    assert 'lastName' in response_json[0].keys()
    assert type(response_json[0]['lastName']) == str

def test_get_user_unknow_id():
    response = app.test_client().get("/user/" + UNKNOWN_USER_ID)
    assert response.status_code == 404  # 404 : Not Found ou 400 : Bad Request si id non conforme

def test_delete_user():

    response = app.test_client().delete("/user/" + VALID_USER_ID)
    assert response.status_code == 200
    user_id_deleted = VALID_USER_ID
    response = app.test_client().get("/user/" + user_id_deleted)
    assert response.status_code == 409  # conflict

def test_delete_user_unknow_id():
    unknow_id = "-1"
    response = app.test_client().delete("/user/" + unknow_id)
    assert response.status_code == 404  # 404 : Not Found ou 400

def test_put_user():

    user_real_birthDay = '14/02/1990'
    user_info = app.test_client().get("/user" + VALID_USER_ID).json
    user_info['birthDay'] = user_real_birthDay
    response = app.test_client().put("/user" + VALID_USER_ID)
    assert response.status_code == 200
    response = app.test_client().get("/user" + VALID_USER_ID)
    assert response.status_code == 200
    assert response.json[0]['birthDay'] == user_real_birthDay

def test_put_user_unknow_id():
    response = app.test_client().put("/user/" + UNKNOWN_USER_ID)
    assert response.status_code == 404  # 404 : Not Found ou 400

def test_post_user():
    user_info = dict()
    user_info['birthDay'] = "01/01/1999"
    user_info['firstName'] = "joe"
    user_info['id'] = AVAILABLE_USER_ID
    user_info['lastName'] = "doe"

    response = app.test_client().post("/user" + AVAILABLE_USER_ID)
    assert response.status_code == 200
    response = app.test_client().get("/user" + AVAILABLE_USER_ID)
    assert response.status_code == 200
    response_json = response.json
    assert response_json['birthDay'] == user_info['birthDay']
    assert response_json['firstName'] == user_info['firstName']
    assert response_json['id'] == user_info['id']
    assert response_json['lastName'] == user_info['lastName']

def test_post_id_exist():
    id_exist = "0"
    position = dict()
    user_info = dict()
    user_info['birthDay'] = "01/01/1999"
    user_info['firstName'] = "joe"
    user_info['id'] = id_exist
    user_info['lastName'] = "doe"

    response = app.test_client().post("/user" + id_exist)
    assert response.status_code == 409  # conflict

def test_post_without_id():
    user_info = dict()
    user_info['birthDay'] = "01/01/1999"
    user_info['firstName'] = "joe"
    user_info['id'] = ""
    user_info['lastName'] = "doe"

    response = app.test_client().post("/user/")
    assert response.status_code == 400  # bad request

def test_post_wrong_id():
    id_1 = "5000"
    id_2 = "5001"

    user_info = dict()
    user_info['birthDay'] = "01/01/1999"
    user_info['firstName'] = "joe"
    user_info['id'] = id_1
    user_info['lastName'] = "doe"

    response = app.test_client().post("/user/" + id_2)
    assert response.status_code == 400  # bad request

