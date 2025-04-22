from datetime import timedelta

from jose import jwt

from ..infra.database import get_database
from ..main import app
from fastapi.testclient import TestClient
from ..routes.auth import return_user_if_authenticated, return_token_jwt, SECRET_KEY, ALGORITHM, get_current_user
from .test_database import *
from fastapi import HTTPException

app.dependency_overrides[get_database] = get_test_database
client = TestClient(app)


def test_return_user_if_authenticated(user_database_mock):
    db = TestSessionLocal()

    ##cuidado o password e feito um hash
    # testar se usuario esta autenticado
    user_authenticated = return_user_if_authenticated(user_database_mock.user_name, "hashedpassword", db)

    assert user_authenticated is not None
    assert user_authenticated.user_name == user_database_mock.user_name
    assert user_authenticated.id == user_database_mock.id
    assert user_authenticated.email == user_database_mock.email
    assert user_authenticated.first_name == user_database_mock.first_name
    assert user_authenticated.last_name == user_database_mock.last_name
    assert user_authenticated.hashed_password == user_database_mock.hashed_password
    assert user_authenticated.is_active == user_database_mock.is_active
    assert user_authenticated.role == user_database_mock.role

    # testar se a senha esta incorreta imposibilitando autenticar
    user_not_authenticated = return_user_if_authenticated(user_database_mock.user_name, "fsf", db)
    assert user_not_authenticated is None

    # testar se o user nao existe imposibilitando autenticar
    user_not_authenticated = return_user_if_authenticated("fsf", "hashedpassword", db)
    assert user_not_authenticated is None


def test_token_jwt(user_database_mock):
    token = return_token_jwt(user_database_mock, timedelta(days=360))

    decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False})

    assert decode.get("sub") == user_database_mock.user_name
    assert decode.get("id") == user_database_mock.id
    assert decode.get("role") == user_database_mock.role


@pytest.mark.asyncio
async def test_get_current_user(user_database_mock):
    token = return_token_jwt(user_database_mock, timedelta(days=360))

    current_user = await get_current_user(token)

    assert current_user == {"user_name": user_database_mock.user_name, "id": user_database_mock.id,
                            "role": user_database_mock.role}


# O with é ideal para gerenciar recursos que precisam ser
# configurados antes de serem usados e liberados depois,
# garantindo que a liberação aconteça mesmo em caso de erros.
#aberturas de arquivo, conexões de banco de dados, etc

#import threading
# lock = threading.Lock()
# with lock:
#     # Seção crítica: acessar recurso compartilhado
#     print("Acessando...")





@pytest.mark.asyncio
async def test_payload_missing_jwt_token():
    # tipo abaixo esta errado de proposito
    # teste aqui e para simular JWTError no
    # get_curren_user
    # error que é disparado pela propria biblioteca
    user_missing_payload = Users(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        hashed_password=crypt_context.hash("hashedpassword"),
        is_active=True,
        role="admin",
        phone_number="123456789"
    )
    token = return_token_jwt(user_missing_payload, timedelta(days=360))

    #estamos configurando para garantir que
    #sera lançado um exceção para depois tentar pegar o user
    with pytest.raises(HTTPException) as exception:
        await get_current_user(token)

    assert exception.value.status_code == 401
    assert exception.value.detail == "Not unauthorized"
