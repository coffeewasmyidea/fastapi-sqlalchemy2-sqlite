import os
from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.database import get_session
from app.main import app
from app.models.base import Base


@pytest.fixture
async def client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="https://test") as client:
        yield client


@pytest.fixture(scope="session")
def setup_db() -> Generator:
    engine = create_engine("sqlite:///./test.db")
    conn = engine.connect()

    with conn.begin():
        yield

    conn.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db(setup_db: Generator) -> Generator:
    engine = create_engine("sqlite:///./test.db")

    with engine.begin():
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        yield
        Base.metadata.drop_all(engine)
        os.unlink("./test.db")


@pytest.fixture
async def session() -> AsyncGenerator:
    async_engine = create_async_engine("sqlite+aiosqlite:///./test.db")
    AsyncSessionLocal = async_sessionmaker(bind=async_engine, autoflush=False)

    async with async_engine.connect() as conn:
        await conn.begin()
        await conn.begin_nested()
        AsyncSessionLocal = async_sessionmaker(
            autocommit=False, autoflush=False, bind=conn, future=True
        )

        async_session = AsyncSessionLocal()

        def test_get_session() -> Generator:
            try:
                yield AsyncSessionLocal
            except SQLAlchemyError:
                pass

        app.dependency_overrides[get_session] = test_get_session

        yield async_session
        await async_session.close()
        await conn.rollback()
