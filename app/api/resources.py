from fastapi import APIRouter, Request


router = APIRouter()


@router.get("/")
async def index(request: Request):
    return {"request": request}
