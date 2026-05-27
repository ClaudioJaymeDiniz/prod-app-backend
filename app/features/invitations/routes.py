from typing import List

from fastapi import APIRouter, Depends, status

from app.features.auth.dependencies import get_current_user
from app.features.invitations.schemas import (
    InvitationCreate,
    InvitationResponse,
)
from app.features.invitations.dependencies import (
    get_create_invitation_use_case,
    get_list_my_pending_invitations_use_case,
)


router = APIRouter(
    prefix="/invitations",
    tags=["Convites"]
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=InvitationResponse
)
async def create_invitation(
    data: InvitationCreate,
    current_user = Depends(get_current_user),
    use_case = Depends(get_create_invitation_use_case)
):
    return await use_case.execute(
        project_id=data.projectId,
        email=data.email,
        owner_id=current_user.id,
        role=data.role
    )


@router.get(
    "/pending",
    response_model=List[InvitationResponse]
)
async def list_my_pending_invitations(
    current_user = Depends(get_current_user),
    use_case = Depends(get_list_my_pending_invitations_use_case)
):
    return await use_case.execute(
        current_user.email
    )