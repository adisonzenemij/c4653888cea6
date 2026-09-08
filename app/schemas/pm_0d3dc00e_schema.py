from pydantic import BaseModel, Field
from app.schemas.base_schema import OutputSchema
class CreateSchema(BaseModel): fd_format: str = Field(max_length=25)
class UpdateSchema(BaseModel): fd_format: str | None = Field(default=None, max_length=25)
class ResponseSchema(CreateSchema, OutputSchema): pass
