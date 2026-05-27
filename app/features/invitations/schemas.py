from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.features.users.schemas import UserSimple


class InvitationStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REVOKED = "REVOKED"


class ProjectSimpleResponse(BaseModel):
    id: str
    name: str
    owner: Optional[UserSimple] = None

    class Config:
        from_attributes = True


class InvitationCreate(BaseModel):
    email: EmailStr
    projectId: str
    role: str = "COLLECTOR"


class InvitationResponse(BaseModel):
    id: str
    email: str
    projectId: str
    status: InvitationStatus
    project: Optional[ProjectSimpleResponse] = None
    createdAt: datetime

    class Config:
        from_attributes = True

class ProjectMemberResponse(BaseModel):
    role: str
    user: UserSimple

    class Config:
        from_attributes = True