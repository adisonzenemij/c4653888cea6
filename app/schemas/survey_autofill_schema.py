from typing import Literal

from pydantic import BaseModel, Field


class AutoFillSchema(BaseModel):
    responses: int = Field(ge=1)
    bots: int = Field(default=1, ge=1, le=10)
    memory_value: int = Field(default=512, ge=1, le=4096)
    memory_unit: Literal["MB", "GB"] = "MB"
