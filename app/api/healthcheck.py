from fastapi import APIRouter
from fastapi.responses import JSONResponse

healthcheck_router = APIRouter(prefix="", tags=["Health check"])


@healthcheck_router.get("/ping")
async def healthcheck() -> JSONResponse:
    return JSONResponse({"message": "Ok!"})
