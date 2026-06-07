from app.features.invitations.exceptions import (
    InvitationAccessDeniedException,
    InvitationAlreadyRespondedException,
    InvitationNotFoundException,
)


class RevokeInvitationUseCase:

    def __init__(self, invitation_repository):
        self.invitation_repository = invitation_repository

    async def execute(self, invitation_id: str, current_user_id: str, current_user_email: str):
        invitation = await self.invitation_repository.find_invitation_by_id(invitation_id)

        if not invitation:
            raise InvitationNotFoundException()

        if invitation.status != "PENDING":
            raise InvitationAlreadyRespondedException()

        is_recipient = invitation.email.lower().strip() == current_user_email.lower().strip()
        is_user_recipient = invitation.userId == current_user_id
        is_project_owner = getattr(invitation.project, 'ownerId', None) == current_user_id

        if not (is_recipient or is_user_recipient or is_project_owner):
            raise InvitationAccessDeniedException()
        # --------------------------------

        return await self.invitation_repository.update_invitation_status(
            invitation_id=invitation_id,
            status="REVOKED",
        )