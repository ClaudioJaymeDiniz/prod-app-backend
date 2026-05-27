from datetime import datetime
from typing import Any, Optional, Dict

from pydantic import BaseModel


class SubmissionUserSimple(BaseModel):
    name: Optional[str] = None
    email: str

    class Config:
        from_attributes = True


class SubmissionBase(BaseModel):
    formData: Dict[str, Any]


class SubmissionCreate(SubmissionBase):
    id: str
    formId: str


class SubmissionUpdate(BaseModel):
    formData: Optional[Dict[str, Any]] = None


class SubmissionResponse(SubmissionBase):
    id: str
    userId: str
    user: Optional[SubmissionUserSimple] = None
    formId: str
    createdAt: datetime

    class Config:
        from_attributes = True