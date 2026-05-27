class ListMyPendingInvitationsUseCase:

    def __init__(self, invitation_repository):
        self.invitation_repository = invitation_repository

    async def execute(self, email: str):
        return await self.invitation_repository.list_pending_by_email(
            email
        )