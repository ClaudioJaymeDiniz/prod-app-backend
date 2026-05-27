from pydantic import BaseModel, EmailStr
from typing import Optional, Any
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    globalMetadata: Optional[dict] = None


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: Optional[str] = None
    provider: str
    createdAt: datetime
    globalMetadata: Optional[Any] = None

    class Config:
        from_attributes = True


class UserSimple(BaseModel):
    id: str
    name: Optional[str] = None
    email: EmailStr

    class Config:
        from_attributes = True