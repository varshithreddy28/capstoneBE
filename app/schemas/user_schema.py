from pydantic import BaseModel, EmailStr, Field
from typing import List

class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    interests: List[str] = Field(..., max_items=3)

class UserSchema(BaseModel):
    id: str
    email: EmailStr
    interests: List[str]
