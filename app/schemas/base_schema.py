from pydantic import BaseModel, ConfigDict


class OutputSchema(BaseModel):
    id_universal: str
    model_config = ConfigDict(from_attributes=True)


class PageSchema(BaseModel):
    offset: int
    limit: int
    total: int
    items: list
