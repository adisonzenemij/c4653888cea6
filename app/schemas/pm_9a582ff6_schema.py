from pydantic import BaseModel, Field
from app.schemas.base_schema import OutputSchema
class CreateSchema(BaseModel):
    fd_option: str
    fd_order: int
    pm_0acc84ae: str = Field(min_length=36, max_length=36)
class UpdateSchema(BaseModel):
    fd_option: str | None = None
    fd_order: int | None = None
    pm_0acc84ae: str | None = Field(default=None, min_length=36, max_length=36)
class ResponseSchema(CreateSchema, OutputSchema): pass
