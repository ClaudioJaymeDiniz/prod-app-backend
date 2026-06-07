class ListProjectPendingInvitationsUseCase:

    def __init__(self, invitation_repository):
        self.invitation_repository = invitation_repository

    async def execute(self, project_id: str):
        return await self.invitation_repository.list_pending_by_project(
            project_id
        )