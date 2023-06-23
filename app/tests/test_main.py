import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.urls import Url
from app.utils import generate_prefix


async def get_entries(session: AsyncSession, nums: int = 10) -> list[Url]:
    for _ in range(nums):
        session.add_all([Url(prefix=generate_prefix(), redirect_to="http://localhost")])

    await session.flush()
    await session.commit()

    return [u async for u in Url.get_all(session)]


@pytest.mark.asyncio
async def test_get_all(session: AsyncSession) -> None:
    urls = await get_entries(session, 20)
    assert len(urls) == 20


@pytest.mark.asyncio
async def test_get_by_id(session: AsyncSession) -> None:
    urls = await get_entries(session)
    url_obj = await Url.get_by_id(session, urls[0].id)
    assert isinstance(url_obj, Url)
    assert url_obj is not None


@pytest.mark.asyncio
async def test_delete(session: AsyncSession) -> None:
    urls = [u async for u in Url.get_all(session)]
    for u in urls:
        await Url.delete(session, u)
    assert await Url.count(session) == 0


@pytest.mark.asyncio
async def test_create(client: AsyncClient, session: AsyncSession) -> None:
    response = await client.post("/v1/api/create", json={"url": "http://localhost"})

    assert response.status_code == 200
    assert response.json()["redirect_to"] == "http://localhost/"


@pytest.mark.asyncio
async def test_get_info(client: AsyncClient, session: AsyncSession) -> None:
    response = await client.post("/v1/api/create", json={"url": "http://localhost"})

    assert response.status_code == 200

    prefix = (response.json()["prefix"]).split("/")[-1]
    response = await client.get("/v1/api/info", params={"prefix": prefix})

    assert response.status_code == 200
    assert response.json().get("prefix") is not None
    assert response.json().get("redirect_to") is not None
    assert response.json().get("hits") is not None
    assert response.json().get("created_at") is not None


@pytest.mark.asyncio
async def test_stats(client: AsyncClient, session: AsyncSession) -> None:
    response = await client.get("/v1/api/stats")

    assert response.status_code == 200
    assert response.json().get("total_urls") > 0


@pytest.mark.asyncio
async def test_missmatch_prefix_pattern(client: AsyncClient, session: AsyncSession) -> None:
    response = await client.get("/foo")

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_prefix_404(client: AsyncClient, session: AsyncSession) -> None:
    response = await client.get("/xxxxx")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_redirect(client: AsyncClient, session: AsyncSession) -> None:
    response = await client.post("/v1/api/create", json={"url": "http://localhost"})
    assert response.status_code == 200

    prefix = (response.json()["prefix"]).split("/")[-1]
    response = await client.get(f"/{prefix}")

    assert response.status_code == 308
