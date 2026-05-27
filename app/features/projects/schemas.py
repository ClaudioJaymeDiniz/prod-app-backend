from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from app.features.users.schemas import UserSimple


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    isPublic: bool = False
    logoUrl: Optional[str] = None
    themeColor: str = Field(
        default="#3B82F6",
        pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    )


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    isPublic: Optional[bool] = None
    logoUrl: Optional[str] = None
    themeColor: Optional[str] = Field(
        None,
        pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    )


class ProjectResponse(ProjectBase):
    id: str
    ownerId: str
    createdAt: datetime
    deletedAt: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProjectMemberResponse(BaseModel):
    role: str
    userId: str
    user: UserSimple

    class Config:
        from_attributes = True


class ProjectFullResponse(ProjectResponse):
    owner: Optional[UserSimple] = None
    members: List[ProjectMemberResponse] = []

    class Config:
        from_attributes = True