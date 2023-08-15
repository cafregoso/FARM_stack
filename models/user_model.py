from pydantic import BaseModel, Field, EmailStr, validator
from enum import Enum


class Role(str, Enum):
    Salesperson = "Salesperson",
    Admin = "Admin",


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr = Field(...)
    role: Role


class UserCreate(UserBase):
    password: str = Field(...)


class LoginUser(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)


class CurrentUser(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr = Field(...)
    role: Role


class FindMe(BaseModel):
    id: str = Field(...)
