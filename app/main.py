from fastapi import APIRouter, FastAPI
import typing
import httpx
from contextlib import asynccontextmanager
from app.constants import global_scope
from .routers import main, second

class State(typing.TypedDict):
    http_client: httpx.AsyncClient
    scope: dict


@asynccontextmanager
async def lifespan(app: FastAPI) -> typing.AsyncIterator[State]:
    async with httpx.AsyncClient() as client:
        yield {"http_client": client, "scope": global_scope}


router = APIRouter(prefix="/v1")
router.include_router(main.router)
router.include_router(second.router)
routes = router.routes

app = FastAPI(debug=True, lifespan=lifespan, routes=routes)
