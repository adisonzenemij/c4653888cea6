from pydantic import BaseModel, Field
from app.schemas.base_schema import OutputSchema
class CreateSchema(BaseModel):
    fd_ask: str = Field(max_length=500); fd_order: int
    pm_0d3dc00e: str = Field(min_length=36, max_length=36); pm_4d802b91: str = Field(min_length=36, max_length=36)
class UpdateSchema(BaseModel):
    fd_ask: str | None = Field(default=None, max_length=500); fd_order: int | None = None
    pm_0d3dc00e: str | None = Field(default=None, min_length=36, max_length=36); pm_4d802b91: str | None = Field(default=None, min_length=36, max_length=36)
class ResponseSchema(CreateSchema, OutputSchema): pass
