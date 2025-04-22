from typing import cast
from fastapi import status
from fastapi.testclient import TestClient

from ..infra.database import get_database
from ..main import app
from ..routes.auth import get_current_user
from .test_database import  *

app.dependency_overrides[get_database] = get_test_database
app.dependency_overrides[get_current_user] = return_mock_current_user


client = TestClient(app)

#abaixo um exemplo quando precisa usar um banco de dados real para teste
#fixture funciona como um before each
#ou seja consigo criar um banco de dados para cada teste
#como garantir mocks para as classes
# @pytest.fixture
# def test_user(setup_test_database):
#     db = TestSessionLocal()
#     user = Users(
#         id=1,
#         email="test@example.com",
#         user_name="testuser",
#         first_name="Test",
#         last_name="User",
#         hashed_password="hashedpassword",  # Em testes, um hash simples é suficiente
#         is_active=True,
#         role="user",
#         phone_number="123456789"
#     )
#     db.add(user)
#     db.commit()
#     yield user
#     with engine.connect() as connection:
#         connection.execute(text("DELETE FROM users;"))
#         connection.commit()
#
#
# @pytest.fixture
# def test_todo(test_user, setup_test_database):
#     db = TestSessionLocal()
#     todos = Todos(
#         title="Learn fast api",
#         description="Fast Api is great for applications",
#         priority=5,
#         completed=False,
#         owner_id=1
#     )
#
#     db.add(todos)
#     db.commit()
#
#     # toda fez que fechar a conexão por causa do yeld
#     yield todos
#     with  engine.connect() as connection:
#         connection.execute(text("DELETE FROM todos;"))
#         connection.commit()





# tem que ser o endpoint correto
# eu tenho prefix  /todos
# por isso /todos que represetna o endpoint
# read_all_todos
#usando o fixture para retornar um todo
def test_read_all_todo(todo_database_mock):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            'completed': todo_database_mock.completed,
            'description': todo_database_mock.description,
            'id': todo_database_mock.id,
            'owner_id': todo_database_mock.owner_id,
            'priority': todo_database_mock.priority,
            'title': todo_database_mock.title,
        },
    ]


def teste_read_one_todo(todo_database_mock):
    response = client.get(f"/todos/{todo_database_mock.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'completed':  todo_database_mock.completed,
        'description': todo_database_mock.description,
        'id': todo_database_mock.id,
        'owner_id': todo_database_mock.owner_id,
        'priority': todo_database_mock.priority,
        'title': todo_database_mock.title,
    }


def teste_read_one_todo_not_found(todo_database_mock):
    response = client.get("/todos/99")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Item not found"}

def test_create_todo(todo_database_mock):
    todo_data = {
        "id": 2,
        "title": "Learn fast api",
        "description": "Fast Api is great for applications",
        "priority": 5,
        "completed": False,
        "owner_id": 1
    }

    response = client.post("/todos", json= todo_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestSessionLocal()
    todos = db.query(Todos).filter(cast("ColumnElement[bool]", Todos.id == 2)).filter(
        cast("ColumnElement[bool]", Todos.owner_id == 1)
    ).first()

    assert todos.title == todo_data.get("title")
    assert todos.description == todo_data.get("description")
    assert todos.priority == todo_data.get("priority")
    assert todos.completed == todo_data.get("completed")


def test_update_todo(todo_database_mock):
    todo_data = {
        "id": 1,
        "title": "New title",
        "description": "Description title",
        "priority": 3,
        "completed": False,
        "owner_id": 1
    }

    response = client.put(f"/todos/{todo_database_mock.id}", json= todo_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestSessionLocal()

    todos = db.query(Todos).filter(cast("ColumnElement[bool]", Todos.id == 1)).filter(
        cast("ColumnElement[bool]", Todos.owner_id == 1)
    ).first()

    assert todos.title == todo_data.get("title")
    assert todos.description == todo_data.get("description")
    assert todos.priority == todo_data.get("priority")

def test_update_todo_not_found(todo_database_mock):
    todo_data = {
        "id": 99,
        "title": "New title",
        "description": "Description title",
        "priority": 3,
        "completed": False,
        "owner_id": 1
    }

    response = client.put(f"/todos/{todo_data.get('id')}", json= todo_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}

def test_delete_todo(todo_database_mock):
    response = client.delete(f"/todos/{todo_database_mock.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestSessionLocal()
    todos = db.query(Todos).filter(cast("ColumnElement[bool]", Todos.id == todo_database_mock.id)).filter(
        cast("ColumnElement[bool]", Todos.owner_id == 1)
    ).first()

    assert todos is None

def test_delete_todo_not_found(todo_database_mock):
    response = client.delete(f"/todos/99")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}