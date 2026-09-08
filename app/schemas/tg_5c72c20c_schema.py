from pydantic import BaseModel, Field
from app.schemas.base_schema import OutputSchema
class CreateSchema(BaseModel):
    fd_login: str = Field(max_length=50)
    fd_passd: str = Field(min_length=8, max_length=250)
class UpdateSchema(BaseModel):
    fd_login: str | None = Field(default=None, max_length=50)
    fd_passd: str | None = Field(default=None, min_length=8, max_length=250)
class ResponseSchema(OutputSchema): fd_login: str
class LoginSchema(BaseModel): fd_login: str; fd_passd: str
