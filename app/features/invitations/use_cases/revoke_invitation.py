from app.features.invitations.exceptions import (
    InvitationNotFoundException,
    InvitationProjectAccessDeniedException,
)


class RevokeInvitationUseCase:

    def __init__(self, invitation_repository):
        self.invitation_repository = invitation_repository

    async def execute(
        self,
        invitation_id: str,
        owner_id: str
    ):
        invitation = await self.invitation_repository.find_by_id(
            invitation_id
        )

        if not invitation:
            raise InvitationNotFoundException()

        if invitation.project.ownerId != owner_id:
            raise InvitationProjectAccessDeniedException()

        return await self.invitation_repository.update_status(
            invitation_id,
            "REVOKED"
        )