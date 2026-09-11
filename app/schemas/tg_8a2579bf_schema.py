from pydantic import BaseModel
from app.schemas.base_schema import OutputSchema
class CreateSchema(BaseModel):
    ms_8b6bd18a: str
    tg_2f997592: str
    tg_9a7bbe6f: str
class UpdateSchema(BaseModel):
    ms_8b6bd18a: str | None = None
    tg_2f997592: str | None = None
    tg_9a7bbe6f: str | None = None
class ResponseSchema(CreateSchema, OutputSchema): pass
