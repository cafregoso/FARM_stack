from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from enum import Enum
from email_validator import validate_email, EmailNotValidError


class Role(str, Enum):
    Salesperson = "Salesperson",
    Admin = "Admin",


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr = Field(...)
    role: Role

    @validator('email')
    def email_validator(cls, v):
        try:
            validate_email(v).email
            return v
        except EmailNotValidError as e:
            raise ValueError('Invalid email') from e


class UserCreate(UserBase):
    password: str = Field(...)


class LoginUser(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)


class CurrentUser(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr = Field(...)
    role: Role
