from fastapi import Depends

from app.features.invitations.prisma_repository import PrismaInvitationRepository
from app.features.invitations.use_cases.create_invitation import CreateInvitationUseCase
from app.features.invitations.use_cases.list_my_pending_invitations import (
    ListMyPendingInvitationsUseCase,
)


def get_invitation_repository():
    return PrismaInvitationRepository()


def get_create_invitation_use_case(
    invitation_repository = Depends(get_invitation_repository)
):
    return CreateInvitationUseCase(invitation_repository)


def get_list_my_pending_invitations_use_case(
    invitation_repository = Depends(get_invitation_repository)
):
    return ListMyPendingInvitationsUseCase(invitation_repository)