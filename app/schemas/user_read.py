from pydantic import BaseModel, EmailStr
from sqlmodel import Field


class UserRead(BaseModel):
    username: str
    email: EmailStr = Field(unique=True, index=True, nullable=False)
    full_name: str = Field(max_length=64)
