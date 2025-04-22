from typing import cast

from ..infra.database import get_database
from ..main import  app
from fastapi.testclient import  TestClient
from starlette import status
from .test_database import *
from ..routes.auth import get_current_user

app.dependency_overrides[get_current_user] = return_mock_current_user
app.dependency_overrides[get_database] = get_test_database

client = TestClient(app)


def test_read_all_todos(todo_database_mock):
    response = client.get("/admin/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'completed':  todo_database_mock.completed,
        'description': todo_database_mock.description,
        'id': todo_database_mock.id,
        'owner_id': todo_database_mock.owner_id,
        'priority': todo_database_mock.priority,
        'title': todo_database_mock.title,
    }]


def test_delete_todo(todo_database_mock):
    response = client.delete(f"/admin/todos/{todo_database_mock.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestSessionLocal()
    todos = db.query(Todos).filter(cast("ColumnElement[bool]", Todos.id == todo_database_mock.id)).filter(
        cast("ColumnElement[bool]", Todos.owner_id == 1)
    ).first()

    assert todos is None


def test_delete_todo_not_found(todo_database_mock):
    response = client.delete(f"/admin/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}

    db = TestSessionLocal()

    todos = db.query(Todos).filter(cast("ColumnElement[bool]", Todos.id == 999)).first()

    assert todos is None