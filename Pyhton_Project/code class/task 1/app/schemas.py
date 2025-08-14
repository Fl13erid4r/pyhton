from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    class Config:
        from_attributes = True

class BookCreate(BaseModel):
    title: str
    author: Optional[str] = None
    user_id: int

class BookRead(BaseModel):
    id: int
    title: str
    author: Optional[str]
    added_at: datetime
    user_id: int
    class Config:
        from_attributes = True
