from pydantic import BaseModel, Field
from app.schemas.base_schema import OutputSchema


class CreateSchema(BaseModel):
    fd_repply: str
    pm_9a582ff6: str = Field(min_length=36, max_length=36)
    pm_1a4a8cd7: str = Field(min_length=36, max_length=36)


class UpdateSchema(BaseModel):
    fd_repply: str | None = None
    pm_9a582ff6: str | None = Field(default=None, min_length=36, max_length=36)
    pm_1a4a8cd7: str | None = Field(default=None, min_length=36, max_length=36)


class ResponseSchema(CreateSchema, OutputSchema):
    pass
