from pydantic import BaseModel, Field

from app.schemas.base_schema import OutputSchema


class CreateSchema(BaseModel):
    fd_name: str = Field(max_length=250)
    fd_path: str = Field(max_length=250)
    sd_3a731d00: str = Field(min_length=36, max_length=36)
    pm_0dfa99e2: str = Field(min_length=36, max_length=36)


class UpdateSchema(BaseModel):
    fd_name: str | None = Field(default=None, max_length=250)
    fd_path: str | None = Field(default=None, max_length=250)
    sd_3a731d00: str | None = Field(default=None, min_length=36, max_length=36)
    pm_0dfa99e2: str | None = Field(default=None, min_length=36, max_length=36)


class ResponseSchema(CreateSchema, OutputSchema):
    pass
