import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../app'))

from interface import app
from db.dbconnect import connection
from flask import json


# Test DB connection
def test_db_connection_successful():
    c, conn = connection()
    assert c and conn
    c.close()
    conn.close()


# Test GET all users2flowers successfully
def test_get_all_users2flowers_succsessful():
    response = app.test_client().get('/users2flowers/')

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200 or response.status_code == 204


'''
# Test POST users2flowers successfully
def test_post_users2flowers_succsessful():
    response = app.test_client().post('/users2flowers/', json={
        "date_of_inception": "2019-09-22",
        "email": True,
        "flower_id": "20",
        "user_id": "59"
    })

    data = json.loads(response.get_data(as_text=True))

    assert data == {"msg": "New user2flower added to DB."} and response.status_code == 201
'''


# Test POST users2flowers invalid data
def test_post_users2flowers_unsuccsessful():
    response = app.test_client().post('/users2flowers/', json={
        "date_of_inception": "2019-09-22",
        "email": True,
        "flower_id": "20"
    })

    data = json.loads(response.get_data(as_text=True))

    assert data == {'msg': 'Data is not valid.'} and response.status_code == 403


# Test Method not allowed
def test_method_not_allowed():
    response = app.test_client().put('/users2flowers/', json={
        "date_of_inception": "2019-09-22",
        "email": True,
        "flower_id": "20",
        "user_id": "59"
    })

    assert response.status_code == 405


# Test GET users2flowers by id successfully
def test_get_users2flowers_by_id_succsessful():
    response = app.test_client().get('/users2flowers/5')

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200 or data == "No data to return."


'''
# Test PUT users2flowers by id successfully
def test_put_users2flowers_by_id_succsessful():
    response = app.test_client().put('/users2flowers/5/', json={
        "date_of_inception": "2019-09-22",
        "email": True,
        "flower_id": "19",
        "user_id": "59"
    })

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201 and data == {"msg": "New user2flower added to DB."} or data == {"msg": "User2flower with user2flower_id 5 is updated."} and response.status_code == 200
'''


# Test DELETE flower by id not existing in DB
def test_delete_users2flowers_by_id_not_exist_in_db():
    response = app.test_client().delete('/users2flowers/6969420666')

    data = json.loads(response.get_data(as_text=True))

    assert data == {"msg": "User2flower with user2flower_id 6969420666 does not exist in DB."} and response.status_code == 200


# Test Method not allowed /users2flowers/<id>
def test_method_not_allowed_users2flowers_with_id():
    response = app.test_client().post('/users2flowers/666', json={
        "date_of_inception": "2019-09-22",
        "email": True,
        "flower_id": "20"
    })

    assert response.status_code == 405
