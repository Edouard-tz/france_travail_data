# pylint: disable=no-self-argument, missing-function-docstring,missing-class-docstring
from pydantic import BaseModel, field_validator


class NonNumberBaseModel(BaseModel):

    @field_validator("*", mode="before")
    def number_to_string(cls, v) -> str:
        if isinstance(v, (int, float)):
            return str(int(v))
        return v
