import httpx
import pytest, pytest_asyncio
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.testclient import TestClient

from auth import __version__
from auth.app.api import main

@pytest.fixture
def anyio_backend() -> str:
    return 'asyncio'

@pytest_asyncio.fixture()
async def client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(app=main.api, base_url='http://testserver') as client:
        yield client

@pytest.mark.asyncio
async def test_version(client : httpx.AsyncClient) -> None:
    response = await client.get('/')
    assert response.status_code == 200
    assert response.json() == { 'version' : __version__ }

@pytest.mark.asyncio
async def test_login(client : httpx.AsyncClient) -> None:
    form_data = {
        'username': 'admin',
        'password': 'admin'
    }
    response = await client.post('/auth/login', data=form_data)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_register(client : httpx.AsyncClient) -> None:
    form_data = {
        'username' : 'patroclio',
        'password' : 'patroclio_capo_total'
    }
    response = await client.post('/auth/register', data=form_data)
    assert response.status_code == 200