from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(CharityProjectCreate):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    @validator("name")
    def validate_name(cls, value: str):
        if value is None or value == "" or value == " ":
            raise ValueError("Недопустимое имя")
        return value

    @validator("description")
    def validate_description(cls, value: str):
        if value is None or value == "" or value == " ":
            raise ValueError("Недопустимое описание")
        return value

    @validator("full_amount")
    def validate_full_amount(cls, value: str):
        if value is None or value == "":
            raise ValueError("Недопустимая сумма")
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: Optional[int] = 0
    fully_invested: Optional[bool] = False
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
