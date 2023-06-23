from fastapi import APIRouter
from starlette.routing import BaseRoute

from app.api.api import api_router


def get_routes() -> list[BaseRoute]:
    api = APIRouter(prefix="/v1/api")
    api.include_router(api_router)

    return api.routes
