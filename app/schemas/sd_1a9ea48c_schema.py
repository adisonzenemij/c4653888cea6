from pydantic import BaseModel, Field
from app.schemas.base_schema import OutputSchema
class CreateSchema(BaseModel): fd_service: str = Field(max_length=250)
class UpdateSchema(BaseModel): fd_service: str | None = Field(default=None, max_length=250)
class ResponseSchema(CreateSchema, OutputSchema): pass
