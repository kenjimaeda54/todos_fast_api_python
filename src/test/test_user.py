from http.client import responses
from typing import cast

from fastapi.testclient import TestClient
from starlette import status

from ..infra.database import get_database
from ..main import  app
from .test_database import *
from ..routes.auth import get_current_user


app.dependency_overrides[get_database] = get_test_database
app.dependency_overrides[get_current_user] = return_mock_current_user


client = TestClient(app)

def  test_read_user(user_database_mock):
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == user_database_mock.email
    assert response.json()["user_name"] == user_database_mock.user_name
    assert response.json()["first_name"] == user_database_mock.first_name
    assert response.json()["last_name"] == user_database_mock.last_name
    assert response.json()["phone_number"] == user_database_mock.phone_number
    assert response.json()["role"] == user_database_mock.role
    assert response.json()["id"] == user_database_mock.id


def test_update_password(user_database_mock):
    #os campos precisam ser iguais ao PasswordRequest
    #UserPasswordRequest
    password_request = {
        "old_password": "hashedpassword",
        "new_password": "newhashedpassword"
    }
    response = client.put("/users",json=password_request)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_update_password_invalid(user_database_mock):
    password_request = {
        "old_password": "wrong",
        "new_password": "newhashedpassword"
    }
    response = client.put("/users",json=password_request)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {"detail": "Error update password"}

def test_update_phone_number(user_database_mock):
    new_phone_number = "23434343"
    response = client.put(f"/users/{new_phone_number}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestSessionLocal()
    user = db.query(Users).filter(cast("Column[bool]", Users.id == user_database_mock.id)).first()

    assert user.phone_number == new_phone_number
