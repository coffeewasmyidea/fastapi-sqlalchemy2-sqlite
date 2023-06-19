from fastapi import APIRouter

router = APIRouter(
    prefix="/second/index",
    tags=["second"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def index():
    return {"hello": "world"}
