import pytest

from db import connexion
import persistence as p

cnx = connexion

persistence = p.Persistence(cnx)

def test_get_users():
    users = persistence.get_users(1)
    assert len(users) > 0
    assert type(users) == list
    for user in users:
        assert user.id is not None and user.id != ""

def test_delete_users():
    assert persistence.delete_users()

def test_put_users():
    users = persistence.get_users()
    for user in users:
        user['firstName'] = "bis"
    assert persistence.put_users(users)
    updated_users = persistence.get_users()
    for user in updated_users:
        assert user['firstName'] == "bis"

def test_get_user():
    id = persistence.get_users()[0]['id']
    user = persistence.get_user(id)
    assert len(user) == 1

def post_user():
    user = persistence.get_users()[0]
    persistence.delete_users()
    assert persistence.post_user(user)
    assert len(persistence.get_user(user['id'])) == 1

def put_user():
    user = persistence.get_users()[0]
    user['firstName'] = "bis"
    assert persistence.put_users(user)
    updated_users = persistence.get_user(user['id'])
    assert updated_users['firstName'] == "bis"

def delete_user():
    user = persistence.get_users()[0]
    assert persistence.delete_user(user['id'])