from __future__ import annotations

from datetime import datetime
from typing import AsyncIterator

from sqlalchemy import Boolean, String, Text, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.utils import generate_prefix

from .base import Base


class Url(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )

    prefix: Mapped[str] = mapped_column("prefix", String(length=32), unique=True, nullable=False)

    redirect_to: Mapped[str] = mapped_column("redirect_to", Text(length=2048), nullable=False)

    hits: Mapped[int] = mapped_column("hits", nullable=False, default=0)

    is_active: Mapped[bool] = mapped_column("is_active", Boolean(), default=True)

    created_at: Mapped[datetime] = mapped_column("created_at", server_default=func.now())

    @classmethod
    async def get_all(cls, session: AsyncSession) -> AsyncIterator[Url]:
        query = select(cls)
        stream = await session.stream_scalars(query.order_by(cls.id))
        async for row in stream:
            yield row

    @classmethod
    async def count(cls, session: AsyncSession) -> int:
        query = select(func.count(cls.id))
        result = await session.scalar(query)
        return 0 if result is None else result

    @classmethod
    async def get_by_id(cls, session: AsyncSession, url_id: int) -> Url | None:
        query = select(cls).where(cls.id == url_id)
        return await session.scalar(query)

    @classmethod
    async def get_by_prefix(cls, session: AsyncSession, prefix: str) -> Url | None:
        query = select(cls).where(cls.prefix == prefix)
        return await session.scalar(query)

    @classmethod
    async def create(cls, session: AsyncSession, redirect_to: str) -> Url:
        url = Url(prefix=generate_prefix(), redirect_to=redirect_to)
        session.add(url)
        await session.flush()

        new = await cls.get_by_id(session, url.id)
        if not new:
            raise RuntimeError()
        return new

    async def increment(self, session: AsyncSession) -> None:
        self.hits += 1
        await session.flush()

    @classmethod
    async def delete(cls, session: AsyncSession, url_object: Url) -> None:
        await session.delete(url_object)
        await session.flush()
