from app.features.invitations.exceptions import (
    InvitationNotFoundException,
    InvitationAccessDeniedException,
)


class AcceptInvitationUseCase:

    def __init__(self, invitation_repository):
        self.invitation_repository = invitation_repository

    async def execute(
        self,
        invitation_id: str,
        user_id: str,
        user_email: str
    ):
        invitation = await self.invitation_repository.find_by_id(
            invitation_id
        )

        if not invitation:
            raise InvitationNotFoundException()

        if invitation.email.lower() != user_email.lower():
            raise InvitationAccessDeniedException()

        await self.invitation_repository.upsert_project_member(
            user_id=user_id,
            project_id=invitation.projectId,
            role=invitation.role
        )

        return await self.invitation_repository.update_status(
            invitation_id,
            "ACCEPTED"
        )