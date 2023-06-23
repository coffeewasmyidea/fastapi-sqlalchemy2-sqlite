from fastapi import APIRouter, Depends

from app.api.dependencies import SiteStats, UrlInfo, UrlShrink
from app.models.schemas import ShrinkUrlSchema, TotalUrlsSchema, UrlInfoSchema, UrlSchema

api_router = APIRouter(prefix="", tags=["API"])


# -----------------------------------------------------------------------------
#     - API -
# -----------------------------------------------------------------------------
@api_router.post("/create", response_model=UrlSchema)
async def url_shnk(url: ShrinkUrlSchema, scenario: UrlShrink = Depends(UrlShrink)) -> UrlSchema:
    return await scenario.execute(url.redirect_to.unicode_string())


@api_router.get(
    "/info",
    response_model=UrlInfoSchema,
    responses={
        404: {"description": "The prefix was not found"},
    },
)
async def url_info(prefix: str, scenario: UrlInfo = Depends(UrlInfo)) -> UrlInfoSchema:
    return await scenario.execute(prefix)


# -----------------------------------------------------------------------------
#     - site stats -
# -----------------------------------------------------------------------------
@api_router.get("/stats", response_model=TotalUrlsSchema)
async def site_stats(scenario: SiteStats = Depends(SiteStats)) -> TotalUrlsSchema:
    return await scenario.execute()
