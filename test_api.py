import pytest
from datetime import datetime
from server import app

VALID_USER_ID = "0"
UNKNOWN_USER_ID = "-1"

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
    assert response.status_code == 500

def test_delete_user():
    response = app.test_client().delete("/user/" + VALID_USER_ID)
    assert response.status_code == 200
    user_id_deleted = VALID_USER_ID
    response = app.test_client().get("/user/" + user_id_deleted)
    assert response.status_code == 500

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
    assert response.status_code == 500

def test_post_user():
    user_info = dict()
    user_info['birthDay'] = "01/01/1999"
    user_info['firstName'] = "joe"
    user_info['lastName'] = "doe"

    response = app.test_client().post("/user")
    assert response.status_code == 200
    response = app.test_client().get("/user")
    assert response.status_code == 200
    response_json = response.json
    assert response_json['birthDay'] == user_info['birthDay']
    assert response_json['firstName'] == user_info['firstName']
    assert response_json['lastName'] == user_info['lastName']

