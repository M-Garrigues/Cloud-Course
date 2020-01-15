import pytest
from hello import app


def test_data():
    response = app.test_client().get("/user")
    assert len(response.json) >= 1
    assert 'birthDay' in response.json[0].keys()
    assert type(response.json[0]['birthDay']) == str

    assert 'id' in response.json[0].keys()
    assert type(response.json[0]['id']) == str

    assert 'firstName' in response.json[0].keys()
    assert type(response.json[0]['firstName']) == str

    assert 'lastName' in response.json[0].keys()
    assert type(response.json[0]['lastName']) == str

    assert 'position' in response.json[0].keys()
    assert type(response.json[0]['position']) == dict

    assert 'lat' in response.json[0]['position'].keys()
    assert type(response.json[0]['position']['lat']) == float

    assert 'lon' in response.json[0]['position'].keys()
    assert type(response.json[0]['position']['lon']) == float



