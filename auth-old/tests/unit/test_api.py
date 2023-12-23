import httpx
import pytest, pytest_asyncio
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.api import api, __version__

@pytest.fixture
def anyio_backend() -> str:
    return 'asyncio'

@pytest_asyncio.fixture()
async def client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(app=api, base_url='http://testserver') as client:
        yield client

@pytest.mark.asyncio
async def test_home(client : httpx.AsyncClient) -> None:
    response = await client.get('/')
    assert response.status_code == 200
    assert response.json() == { 'version' : __version__ }


@pytest.mark.asyncio
async def test_login(client: TestClient) -> None:
    login_data = {
        "username": "johndoe",
        "password": "secret"
    }
    
    response = await client.post('/auth/login', data=login_data)
    assert response.status_code == 200

    login_data = {
        "username": "invaliduser",
        "password": "invalidpassword"
    }

    response = await client.post('/auth/login', data=login_data)
    assert response.status_code == 401