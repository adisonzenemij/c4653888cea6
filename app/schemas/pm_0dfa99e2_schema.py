from pydantic import BaseModel, Field

from app.schemas.base_schema import OutputSchema


class CreateSchema(BaseModel):
    fd_name: str = Field(max_length=250)
    fd_service: str = Field(max_length=500)


class UpdateSchema(BaseModel):
    fd_name: str | None = Field(default=None, max_length=250)
    fd_service: str | None = Field(default=None, max_length=500)


class ResponseSchema(CreateSchema, OutputSchema):
    pass
