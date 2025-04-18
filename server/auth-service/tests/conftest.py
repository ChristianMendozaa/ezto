# tests/conftest.py
import pytest_asyncio
from httpx import AsyncClient
from app.main import create_app

@pytest_asyncio.fixture
async def client():
    app = create_app(testing=True)  # 👈 Carga la app en modo testing

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
