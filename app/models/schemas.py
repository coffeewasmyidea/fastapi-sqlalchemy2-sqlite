from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

from app.settings import settings


class ShrinkUrlSchema(BaseModel):
    redirect_to: HttpUrl = Field(alias="url")


class UrlSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    prefix: str
    redirect_to: str

    @field_validator("prefix")
    def prefix_with_domain(cls, prefix: str) -> str:
        return f"{settings.DOMAIN_NAME}/{prefix}"


class UrlInfoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    prefix: str
    redirect_to: str
    hits: int
    created_at: datetime

    @field_validator("prefix")
    def prefix_with_domain(cls, prefix: str) -> str:
        return f"{settings.DOMAIN_NAME}/{prefix}"


class TotalUrlsSchema(BaseModel):
    total_urls: int
