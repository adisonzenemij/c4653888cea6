from pydantic import BaseModel, ConfigDict, Field


class OutputSchema(BaseModel):
    id_universal: str
    fd_associated: bool = False
    fd_association_details: list[dict[str, str | int]] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)


class PageSchema(BaseModel):
    offset: int
    limit: int
    total: int
    items: list
