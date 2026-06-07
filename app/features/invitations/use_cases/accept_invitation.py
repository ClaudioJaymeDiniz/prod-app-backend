from app.features.invitations.exceptions import (
    InvitationAccessDeniedException,
    InvitationAlreadyRespondedException,
    InvitationNotFoundException,
)


class AcceptInvitationUseCase:

    def __init__(self, invitation_repository):
        self.invitation_repository = invitation_repository

    async def execute(self, invitation_id: str, current_user_id: str, current_user_email: str):
        invitation = await self.invitation_repository.find_invitation_by_id(invitation_id)

        if not invitation:
            raise InvitationNotFoundException()

        if invitation.status != "PENDING":
            raise InvitationAlreadyRespondedException()

        if invitation.email.lower().strip() != current_user_email.lower().strip() and invitation.userId != current_user_id:
            raise InvitationAccessDeniedException()

        await self.invitation_repository.upsert_project_member(
            user_id=current_user_id,
            project_id=invitation.projectId,
            role=invitation.role,
        )

        return await self.invitation_repository.update_invitation_status(
            invitation_id=invitation_id,
            status="ACCEPTED",
            user_id=current_user_id,
        )