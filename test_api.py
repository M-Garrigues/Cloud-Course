import pytest
from datetime import datetime
from server import app


def test_data():
    response = app.test_client().get("/user")
    assert response.status_code == 200
    
    response_json = response.json
    assert len(response_json) >= 1

    assert 'birthDay' in response_json[0].keys()
    assert type(response_json[0]['birthDay']) == str
    datetime(response_json[0]['birthDay'], '%d/%m/%Y')

    assert 'id' in response_json[0].keys()
    assert type(response_json[0]['id']) == str

    assert 'firstName' in response_json[0].keys()
    assert type(response_json[0]['firstName']) == str

    assert 'lastName' in response_json[0].keys()
    assert type(response_json[0]['lastName']) == str

# Attribut position ignoré
    #assert 'position' in response_json[0].keys()
    #assert type(response_json[0]['position']) == dict

    #assert 'lat' in response_json[0]['position'].keys()
    #assert type(response_json[0]['position']['lat']) == float

    #assert 'lon' in response_json[0]['position'].keys()
    #assert type(response_json[0]['position']['lon']) == float

def test_get_user():
    user_id = "0"
    response = app.test_client().get("/user" + user_id)
    assert response.status_code == 200

    response_json = response.json
    assert len(response_json) == 1
    assert 'id' in response_json[0].keys()
    assert type(response_json[0]['id']) == str

    assert 'firstName' in response_json[0].keys()
    assert type(response_json[0]['firstName']) == str

    assert 'lastName' in response_json[0].keys()
    assert type(response_json[0]['lastName']) == str

#Attribut position ignoré
    #assert 'position' in response_json[0].keys()
    #assert type(response_json[0]['position']) == dict

    #assert 'lat' in response_json[0]['position'].keys()
    #assert type(response_json[0]['position']['lat']) == float

    #assert 'lon' in response_json[0]['position'].keys()
    #assert type(response_json[0]['position']['lon']) == float

def test_get_user_unknow_id():
    unknow_id = "-1"
    response = app.test_client().get("/user/" + unknow_id)
    assert response.status_code == 404  # 404 : Not Found

def test_put_user_unknow_id():
    unknow_id = "-1"
    response = app.test_client().put("/user/" + unknow_id)
    assert response.status_code == 404  # 404 : Not Found

def test_delete_user_unknow_id():
    unknow_id = "-1"
    response = app.test_client().delete("/user/" + unknow_id)
    assert response.status_code == 404  # 404 : Not Found

def test_put_user():
    user_id = "0"
    user_real_birthDay = '14/02/1990'
    user_info = app.test_client().get("/user" + user_id).json
    user_info['birthDay'] = user_real_birthDay
    response = app.test_client().put("/user" + user_id)
    assert response.status_code == 200

def tests():
    response = app.test_client().get("/user")
    print(response.json)

tests()