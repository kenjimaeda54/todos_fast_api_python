from fastapi.testclient import  TestClient
from fastapi import  FastAPI
from starlette import status

from  ..main import app


client = TestClient(app)


def test_healthy_main():
    response = client.get("/healthy")
    assert  response.status_code == status.HTTP_200_OK
    assert  response.json() == {"status": "200"}