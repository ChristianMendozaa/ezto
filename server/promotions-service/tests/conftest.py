import pytest_asyncio
from httpx import AsyncClient

BASE_URL = "http://localhost:8001"  # Cambia si estás usando otro puerto

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(base_url=BASE_URL) as ac:
        yield ac
