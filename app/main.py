import typing
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from app.api.healthcheck import healthcheck_router
from app.api.main import main_router
from app.routes import get_routes
from app.settings import settings


class State(typing.TypedDict):
    http_client: httpx.AsyncClient


@asynccontextmanager
async def lifespan(app: FastAPI) -> typing.AsyncIterator[State]:
    async with httpx.AsyncClient() as client:
        yield {"http_client": client}


app = FastAPI(
    title=settings.APP_TITLE,
    debug=settings.DEBUG,
    lifespan=lifespan,
    routes=get_routes(),
)

# Health check endpoint
app.include_router(healthcheck_router)

# This is important to include the main route as the last one because it parse
# root path `/{prefix}` and absorbs all paths including/docs
app.include_router(main_router)
