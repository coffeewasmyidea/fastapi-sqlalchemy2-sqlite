import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_healthcheck(client: AsyncClient) -> None:
    response = await client.get("/ping")

    assert 200 == response.status_code
    assert response.json()["message"] == "Ok!"
