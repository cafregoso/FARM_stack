from pydantic import BaseModel, Field
from typing import Optional


class CarBase(BaseModel):
    brand: str = Field(..., min_length=3)
    make: str = Field(..., min_length=3)
    year: int = Field(..., gt=1975, lt=2023)
    price: int = Field(...)
    km: int = Field(...)
    cm3: int = Field(..., gt=600, lt=8000)


class CarUpdate(BaseModel):
    price: Optional[int] = None


class CarDB(CarBase):
    owner: str = Field(...)
