from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import RedirectResponse

from app.api.dependencies import BasicUrlLogic
from app.settings import settings

main_router = APIRouter(prefix="", tags=["Main"])


@main_router.get("/{prefix}", status_code=status.HTTP_308_PERMANENT_REDIRECT)
async def redirect(
    prefix: Annotated[
        str,
        Path(
            title="Url prefix",
            min_length=settings.SHRINK_LENGTH,
            max_length=settings.SHRINK_LENGTH,
            pattern=settings.PREFIX_PATTERN,
        ),
    ],
    scenario: BasicUrlLogic = Depends(BasicUrlLogic),
):
    redirect_to = await scenario.execute(prefix)
    return RedirectResponse(status_code=status.HTTP_308_PERMANENT_REDIRECT, url=redirect_to)
