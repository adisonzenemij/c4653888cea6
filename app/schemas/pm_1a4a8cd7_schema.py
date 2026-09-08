from pydantic import BaseModel, Field
from app.schemas.base_schema import OutputSchema
class CreateSchema(BaseModel): fd_random: str = Field(max_length=50)
class UpdateSchema(BaseModel): fd_random: str | None = Field(default=None, max_length=50)
class ResponseSchema(CreateSchema, OutputSchema): pass
