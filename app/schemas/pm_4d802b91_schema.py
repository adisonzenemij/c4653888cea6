from pydantic import BaseModel, Field
from app.schemas.base_schema import OutputSchema
class CreateSchema(BaseModel):
    fd_count: int; fd_name: str = Field(max_length=250); fd_query: int
    fd_since: str = Field(max_length=25); fd_until: str = Field(max_length=25)
    pm_8e417bb2: str = Field(min_length=36, max_length=36)
class UpdateSchema(BaseModel):
    fd_count: int | None = None; fd_name: str | None = Field(default=None, max_length=250); fd_query: int | None = None
    fd_since: str | None = Field(default=None, max_length=25); fd_until: str | None = Field(default=None, max_length=25)
    pm_8e417bb2: str | None = Field(default=None, min_length=36, max_length=36)
class ResponseSchema(CreateSchema, OutputSchema): pass
