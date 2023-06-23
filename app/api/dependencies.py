from fastapi import HTTPException, status

from app.database import AsyncSession
from app.models.schemas import TotalUrlsSchema, UrlInfoSchema, UrlSchema
from app.models.urls import Url


class UrlShrink:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, redirect_to: str) -> UrlSchema:
        async with self.async_session.begin() as session:
            new_url = await Url.create(session, redirect_to)
            return UrlSchema.model_validate(new_url)


class UrlInfo:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, prefix: str) -> UrlInfoSchema:
        async with self.async_session.begin() as session:
            url = await Url.get_by_prefix(session, prefix)

            if url is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
            return UrlInfoSchema.model_validate(url)


class BasicUrlLogic:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, prefix: str) -> str:
        async with self.async_session.begin() as session:
            url = await Url.get_by_prefix(session, prefix)

            if url is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
            # increment
            await url.increment(session)

            url_schema = UrlSchema.model_validate(url)
        return url_schema.redirect_to


# -----------------------------------------------------------------------------
#     - Site stats -
# -----------------------------------------------------------------------------
class SiteStats:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self) -> TotalUrlsSchema:
        async with self.async_session.begin() as session:
            urls = await Url.count(session)
            return TotalUrlsSchema(total_urls=urls)
