import pytest
from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from ..entities.entities import Todos, Users
from ..infra.database import Base
from ..routes.users import crypt_context


SQLALCHEMY_DATABASE_URL_TEST = "sqlite:/// ../../testetodosapp.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL_TEST)

TestSessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)


def get_test_database():
    db  = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def setup_test_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

#tem que ser o mesmo da entidade user
def return_mock_current_user() :
    return {"id": 1, "email": "kenji@gmail", "user_name": "maeda", "role": "admin"}



@pytest.fixture
def todo_database_mock(setup_test_database):
    db = TestSessionLocal()
    todos = Todos(
         id = 1,
        title="Learn fast api",
        description="Fast Api is great for applications",
        priority=5,
        completed=False,
        owner_id=1
    )

    db.add(todos)
    db.commit()

    # toda fez que fechar a conexão por causa do yeld
    yield todos
    with  engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def user_database_mock(setup_test_database):
    db = TestSessionLocal()
    users = Users(
        id=1,
        email="test@example.com",
        user_name="testuser",
        first_name="Test",
        last_name="User",
        hashed_password=crypt_context.hash("hashedpassword"),
        is_active=True,
        role="admin",
        phone_number="123456789"
    )

    db.add(users)
    db.commit()

    yield users
    with  engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
