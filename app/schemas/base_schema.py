from pydantic import BaseModel, ConfigDict


class OutputSchema(BaseModel):
    id_universal: str
    fd_associated: int = 0
    model_config = ConfigDict(from_attributes=True)


class PageSchema(BaseModel):
    offset: int
    limit: int
    total: int
    items: list
